#!/usr/bin/env python3
"""Validate semantic schema, workflow coverage, and artifact aliases for SDLC golden evaluation fixtures.

Note: This tool is the Evaluation Fixture Schema & Semantic Gate (Google agents-cli).
It verifies the machine-readable contracts of golden evaluation fixtures (ensuring workflows,
skills, agent spec targets, guardrails, invariants, and artifact aliases exist), and
validates empirical benchmark execution transcripts under `evals/results/`.

Usage:
    python scripts/run_evals.py [--check-only] [--verify-results] [--fixtures-only]
                                [--strict] [--format {pretty,json,summary}]
                                [--fixture FIXTURE_ID] [-v] [-q]
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import importlib.util
import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


@dataclass
class ValidationError:
    category: str  # SCHEMA, SPEC_ALIGNMENT, WORKFLOW_COVERAGE, ARTIFACT, GUARDRAIL, TRANSCRIPT
    file: str
    field: str
    message: str
    remediation: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)

    def __str__(self) -> str:
        return f"[{self.category}] {self.file}:{self.field}\n    Error: {self.message}\n    Remediation: {self.remediation}"


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
    errors: list[ValidationError],
    strict: bool = False,
) -> dict[str, Any] | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(
            ValidationError(
                category="SCHEMA",
                file=path.name,
                field="syntax",
                message=f"invalid JSON - {exc}",
                remediation="Ensure the fixture contains valid, well-formed JSON syntax.",
            )
        )
        return None

    if not isinstance(data, dict):
        errors.append(
            ValidationError(
                category="SCHEMA",
                file=path.name,
                field="root",
                message="JSON root must be an object ({...})",
                remediation="Ensure the JSON file root is an object mapping, not a list or scalar.",
            )
        )
        return None

    required_keys = [
        "id",
        "name",
        "workflow",
        "agent_spec_target",
        "task_description",
        "expected_stages",
        "expected_skills",
        "expected_artifacts",
        "guardrails",
        "invariants",
    ]
    for key in required_keys:
        if key not in data:
            errors.append(
                ValidationError(
                    category="SCHEMA",
                    file=path.name,
                    field=key,
                    message=f"missing required key '{key}'",
                    remediation=f"Add mandatory field '{key}' to fixture.",
                )
            )

    wf = data.get("workflow", "")
    if wf not in available_workflows:
        errors.append(
            ValidationError(
                category="SPEC_ALIGNMENT",
                file=path.name,
                field="workflow",
                message=f"references non-existent workflow '{wf}'",
                remediation="Ensure workflow path exists under workflows/*.md.",
            )
        )

    spec_target = data.get("agent_spec_target", "")
    if not spec_target or not isinstance(spec_target, str):
        errors.append(
            ValidationError(
                category="SPEC_ALIGNMENT",
                file=path.name,
                field="agent_spec_target",
                message="'agent_spec_target' must be a non-empty string path",
                remediation="Specify the canonical workflow contract path as ground truth.",
            )
        )
    else:
        target_file = ROOT / spec_target
        if not target_file.is_file():
            errors.append(
                ValidationError(
                    category="SPEC_ALIGNMENT",
                    file=path.name,
                    field="agent_spec_target",
                    message=f"'agent_spec_target' path '{spec_target}' does not exist on disk",
                    remediation=f"Verify target file exists at '{spec_target}'.",
                )
            )

    for skill in data.get("expected_skills", []):
        if skill not in available_skills:
            errors.append(
                ValidationError(
                    category="SCHEMA",
                    file=path.name,
                    field="expected_skills",
                    message=f"references non-existent skill '{skill}'",
                    remediation="Ensure referenced skill exists in skills/ or extras/.",
                )
            )

    if strict and "verification-before-completion" not in data.get("expected_skills", []):
        errors.append(
            ValidationError(
                category="GUARDRAIL",
                file=path.name,
                field="expected_skills",
                message="fixture missing required skill 'verification-before-completion' under --strict mode",
                remediation="Add 'verification-before-completion' to expected_skills.",
            )
        )

    stages = data.get("expected_stages", [])
    if not isinstance(stages, list) or not stages:
        errors.append(
            ValidationError(
                category="SCHEMA",
                file=path.name,
                field="expected_stages",
                message="'expected_stages' must be a non-empty list",
                remediation="Define an ordered list of lifecycle stages for this workflow.",
            )
        )
    else:
        if not any("compounding" in str(s).lower() for s in stages):
            errors.append(
                ValidationError(
                    category="GUARDRAIL",
                    file=path.name,
                    field="expected_stages",
                    message="'expected_stages' must contain an explicit Compounding stage",
                    remediation="Add terminal Compounding stage aligning with workflow primary stages.",
                )
            )

    guardrails = data.get("guardrails")
    if not guardrails or (not isinstance(guardrails, dict) and not isinstance(guardrails, list)):
        errors.append(
            ValidationError(
                category="GUARDRAIL",
                file=path.name,
                field="guardrails",
                message="'guardrails' must be a non-empty object or list",
                remediation="Define structured guardrails mapping rules (e.g. YAGNI, surgical diff, 5 Whys, reachability).",
            )
        )

    invariants = data.get("invariants", [])
    if not isinstance(invariants, list) or len(invariants) < 3:
        errors.append(
            ValidationError(
                category="GUARDRAIL",
                file=path.name,
                field="invariants",
                message="'invariants' must be a list of at least 3 constraint strings",
                remediation="Provide at least 3 behavioral constraints/invariants for evaluation.",
            )
        )

    # Strict Artifact Alias and Path Validation (prevents invented artifact mutations)
    artifacts = data.get("expected_artifacts", [])
    if not isinstance(artifacts, list) or not artifacts:
        errors.append(
            ValidationError(
                category="ARTIFACT",
                file=path.name,
                field="expected_artifacts",
                message="expected_artifacts must be a non-empty list",
                remediation="Specify expected artifacts with canonical aliases from scripts/scaffold.py.",
            )
        )
    else:
        for idx, art in enumerate(artifacts):
            if not isinstance(art, dict):
                errors.append(
                    ValidationError(
                        category="ARTIFACT",
                        file=path.name,
                        field=f"expected_artifacts[{idx}]",
                        message=f"artifact entry #{idx} must be an object",
                        remediation="Ensure artifact entry is a JSON object with alias, canonical_path, and must_contain.",
                    )
                )
                continue
            alias = art.get("alias")
            if not alias or alias not in valid_aliases:
                errors.append(
                    ValidationError(
                        category="ARTIFACT",
                        file=path.name,
                        field=f"expected_artifacts[{idx}].alias",
                        message=f"artifact entry #{idx} has invalid or unknown alias '{alias}'",
                        remediation=f"Use a valid canonical alias defined in scripts/scaffold.py:ARTIFACT_MAP.",
                    )
                )
            cpath = art.get("canonical_path")
            if not cpath or not isinstance(cpath, str) or not cpath.strip():
                errors.append(
                    ValidationError(
                        category="ARTIFACT",
                        file=path.name,
                        field=f"expected_artifacts[{alias}].canonical_path",
                        message=f"artifact entry '{alias}' missing valid 'canonical_path'",
                        remediation="Specify non-empty relative canonical_path.",
                    )
                )
            must_contain = art.get("must_contain")
            if not isinstance(must_contain, list) or not must_contain:
                errors.append(
                    ValidationError(
                        category="ARTIFACT",
                        file=path.name,
                        field=f"expected_artifacts[{alias}].must_contain",
                        message=f"artifact entry '{alias}' must define non-empty 'must_contain' list",
                        remediation="List required header/content substrings.",
                    )
                )
            if alias == "completion":
                if not any("compounded knowledge" in str(mc).lower() for mc in must_contain):
                    errors.append(
                        ValidationError(
                            category="ARTIFACT",
                            file=path.name,
                            field="expected_artifacts[completion].must_contain",
                            message="completion artifact must mandate 'Compounded Knowledge & Learnings' in 'must_contain'",
                            remediation="Add 'Compounded Knowledge & Learnings' to must_contain in completion artifact.",
                        )
                    )

    return data


def validate_benchmark_transcript(
    path: Path,
    fixtures_by_id: dict[str, dict[str, Any]],
    valid_aliases: set[str],
    errors: list[ValidationError],
) -> dict[str, Any] | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(
            ValidationError(
                category="SCHEMA",
                file=f"results/{path.name}",
                field="syntax",
                message=f"invalid JSON - {exc}",
                remediation="Ensure benchmark transcript contains valid JSON.",
            )
        )
        return None

    if not isinstance(data, dict):
        errors.append(
            ValidationError(
                category="SCHEMA",
                file=f"results/{path.name}",
                field="root",
                message="JSON root must be an object ({...})",
                remediation="Ensure the JSON file root is an object mapping, not a list or scalar.",
            )
        )
        return None

    required_keys = [
        "run_id",
        "fixture_id",
        "task_title",
        "runtime",
        "model",
        "profile",
        "timestamp",
        "execution_metrics",
        "workflow_traversal",
        "artifacts_produced",
        "quality_gates",
    ]
    for key in required_keys:
        if key not in data:
            errors.append(
                ValidationError(
                    category="TRANSCRIPT",
                    file=f"results/{path.name}",
                    field=key,
                    message=f"missing required transcript key '{key}'",
                    remediation=f"Add '{key}' to benchmark transcript.",
                )
            )

    fixture_id = data.get("fixture_id", "")
    fixture = fixtures_by_id.get(fixture_id)
    if not fixture:
        errors.append(
            ValidationError(
                category="TRANSCRIPT",
                file=f"results/{path.name}",
                field="fixture_id",
                message=f"references unknown fixture_id '{fixture_id}'",
                remediation="Set fixture_id to match a defined golden evaluation fixture.",
            )
        )
        return data

    metrics = data.get("execution_metrics", {})
    if not isinstance(metrics, dict):
        errors.append(
            ValidationError(
                category="TRANSCRIPT",
                file=f"results/{path.name}",
                field="execution_metrics",
                message="'execution_metrics' must be an object",
                remediation="Provide numeric execution telemetry metrics.",
            )
        )
    else:
        for metric_key in ["duration_seconds", "total_tool_calls", "prompt_tokens", "completion_tokens", "total_tokens"]:
            if metric_key not in metrics or not isinstance(metrics[metric_key], (int, float)):
                errors.append(
                    ValidationError(
                        category="TRANSCRIPT",
                        file=f"results/{path.name}",
                        field=f"execution_metrics.{metric_key}",
                        message=f"execution_metrics missing or invalid numeric '{metric_key}'",
                        remediation=f"Include valid numeric value for '{metric_key}'.",
                    )
                )

    traversal = data.get("workflow_traversal", {})
    if not isinstance(traversal, dict):
        errors.append(
            ValidationError(
                category="TRANSCRIPT",
                file=f"results/{path.name}",
                field="workflow_traversal",
                message="'workflow_traversal' must be an object",
                remediation="Provide workflow traversal recording resolved workflow and invoked skills.",
            )
        )
    else:
        wf = traversal.get("workflow_resolved", "")
        if wf != fixture.get("workflow"):
            errors.append(
                ValidationError(
                    category="TRANSCRIPT",
                    file=f"results/{path.name}",
                    field="workflow_traversal.workflow_resolved",
                    message=f"workflow_resolved '{wf}' does not match fixture workflow '{fixture.get('workflow')}'",
                    remediation="Align workflow_resolved with referenced fixture workflow.",
                )
            )
        invoked_skills = set(traversal.get("skills_invoked", []))
        expected_skills = set(fixture.get("expected_skills", []))
        missing_skills = expected_skills - invoked_skills
        if missing_skills:
            errors.append(
                ValidationError(
                    category="TRANSCRIPT",
                    file=f"results/{path.name}",
                    field="workflow_traversal.skills_invoked",
                    message=f"missing expected skill activations: {', '.join(sorted(missing_skills))}",
                    remediation="Activate expected skills in benchmark execution.",
                )
            )

    artifacts = data.get("artifacts_produced", [])
    if not isinstance(artifacts, list) or not artifacts:
        errors.append(
            ValidationError(
                category="TRANSCRIPT",
                file=f"results/{path.name}",
                field="artifacts_produced",
                message="'artifacts_produced' must be a non-empty list",
                remediation="Record produced artifacts with status in benchmark transcript.",
            )
        )
    else:
        produced_aliases = set()
        for idx, art in enumerate(artifacts):
            if not isinstance(art, dict):
                errors.append(
                    ValidationError(
                        category="TRANSCRIPT",
                        file=f"results/{path.name}",
                        field=f"artifacts_produced[{idx}]",
                        message=f"artifact entry #{idx} must be an object",
                        remediation="Ensure artifact entry is an object with alias and status.",
                    )
                )
                continue
            alias = art.get("alias")
            produced_aliases.add(alias)
            if not alias or alias not in valid_aliases:
                errors.append(
                    ValidationError(
                        category="TRANSCRIPT",
                        file=f"results/{path.name}",
                        field=f"artifacts_produced[{idx}].alias",
                        message=f"artifact #{idx} has invalid alias '{alias}'",
                        remediation="Use valid canonical artifact alias from scaffold.py.",
                    )
                )
            if art.get("status") not in ("valid", "passed"):
                errors.append(
                    ValidationError(
                        category="TRANSCRIPT",
                        file=f"results/{path.name}",
                        field=f"artifacts_produced[{alias}].status",
                        message=f"artifact '{alias}' has invalid status '{art.get('status')}'",
                        remediation="Artifact status must be 'valid' or 'passed'.",
                    )
                )
        expected_aliases = {a.get("alias") for a in fixture.get("expected_artifacts", []) if isinstance(a, dict)}
        missing_aliases = expected_aliases - produced_aliases
        if missing_aliases:
            errors.append(
                ValidationError(
                    category="TRANSCRIPT",
                    file=f"results/{path.name}",
                    field="artifacts_produced",
                    message=f"missing required artifact aliases: {', '.join(sorted(missing_aliases))}",
                    remediation="Generate all required artifacts defined in golden fixture.",
                )
            )

    quality_gates = data.get("quality_gates", {})
    if not isinstance(quality_gates, dict):
        errors.append(
            ValidationError(
                category="TRANSCRIPT",
                file=f"results/{path.name}",
                field="quality_gates",
                message="'quality_gates' must be an object",
                remediation="Record syntax check and unit test exit code results in quality_gates.",
            )
        )
    else:
        if quality_gates.get("syntax_check") != "passed":
            errors.append(
                ValidationError(
                    category="TRANSCRIPT",
                    file=f"results/{path.name}",
                    field="quality_gates.syntax_check",
                    message="quality_gates.syntax_check is not 'passed'",
                    remediation="Ensure syntax_check passes before recording benchmark run.",
                )
            )
        if quality_gates.get("unit_tests_exit_code") != 0:
            errors.append(
                ValidationError(
                    category="TRANSCRIPT",
                    file=f"results/{path.name}",
                    field="quality_gates.unit_tests_exit_code",
                    message="quality_gates.unit_tests_exit_code must be 0",
                    remediation="Ensure unit tests pass with exit code 0.",
                )
            )

    return data


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="verify fixture schema and references only (alias for --fixtures-only)",
    )
    parser.add_argument(
        "--verify-results",
        action="store_true",
        help="explicitly enforce benchmark results verification (fails if no transcripts found)",
    )
    parser.add_argument(
        "--fixtures-only",
        action="store_true",
        help="only verify golden evaluation fixtures, skipping transcripts",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="enforce strict regression guardrails across all fixtures",
    )
    parser.add_argument(
        "--format",
        choices=["pretty", "json", "summary"],
        default="pretty",
        help="output format (default: pretty)",
    )
    parser.add_argument(
        "--fixture",
        type=str,
        default=None,
        help="filter verification to a specific fixture by ID or filename",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="display expanded fixture and invariant details")
    parser.add_argument("-q", "--quiet", action="store_true", help="suppress progress messages, outputting only summary")
    args = parser.parse_args()

    skip_transcripts = args.fixtures_only or args.check_only
    if args.verify_results and skip_transcripts:
        print("ERROR: cannot combine --verify-results with --fixtures-only or --check-only (mutually exclusive)", file=sys.stderr)
        return 1

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

    # Optional filtering by fixture ID or filename
    if args.fixture:
        target = args.fixture.strip()
        matched_files = [
            f for f in eval_files
            if f.stem == target or f.name == target or target in f.name
        ]
        if not matched_files:
            # Try matching inside JSON id
            for f in eval_files:
                try:
                    data = json.loads(f.read_text(encoding="utf-8"))
                    if isinstance(data, dict) and data.get("id") == target:
                        matched_files.append(f)
                except Exception:
                    pass
        if not matched_files:
            print(f"ERROR: fixture '{args.fixture}' not found in evals/", file=sys.stderr)
            return 1
        eval_files = matched_files

    errors: list[ValidationError] = []
    fixtures: list[tuple[Path, dict[str, Any]]] = []
    fixtures_by_id: dict[str, dict[str, Any]] = {}
    covered_workflows: set[str] = set()

    for f in eval_files:
        data = validate_eval_fixture(
            f, available_skills, available_workflows, valid_aliases, errors, strict=args.strict
        )
        if data:
            fixtures.append((f, data))
            if "id" in data:
                fixtures_by_id[data["id"]] = data
            if "workflow" in data:
                covered_workflows.add(data["workflow"])

    # If not filtering, ensure all workflows have at least one golden evaluation fixture
    if not args.fixture:
        uncovered_wfs = sorted(available_workflows - covered_workflows)
        if uncovered_wfs:
            errors.append(
                ValidationError(
                    category="WORKFLOW_COVERAGE",
                    file="evals/",
                    field="workflows",
                    message=f"missing evaluation fixtures for workflows: {', '.join(uncovered_wfs)}",
                    remediation="Add missing workflow fixtures to evals/.",
                )
            )

    # Benchmark results transcripts verification
    transcripts: list[tuple[Path, dict[str, Any]]] = []
    results_dir = evals_dir / "results"
    if not skip_transcripts and results_dir.is_dir():
        result_files = sorted(results_dir.glob("*.json"))
        for rf in result_files:
            # When filtering by fixture, skip transcripts for unrelated fixtures
            if args.fixture:
                try:
                    raw_t = json.loads(rf.read_text(encoding="utf-8"))
                    if isinstance(raw_t, dict) and raw_t.get("fixture_id") not in fixtures_by_id:
                        continue
                except Exception:
                    pass
            rdata = validate_benchmark_transcript(rf, fixtures_by_id, valid_aliases, errors)
            if rdata:
                transcripts.append((rf, rdata))

    # Enforce transcript presence when explicitly requested
    if args.verify_results and not transcripts:
        if not any(e.category == "TRANSCRIPT" for e in errors):
            if args.fixture:
                msg = f"no benchmark execution transcripts found matching fixture '{args.fixture}' under --verify-results"
                remed = f"Add a benchmark execution transcript for '{args.fixture}' under evals/results/."
            else:
                msg = "no benchmark execution transcripts found to verify under --verify-results"
                remed = "Ensure at least one valid benchmark transcript exists in evals/results/."
            errors.append(
                ValidationError(
                    category="TRANSCRIPT",
                    file="evals/results/",
                    field="transcripts",
                    message=msg,
                    remediation=remed,
                )
            )

    # Error handling and formatted output
    if errors:
        if args.format == "json":
            payload = {
                "status": "failed",
                "total_fixtures": len(fixtures),
                "total_transcripts": len(transcripts),
                "error_count": len(errors),
                "errors": [err.to_dict() for err in errors],
            }
            print(json.dumps(payload, indent=2), file=sys.stderr)
        else:
            print(f"FAILED: {len(errors)} validation errors found in evaluation system:", file=sys.stderr)
            for err in errors:
                print(f"  {err}", file=sys.stderr)
        return 1

    # Format output
    if args.format == "json":
        payload = {
            "status": "passed",
            "total_fixtures": len(fixtures),
            "total_transcripts": len(transcripts),
            "covered_workflows": sorted(list(covered_workflows)),
            "fixtures": [
                {
                    "id": d["id"],
                    "workflow": d["workflow"],
                    "spec_target": d["agent_spec_target"],
                    "guardrails_count": len(d["guardrails"]) if isinstance(d.get("guardrails"), (dict, list)) else 0,
                    "invariants_count": len(d.get("invariants", [])),
                }
                for _, d in fixtures
            ],
            "transcripts": [
                {
                    "run_id": rd["run_id"],
                    "fixture_id": rd["fixture_id"],
                    "runtime": rd["runtime"],
                    "model": rd.get("model", "unknown"),
                    "total_tokens": rd.get("execution_metrics", {}).get("total_tokens", 0),
                }
                for _, rd in transcripts
            ],
        }
        print(json.dumps(payload, indent=2))
        return 0

    if not args.quiet and args.format != "summary":
        print("=" * 72)
        print(" SDLC GOLDEN TASK FIXTURES SEMANTIC GATE (Google agents-cli)")
        print("=" * 72)
        for f, d in fixtures:
            guardrails_count = len(d["guardrails"]) if isinstance(d.get("guardrails"), (dict, list)) else 0
            print(f"PASS: {d['id']:<28} | Workflow: {d['workflow']}")
            print(f"      Title: {d['name']}")
            print(f"      Spec Target: {d['agent_spec_target']}")
            print(f"      Skills ({len(d['expected_skills'])}): {', '.join(d['expected_skills'])}")
            print(f"      Scaffold Aliases ({len(d['expected_artifacts'])}): {', '.join(a['alias'] for a in d['expected_artifacts'])}")
            print(f"      Guardrails ({guardrails_count}) | Invariants ({len(d['invariants'])})")
            if args.verbose:
                print("      Stages:")
                for stg in d.get("expected_stages", []):
                    print(f"        - {stg}")
                print("      Invariants:")
                for inv in d.get("invariants", []):
                    print(f"        * {inv}")
                if isinstance(d.get("guardrails"), dict):
                    print("      Guardrails Details:")
                    for gk, gv in d["guardrails"].items():
                        print(f"        > {gk}: {gv}")
            print("-" * 72)

        if transcripts:
            print("=" * 72)
            print(" SDLC BENCHMARK RESULTS & TRANSCRIPTS GATE")
            print("=" * 72)
            for rf, rd in transcripts:
                metrics = rd.get("execution_metrics", {})
                tokens = metrics.get("total_tokens", 0)
                skills_count = len(rd.get("workflow_traversal", {}).get("skills_invoked", []))
                arts_count = len(rd.get("artifacts_produced", []))
                print(f"PASS: {rd['run_id']:<28} | Fixture: {rd['fixture_id']}")
                print(f"      Runtime: {rd['runtime']} ({rd.get('model', 'unknown')}) | Tokens: {tokens}")
                print(f"      Skills ({skills_count}) | Artifacts ({arts_count}) | Quality Gates: passed")
                if args.verbose and "guardrails_evaluated" in rd:
                    print("      Guardrails Evaluated:")
                    for gk, gv in rd["guardrails_evaluated"].items():
                        print(f"        > {gk}: {gv}")
                print("-" * 72)

    # Invariant required by tests/test_pack.py:289
    print(f"SUCCESS: Verified {len(fixtures)} golden evaluation fixtures across all {len(covered_workflows)} workflows.")
    if transcripts and not args.quiet:
        print(f"SUCCESS: Verified {len(transcripts)} benchmark execution transcript(s) in evals/results/.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
