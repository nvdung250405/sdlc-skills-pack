#!/usr/bin/env python3
"""Synchronize selected upstream skills while preserving local adaptations and provenance.

The sync is transactional: every source is fetched, validated and staged first. Only
then are active files replaced. If a replacement fails, prior files are restored.
A first successful run records exact upstream commits in manifests/upstream-lock.json.
"""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "upstream.json"
LOCK_PATH = ROOT / "manifests" / "upstream-lock.json"
PROVENANCE_PATH = ROOT / "manifests" / "skill-provenance.json"
NOTICE_PATH = ROOT / "THIRD_PARTY_NOTICES.md"
ALLOWED_FRONTMATTER = {
    "name", "description", "license", "compatibility", "metadata", "allowed-tools"
}
PACK_OWNED_SKILLS = {"using-sdlc-skills", "task-handoff", "api-contract-testing"}


def run(command: list[str], *, cwd: Path | None = None) -> str:
    env = os.environ.copy()
    env.setdefault("GIT_TERMINAL_PROMPT", "0")
    try:
        result = subprocess.run(
            command, cwd=cwd, check=True, capture_output=True, text=True,
            encoding="utf-8", errors="replace", env=env,
        )
    except FileNotFoundError as exc:
        raise RuntimeError("Git is required for upstream sync but was not found on PATH.") from exc
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or exc.stdout or str(exc)).strip()
        raise RuntimeError(f"Command failed: {' '.join(command)}\n{detail}") from exc
    return result.stdout.strip()


