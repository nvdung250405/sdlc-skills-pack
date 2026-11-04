#!/usr/bin/env python3
"""Render a compact AGENTS.md index for environments without native skill loading.

Run from the project root. --skill-root points to the directory containing the
installed skill folders; --asset-root points to the pack copy containing workflows/
and templates/.
"""
from __future__ import annotations
import sys
import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def frontmatter_value(text: str, key: str) -> str:
    match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", text, re.S)
    if not match:
        return ""
    for line in match.group(1).splitlines():
        if line.startswith(key + ":"):
            return line.split(":", 1)[1].strip().strip("\"'")
    return ""


def normalize_path(value: str) -> str:
    return Path(value or ".").as_posix().rstrip("/") or "."


def render(with_extras: bool = False, skill_root: str = "skills", asset_root: str = ".") -> str:
    tiers = ["skills"] + (["extras"] if with_extras else [])
    skill_root = normalize_path(skill_root)
    asset_root = normalize_path(asset_root)
    skill_folder = ROOT / "skills"
    lines = [
        "# SDLC Agent Skills — portable index", "",
        "For each task, identify the applicable skill(s) and read their `SKILL.md` before acting. Load only relevant skills; do not paste the whole library into context.",
        f"The pack-level router is `{skill_root}/using-sdlc-skills/SKILL.md`. For a full lifecycle, follow `{asset_root}/workflows/full-sdlc.md` when that pack asset is available.",
        f"Use the shared output templates in `{asset_root}/templates/` when present; otherwise follow the project's existing artifact conventions.",
        "Do not claim checks passed unless they ran. Stop for required human approval before production/destructive actions.", "",
        "## Available skills", "", "| Skill | Load when |", "|---|---|"
    ]
    for tier in tiers:
        folder = ROOT / tier
        if not folder.is_dir():
            continue
        for skill_dir in sorted((p for p in folder.iterdir() if p.is_dir() and (p / "SKILL.md").is_file()), key=lambda p: p.name.casefold()):
            text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
            desc = frontmatter_value(text, "description").replace("|", "/").replace("\n", " ")
            link = f"{skill_root}/{skill_dir.name}/SKILL.md"
            lines.append(f"| `{skill_dir.name}` (`{link}`) | {desc} |")
    lines += [
        "", "## Workflow references", "",
        f"- `{asset_root}/workflows/full-sdlc.md` — full requirements-to-release lifecycle.",
        f"- `{asset_root}/workflows/feature-loop.md` — incremental feature implementation.",
        f"- `{asset_root}/workflows/bug-fix.md` — root-cause diagnosis and regression verification.",
        f"- `{asset_root}/workflows/quick-change.md` — low-risk, well-scoped changes.",
        f"- `{asset_root}/workflows/agent-handoff-contract.md` — durable cross-agent handoff contract.",
        "- `.agent/tasks/<id>.md` — durable handoff record for multi-step work.", ""
    ]
    return "\n".join(lines)


def main() -> None:
    # Ensure stdout uses UTF-8 on Windows where the console may default to cp1252.
    if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--with-extras", action="store_true")
    parser.add_argument("--skill-root", default="skills", help="project-relative path containing installed skill folders")
    parser.add_argument("--asset-root", default=".", help="project-relative path containing workflows/ and templates/")
    args = parser.parse_args()
    print(render(args.with_extras, args.skill_root, args.asset_root), end="")


if __name__ == "__main__":
    main()
