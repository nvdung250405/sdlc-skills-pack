#!/usr/bin/env python3
"""Measure prompt footprint and disk size across SDLC skill pack profiles.

Usage:
    python scripts/measure_footprint.py [--json]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def get_skill_stats(skill_dir: Path) -> dict[str, int]:
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        return {"skill_md_bytes": 0, "skill_md_chars": 0, "total_bytes": 0}
    text = skill_file.read_text(encoding="utf-8", errors="replace")
    total_bytes = sum(p.stat().st_size for p in skill_dir.rglob("*") if p.is_file())
    return {
        "skill_md_bytes": len(text.encode("utf-8")),
        "skill_md_chars": len(text),
        "total_bytes": total_bytes,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="output as machine-readable JSON")
    args = parser.parse_args()

    manifest_file = ROOT / "manifests" / "skill-map.json"
    if not manifest_file.is_file():
        print("ERROR: manifests/skill-map.json not found", file=sys.stderr)
        return 1

    manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    profiles = manifest.get("profiles", {})

    all_skills: dict[str, Path] = {}
    for folder in [ROOT / "skills", ROOT / "extras"]:
        if folder.is_dir():
            for p in folder.iterdir():
                if p.is_dir() and (p / "SKILL.md").is_file():
                    all_skills[p.name] = p

    report: dict[str, dict] = {}

    # Router alone
    router_stats = get_skill_stats(ROOT / "skills" / "using-sdlc-skills")
    report["router-alone"] = {
        "skill_count": 1,
        "skill_md_bytes": router_stats["skill_md_bytes"],
        "estimated_tokens": router_stats["skill_md_chars"] // 4,
        "total_bytes": router_stats["total_bytes"],
    }

    # Profiles
    for prof_name, skill_names in profiles.items():
        matched = [all_skills[name] for name in skill_names if name in all_skills]
        total_md_bytes = 0
        total_md_chars = 0
        total_bytes = 0
        for s_path in matched:
            st = get_skill_stats(s_path)
            total_md_bytes += st["skill_md_bytes"]
            total_md_chars += st["skill_md_chars"]
            total_bytes += st["total_bytes"]
        report[f"profile:{prof_name}"] = {
            "skill_count": len(matched),
            "skill_md_bytes": total_md_bytes,
            "estimated_tokens": total_md_chars // 4,
            "total_bytes": total_bytes,
        }

    if args.json:
        print(json.dumps(report, indent=2))
        return 0

    print("=" * 72)
    print(" SDLC SKILL PACK CONTEXT & STORAGE FOOTPRINT")
    print("=" * 72)
    print(f"{'Profile / Target':<22} | {'Skills':<6} | {'Prompt MD (KB)':<14} | {'Est Tokens':<11} | {'Total Disk':<10}")
    print("-" * 72)
    for name, data in report.items():
        kb = f"{data['skill_md_bytes'] / 1024:.1f} KB"
        disk = f"{data['total_bytes'] / 1024:.1f} KB"
        print(f"{name:<22} | {data['skill_count']:<6} | {kb:<14} | ~{data['estimated_tokens']:<10} | {disk:<10}")
    print("=" * 72)
    print("Note: In demand-driven loading (lazy runtime), agent only loads the router")
    print("plus 1-2 skills per task step (~3k tokens), NOT the whole profile at once.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