def read_json(path: Path, description: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Cannot read {description} {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise RuntimeError(f"{description} must contain a JSON object: {path}")
    return value


def load_lock(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"schema_version": 1, "sources": {}, "managed_paths": []}
    data = read_json(path, "upstream lock")
    sources = data.get("sources", {})
    if not isinstance(sources, dict):
        raise RuntimeError(f"Invalid sources object in lock: {path}")
    managed = data.get("managed_paths", [])
    if not isinstance(managed, list) or any(not isinstance(x, str) for x in managed):
        raise RuntimeError(f"Invalid managed_paths list in lock: {path}")
    return data


def safe_relative(value: str, label: str) -> Path:
    rel = Path(value)
    if rel.is_absolute() or ".." in rel.parts or not rel.parts:
        raise RuntimeError(f"Unsafe {label}: {value}")
    return rel


def resolve_source(upstream: dict[str, Any], lock: dict[str, Any], update: bool, scratch: Path) -> tuple[Path, str]:
    source_id = upstream["id"]
    repo = scratch / f"repo-{source_id}"
    run(["git", "clone", "--quiet", "--filter=blob:none", "--no-checkout", upstream["url"], str(repo)])
    pinned = lock.get("sources", {}).get(source_id, {}).get("commit")
    target = upstream.get("ref", "main") if update or not pinned else pinned
    run(["git", "fetch", "--quiet", "--depth", "1", "origin", target], cwd=repo)
    run(["git", "checkout", "--quiet", "--detach", "FETCH_HEAD"], cwd=repo)
    commit = run(["git", "rev-parse", "HEAD"], cwd=repo)
    return repo, commit


def parse_frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", text, re.S)
    if not match:
        raise ValueError("missing YAML frontmatter delimiters")
    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#") or line[:1].isspace():
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip().strip("\"'")
    extra = set(values) - ALLOWED_FRONTMATTER
    if extra:
        raise ValueError(f"non-portable frontmatter keys: {sorted(extra)}")
    return values


def ensure_inside(path: Path, parent: Path, label: str) -> Path:
    resolved_path = path.resolve()
    resolved_parent = parent.resolve()
    if not resolved_path.is_relative_to(resolved_parent):
        raise RuntimeError(f"{label} escapes its expected directory: {path}")
    return resolved_path


def rewrite_shared_refs(
    skill_dir: Path,
    source_repo: Path,
    shared_refs_dir: str | None,
    patches: list[dict[str, str]] | None,
) -> list[str]:
    """Localize shared markdown references while preserving working relative links."""
    transformations: list[str] = []
    pattern = None
    shared_root = None
    if shared_refs_dir:
        shared_rel = safe_relative(shared_refs_dir, "shared reference directory")
        shared_root = ensure_inside(source_repo / shared_rel, source_repo, "shared reference directory")
        pattern = re.compile(
            r"(?P<rel>(?:\.\./)+" + re.escape(shared_refs_dir) + r"/(?P<name>[\w./-]+\.md))"
        )

    for markdown in skill_dir.rglob("*.md"):
        original = markdown.read_text(encoding="utf-8")
        updated = original
        for patch in patches or []:
            old, new = patch.get("from"), patch.get("to")
            if not old:
                raise RuntimeError(f"Empty patch source in {markdown}")
            updated = updated.replace(old, new or "")
            if updated != original:
                transformations.append(f"text replacement in {markdown.relative_to(skill_dir).as_posix()}")

        if pattern and shared_root:
            names = sorted(set(m.group("name") for m in pattern.finditer(updated)))
            target_by_name: dict[str, Path] = {}
            for name in names:
                rel_name = safe_relative(name, "shared reference path")
                source = ensure_inside(shared_root / rel_name, shared_root, "shared reference")
                if not source.is_file():
                    raise RuntimeError(f"Shared reference declared but absent: {source}")
                target = skill_dir / "references" / rel_name
                # Never overwrite a skill-local file if the shared source differs.
                if target.exists() and target.read_bytes() != source.read_bytes():
                    target = skill_dir / "references" / "_upstream_shared" / rel_name
                target.parent.mkdir(parents=True, exist_ok=True)
                if not target.exists() or target.read_bytes() != source.read_bytes():
                    shutil.copy2(source, target)
                target_by_name[name] = target
                transformations.append(f"localized shared reference {name}")

            def replace_ref(match: re.Match[str]) -> str:
                target = target_by_name[match.group("name")]
                return Path(os.path.relpath(target, markdown.parent)).as_posix()

            updated = pattern.sub(replace_ref, updated)

        if updated != original:
            markdown.write_text(updated, encoding="utf-8")

    # Keep the record short and deterministic while showing every transformation type.
    return sorted(set(transformations))


def validate_skill(skill_dir: Path, expected_name: str) -> None:
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        raise RuntimeError(f"Upstream skill has no SKILL.md: {skill_dir}")
    try:
        meta = parse_frontmatter(skill_file.read_text(encoding="utf-8"))
    except ValueError as exc:
        raise RuntimeError(f"Invalid {skill_file}: {exc}") from exc
    if meta.get("name") != expected_name:
        raise RuntimeError(
            f"Skill name mismatch at {skill_file}: expected {expected_name!r}, got {meta.get('name')!r}"
        )
    if not meta.get("description"):
        raise RuntimeError(f"Empty description in {skill_file}")
    if len(meta["description"]) > 1024:
        raise RuntimeError(f"Description exceeds 1024 characters in {skill_file}")


def generated_notices(manifest: dict[str, Any], lock: dict[str, Any]) -> str:
    lines = [
        "# Third-party notices", "",
        "This pack redistributes selected upstream skills and reference templates listed below.",
        "Keep each source's license/notice files when redistributing this pack.",
        "Upstream files are retained as close to their source as practical; portability changes are recorded in manifests/skill-provenance.json.", "",
    ]
    sources = lock.get("sources", {})
    for upstream in manifest["upstreams"]:
        source_id = upstream["id"]
        record = sources.get(source_id, {})
        commit = record.get("commit", "not yet synchronized")
        url = upstream["url"][:-4] if upstream["url"].endswith(".git") else upstream["url"]
        lines.extend([f"## {source_id} — {upstream.get('license', 'see upstream license')}", f"Source: {url} @ `{commit}`", ""])
        for item in upstream.get("items", []):
            dest = f"{item.get('tier', 'skills')}/{item.get('name', Path(item['src']).name)}"
            lines.append(f"- `{dest}` from `{item['src']}`")
        for resource in upstream.get("resources", []):
            lines.append(f"- `{resource['dest']}` from `{resource['src']}` (reference only; not installed as a skill)")
        lines.append("")
    derived_sources = {item.get("id"): item for item in manifest.get("derived_sources", [])}
    if derived_sources:
        lines.extend(["## Adapted upstream skills (manual refresh only)", ""])
        for source_id, source in derived_sources.items():
            lines.extend([
                f"### {source_id} — {source.get('license', 'see source license')}",
                f"Source: {source.get('url', '')} @ `{source.get('source_ref', 'unspecified')}`",
                f"Revision status: `{source.get('revision_status', 'unspecified')}`; refresh: `{source.get('refresh_policy', 'manual')}`.",
                source.get("note", "Adapted files are maintained locally and are not overwritten by the sync command."),
                "",
            ])
            for item in manifest.get("derived_skills", []):
                if item.get("source_id") == source_id:
                    lines.append(f"- `skills/{item.get('name')}` adapted from `{item.get('source_path')}`; transformations recorded in `manifests/skill-provenance.json`.")
            lines.append("")
    reference_sources = manifest.get("reference_sources", [])
    if reference_sources:
        lines.extend(["## Reference-only sources (not bundled)", ""])
        for source in reference_sources:
            lines.append(f"- **{source.get('id')}**: {source.get('url')} — {source.get('purpose', 'reference only')}.")
        lines.append("")
    lines.extend([
        "## Pack-owned integration assets", "",
        "The router/handoff/authoring skills, workflows, adapters, manifests, scripts, and portable templates are integration assets in this pack and are governed by the root LICENSE. Adapted skills are explicitly marked, content-hashed and not overwritten by upstream sync.", "",
    ])
    return "\n".join(lines)


def add_action(actions: dict[Path, Path], rel: Path, staged: Path) -> None:
    rel = safe_relative(rel.as_posix(), "destination")
    for existing in actions:
        if rel == existing or rel.is_relative_to(existing) or existing.is_relative_to(rel):
            raise RuntimeError(f"Overlapping or duplicate sync destinations: {existing} and {rel}")
    actions[rel] = staged


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--update", action="store_true", help="refresh all upstream refs and update the lock")
    parser.add_argument("--prune", action="store_true", help="archive previously managed paths no longer selected by the manifest")
    parser.add_argument("--dry-run", action="store_true", help="fetch/stage/validate without modifying pack files")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST, help="manifest path (default: upstream.json)")
    args = parser.parse_args()

    try:
        manifest = read_json(args.manifest, "upstream manifest")
        old_lock = load_lock(LOCK_PATH)
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if manifest.get("schema_version", 0) != 2 or not isinstance(manifest.get("upstreams"), list):
        print("ERROR: upstream.json must use schema_version 2 and contain an upstreams list.", file=sys.stderr)
        return 2
    ids = [u.get("id") for u in manifest["upstreams"]]
    if any(not i for i in ids) or len(set(ids)) != len(ids):
        print("ERROR: every upstream must have a unique non-empty id.", file=sys.stderr)
        return 2

    scratch = Path(tempfile.mkdtemp(prefix=".sdlc-sync-", dir=str(ROOT)))
    payload = scratch / "payload"
    payload.mkdir()
    staged_lock: dict[str, Any] = {"schema_version": 1, "sources": {}, "managed_paths": []}
    actions: dict[Path, Path] = {}
    provenance: dict[str, Any] = {"schema_version": 1, "skills": {}, "resources": {}}
    report: list[str] = []

    try:
        for upstream in manifest["upstreams"]:
            source_id = upstream["id"]
            print(f"Fetching {source_id}...")
            repo, commit = resolve_source(upstream, old_lock, args.update, scratch)
            license_rel = safe_relative(upstream.get("license_file", "LICENSE"), "license path")
            license_src = ensure_inside(repo / license_rel, repo, "license file")
            if not license_src.is_file():
                raise RuntimeError(f"License file missing for {source_id}: {license_rel}")

            license_rel_dest = Path("third_party") / source_id
            license_stage = payload / license_rel_dest
            license_stage.mkdir(parents=True, exist_ok=True)
            shutil.copy2(license_src, license_stage / "LICENSE")
            notice_rel = upstream.get("notice_file")
            if notice_rel:
                notice_source_rel = safe_relative(notice_rel, "notice path")
                notice_src = ensure_inside(repo / notice_source_rel, repo, "notice file")
                if not notice_src.is_file():
                    raise RuntimeError(f"NOTICE file missing for {source_id}: {notice_rel}")
                shutil.copy2(notice_src, license_stage / "NOTICE")
            add_action(actions, license_rel_dest, license_stage)

            record: dict[str, Any] = {
                "url": upstream["url"],
                "ref": upstream.get("ref", "main"),
                "commit": commit,
                "license": upstream.get("license", "unknown"),
                "license_file": license_rel.as_posix(),
                "items": [],
            }
            transformations_common = upstream.get("transformations", [])
            for item in upstream.get("items", []):
                source_rel = safe_relative(item["src"], "upstream item path")
                tier = item.get("tier", "skills")
                if tier not in {"skills", "extras"}:
                    raise RuntimeError(f"Unsupported tier {tier!r} for {item['src']}")
                name = item.get("name", source_rel.name)
                if tier == "skills" and name in PACK_OWNED_SKILLS:
                    raise RuntimeError(f"Upstream skill {name!r} collides with a pack-owned skill.")
                dest_rel = safe_relative((Path(tier) / name).as_posix(), "skill destination")
                source = ensure_inside(repo / source_rel, repo, "upstream skill directory")
                if not source.is_dir():
                    raise RuntimeError(f"Required skill directory missing from {source_id}: {source_rel}")
                staged = payload / dest_rel
                exclude_patterns = item.get("exclude", [])
                shutil.copytree(
                    source, staged,
                    ignore=lambda directory, names: [n for n in names if any(fnmatch.fnmatch(n, p) for p in exclude_patterns)],
                )
                local_transforms = rewrite_shared_refs(
                    staged, repo, upstream.get("shared_refs_dir"), item.get("patches")
                )
                validate_skill(staged, name)
                add_action(actions, dest_rel, staged)
                item_record = {
                    "source_path": source_rel.as_posix(),
                    "destination": dest_rel.as_posix(),
                    "name": name,
                    "transformations": sorted(set(transformations_common + local_transforms)),
                }
                record["items"].append(item_record)
                provenance["skills"][dest_rel.as_posix()] = {
                    "upstream": source_id, "source_path": source_rel.as_posix(), "commit": commit,
                    "license": upstream.get("license", "unknown"),
                    "transformations": item_record["transformations"],
                }
                report.append(f"{source_id}@{commit[:7]} -> {dest_rel.as_posix()}")

            for resource in upstream.get("resources", []):
                source_rel = safe_relative(resource["src"], "resource source path")
                dest_rel = safe_relative(resource["dest"], "resource destination")
                src = ensure_inside(repo / source_rel, repo, "upstream reference resource")
                if not src.is_file():
                    if resource.get("required", True):
                        raise RuntimeError(f"Required upstream asset missing for {source_id}: {source_rel}")
                    print(f"WARNING: optional resource missing: {source_id}:{source_rel}")
                    continue
                staged = payload / dest_rel
                staged.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, staged)
                add_action(actions, dest_rel, staged)
                record.setdefault("resources", []).append({
                    "source_path": source_rel.as_posix(), "destination": dest_rel.as_posix()
                })
                provenance["resources"][dest_rel.as_posix()] = {
                    "upstream": source_id, "source_path": source_rel.as_posix(), "commit": commit,
                    "license": upstream.get("license", "unknown"),
                }
                report.append(f"{source_id}@{commit[:7]} -> {dest_rel.as_posix()} (reference only)")

            staged_lock["sources"][source_id] = record

        # Derived skills are intentionally not sync-managed. Carry explicit provenance and
        # a content hash so future local edits cannot silently drift from the audit record.
        for item in manifest.get("derived_skills", []):
            tier = item.get("tier", "skills")
            name = item.get("name", "")
            destination = f"{tier}/{name}"
            source_id = item.get("source_id")
            license_name = item.get("license", "unknown")
            skill_file = ROOT / destination / "SKILL.md"
            if not skill_file.is_file():
                raise RuntimeError(f"Derived skill is declared but not materialized: {destination}")
            provenance["skills"][destination] = {
                "upstream": source_id,
                "source_path": item.get("source_path"),
                "commit": item.get("source_ref", "main-unpinned"),
                "source_ref": item.get("source_ref", "main-unpinned"),
                "revision_status": item.get("revision_status", "unverified"),
                "license": license_name,
                "transformations": item.get("transformations", []),
                "kind": "adapted-derived-skill",
                "refresh_policy": "manual-review-only",
                "content_sha256": hashlib.sha256(skill_file.read_bytes().replace(b"\r\n", b"\n")).hexdigest(),
            }
        for name in sorted(PACK_OWNED_SKILLS):
            destination = f"skills/{name}" if (ROOT / "skills" / name).is_dir() else f"extras/{name}"
            skill_file = ROOT / destination / "SKILL.md"
            if skill_file.is_file():
                provenance["skills"][destination] = {
                    "upstream": "pack-owned", "source_path": destination, "commit": "local-pack",
                    "license": "MIT", "transformations": [], "kind": "pack-owned", "refresh_policy": "local"
                }

        # Keep the lock, provenance and notices in the same commit transaction.
        managed_paths = sorted(p.as_posix() for p in actions if p.parts[0] in {"skills", "extras", "third_party"})
        current_managed = set(managed_paths)
        previous_managed = set(old_lock.get("managed_paths", []))
        previously_retired = set(old_lock.get("retired_paths", []))
        stale_candidates = ((previous_managed - current_managed) | previously_retired) - current_managed
        stale_paths: list[Path] = []
        for item in sorted(stale_candidates):
            rel = safe_relative(item, "previous managed path")
            if rel.parts[0] not in {"skills", "extras", "third_party"}:
                raise RuntimeError(f"Refusing to clean an unmanaged path from lock: {item}")
            stale_paths.append(rel)

        # By default obsolete managed folders are retained and tracked for review.
        # --prune moves them into a persistent backup directory before removing them
        # from their active location, so they are never silently discarded.
        staged_lock["managed_paths"] = managed_paths
        staged_lock["retired_paths"] = [] if args.prune else [p.as_posix() for p in stale_paths]
        lock_rel = Path("manifests/upstream-lock.json")
        lock_stage = payload / lock_rel
        lock_stage.parent.mkdir(parents=True, exist_ok=True)
        lock_stage.write_text(json.dumps(staged_lock, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        add_action(actions, lock_rel, lock_stage)

        provenance_rel = Path("manifests/skill-provenance.json")
        provenance_stage = payload / provenance_rel
        provenance_stage.parent.mkdir(parents=True, exist_ok=True)
        provenance_stage.write_text(json.dumps(provenance, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        add_action(actions, provenance_rel, provenance_stage)

        notice_stage = payload / "THIRD_PARTY_NOTICES.md"
        notice_stage.write_text(generated_notices(manifest, staged_lock), encoding="utf-8")
        add_action(actions, Path("THIRD_PARTY_NOTICES.md"), notice_stage)

        if args.dry_run:
            print("\nDRY RUN: all sources and selected assets fetched, staged and validated; no files changed.")
            print("\n".join(report))
            if stale_paths:
                verb = "would archive and retire" if args.prune else "would retain for review (use --prune to archive)"
                print(f"Obsolete managed paths {verb}: " + ", ".join(p.as_posix() for p in stale_paths))
            return 0

        # Commit staged replacements. Retired paths are moved to persistent backups
        # only when --prune is explicit; ordinary source sync never deletes old paths.
        backup_root = scratch / "backups"
        retirement_root = ROOT / ".sdlc-upstream-backups" / datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        committed: list[tuple[Path, Path | None, bool]] = []
        transaction: list[tuple[Path, Path | None, bool]] = [(ROOT / rel, staged, False) for rel, staged in actions.items()]
        if args.prune:
            transaction += [(ROOT / rel, None, True) for rel in stale_paths]
        try:
            for dest, staged, is_retired in transaction:
                dest.parent.mkdir(parents=True, exist_ok=True)
                existed = dest.exists() or dest.is_symlink()
                backup: Path | None = None
                if existed:
                    rel = dest.relative_to(ROOT)
                    backup = (retirement_root / rel) if is_retired else (backup_root / rel)
                    backup.parent.mkdir(parents=True, exist_ok=True)
                    os.replace(dest, backup)
                try:
                    if staged is not None:
                        os.replace(staged, dest)
                except Exception:
                    if backup is not None and backup.exists():
                        os.replace(backup, dest)
                    raise
                committed.append((dest, backup, existed))
        except Exception:
            for dest, backup, existed in reversed(committed):
                if dest.exists() or dest.is_symlink():
                    if dest.is_dir() and not dest.is_symlink():
                        shutil.rmtree(dest, ignore_errors=True)
                    else:
                        try:
                            dest.unlink(missing_ok=True)
                        except OSError:
                            pass
                if backup is not None and (backup.exists() or backup.is_symlink()):
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    os.replace(backup, dest)
            raise

        print("\n".join(report))
        print(f"\nSynced {len(report)} upstream items across {len(staged_lock['sources'])} sources.")
        print(f"Lock written: {LOCK_PATH.relative_to(ROOT)}")
        print(f"Provenance written: {PROVENANCE_PATH.relative_to(ROOT)}")
        if stale_paths:
            if args.prune:
                print(f"Archived obsolete managed paths under: {retirement_root}")
            else:
                print("WARNING: obsolete managed paths were retained for review: " + ", ".join(p.as_posix() for p in stale_paths))
                print("Run the same sync command with --prune to archive them and remove them from active paths.")
        print("Next: python scripts/lint_pack.py --strict")
        return 0
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        print("No partial sync was intentionally committed. Check the manifest/source and retry.", file=sys.stderr)
        return 1
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
