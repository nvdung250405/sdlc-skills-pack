#!/usr/bin/env python3
"""Validate and run SDLC skill pack golden evaluation fixtures.

Usage:
    python scripts/run_evals.py [--check-only]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def validate_eval_fixture(path: Path, available_skills: set[str], available_workflows: set[str], errors: list[str]) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path.name}: invalid JSON - {exc}")
        return {}

    required_keys = ["id", "name", "workflow", "task_description", "expected_stages", "expected_skills", "expected_artifacts", "invariants"]
    for key in required_keys:
        if key not in data:
            errors.append(f"{path.name}: missing required key '{key}'")

    wf = data.get("workflow", "")
    if wf not in available_workflows:
        errors.append(f"{path.name}: references non-existent workflow '{wf}'")

    for skill in data.get("expected_skills", []):
        if skill not in available_skills:
            errors.append(f"{path.name}: references non-existent skill '{skill}'")

    return data


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-only", action="store_true", help="verify fixture schema and references")
    args = parser.parse_args()

    evals_dir = ROOT / "evals"
    if not evals_dir.is_dir():
        print("ERROR: evals/ directory not found", file=sys.stderr)
        return 1

    available_skills: set[str] = set()
    for folder in [ROOT / "skills", ROOT / "extras"]:
        if folder.is_dir():
            for p in folder.iterdir():
                if p.is_dir() and (p / "SKILL.md").is_file():
                    available_skills.add(p.name)

    available_workflows: set[str] = {
        f"workflows/{p.name}" for p in (ROOT / "workflows").glob("*.md")
    }

    eval_files = sorted(evals_dir.glob("*.json"))
    if not eval_files:
        print("ERROR: no evaluation fixtures found in evals/", file=sys.stderr)
        return 1

    errors: list[str] = []
    fixtures = []
    for f in eval_files:
        data = validate_eval_fixture(f, available_skills, available_workflows, errors)
        if data:
            fixtures.append((f, data))

    if errors:
        print(f"FAILED: {len(errors)} validation errors found in evaluation fixtures:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print("=" * 68)
    print(" SDLC GOLDEN TASK FIXTURES VERIFICATION")
    print("=" * 68)
    for f, d in fixtures:
        print(f"PASS: {d['id']:<24} | Workflow: {d['workflow']}")
        print(f"      Title: {d['name']}")
        print(f"      Required skills ({len(d['expected_skills'])}): {', '.join(d['expected_skills'])}")
        print(f"      Artifact contracts ({len(d['expected_artifacts'])}): {', '.join(a['alias'] for a in d['expected_artifacts'])}")
        print("-" * 68)

    print(f"Successfully verified {len(fixtures)} golden evaluation fixtures.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
