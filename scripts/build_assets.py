#!/usr/bin/env python3
"""Synchronize and build router bundled assets from canonical root sources.

Canonical sources of truth:
- templates/ -> skills/using-sdlc-skills/assets/templates/
- workflows/ -> skills/using-sdlc-skills/assets/workflows/
- scripts/   -> skills/using-sdlc-skills/scripts/

Usage:
  python scripts/build_assets.py
  python scripts/build_assets.py --check
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ROUTER_DIR = ROOT / "skills" / "using-sdlc-skills"
DEST_TEMPLATES = ROUTER_DIR / "assets" / "templates"
DEST_WORKFLOWS = ROUTER_DIR / "assets" / "workflows"
DEST_SCRIPTS = ROUTER_DIR / "scripts"


def sync_templates(check_only: bool) -> list[str]:
    diffs = []
    src_dir = ROOT / "templates"
    src_files = [p for p in src_dir.rglob("*") if p.is_file() and p.name != "README.md"]
    
    # Check / copy
    for src in src_files:
        rel = src.relative_to(src_dir)
        dest = DEST_TEMPLATES / rel
        src_bytes = src.read_bytes().replace(b"\r\n", b"\n")
        if not dest.is_file() or dest.read_bytes().replace(b"\r\n", b"\n") != src_bytes:
            diffs.append(f"template: {rel}")
            if not check_only:
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(src_bytes)

    # Check for orphans
    for dest in DEST_TEMPLATES.rglob("*"):
        if dest.is_file():
            rel = dest.relative_to(DEST_TEMPLATES)
            src = src_dir / rel
            if not src.is_file():
                diffs.append(f"orphan template in router assets: {rel}")
                if not check_only:
                    dest.unlink()

    return diffs


def sync_workflows(check_only: bool) -> list[str]:
    diffs = []
    src_dir = ROOT / "workflows"
    src_files = list(src_dir.glob("*.md"))

    for src in src_files:
        dest = DEST_WORKFLOWS / src.name
        src_bytes = src.read_bytes().replace(b"\r\n", b"\n")
        if not dest.is_file() or dest.read_bytes().replace(b"\r\n", b"\n") != src_bytes:
            diffs.append(f"workflow: {src.name}")
            if not check_only:
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(src_bytes)

    for dest in DEST_WORKFLOWS.glob("*.md"):
        src = src_dir / dest.name
        if not src.is_file():
            diffs.append(f"orphan workflow in router assets: {dest.name}")
            if not check_only:
                dest.unlink()

    return diffs


def sync_scripts(check_only: bool) -> list[str]:
    diffs = []
    scripts_to_sync = ["scaffold.py", "bounded_run.py", "verify_contracts.py"]
    for s_name in scripts_to_sync:
        src = ROOT / "scripts" / s_name
        dest = DEST_SCRIPTS / s_name
        if not src.is_file():
            continue
        src_bytes = src.read_bytes().replace(b"\r\n", b"\n")
        if not dest.is_file() or dest.read_bytes().replace(b"\r\n", b"\n") != src_bytes:
            diffs.append(f"script: {s_name}")
            if not check_only:
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(src_bytes)
    return diffs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify synchronization without modifying files")
    args = parser.parse_args()

    DEST_TEMPLATES.mkdir(parents=True, exist_ok=True)
    DEST_WORKFLOWS.mkdir(parents=True, exist_ok=True)
    DEST_SCRIPTS.mkdir(parents=True, exist_ok=True)

    tmpl_diffs = sync_templates(args.check)
    wf_diffs = sync_workflows(args.check)
    script_diffs = sync_scripts(args.check)

    all_diffs = tmpl_diffs + wf_diffs + script_diffs

    if args.check:
        if all_diffs:
            print(f"Router bundled assets OUT OF SYNC ({len(all_diffs)} differences):", file=sys.stderr)
            for d in all_diffs:
                print(f"  - {d}", file=sys.stderr)
            print("Run `python scripts/build_assets.py` to synchronize bundled assets.", file=sys.stderr)
            return 1
        print("Router bundled assets are 100% in sync with root.")
        return 0

    if all_diffs:
        print(f"Synchronized {len(all_diffs)} router assets from canonical root:")
        for d in all_diffs:
            print(f"  + {d}")
    else:
        print("Router bundled assets already up-to-date.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

