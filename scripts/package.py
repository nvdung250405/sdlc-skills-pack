#!/usr/bin/env python3
"""Build a clean distribution release archive of the SDLC skill pack.

Validates the pack with strict linting, asset checks, and contract gates,
then creates a clean ZIP archive excluding all developer junk and git metadata.

Usage:
    python scripts/package.py [--version X.Y.Z] [--out dist/sdlc-skills-pack.zip]
"""

from __future__ import annotations

import argparse
import fnmatch
import os
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDE_PATTERNS = {
    ".git",
    ".git/**",
    ".agent",
    ".agent/**",
    "__pycache__",
    "**/__pycache__/**",
    "*.pyc",
    "*.pyo",
    ".DS_Store",
    "**/.DS_Store",
    ".pytest_cache",
    "**/.pytest_cache/**",
    "*.log",
    "**/*.log",
    ".sdlc-upstream-backups",
    "**/.sdlc-upstream-backups/**",
    ".sdlc-skill-backups",
    "**/.sdlc-skill-backups/**",
    "dist",
    "dist/**",
    "tmp*",
    "**/tmp*/**",
}


def should_exclude(rel_path: str) -> bool:
    normalized = rel_path.replace("\\", "/")
    parts = normalized.split("/")
    # Exclude prohibited folder names anywhere in path
    bad_dirs = {".git", ".agent", "__pycache__", ".pytest_cache", ".sdlc-upstream-backups", ".sdlc-skill-backups", "dist"}
    if any(part in bad_dirs for part in parts):
        return True
    for pat in EXCLUDE_PATTERNS:
        if fnmatch.fnmatch(normalized, pat) or fnmatch.fnmatch(parts[-1], pat):
            return True
    return False


def run_gate(cmd: list[str], name: str) -> None:
    print(f"Running gate: {' '.join(cmd)} ...")
    res = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    if res.returncode != 0:
        print(f"ERROR: Quality gate '{name}' failed with exit code {res.returncode}:", file=sys.stderr)
        print(res.stdout, file=sys.stderr)
        print(res.stderr, file=sys.stderr)
        sys.exit(1)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", default="0.2.0", help="version tag for release filename")
    parser.add_argument("--out", help="explicit output archive path")
    parser.add_argument("--skip-tests", action="store_true", help="skip full test suite prior to packaging")
    args = parser.parse_args()

    # Pre-packaging quality gates
    run_gate([sys.executable, str(ROOT / "scripts" / "build_assets.py"), "--check"], "Router Assets Sync")
    run_gate([sys.executable, str(ROOT / "scripts" / "lint_pack.py"), "--strict"], "Strict Pack Linter")
    run_gate([sys.executable, str(ROOT / "scripts" / "verify_contracts.py")], "Machine Contract Syntax Gate")
    run_gate([sys.executable, str(ROOT / "scripts" / "run_evals.py")], "Evaluation Fixtures Verification")
    if not args.skip_tests:
        run_gate([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], "Unit Test Suite")

    dist_dir = ROOT / "dist"
    dist_dir.mkdir(parents=True, exist_ok=True)
    out_path = Path(args.out).resolve() if args.out else dist_dir / f"sdlc-skills-pack-v{args.version}.zip"

    files_to_pack: list[tuple[Path, str]] = []
    for root, dirs, files in os.walk(ROOT):
        # Prune excluded directories in-place
        dirs[:] = [d for d in dirs if not should_exclude(str((Path(root) / d).relative_to(ROOT)))]
        for f in files:
            file_path = Path(root) / f
            rel = str(file_path.relative_to(ROOT))
            if not should_exclude(rel):
                files_to_pack.append((file_path, rel.replace("\\", "/")))

    print(f"Packaging {len(files_to_pack)} clean files into {out_path.relative_to(ROOT)}...")
    with zipfile.ZipFile(out_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for fpath, arcname in files_to_pack:
            zf.write(fpath, arcname)

    # Post-packaging hygiene verification
    with zipfile.ZipFile(out_path, "r") as zf:
        names = zf.namelist()
        for name in names:
            if should_exclude(name):
                print(f"HYGIENE ERROR: prohibited file made it into zip archive: {name}", file=sys.stderr)
                out_path.unlink(missing_ok=True)
                return 1

    size_kb = out_path.stat().st_size / 1024
    print(f"SUCCESS: Created clean release archive {out_path.name} ({size_kb:.1f} KB, {len(names)} files).")
    print(f"Archive path: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

