#!/usr/bin/env python3
"""Render a compact AGENTS.md index and project operating guidelines.

Audits active environment capabilities (ast-grep, memory MCP, SWE-agent bounded harness,
repo map) and project tech stacks (Python, Node/TS, Rust, Go, Java) to generate an
actionable, portable AGENTS.md rulebook for autonomous agents.

Usage:
  python scripts/build_agents_md.py [--auto-detect] [--project-root <dir>] [--output <file>]
"""
from __future__ import annotations
import sys
import os
import argparse
import re
import json
import shutil
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


def detect_environment(project_root: Path) -> dict:
    """Inspect local tooling, MCP servers, and bounded harness in the environment."""
    env_info = {
        "bounded_run": None,
        "repo_map": None,
        "ast_grep": False,
        "memory_mcp": False,
    }

    # Bounded Run harness
    bounded = project_root / "scripts" / "bounded_run.py"
    if bounded.is_file():
        env_info["bounded_run"] = "python scripts/bounded_run.py <cmd>"
    elif (ROOT / "scripts" / "bounded_run.py").is_file():
        env_info["bounded_run"] = f"python {ROOT / 'scripts' / 'bounded_run.py'} <cmd>"

    # Repo Map
    repo_map = project_root / ".agent" / "repo_map.txt"
    repo_script = project_root / "scripts" / "repo_map.py"
    if repo_map.is_file():
        env_info["repo_map"] = ".agent/repo_map.txt"
    elif repo_script.is_file():
        env_info["repo_map"] = "python scripts/repo_map.py"

    # MCP servers and CLI tools
    if shutil.which("ast-grep") or shutil.which("sg"):
        env_info["ast_grep"] = True

    mcp_locations = [
        Path.home() / ".gemini" / "config" / "mcp_config.json",
        Path.home() / ".gemini" / "antigravity" / "mcp_config.json",
        Path.home() / "AppData" / "Roaming" / "Claude" / "claude_desktop_config.json",
        Path.home() / ".config" / "Claude" / "claude_desktop_config.json",
        project_root / ".cursor" / "mcp.json",
        project_root / ".vscode" / "mcp.json",
    ]
    for mcp_path in mcp_locations:
        if mcp_path.is_file():
            try:
                data = json.loads(mcp_path.read_text(encoding="utf-8"))
                servers = data.get("mcpServers", {})
                if "ast-grep" in servers or "ast_grep" in servers:
                    env_info["ast_grep"] = True
                if "memory" in servers:
                    env_info["memory_mcp"] = True
            except Exception:
                pass

    return env_info


def detect_stack(project_root: Path) -> dict:
    """Inspect project manifests to infer language, test runner, and linter."""
    stack = {
        "language": None,
        "test_runner": None,
        "linter": None,
    }

    pyproject = project_root / "pyproject.toml"
    requirements = project_root / "requirements.txt"
    setup_py = project_root / "setup.py"
    tests_dir = project_root / "tests"
    scripts_dir = project_root / "scripts"
    package_json = project_root / "package.json"
    cargo_toml = project_root / "Cargo.toml"
    go_mod = project_root / "go.mod"

    if pyproject.is_file() or requirements.is_file() or setup_py.is_file() or (scripts_dir.is_dir() and any(scripts_dir.glob("*.py"))):
        stack["language"] = "Python 3.x"
        if pyproject.is_file() and "pytest" in pyproject.read_text(encoding="utf-8", errors="ignore"):
            stack["test_runner"] = "pytest"
        elif tests_dir.is_dir():
            stack["test_runner"] = "python -m unittest discover -s tests -v"
        
        if (scripts_dir / "lint_pack.py").is_file():
            stack["linter"] = "python scripts/lint_pack.py --strict"
        elif shutil.which("ruff"):
            stack["linter"] = "ruff check ."
        elif shutil.which("flake8"):
            stack["linter"] = "flake8 ."

    elif package_json.is_file():
        stack["language"] = "Node.js / TypeScript" if (project_root / "tsconfig.json").is_file() else "Node.js / JavaScript"
        try:
            pkg = json.loads(package_json.read_text(encoding="utf-8"))
            scripts = pkg.get("scripts", {})
            if "test" in scripts:
                stack["test_runner"] = "npm test"
            if "lint" in scripts:
                stack["linter"] = "npm run lint"
        except Exception:
            pass

    elif cargo_toml.is_file():
        stack["language"] = "Rust"
        stack["test_runner"] = "cargo test"
        stack["linter"] = "cargo clippy"

    elif go_mod.is_file():
        stack["language"] = "Go"
        stack["test_runner"] = "go test ./..."
        stack["linter"] = "golangci-lint run"

    return stack


