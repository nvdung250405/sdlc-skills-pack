#!/usr/bin/env python3
"""Scaffold canonical SDLC artifacts from standardized pack templates."""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Mapping of artifact aliases to (template_filename, default_destination_pattern)
ARTIFACT_MAP: dict[str, tuple[str, str]] = {
    # Discovery & Requirements
    "brief": ("opportunity-brief.md", "docs/discovery/{id}/opportunity-brief.md"),
    "research": ("research-synthesis.md", "docs/discovery/{id}/research-synthesis.md"),
    "prd": ("PRD.md", "docs/prd.md"),
    "spec": ("feature-spec.md", "docs/features/{id}/spec.md"),
    "srs": ("SRS.md", "docs/specs/SRS.md"),
    "rtm": ("RTM.md", "docs/specs/RTM.md"),
    # Architecture & Executable Contracts
    "arch": ("architecture-overview.md", "docs/architecture.md"),
    "adr": ("ADR.md", "docs/adr/ADR-{id}-{slug}.md"),
    "design": ("DDS.md", "docs/features/{id}/design.md"),
    "openapi": ("openapi.yaml", "contracts/openapi.yaml"),
    "asyncapi": ("asyncapi.yaml", "contracts/asyncapi.yaml"),
    "stomp": ("stomp-websocket.yaml", "contracts/stomp-websocket.yaml"),
    "proto": ("service.proto", "contracts/service.proto"),
    "graphql": ("schema.graphql", "contracts/schema.graphql"),
    "data-contract": ("data-contract.json", "contracts/data-contract.json"),
    "tokens": ("design-tokens.json", "design/tokens.json"),
    # Planning & Construction
    "plan": ("plan.md", "docs/features/{id}/plan.md"),
    "tasks": ("tasks.md", "docs/features/{id}/tasks.md"),
    "handoff": ("task-handoff.md", ".agent/tasks/{id}.md"),
    "migration": ("migration.sql", "migrations/{id}_migration.sql"),
    "env": ("env.example", ".env.example"),
    # Testing & Verification
    "acceptance": ("acceptance-report.md", "docs/features/{id}/acceptance-report.md"),
    "benchmark": ("benchmark-report.md", "docs/features/{id}/benchmark-report.md"),
    # Review & Release
    "pr": ("pull-request.md", ".github/pull_request_template.md"),
    "release": ("release-notes.md", "docs/releases/v{id}.md"),
    "checklist": ("release-checklist.md", "docs/releases/release-checklist.md"),
    "ci": ("ci-pipeline.yaml", ".github/workflows/ci.yaml"),
    # Operations & Incidents
    "postmortem": ("incident-postmortem.md", "docs/incidents/{id}/postmortem.md"),
    "runbook": ("runbook.md", "docs/runbooks/{id}.md"),
    "alert-rules": ("alert-rules.yaml", "deploy/alerts/{id}-rules.yaml"),
    # Maintenance & Learning
    "deprecation": ("deprecation-notice.md", "docs/migrations/{id}-deprecation.md"),
    "experiment": ("experiment-brief.md", "docs/experiments/{id}.md"),
    "tracking": ("tracking-plan.md", "docs/analytics/tracking-plan.md"),
    "event-schema": ("event-schema.json", "analytics/schemas/{id}-event.json"),
    # Security, DevEx, AI Governance & FinOps
    "threat-model": ("threat-model.md", "docs/security/threat-model-{id}.md"),
    "security": ("security-assessment.md", "docs/security/security-assessment-{id}.md"),
    "devcontainer": ("devcontainer.json", ".devcontainer/devcontainer.json"),
    "pre-commit": ("pre-commit-config.yaml", ".pre-commit-config.yaml"),
    "constitution": ("constitution.md", "AGENTS.md"),
    "model-card": ("model-card.md", "docs/ai/model-card-{id}.md"),
    "cost": ("cost-attribution-report.md", "docs/finops/cost-report-{id}.md"),
}


def slugify(value: str) -> str:
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-")


def resolve_template(name: str) -> Path | None:
    # 1. Project-level templates/
    candidate = Path("templates") / name
    if candidate.is_file():
        return candidate
    # 2. Pack root templates/
    candidate = ROOT / "templates" / name
    if candidate.is_file():
        return candidate
    # 3. Router bundled assets
    candidate = ROOT / "skills" / "using-sdlc-skills" / "assets" / "templates" / name
    if candidate.is_file():
        return candidate
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("type", choices=sorted(ARTIFACT_MAP.keys()), help="Type of artifact to scaffold")
    parser.add_argument("--id", default="sample", help="Identifier (e.g. feature-id, ticket-id, version, ADR number)")
    parser.add_argument("--title", default="", help="Title or short description (used for slugs)")
    parser.add_argument("--target", help="Override canonical output path")
    parser.add_argument("--force", action="store_true", help="Overwrite target file if it already exists")

    args = parser.parse_args()

    template_file, dest_pattern = ARTIFACT_MAP[args.type]
    template_path = resolve_template(template_file)

    if not template_path:
        print(f"ERROR: Template '{template_file}' not found.", file=sys.stderr)
        return 1

    slug = slugify(args.title) if args.title else slugify(args.id)
    dest_str = args.target or dest_pattern.format(id=args.id, slug=slug)
    dest_path = Path(dest_str)

    if dest_path.exists() and not args.force:
        print(f"ERROR: Destination file '{dest_path}' already exists. Use --force to overwrite.", file=sys.stderr)
        return 1

    dest_path.parent.mkdir(parents=True, exist_ok=True)
    content = template_path.read_text(encoding="utf-8")

    # Basic placeholder substitutions
    content = content.replace("[FEATURE_NAME]", args.title or args.id)
    content = content.replace("[INITIATIVE_NAME]", args.title or args.id)
    content = content.replace("FEAT-NNN", args.id.upper())
    content = content.replace("NNN", args.id)

    dest_path.write_text(content, encoding="utf-8")
    print(f"Scaffolded '{args.type}' artifact from '{template_file}' -> '{dest_path}'.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

