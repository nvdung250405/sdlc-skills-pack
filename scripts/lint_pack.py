#!/usr/bin/env python3
"""Validate the portable SDLC pack, upstream selection, references and provenance.

Default mode can run offline and reports a partial pack as warnings. --strict is the
release/installation gate: all selected upstream skills, source licenses, resource
snapshots, and commit/provenance records must be present.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_FRONTMATTER = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}


def parse_frontmatter(text: str) -> tuple[dict[str, str] | None, str | None]:
    match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", text, re.S)
    if not match:
        return None, "missing YAML frontmatter delimiters"
    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#") or line[:1].isspace():
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            if key in values:
                return values, f"duplicate frontmatter key {key!r}"
            values[key] = value.strip().strip("\"'")
    extra = set(values) - ALLOWED_FRONTMATTER
    if extra:
        return values, f"non-portable frontmatter keys: {sorted(extra)}"
    return values, None


def local_markdown_target(doc: Path, raw: str) -> Path | None:
    target = raw.strip().strip("<>").split()[0] if raw.strip() else ""
    target = target.split("#", 1)[0].split("?", 1)[0]
    if not target or target.startswith(("https://", "http://", "mailto:", "data:", "#", "/")):
        return None
    try:
        return (doc.parent / target).resolve()
    except OSError:
        return None


def check_markdown_links(doc: Path, errors: list[str]) -> None:
    try:
        body = doc.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        errors.append(f"{doc.relative_to(ROOT)}: cannot read Markdown: {exc}")
        return
    for raw in re.findall(r"(?<!!)(?:\[[^\]]*\]|\*\*[^*]+\*\*)\(([^)]+)\)", body):
        target = local_markdown_target(doc, raw)
        if target is not None and not target.exists():
            errors.append(f"{doc.relative_to(ROOT)}: broken local link {raw!r}")


def read_json(path: Path, label: str, errors: list[str]) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{path.relative_to(ROOT)}: cannot parse {label}: {exc}")
        return None
    if not isinstance(value, dict):
        errors.append(f"{path.relative_to(ROOT)}: {label} must be a JSON object")
        return None
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true", help="fail if sync/provenance/resources are incomplete")
    parser.add_argument("--json", action="store_true", help="emit a machine-readable summary")
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []
    skill_count = 0
    available_by_tier: dict[str, set[str]] = {"skills": set(), "extras": set()}
    seen_names: dict[str, Path] = {}

    for tier_name in ("skills", "extras"):
        root = ROOT / tier_name
        if not root.is_dir():
            errors.append(f"missing required directory {tier_name}/")
            continue
        for skill_dir in sorted((p for p in root.iterdir() if p.is_dir()), key=lambda p: p.name.casefold()):
            skill_count += 1
            skill_file = skill_dir / "SKILL.md"
            if not skill_file.is_file():
                errors.append(f"{tier_name}/{skill_dir.name}: missing SKILL.md")
                continue
            available_by_tier[tier_name].add(skill_dir.name)
            if skill_dir.name in seen_names:
                errors.append(f"duplicate skill folder name {skill_dir.name!r}: {seen_names[skill_dir.name]} and {skill_dir}")
            seen_names[skill_dir.name] = skill_dir

            text = skill_file.read_text(encoding="utf-8")
            metadata, problem = parse_frontmatter(text)
            if problem or metadata is None:
                errors.append(f"{tier_name}/{skill_dir.name}: {problem or 'invalid frontmatter'}")
                continue
            if metadata.get("name") != skill_dir.name:
                errors.append(f"{tier_name}/{skill_dir.name}: frontmatter name does not match folder")
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", skill_dir.name):
                errors.append(f"{tier_name}/{skill_dir.name}: invalid skill folder name")
            description = metadata.get("description", "")
            if not description:
                errors.append(f"{tier_name}/{skill_dir.name}: empty description")
            if len(description) > 1024:
                errors.append(f"{tier_name}/{skill_dir.name}: description exceeds 1024 characters")
            if len(text.splitlines()) > 1200:
                warnings.append(f"{tier_name}/{skill_dir.name}: SKILL.md exceeds 1200 lines; consider progressive disclosure")
            for doc in skill_dir.rglob("*.md"):
                check_markdown_links(doc, errors)

    # Validate pack-owned docs too. Do not scan raw upstream snapshots because they
    # intentionally preserve source links to files outside the selected snapshot.
    for relative in ("workflows", "templates", "docs"):
        folder = ROOT / relative
        if folder.exists():
            for doc in folder.rglob("*.md"):
                check_markdown_links(doc, errors)

    manifest = read_json(ROOT / "upstream.json", "upstream manifest", errors)
    expected_by_tier: dict[str, set[str]] = {"skills": set(), "extras": set()}
    expected_resources: list[tuple[str, str, bool]] = []
    expected_sources: set[str] = set()
    if manifest is not None:
        if manifest.get("schema_version") != 2:
            errors.append("upstream.json: schema_version must be 2")
        upstream_ids: set[str] = set()
        destinations: set[str] = set()
        for upstream in manifest.get("upstreams", []):
            source_id = upstream.get("id")
            if not source_id or source_id in upstream_ids:
                errors.append(f"upstream.json: missing or duplicate upstream id {source_id!r}")
                continue
            upstream_ids.add(source_id)
            expected_sources.add(source_id)
            if not upstream.get("url") or not upstream.get("license_file"):
                errors.append(f"upstream.json: {source_id} must define url and license_file")
            for item in upstream.get("items", []):
                tier = item.get("tier", "skills")
                name = item.get("name", Path(item.get("src", "unknown")).name)
                if tier not in expected_by_tier:
                    errors.append(f"upstream.json: unsupported tier {tier!r} for {source_id}:{name}")
                    continue
                destination = f"{tier}/{name}"
                if destination in destinations:
                    errors.append(f"upstream.json: duplicate destination {destination}")
                destinations.add(destination)
                expected_by_tier[tier].add(name)
            for resource in upstream.get("resources", []):
                expected_resources.append((source_id, resource.get("dest", ""), resource.get("required", True)))

        # Locally adapted skills are explicitly listed and never overwritten by upstream sync.
        for item in manifest.get("derived_skills", []):
            tier = item.get("tier", "skills")
            name = item.get("name")
            if tier not in expected_by_tier or not name:
                errors.append(f"upstream.json: invalid derived skill declaration {item!r}")
                continue
            if name in expected_by_tier[tier]:
                errors.append(f"upstream.json: derived skill duplicates selected destination {tier}/{name}")
            expected_by_tier[tier].add(name)

        # A pack-owned skill directory is a legitimate installed skill as well.
        expected_by_tier["skills"].update({"using-sdlc-skills", "task-handoff"})
        expected_by_tier["extras"].add("skill-authoring")
        for tier_name, expected in expected_by_tier.items():
            missing = sorted(expected - available_by_tier[tier_name])
            if missing:
                message = f"upstream {tier_name} not materialized yet: " + ", ".join(missing)
                (errors if args.strict else warnings).append(message)

    adapter_data = read_json(ROOT / "adapters" / "agents.json", "agent adapter config", errors)
    skill_map = read_json(ROOT / "manifests" / "skill-map.json", "skill map", errors)
    if adapter_data is not None:
        if not adapter_data.get("agents"):
            errors.append("adapters/agents.json: no agents configured")
        for agent, options in adapter_data.get("agents", {}).items():
            if not options.get("project") or not options.get("global"):
                errors.append(f"adapters/agents.json: {agent} must define project and global paths")

    if skill_map is not None:
        groups = skill_map.get("groups", {})
        mapped = {name for members in groups.values() if isinstance(members, list) for name in members}
        duplicate_map = sorted(name for name in mapped if sum(name in members for members in groups.values()) > 1)
        if duplicate_map:
            errors.append("manifests/skill-map.json: skill appears in multiple groups: " + ", ".join(duplicate_map))
        known = set().union(*expected_by_tier.values())
        unknown_map = sorted(mapped - known)
        if unknown_map:
            errors.append("manifests/skill-map.json: refers to skills absent from upstream.json/pack-owned list: " + ", ".join(unknown_map))
        unmapped = sorted(known - mapped)
        if unmapped:
            message = "selected skills missing from role map: " + ", ".join(unmapped)
            (errors if args.strict else warnings).append(message)
        for owner, rule in skill_map.get("precedence", {}).items():
            if owner not in known:
                errors.append(f"manifests/skill-map.json: precedence owner {owner!r} is not a selected skill")
            if not isinstance(rule, str) or not rule.strip():
                errors.append(f"manifests/skill-map.json: precedence entry for {owner!r} needs an explanation")

    required_files = [
        # 11 Standardized Workflows
        "workflows/full-sdlc.md", "workflows/feature-loop.md", "workflows/bug-fix.md",
        "workflows/quick-change.md", "workflows/agent-handoff-contract.md",
        "workflows/incident-response.md", "workflows/refactoring.md",
        "workflows/performance-tuning.md", "workflows/dependency-upgrade.md",
        "workflows/deprecation-and-migration.md", "workflows/experimentation-loop.md",
        # 41 Canonical Artifact Templates across 5 Functional Groups
        # specs/
        "templates/specs/opportunity-brief.md", "templates/specs/research-synthesis.md",
        "templates/specs/PRD.md", "templates/specs/feature-spec.md", "templates/specs/SRS.md",
        "templates/specs/RTM.md", "templates/specs/architecture-overview.md",
        "templates/specs/ADR.md", "templates/specs/DDS.md", "templates/specs/design-tokens.json",
        # contracts/
        "templates/contracts/openapi.yaml", "templates/contracts/asyncapi.yaml",
        "templates/contracts/stomp-websocket.yaml", "templates/contracts/service.proto",
        "templates/contracts/schema.graphql", "templates/contracts/data-contract.json",
        "templates/contracts/migration.sql",
        # delivery/
        "templates/delivery/plan.md", "templates/delivery/tasks.md",
        "templates/delivery/task-handoff.md", "templates/delivery/acceptance-report.md",
        "templates/delivery/benchmark-report.md", "templates/delivery/pull-request.md",
        "templates/delivery/release-notes.md", "templates/delivery/release-checklist.md",
        "templates/delivery/deprecation-notice.md",
        # platform/
        "templates/platform/ci-pipeline.yaml", "templates/platform/devcontainer.json",
        "templates/platform/pre-commit-config.yaml", "templates/platform/alert-rules.yaml",
        "templates/platform/runbook.md", "templates/platform/incident-postmortem.md",
        "templates/platform/env.example",
        # governance/
        "templates/governance/constitution.md", "templates/governance/threat-model.md",
        "templates/governance/security-assessment.md", "templates/governance/model-card.md",
        "templates/governance/cost-attribution-report.md", "templates/governance/tracking-plan.md",
        "templates/governance/event-schema.json", "templates/governance/experiment-brief.md",
        # Pack-owned assets
        "skills/task-handoff/assets/task-template.md",
    ]
    for rel in required_files:
        if not (ROOT / rel).is_file():
            errors.append(f"missing pack contract file: {rel}")

    # Check synchronization of router bundled assets
    router_templates = ROOT / "skills" / "using-sdlc-skills" / "assets" / "templates"
    for tmpl in (ROOT / "templates").rglob("*"):
        if tmpl.is_file() and tmpl.name != "README.md":
            rel = tmpl.relative_to(ROOT / "templates")
            bundled = router_templates / rel
            if not bundled.is_file():
                errors.append(f"router bundled template missing: {bundled.relative_to(ROOT)}")
            elif bundled.read_bytes() != tmpl.read_bytes():
                errors.append(f"router bundled template out of sync with root: {rel}")

    router_workflows = ROOT / "skills" / "using-sdlc-skills" / "assets" / "workflows"
    for wf in (ROOT / "workflows").glob("*.md"):
        bundled = router_workflows / wf.name
        if not bundled.is_file():
            errors.append(f"router bundled workflow missing: {bundled.relative_to(ROOT)}")
        elif bundled.read_bytes() != wf.read_bytes():
            errors.append(f"router bundled workflow out of sync with root: {wf.name}")

    lock_path = ROOT / "manifests" / "upstream-lock.json"
    provenance_path = ROOT / "manifests" / "skill-provenance.json"
    if not lock_path.is_file():
        msg = "no upstream lock yet; first successful sync records commits in manifests/upstream-lock.json"
        (errors if args.strict else warnings).append(msg)
        lock = None
    else:
        lock = read_json(lock_path, "upstream lock", errors)
        if lock is not None:
            records = lock.get("sources", {})
            for source in (manifest or {}).get("upstreams", []):
                source_id = source.get("id")
                record = records.get(source_id, {})
                if not record.get("commit"):
                    (errors if args.strict else warnings).append(f"upstream lock has no commit for {source_id}")
                if record.get("url") and record.get("url") != source.get("url"):
                    errors.append(f"upstream lock URL differs from upstream.json for {source_id}")
                if not record.get("url"):
                    (errors if args.strict else warnings).append(f"upstream lock has no URL for {source_id}")

    missing_resources = []
    for source_id, destination, required in expected_resources:
        if destination and not (ROOT / destination).is_file():
            if required:
                missing_resources.append(f"{source_id}:{destination}")
    if missing_resources:
        message = "upstream reference templates not materialized: " + ", ".join(missing_resources)
        (errors if args.strict else warnings).append(message)

    # All upstream licenses/notices must exist before distributing a fully synced pack.
    if manifest is not None:
        for upstream in manifest.get("upstreams", []):
            source_id = upstream.get("id", "unknown")
            license_path = ROOT / "third_party" / source_id / "LICENSE"
            if not license_path.is_file():
                message = f"missing copied upstream license: third_party/{source_id}/LICENSE"
                (errors if args.strict else warnings).append(message)
            if upstream.get("notice_file") and not (ROOT / "third_party" / source_id / "NOTICE").is_file():
                message = f"missing copied upstream notice: third_party/{source_id}/NOTICE"
                (errors if args.strict else warnings).append(message)

    if manifest is not None:
        for source in manifest.get("derived_sources", []):
            source_id = source.get("id", "unknown")
            license_path = ROOT / "third_party" / source_id / "LICENSE"
            if not license_path.is_file():
                message = f"missing copied derived-source license: third_party/{source_id}/LICENSE"
                (errors if args.strict else warnings).append(message)

    if manifest is not None and manifest.get("upstreams") and not provenance_path.is_file():
        message = "no skill provenance yet; a successful sync generates manifests/skill-provenance.json"
        (errors if args.strict else warnings).append(message)
    elif provenance_path.is_file():
        provenance = read_json(provenance_path, "skill provenance", errors)
        if provenance is not None:
            if not isinstance(provenance.get("skills"), dict) or not isinstance(provenance.get("resources"), dict):
                errors.append("manifests/skill-provenance.json: skills/resources must be JSON objects")
            elif manifest is not None:
                skill_records = provenance["skills"]
                resource_records = provenance["resources"]
                locked_sources = (lock or {}).get("sources", {})
                for source in manifest.get("upstreams", []):
                    source_id = source.get("id")
                    source_lock = locked_sources.get(source_id, {})
                    source_commit = source_lock.get("commit")
                    for item in source.get("items", []):
                        tier = item.get("tier", "skills")
                        name = item.get("name", Path(item.get("src", "unknown")).name)
                        destination = f"{tier}/{name}"
                        record = skill_records.get(destination)
                        if not record:
                            message = f"provenance entry missing for {destination}"
                            (errors if args.strict else warnings).append(message)
                            continue
                        for key, expected in (("upstream", source_id), ("source_path", item.get("src")), ("license", source.get("license"))):
                            if record.get(key) != expected:
                                errors.append(f"provenance mismatch for {destination}: {key} should be {expected!r}")
                        if source_commit and record.get("commit") != source_commit:
                            errors.append(f"provenance commit mismatch for {destination}")
                    for resource in source.get("resources", []):
                        destination = resource.get("dest", "")
                        record = resource_records.get(destination)
                        if not record:
                            message = f"resource provenance entry missing for {destination}"
                            (errors if args.strict else warnings).append(message)
                            continue
                        for key, expected in (("upstream", source_id), ("source_path", resource.get("src")), ("license", source.get("license"))):
                            if record.get(key) != expected:
                                errors.append(f"resource provenance mismatch for {destination}: {key} should be {expected!r}")
                        if source_commit and record.get("commit") != source_commit:
                            errors.append(f"resource provenance commit mismatch for {destination}")
                # Adapted skills are manual-review-only, content-hashed and never overwritten by sync.
                for item in (manifest or {}).get("derived_skills", []):
                    tier = item.get("tier", "skills")
                    name = item.get("name", "")
                    destination = f"{tier}/{name}"
                    record = skill_records.get(destination)
                    if not record:
                        message = f"provenance entry missing for derived skill {destination}"
                        (errors if args.strict else warnings).append(message)
                        continue
                    expected_fields = {
                        "upstream": item.get("source_id"),
                        "source_path": item.get("source_path"),
                        "license": item.get("license"),
                        "revision_status": item.get("revision_status"),
                        "kind": "adapted-derived-skill",
                        "refresh_policy": "manual-review-only",
                    }
                    for key, expected in expected_fields.items():
                        if record.get(key) != expected:
                            errors.append(f"provenance mismatch for {destination}: {key} should be {expected!r}")
                    skill_file = ROOT / destination / "SKILL.md"
                    if skill_file.is_file() and record.get("content_sha256"):
                        digest = hashlib.sha256(skill_file.read_bytes()).hexdigest()
                        if digest != record.get("content_sha256"):
                            errors.append(f"provenance content hash mismatch for {destination}; update provenance after a reviewed edit")
                    elif args.strict:
                        errors.append(f"provenance content hash missing for {destination}")

    print(f"Checked {skill_count} materialized skills across skills/ and extras/.")
    for warning in warnings:
        print("WARNING:", warning)
    for error in errors:
        print("ERROR:", error)
    if args.json:
        print(json.dumps({
            "checked_skills": skill_count,
            "warnings": warnings,
            "errors": errors,
            "complete": not errors and not any("not materialized" in w or "no upstream lock" in w for w in warnings),
        }, indent=2, ensure_ascii=False))
    if errors:
        print("Pack validation FAILED.")
        return 1
    if warnings:
        print("Local structure is valid, but upstream synchronization/release checks may still be incomplete.")
    else:
        print("Pack structure, upstream selection, resources and provenance are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
