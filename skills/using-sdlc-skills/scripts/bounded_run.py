#!/usr/bin/env python3
"""Bounded Context Execution Runner for SDLC Agent Skills.

Enforces Section 8.3 of docs/architecture.md:
Captures full verbose command output to disk while returning a bounded,
actionable summary (and relevant failure stacktraces) to agent context.

Usage:
  python scripts/bounded_run.py npm test
  python scripts/bounded_run.py --max-lines 40 pytest
  python scripts/bounded_run.py --log-dir .agent/logs npm run lint
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

ROOT = Path(__file__).resolve().parents[1]


def slugify(text: str) -> str:
    slug = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[-\s]+", "-", slug).strip("-")[:30] or "cmd"


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--max-lines", type=int, default=50, help="Maximum lines to return to context (default: 50)")
    parser.add_argument("--timeout", type=int, default=180, help="Execution timeout in seconds (default: 180s, 0 for unlimited)")
    parser.add_argument("--log-dir", default=".agent/logs", help="Directory to save full raw output logs")
    parser.add_argument("command", nargs=argparse.REMAINDER, help="The command and arguments to execute")

    args = parser.parse_args()

    cmd = args.command
    if cmd and cmd[0] == "--":
        cmd = cmd[1:]

    if not cmd:
        print("ERROR: No command specified to run.", file=sys.stderr)
        return 2

    # Prepare log destination
    log_dir = Path(args.log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    cmd_slug = slugify(Path(cmd[0]).stem)
    log_file = log_dir / f"{stamp}_{cmd_slug}.log"

    cmd_str = " ".join(cmd)
    start_time = time.time()
    timed_out = False

    try:
        # Run process and capture merged stdout/stderr
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        timeout_val = args.timeout if args.timeout > 0 else None
        try:
            stdout, _ = proc.communicate(timeout=timeout_val)
            exit_code = proc.returncode
        except subprocess.TimeoutExpired:
            proc.kill()
            stdout_timeout, _ = proc.communicate()
            stdout = (stdout_timeout or "") + f"\n\nERROR: Command timed out after {args.timeout} seconds and was killed."
            exit_code = 124
            timed_out = True
    except Exception as exc:
        print(f"ERROR: Failed to launch command '{cmd_str}': {exc}", file=sys.stderr)
        return 1

    duration = time.time() - start_time
    full_output = stdout or ""

    # Persist full raw output to disk
    log_header = f"=== Bounded Execution Log ===\nCommand: {cmd_str}\nTimestamp: {stamp}\nExit Code: {exit_code}\nDuration: {duration:.2f}s\n=============================\n\n"
    log_file.write_text(log_header + full_output, encoding="utf-8")

    lines = full_output.splitlines()
    total_lines = len(lines)

    # If output is small, print directly
    if total_lines <= args.max_lines:
        if full_output:
            print(full_output)
        return exit_code

    # If output exceeds budget, construct bounded actionable view
    head_count = 10
    tail_count = max(5, args.max_lines - head_count - 5)

    head_lines = lines[:head_count]
    tail_lines = lines[-tail_count:]

    print(f"--- [BOUNDED CONTEXT RUNNER] Command: {cmd_str} ---")
    print(f"Exit Code: {exit_code} | Duration: {duration:.2f}s | Total Output: {total_lines} lines")
    print(f"Full log written to: {log_file}")
    print("-" * 60)
    print("\n".join(head_lines))
    print(f"\n... [{total_lines - head_count - tail_count} lines truncated; see full log file] ...\n")
    print("\n".join(tail_lines))
    print("-" * 60)

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())