def render(
    with_extras: bool = False,
    skill_root: str = "skills",
    asset_root: str = ".",
    auto_detect: bool = False,
    project_root: Path | None = None,
) -> str:
    if project_root is None:
        project_root = Path.cwd()

    skill_root = normalize_path(skill_root)
    asset_root = normalize_path(asset_root)
    lines: list[str] = []

    if auto_detect:
        env = detect_environment(project_root)
        stack = detect_stack(project_root)

        lines.append("# Project Operating Guidelines (AGENTS.md)\n")
        lines.append("## 0. Tool Isolation Boundary (Đồ nghề của thợ vs Nhà của khách)")
        lines.append("- **Tool Isolation Invariant:** Mọi công cụ harness (`bounded_run`, `repo_map`, `scaffold`, `verify_contracts`, `ast-grep`) là công cụ môi trường của Agent. CẤM TUYỆT ĐỐI copy, di chuyển hoặc commit các script nội bộ này vào repository của dự án. Gọi trực tiếp qua Global CLI command (`bounded_run \"<cmd>\"`, `repo_map`) hoặc đường dẫn toolkit môi trường.\n")

        lines.append("## 1. Project Context & Detected Stack")
        if stack["language"]:
            lines.append(f"- **Language & Runtime:** {stack['language']}")
        if stack["test_runner"]:
            runner = stack["test_runner"]
            runner = f'bounded_run "{runner}"'
            lines.append(f"- **Primary Test Command:** `{runner}`")
        if stack["linter"]:
            linter = stack["linter"]
            linter = f'bounded_run "{linter}"'
            lines.append(f"- **Lint / Quality Gate:** `{linter}`")
        lines.append("")

        lines.append("## 2. Environment Tools & Execution Harness")
        lines.append("- **Mandatory Bounded Execution:** BẮT BUỘC chạy các lệnh test, build, lint dài qua `bounded_run \"<command>\"` để tránh tràn context và tự động trích xuất stacktrace lỗi.")
        if env["repo_map"]:
            lines.append(f"- **Structural Code Navigation:** Consult `{env['repo_map']}` for structural orientation. Read viewports (`bounded_run view <file> --line <N>`) instead of loading entire large files.")
        if env["ast_grep"]:
            lines.append("- **AST Search:** `ast-grep` is active. Use `ast-grep:find_code` or `ast-grep:analyze-imports` for structural search across declarations instead of raw regex or full-file inspection.")
        if env["memory_mcp"]:
            lines.append("- **Knowledge Graph Memory:** Memory MCP is active. Persist architectural decisions and entity relations via `memory:add_observations` / `memory:create_entities` to maintain cross-session context.")
        lines.append("- **Verification Before Completion:** Always run `verification-before-completion` before declaring work done. Report actual executed commands and evidence honestly.\n")

    lines += [
        "# SDLC Agent Skills — portable index", "",
        "For each task, identify the applicable skill(s) and read their `SKILL.md` before acting. Load only relevant skills; do not paste the whole library into context.",
        f"The pack-level router is `{skill_root}/using-sdlc-skills/SKILL.md`. For a full lifecycle, follow `{asset_root}/workflows/full-sdlc.md` when that pack asset is available.",
        f"Use the shared output templates in `{asset_root}/templates/` when present; otherwise follow the project's existing artifact conventions.",
        "Do not claim checks passed unless they ran. Stop for required human approval before production/destructive actions.", "",
        "## Available skills", "", "| Skill | Load when |", "|---|---|"
    ]

    skill_folder = ROOT / "skills"
    if skill_folder.is_dir():
        for skill_dir in sorted((p for p in skill_folder.iterdir() if p.is_dir() and (p / "SKILL.md").is_file()), key=lambda p: p.name.casefold()):
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
    if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--auto-detect", "--init", dest="auto_detect", action="store_true", help="audit environment tools and project stack to generate project guidelines")
    parser.add_argument("--project-root", default=".", help="project root to audit")
    parser.add_argument("--output", "-o", default=None, help="write output directly to target file")
    parser.add_argument("--force", action="store_true", help="overwrite output file if it exists")
    parser.add_argument("--with-extras", action="store_true", help="legacy flag for backwards compatibility")
    parser.add_argument("--skill-root", default="skills", help="project-relative path containing installed skill folders")
    parser.add_argument("--asset-root", default=".", help="project-relative path containing workflows/ and templates/")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    content = render(
        with_extras=args.with_extras,
        skill_root=args.skill_root,
        asset_root=args.asset_root,
        auto_detect=args.auto_detect,
        project_root=project_root,
    )

    if args.output:
        out_path = Path(args.output).resolve()
        if out_path.exists() and not args.force:
            print(f"Error: {out_path} already exists. Pass --force to overwrite.", file=sys.stderr)
            sys.exit(3)
        out_path.write_text(content, encoding="utf-8")
        print(f"Generated {out_path} successfully.")
    else:
        print(content, end="")


if __name__ == "__main__":
    main()
