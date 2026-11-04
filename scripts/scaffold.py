#!/usr/bin/env python3
"""Scaffold canonical SDLC artifacts from standardized pack templates."""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Mapping of artifact aliases to (template_relative_path, default_destination_pattern)
ARTIFACT_MAP: dict[str, tuple[str, str]] = {
    # Discovery & Requirements (specs/)
    "brief": ("specs/opportunity-brief.md", "docs/discovery/{id}/opportunity-brief.md"),
    "prd": ("specs/PRD.md", "docs/prd.md"),
    "spec": ("specs/feature-spec.md", "docs/features/{id}/spec.md"),
    "srs": ("specs/SRS.md", "docs/specs/SRS.md"),
    "rtm": ("specs/RTM.md", "docs/specs/RTM.md"),
    "arch": ("specs/architecture-overview.md", "docs/architecture.md"),
    "adr": ("specs/ADR.md", "docs/adr/ADR-{id}-{slug}.md"),
    "design": ("specs/DDS.md", "docs/features/{id}/design.md"),
    # Machine-Executable Contracts (contracts/)
    "openapi": ("contracts/openapi.yaml", "contracts/openapi.yaml"),
    "asyncapi": ("contracts/asyncapi.yaml", "contracts/asyncapi.yaml"),
    "stomp": ("contracts/stomp-websocket.yaml", "contracts/stomp-websocket.yaml"),
    "proto": ("contracts/service.proto", "contracts/service.proto"),
    "graphql": ("contracts/schema.graphql", "contracts/schema.graphql"),
    "data-contract": ("contracts/data-contract.json", "contracts/data-contract.json"),
    "migration": ("contracts/migration.sql", "migrations/{id}_migration.sql"),
    # Planning & Delivery (delivery/)
    "plan": ("delivery/plan.md", "docs/features/{id}/plan.md"),
    "tasks": ("delivery/tasks.md", "docs/features/{id}/tasks.md"),
    "handoff": ("delivery/task-handoff.md", ".agent/tasks/{id}.md"),
    "acceptance": ("delivery/acceptance-report.md", "docs/features/{id}/acceptance-report.md"),
    "pr": ("delivery/pull-request.md", ".github/pull_request_template.md"),
    "release": ("delivery/release-notes.md", "docs/releases/v{id}.md"),
    "checklist": ("delivery/release-checklist.md", "docs/releases/release-checklist.md"),
    "deprecation": ("delivery/deprecation-notice.md", "docs/migrations/{id}-deprecation.md"),
    # Platform & Operations (platform/)
    "alert-rules": ("platform/alert-rules.yaml", "deploy/alerts/{id}-rules.yaml"),
    "runbook": ("platform/runbook.md", "docs/runbooks/{id}.md"),
    "postmortem": ("platform/incident-postmortem.md", "docs/incidents/{id}/postmortem.md"),
    # Governance, Security & Measurement (governance/)
    "constitution": ("governance/constitution.md", "AGENTS.md"),
    "threat-model": ("governance/threat-model.md", "docs/security/threat-model-{id}.md"),
    "tracking": ("governance/tracking-plan.md", "docs/analytics/tracking-plan.md"),
    "event-schema": ("governance/event-schema.json", "analytics/schemas/{id}-event.json"),
    "experiment": ("governance/experiment-brief.md", "docs/experiments/{id}.md"),
}


def slugify(value: str) -> str:
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-")


def resolve_template(name: str) -> Path | None:
    roots = [
        Path("templates"),
        ROOT / "templates",
        ROOT / "skills" / "using-sdlc-skills" / "assets" / "templates",
    ]
    for r in roots:
        if not r.is_dir():
            continue
        candidate = r / name
        if candidate.is_file():
            return candidate
        # filename-only fallback
        matches = [p for p in r.rglob(Path(name).name) if p.is_file()]
        if matches:
            return matches[0]
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

