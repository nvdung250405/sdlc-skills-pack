#!/usr/bin/env python3
"""SWE-agent & OpenHands Inspired Execution & Context Harness for Coding Agents.

Enforces Section 8.3 of docs/architecture.md:
1. Bounded Execution: Captures full verbose command output to disk while
   extracting relevant failure stacktraces & bounded summaries to context.
2. Viewport Inspection: Allows agents to inspect numbered line slices of files
   without consuming tokens reading entire documents (SWE-agent ACI style).
3. Test Verification Gate: Formats test execution diagnostics for self-healing loops.

Usage:
  python scripts/bounded_run.py pytest
  python scripts/bounded_run.py --max-lines 40 npm test
  python scripts/bounded_run.py view scripts/install.py --line 45 --window 25
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parents[1]


def slugify(text: str) -> str:
    slug = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[-\s]+", "-", slug).strip("-")[:30] or "cmd"


def extract_failure_context(lines: List[str], max_error_lines: int = 25) -> List[str]:
    """Isolates relevant error stacktraces and assertion failures from output."""
    error_patterns = [
        re.compile(r"Traceback \(most recent call last\):", re.IGNORECASE),
        re.compile(r"FAILED\s+tests/", re.IGNORECASE),
        re.compile(r"FAIL:\s+", re.IGNORECASE),
        re.compile(r"AssertionError:", re.IGNORECASE),
        re.compile(r"Error:", re.IGNORECASE),
        re.compile(r"Exception:", re.IGNORECASE),
        re.compile(r"^\s*File\s+\".*\",\s+line\s+\d+", re.IGNORECASE),
    ]

    matched_indices = set()
    for idx, line in enumerate(lines):
        if any(pat.search(line) for pat in error_patterns):
            # Include a few lines of context around the error
            start = max(0, idx - 2)
            end = min(len(lines), idx + 6)
            for i in range(start, end):
                matched_indices.add(i)

    if not matched_indices:
        return []

    sorted_indices = sorted(matched_indices)
    extracted = []
    prev_idx = None
    for idx in sorted_indices[:max_error_lines]:
        if prev_idx is not None and idx > prev_idx + 1:
            extracted.append("  ...")
        extracted.append(f"  {lines[idx]}")
        prev_idx = idx

    return extracted


def handle_view(args: argparse.Namespace) -> int:
    """Implements SWE-agent ACI Viewport inspection."""
    target_path = Path(args.file)
    if not target_path.is_absolute():
        target_path = ROOT / target_path

    if not target_path.exists():
        print(f"ERROR: File not found: {target_path}", file=sys.stderr)
        return 1

    try:
        content = target_path.read_text(encoding="utf-8", errors="replace")
    except Exception as exc:
        print(f"ERROR: Failed to read {target_path}: {exc}", file=sys.stderr)
        return 1

    lines = content.splitlines()
    total_lines = len(lines)

    center = args.line if args.line and args.line > 0 else 1
    window = args.window if args.window and args.window > 0 else 50
    half = window // 2

    start = max(1, center - half)
    end = min(total_lines, start + window - 1)
    start = max(1, end - window + 1)

    print(f"--- [VIEWPORT] {target_path.relative_to(ROOT) if target_path.is_relative_to(ROOT) else target_path} (Lines {start}-{end} of {total_lines}) ---")
    for lno in range(start, end + 1):
        marker = " >" if lno == center else "  "
        print(f"{marker} {lno:4d} | {lines[lno - 1]}")
    print("-" * 70)
    return 0


def handle_run(args: argparse.Namespace) -> int:
    cmd = args.command
    if cmd and cmd[0] == "--":
        cmd = cmd[1:]

    if not cmd:
        print("ERROR: No command specified to run.", file=sys.stderr)
        return 2

    log_dir = Path(args.log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    cmd_slug = slugify(Path(cmd[0]).stem)
    log_file = log_dir / f"{stamp}_{cmd_slug}.log"

    cmd_str = " ".join(cmd)
    start_time = time.time()

    # On Windows, flatten command string for shell execution to support .cmd wrappers (npm, mvn) and quoted strings
    use_shell = os.name == "nt"
    exec_target = cmd_str if use_shell else cmd

    try:
        proc = subprocess.Popen(
            exec_target,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=use_shell,
        )
        timeout_val = args.timeout if args.timeout > 0 else None
        try:
            stdout, _ = proc.communicate(timeout=timeout_val)
            exit_code = proc.returncode
        except subprocess.TimeoutExpired:
            proc.kill()
            stdout_timeout, _ = proc.communicate()
            stdout = (stdout_timeout or "") + f"\n\nERROR: Command timed out after {args.timeout}s and was killed."
            exit_code = 124
    except Exception as exc:
        print(f"ERROR: Failed to launch command '{cmd_str}': {exc}", file=sys.stderr)
        return 1

    duration = time.time() - start_time
    full_output = stdout or ""

    log_header = f"=== Bounded Execution Log ===\nCommand: {cmd_str}\nTimestamp: {stamp}\nExit Code: {exit_code}\nDuration: {duration:.2f}s\n=============================\n\n"
    log_file.write_text(log_header + full_output, encoding="utf-8")

    lines = full_output.splitlines()
    total_lines = len(lines)

    if total_lines <= args.max_lines:
        if full_output:
            print(full_output)
        return exit_code

    # Extract failure slices if command failed
    failure_slice = extract_failure_context(lines) if exit_code != 0 else []

    head_count = 8
    tail_count = max(8, args.max_lines - head_count - len(failure_slice) - 6)

    print(f"--- [BOUNDED CONTEXT HARNESS] Command: {cmd_str} ---")
    print(f"Exit Code: {exit_code} | Duration: {duration:.2f}s | Total Output: {total_lines} lines")
    print(f"Full raw log preserved at: {log_file}")
    print("-" * 70)

    print("\n".join(lines[:head_count]))
    print(f"\n... [{total_lines - head_count - tail_count} lines truncated; see full log] ...\n")

    if failure_slice:
        print(">>> [ISOLATED FAILURE STACKTRACES / ERRORS] <<<")
        print("\n".join(failure_slice))
        print("-" * 70)

    print("\n".join(lines[-tail_count:]))
    print("-" * 70)

    return exit_code


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    if len(sys.argv) > 1 and sys.argv[1] == "view":
        parser.add_argument("view_action", help="View file viewport")
        parser.add_argument("file", help="File to view")
        parser.add_argument("--line", type=int, default=1, help="Center line number (default: 1)")
        parser.add_argument("--window", type=int, default=50, help="Window line count (default: 50)")
        args = parser.parse_args()
        return handle_view(args)

    parser.add_argument("--max-lines", type=int, default=50, help="Maximum lines to return to context (default: 50)")
    parser.add_argument("--timeout", type=int, default=180, help="Execution timeout in seconds (default: 180s)")
    parser.add_argument("--log-dir", default=".agent/logs", help="Directory to save full raw output logs")
    parser.add_argument("command", nargs=argparse.REMAINDER, help="The command and arguments to execute")

    args = parser.parse_args()
    return handle_run(args)


if __name__ == "__main__":
    raise SystemExit(main())
