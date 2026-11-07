#!/usr/bin/env python3
"""Install the curated SDLC skills into an agent's skill directory safely.

Examples:
  python scripts/install.py codex
  python scripts/install.py claude --global --link
  python scripts/install.py copilot --dest .github/skills --force
  python scripts/install.py custom --dest ./my-agent/skills --allow-partial
  python scripts/install.py agents-md --force
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADAPTER_FILE = ROOT / "adapters" / "agents.json"
MANIFEST_FILE = ROOT / "upstream.json"


def tree_hash(path: Path) -> str:
    digest = hashlib.sha256()
    if path.is_symlink():
        digest.update(b"SYMLINK\0")
        digest.update(os.readlink(path).encode("utf-8", "surrogateescape"))
        return digest.hexdigest()
    if path.is_file():
        digest.update(b"FILE\0")
        digest.update(path.read_bytes())
        return digest.hexdigest()
    for item in sorted(path.rglob("*"), key=lambda p: p.as_posix().casefold()):
        rel = item.relative_to(path).as_posix()
        digest.update(rel.encode("utf-8", "surrogateescape") + b"\0")
        if item.is_symlink():
            digest.update(b"L\0" + os.readlink(item).encode("utf-8", "surrogateescape"))
        elif item.is_file():
            digest.update(b"F\0" + item.read_bytes())
        elif item.is_dir():
            digest.update(b"D\0")
    return digest.hexdigest()


def expected_skill_names(include_extras: bool = False) -> set[str]:
    if not MANIFEST_FILE.exists():
        return set()
    data = json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))
    expected = set()
    for upstream in data.get("upstreams", []):
        for item in upstream.get("items", []):
            tier = item.get("tier", "skills")
            if tier == "skills" or (include_extras and tier == "extras"):
                expected.add(item.get("name", Path(item["src"]).name))
    for item in data.get("derived_skills", []):
        tier = item.get("tier", "skills")
        if tier == "skills" or (include_extras and tier == "extras"):
            expected.add(item.get("name", Path(item["src"]).name if "src" in item else ""))
    # Pack-owned skills are installed too but are not upstream-managed.
    expected.update({p.name for p in (ROOT / "skills").iterdir() if p.is_dir()})
    return expected


def missing_required_skills(include_extras: bool = False) -> list[str]:
    expected = expected_skill_names(include_extras=include_extras)
    roots = [ROOT / "skills"] + ([ROOT / "extras"] if include_extras else [])
    available = {p.name for root in roots if root.is_dir() for p in root.iterdir() if p.is_dir() and (p / "SKILL.md").is_file()}
    return sorted(expected - available)


def sync_problems(include_extras: bool = False) -> list[str]:
    """Return provenance/materialization gaps that make a full install unsafe."""
    problems: list[str] = []
    for name in missing_required_skills(include_extras=include_extras):
        problems.append(f"missing selected skill: {name}")
    try:
        manifest = json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return problems + [f"cannot read upstream manifest: {exc}"]
    for upstream in manifest.get("upstreams", []):
        source_id = upstream.get("id", "unknown")
        if not (ROOT / "third_party" / source_id / "LICENSE").is_file():
            problems.append(f"missing upstream license: {source_id}")
        if upstream.get("notice_file") and not (ROOT / "third_party" / source_id / "NOTICE").is_file():
            problems.append(f"missing upstream NOTICE: {source_id}")
        for resource in upstream.get("resources", []):
            if resource.get("required", True) and not (ROOT / resource["dest"]).is_file():
                problems.append(f"missing upstream resource: {resource['dest']}")
    lock_path = ROOT / "manifests" / "upstream-lock.json"
    provenance_path = ROOT / "manifests" / "skill-provenance.json"
    if not lock_path.is_file():
        problems.append("missing manifests/upstream-lock.json")
    else:
        try:
            lock = json.loads(lock_path.read_text(encoding="utf-8"))
            for upstream in manifest.get("upstreams", []):
                record = lock.get("sources", {}).get(upstream.get("id"), {})
                if not record.get("commit"):
                    problems.append(f"source is not locked: {upstream.get('id')}")
        except (OSError, json.JSONDecodeError) as exc:
            problems.append(f"invalid upstream lock: {exc}")
    if not provenance_path.is_file():
        problems.append("missing manifests/skill-provenance.json")
    return problems


def backup_path(path: Path, dest_root: Path, stamp: str) -> Path:
    return dest_root.parent / ".sdlc-skill-backups" / stamp / dest_root.name / path.name


def backup_existing(path: Path, dest_root: Path, stamp: str) -> Path:
    target = backup_path(path, dest_root, stamp)
    target.parent.mkdir(parents=True, exist_ok=True)
    os.replace(path, target)
    return target


def copy_or_link(source: Path, dest: Path, mode: str) -> None:
    if mode == "link":
        os.symlink(source.resolve(), dest, target_is_directory=True)
    else:
        shutil.copytree(source, dest, symlinks=True)


def relative_to_project(value: str | None, default: str) -> str:
    if not value:
        return default
    path = Path(value).expanduser()
    target = path.resolve() if path.is_absolute() else (Path.cwd() / path).resolve()
    return Path(os.path.relpath(target, Path.cwd().resolve())).as_posix()


def render_agents_md(with_extras: bool, skill_root: str, asset_root: str, auto_detect: bool = False) -> str:
    command = [
        sys.executable, str(ROOT / "scripts" / "build_agents_md.py"),
        "--skill-root", skill_root, "--asset-root", asset_root,
    ]
    if with_extras:
        command.append("--with-extras")
    if auto_detect:
        command.append("--auto-detect")
    result = subprocess.run(command, check=True, capture_output=True)
    return result.stdout.decode("utf-8")


def print_missing_optional_summary(sources: list[Path], args: argparse.Namespace, manifest_path: Path) -> None:
    if manifest_path.is_file():
        try:
            skill_map_data = json.loads(manifest_path.read_text(encoding="utf-8"))
            installed_names = {s.name for s in sources}
            all_known = set(skill_map_data.get("core_skills", [])) | set(skill_map_data.get("extras", []))
            missing_optional = sorted(all_known - installed_names)
            if missing_optional:
                active_profile = args.profile or ("full" if args.with_extras else "core")
                print(f"Profile: '{active_profile}' ({len(installed_names)} skills selected).")
                print(f"Skills omitted in this profile ({len(missing_optional)} skills omitted):")
                print(f"  {', '.join(missing_optional[:8])}{'...' if len(missing_optional) > 8 else ''}")
                print("  (Tip: use `--profile canonical-32` or `--profile full` to include all 32 Universal SDLC skills)")
        except Exception:
            pass


def install_agents_md(args: argparse.Namespace) -> int:
    target = (Path.cwd() / "AGENTS.md").resolve()
    skill_root = relative_to_project(args.dest, "skills")
    asset_root = relative_to_project(args.asset_root, ".")

    # Preserve an existing AGENTS.md by default, even when the proposed index cannot
    # yet be rendered because the user has not copied the skills/assets into place.
    auto_detect = getattr(args, "auto_detect", False)
    if target.exists() and not args.force:
        try:
            content = render_agents_md(args.with_extras, skill_root, asset_root, auto_detect=auto_detect)
            old = target.read_text(encoding="utf-8", errors="replace")
            if old == content:
                print(f"Unchanged: {target}")
                return 0
        except (OSError, subprocess.CalledProcessError):
            pass
        print(f"ERROR: {target} already exists and differs. Use --force to back it up before replacement.", file=sys.stderr)
        return 3

    skill_path = Path(skill_root)
    if not skill_path.is_absolute():
        skill_path = Path.cwd() / skill_path
    asset_path = Path(asset_root)
    if not asset_path.is_absolute():
        asset_path = Path.cwd() / asset_path
    if not skill_path.is_dir() or not any(p.is_dir() and (p / "SKILL.md").is_file() for p in skill_path.iterdir()):
        print(f"ERROR: no installed SKILL.md folders found under {skill_path}. Install/copy skills first or set --dest.", file=sys.stderr)
        return 2
    has_srs = (asset_path / "templates" / "specs" / "SRS.md").is_file() or (asset_path / "templates" / "SRS.md").is_file()
    if not (asset_path / "workflows" / "full-sdlc.md").is_file() or not has_srs:
        print(f"ERROR: pack workflows/templates were not found under {asset_path}. Keep the pack assets in the project or set --asset-root.", file=sys.stderr)
        return 2

    content = render_agents_md(args.with_extras, skill_root, asset_root, auto_detect=auto_detect)
    if args.dry_run:
        print(f"DRY RUN: would write {target} ({len(content.splitlines())} lines)")
        return 0
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    backup = None
    try:
        if target.exists():
            backup = target.parent / ".sdlc-skill-backups" / stamp / "AGENTS.md"
            backup.parent.mkdir(parents=True, exist_ok=True)
            os.replace(target, backup)
        target.write_text(content, encoding="utf-8")
    except Exception as exc:
        if backup is not None and backup.exists() and not target.exists():
            os.replace(backup, target)
        print(f"ERROR: failed to write AGENTS.md: {exc}", file=sys.stderr)
        return 1
    if backup:
        print(f"Backed up previous AGENTS.md to: {backup}")
    print(f"Wrote {target}. This is an index/guide; native skill directories are still needed for full skill loading.")
    return 0


def resolve_destination(target: str, args: argparse.Namespace, adapters: dict) -> Path:
    if args.dest:
        dest = Path(args.dest).expanduser()
        return (Path.cwd() / dest).resolve() if not dest.is_absolute() else dest.resolve()
    agents = adapters.get("agents", {})
    if target not in agents:
        raise ValueError(f"Unknown target {target!r}. Available: {', '.join(sorted(agents))}, custom, agents-md")
    value = agents[target]["global" if args.global_scope else "project"]
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = Path.cwd() / path
    return path.resolve()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", help="claude, codex, gemini, cursor, copilot, custom, or agents-md")
    parser.add_argument("--global", dest="global_scope", action="store_true", help="install into the configured user-level directory")
    parser.add_argument("--link", action="store_true", help="create symlinks instead of copying skill folders")
    parser.add_argument("--profile", choices=["eager-lean", "canonical-32", "core", "full"], default=None, help="installation profile: eager-lean (8 skills, ~20k tokens), canonical-32 (32 skills, ~81k tokens), core (32 skills), or full (32 skills)")
    parser.add_argument("--with-extras", action="store_true", help="also install skills from extras/ (equivalent to --profile full)")
    parser.add_argument("--auto-detect", "--init", dest="auto_detect", action="store_true", help="for agents-md, audit environment and stack")
    parser.add_argument("--dest", help="skill install directory; for agents-md, path to installed skill folders")
    parser.add_argument("--asset-root", help="for agents-md, project-relative path to the pack copy containing workflows/ and templates/")
    parser.add_argument("--force", action="store_true", help="back up conflicting entries before replacing them")
    parser.add_argument("--dry-run", action="store_true", help="show planned operations without writing")
    parser.add_argument("--allow-partial", action="store_true", help="allow installing before upstream sync (not recommended)")
    args = parser.parse_args()
    target_name = args.target.lower()

    if target_name == "agents-md":
        return install_agents_md(args)
    if target_name == "custom" and not args.dest:
        print("ERROR: target 'custom' requires --dest DIR.", file=sys.stderr)
        return 2

    try:
        adapters = json.loads(ADAPTER_FILE.read_text(encoding="utf-8"))
        dest_root = resolve_destination(target_name, args, adapters)
        mode = adapters.get("agents", {}).get(target_name, {}).get("loading_mode", "unknown")
        if mode in ("eager", "unknown"):
            if args.with_extras or args.profile == "full":
                print(f"TIP: Target '{target_name}' has '{mode}' loading behavior. Installing all 32 skills consumes substantial context (~81k tokens). Consider --profile eager-lean (8 skills, ~20k tokens).", file=sys.stderr)
            elif not args.profile:
                print(f"TIP: Target '{target_name}' has '{mode}' loading. Default Core installs 32 skills (~81k tokens). For an ultra-light context footprint, use --profile eager-lean (8 skills, ~20k tokens).", file=sys.stderr)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.profile == "full":
        args.with_extras = True
    elif args.profile == "core":
        args.with_extras = False

    problems = sync_problems(include_extras=args.with_extras)
    if problems and not args.allow_partial:
        print("ERROR: the curated pack is not fully synchronized/verified.", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        print("Run `python scripts/sync_upstream.py`, then `python scripts/lint_pack.py --strict`.", file=sys.stderr)
        print("Use --allow-partial only for testing the currently bundled subset.", file=sys.stderr)
        return 2

    manifest_path = ROOT / "manifests" / "skill-map.json"
    profiles_data: dict[str, list[str]] = {}
    if manifest_path.is_file():
        try:
            profiles_data = json.loads(manifest_path.read_text(encoding="utf-8")).get("profiles", {})
        except Exception:
            profiles_data = {}

    roots = [ROOT / "skills", ROOT / "extras"]
    all_available: dict[str, Path] = {}
    for folder in roots:
        if folder.is_dir():
            for p in folder.iterdir():
                if p.is_dir() and (p / "SKILL.md").is_file():
                    all_available[p.name] = p

    sources: list[Path] = []
    if args.profile and args.profile in profiles_data:
        target_names = set(profiles_data[args.profile])
        sources = [p for name, p in all_available.items() if name in target_names]
    elif args.with_extras:
        sources = list(all_available.values())
    else:
        # Default: core skills
        core_names = set(profiles_data.get("core", [p.name for p in (ROOT / "skills").iterdir() if p.is_dir()]))
        sources = [p for name, p in all_available.items() if name in core_names]

    sources.sort(key=lambda p: p.name.casefold())
    if not sources:
        print("ERROR: no valid skills found.", file=sys.stderr)
        return 2

    # Never install a pack into its own source directory.
    for source_root in roots:
        try:
            dest_root.relative_to(source_root.resolve())
            print(f"ERROR: destination {dest_root} is inside source directory {source_root.resolve()}.", file=sys.stderr)
            return 2
        except ValueError:
            pass

    actions = []
    conflicts = []
    for source in sources:
        dest = dest_root / source.name
        unchanged = False
        if dest.exists() or dest.is_symlink():
            if args.link and dest.is_symlink():
                try:
                    unchanged = dest.resolve() == source.resolve()
                except OSError:
                    unchanged = False
            elif not args.link and dest.is_dir() and not dest.is_symlink():
                unchanged = tree_hash(dest) == tree_hash(source)
            if not unchanged:
                conflicts.append(dest)
        if not unchanged:
            actions.append((source, dest))

    if conflicts and not args.force:
        print("ERROR: existing destinations differ; nothing was installed. Use --force to back them up first:", file=sys.stderr)
        for path in conflicts:
            print(f"  - {path}", file=sys.stderr)
        return 3

    if args.dry_run:
        print(f"Target: {target_name}\nDestination: {dest_root}\nMode: {'symlink' if args.link else 'copy'}")
        for source, dest in actions:
            verb = "link" if args.link else "copy"
            print(f"Would {verb}: {source.relative_to(ROOT)} -> {dest}")
        print(f"Unchanged skills: {len(sources) - len(actions)}; planned writes: {len(actions)}")
        print_missing_optional_summary(sources, args, manifest_path)
        return 0

    dest_root.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    backups: list[tuple[Path, Path]] = []
    created: list[Path] = []
    try:
        for source, dest in actions:
            if dest.exists() or dest.is_symlink():
                backup = backup_existing(dest, dest_root, stamp)
                backups.append((dest, backup))
            try:
                copy_or_link(source, dest, "link" if args.link else "copy")
                created.append(dest)
            except Exception:
                if dest.exists() or dest.is_symlink():
                    if dest.is_dir() and not dest.is_symlink():
                        shutil.rmtree(dest, ignore_errors=True)
                    else:
                        dest.unlink(missing_ok=True)
                for old_dest, backup in reversed(backups):
                    if backup.exists() or backup.is_symlink():
                        os.replace(backup, old_dest)
                raise
    except OSError as exc:
        # Roll back newly created entries as well as restore backed-up conflicts.
        for new_dest in reversed(created):
            if new_dest.exists() or new_dest.is_symlink():
                if new_dest.is_dir() and not new_dest.is_symlink():
                    shutil.rmtree(new_dest, ignore_errors=True)
                else:
                    try:
                        new_dest.unlink(missing_ok=True)
                    except OSError:
                        pass
        for old_dest, backup in reversed(backups):
            if backup.exists() or backup.is_symlink():
                if old_dest.exists() or old_dest.is_symlink():
                    if old_dest.is_dir() and not old_dest.is_symlink():
                        shutil.rmtree(old_dest, ignore_errors=True)
                    else:
                        try:
                            old_dest.unlink(missing_ok=True)
                        except OSError:
                            pass
                old_dest.parent.mkdir(parents=True, exist_ok=True)
                os.replace(backup, old_dest)
        print(f"ERROR: install failed and rollback was attempted: {exc}", file=sys.stderr)
        if args.link and os.name == "nt":
            print("Windows may require Developer Mode or elevated privileges for directory symlinks; retry without --link.", file=sys.stderr)
        return 1
    except Exception as exc:
        for new_dest in reversed(created):
            if new_dest.exists() or new_dest.is_symlink():
                if new_dest.is_dir() and not new_dest.is_symlink():
                    shutil.rmtree(new_dest, ignore_errors=True)
                else:
                    try:
                        new_dest.unlink(missing_ok=True)
                    except OSError:
                        pass
        for old_dest, backup in reversed(backups):
            if backup.exists() or backup.is_symlink():
                if old_dest.exists() or old_dest.is_symlink():
                    if old_dest.is_dir() and not old_dest.is_symlink():
                        shutil.rmtree(old_dest, ignore_errors=True)
                    else:
                        try:
                            old_dest.unlink(missing_ok=True)
                        except OSError:
                            pass
                old_dest.parent.mkdir(parents=True, exist_ok=True)
                os.replace(backup, old_dest)
        print(f"ERROR: install failed and rollback was attempted: {exc}", file=sys.stderr)
        return 1

    print(f"Installed/updated {len(created)} skills to {dest_root} ({'symlink' if args.link else 'copy'} mode).")
    print(f"Already unchanged: {len(sources) - len(actions)}.")
    if backups:
        print(f"Backups saved under: {dest_root.parent / '.sdlc-skill-backups' / stamp / dest_root.name}")
    print("Adapter path note: confirm this destination against the target agent's current documentation; --dest overrides it.")
    if problems:
        print("WARNING: partial install; unresolved pack issues:")
        for problem in problems:
            print(f"  - {problem}")
    print_missing_optional_summary(sources, args, manifest_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
