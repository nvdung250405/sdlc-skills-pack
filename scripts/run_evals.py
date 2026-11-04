#!/usr/bin/env python3
"""Validate semantic schema, workflow coverage, and artifact aliases for SDLC golden evaluation fixtures.

Note: This tool is the Evaluation Fixture Schema & Semantic Gate. It verifies
the machine-readable contracts of golden evaluation fixtures (ensuring workflows,
skills, and artifact aliases exist). Live multi-agent benchmark executions and
empirical results are tracked separately under `evals/results/`.

Usage:
    python scripts/run_evals.py [--check-only]
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_scaffold_aliases() -> set[str]:
    """Dynamically extract canonical artifact aliases from scripts/scaffold.py."""
    scaffold_path = ROOT / "scripts" / "scaffold.py"
    if not scaffold_path.is_file():
        return set()
    spec = importlib.util.spec_from_file_location("scaffold_module", scaffold_path)
    if not spec or not spec.loader:
        return set()
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    artifact_map = getattr(module, "ARTIFACT_MAP", {})
    return set(artifact_map.keys())


def validate_eval_fixture(
    path: Path,
    available_skills: set[str],
    available_workflows: set[str],
    valid_aliases: set[str],
    errors: list[str],
) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path.name}: invalid JSON - {exc}")
        return {}

    required_keys = [
        "id",
        "name",
        "workflow",
        "task_description",
        "expected_stages",
        "expected_skills",
        "expected_artifacts",
        "invariants",
    ]
    for key in required_keys:
        if key not in data:
            errors.append(f"{path.name}: missing required key '{key}'")

    wf = data.get("workflow", "")
    if wf not in available_workflows:
        errors.append(f"{path.name}: references non-existent workflow '{wf}'")

    for skill in data.get("expected_skills", []):
        if skill not in available_skills:
            errors.append(f"{path.name}: references non-existent skill '{skill}'")

    # Strict Artifact Alias and Path Validation (prevents invented artifact mutations)
    artifacts = data.get("expected_artifacts", [])
    if not isinstance(artifacts, list) or not artifacts:
        errors.append(f"{path.name}: expected_artifacts must be a non-empty list")
    else:
        for idx, art in enumerate(artifacts):
            if not isinstance(art, dict):
                errors.append(f"{path.name}: artifact entry #{idx} must be an object")
                continue
            alias = art.get("alias")
            if not alias or alias not in valid_aliases:
                errors.append(
                    f"{path.name}: artifact entry #{idx} has invalid or unknown alias '{alias}' (must match scaffold.py aliases)"
                )
            cpath = art.get("canonical_path")
            if not cpath or not isinstance(cpath, str) or not cpath.strip():
                errors.append(f"{path.name}: artifact entry '{alias}' missing valid 'canonical_path'")
            must_contain = art.get("must_contain")
            if not isinstance(must_contain, list) or not must_contain:
                errors.append(f"{path.name}: artifact entry '{alias}' must define non-empty 'must_contain' list")

    return data


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-only", action="store_true", help="verify fixture schema and references")
    args = parser.parse_args()

    evals_dir = ROOT / "evals"
    if not evals_dir.is_dir():
        print("ERROR: evals/ directory not found", file=sys.stderr)
        return 1

    valid_aliases = load_scaffold_aliases()
    if not valid_aliases:
        print("ERROR: failed to load canonical artifact aliases from scripts/scaffold.py", file=sys.stderr)
        return 1

    available_skills: set[str] = set()
    for folder in [ROOT / "skills", ROOT / "extras"]:
        if folder.is_dir():
            for p in folder.iterdir():
                if p.is_dir() and (p / "SKILL.md").is_file():
                    available_skills.add(p.name)

    workflow_files = list((ROOT / "workflows").glob("*.md"))
    available_workflows: set[str] = {f"workflows/{p.name}" for p in workflow_files}

    eval_files = sorted(evals_dir.glob("*.json"))
    if not eval_files:
        print("ERROR: no evaluation fixtures found in evals/", file=sys.stderr)
        return 1

    errors: list[str] = []
    fixtures = []
    covered_workflows: set[str] = set()

    for f in eval_files:
        data = validate_eval_fixture(f, available_skills, available_workflows, valid_aliases, errors)
        if data:
            fixtures.append((f, data))
            if "workflow" in data:
                covered_workflows.add(data["workflow"])

    # Ensure all 11 workflows have at least one golden evaluation fixture
    uncovered_wfs = sorted(available_workflows - covered_workflows)
    if uncovered_wfs:
        errors.append(f"missing evaluation fixtures for workflows: {', '.join(uncovered_wfs)}")

    if errors:
        print(f"FAILED: {len(errors)} validation errors found in evaluation fixtures:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print("=" * 72)
    print(" SDLC GOLDEN TASK FIXTURES SEMANTIC GATE")
    print("=" * 72)
    for f, d in fixtures:
        print(f"PASS: {d['id']:<28} | Workflow: {d['workflow']}")
        print(f"      Title: {d['name']}")
        print(f"      Skills ({len(d['expected_skills'])}): {', '.join(d['expected_skills'])}")
        print(f"      Scaffold Aliases ({len(d['expected_artifacts'])}): {', '.join(a['alias'] for a in d['expected_artifacts'])}")
        print("-" * 72)

    print(f"SUCCESS: Verified {len(fixtures)} golden evaluation fixtures across all {len(covered_workflows)} workflows.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
