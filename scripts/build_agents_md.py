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


def load_known_tools() -> dict:
    """Load known developer tools registry with multi-location fallback."""
    candidates = [
        ROOT / "manifests" / "known-tools.json",
        Path(__file__).resolve().parent.parent / "assets" / "manifests" / "known-tools.json",
        Path.home() / ".gemini" / "config" / "skills" / "using-sdlc-skills" / "assets" / "manifests" / "known-tools.json",
    ]
    for c in candidates:
        if c.is_file():
            try:
                data = json.loads(c.read_text(encoding="utf-8"))
                if "categories" in data:
                    return data["categories"]
            except Exception:
                pass

    return {
        "testing": {
            "label": "The Golden Testing Toolchain",
            "tools": {
                "playwright": "Playwright E2E & Browser Automation CLI",
                "schemathesis": "Schemathesis OpenAPI/GraphQL Contract Fuzzing CLI",
                "pytest": "PyTest Python Test Runner",
                "vitest": "Vitest Vite Native Test Runner",
                "jest": "Jest JavaScript Test Runner",
                "k6": "k6 High-concurrency Load & Performance Testing CLI",
            },
        },
        "security": {
            "label": "The Golden Security & Audit Toolchain",
            "tools": {
                "semgrep": "Semgrep OWASP Top 10 SAST Scanner",
                "trivy": "Trivy CVE, Container & Dependency SCA Scanner",
                "snyk": "Snyk Security & Vulnerability CLI",
                "gitleaks": "Gitleaks Hardcoded Secret Detection CLI",
            },
        },
        "containers": {
            "label": "Containers & Infrastructure Orchestration",
            "tools": {
                "docker": "Docker CLI & Engine",
                "kubectl": "Kubernetes Cluster Management CLI",
                "terraform": "Terraform Infrastructure as Code CLI",
            },
        },
        "navigation": {
            "label": "Structural Search & Navigation",
            "tools": {
                "ast-grep": "ast-grep Syntax-aware Tree-sitter Code Search Engine",
                "rg": "Ripgrep Ultra-fast Regex Search CLI",
                "jq": "jq JSON Processor CLI",
                "curl": "cURL CLI",
            },
        },
        "vcs": {
            "label": "Version Control & Collaboration",
            "tools": {
                "git": "Git Distributed Version Control CLI",
                "gh": "GitHub CLI (gh)",
            },
        },
    }


def detect_environment(project_root: Path) -> dict:
    """Inspect local tooling, MCP servers, and bounded harness in the environment."""
    env_info = {
        "bounded_run": bool(shutil.which("bounded_run")),
        "repo_map": bool(shutil.which("repo_map")),
        "ast_grep": bool(shutil.which("ast-grep") or shutil.which("sg")),
        "memory_mcp": False,
        "tools_by_category": {},
        "additional_clis": [],
        "clis": [],
    }

    # Bounded Run & Repo Map fallbacks
    if not env_info["bounded_run"]:
        if (project_root / "scripts" / "bounded_run.py").is_file():
            env_info["bounded_run"] = True
        elif (ROOT / "scripts" / "bounded_run.py").is_file():
            env_info["bounded_run"] = True

    if not env_info["repo_map"]:
        if (project_root / "scripts" / "repo_map.py").is_file() or (ROOT / "scripts" / "repo_map.py").is_file():
            env_info["repo_map"] = True

    # MCP servers detection (files and directory schemas)
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

    agy_mcp_dir = Path.home() / ".gemini" / "antigravity" / "mcp"
    if agy_mcp_dir.is_dir():
        if (agy_mcp_dir / "memory").is_dir():
            env_info["memory_mcp"] = True
        if (agy_mcp_dir / "ast-grep").is_dir() or (agy_mcp_dir / "ast_grep").is_dir():
            env_info["ast_grep"] = True

    # Dynamic tool detection using known-tools registry
    categories = load_known_tools()
    detected_binaries = set()

    for cat_key, cat_meta in categories.items():
        cat_label = cat_meta.get("label", cat_key.title())
        matched = []
        for binary, desc in cat_meta.get("tools", {}).items():
            if binary == "sg" and "ast-grep" in detected_binaries:
                detected_binaries.add("sg")
                continue
            if shutil.which(binary):
                matched.append(f"`{binary}` ({desc})")
                detected_binaries.add(binary.lower())
                if binary.lower() == "ast-grep":
                    detected_binaries.add("sg")
                if binary.lower() in ("ast-grep", "sg"):
                    env_info["ast_grep"] = True
        if matched:
            env_info["tools_by_category"][cat_label] = matched
            env_info["clis"].extend(matched)

    # Dynamic detection of uncataloged dev CLIs from package manager directories
    dev_roots = [
        Path.home() / "AppData" / "Local" / "Microsoft" / "WinGet" / "Links",
        Path.home() / "AppData" / "Roaming" / "npm",
        Path.home() / ".cargo" / "bin",
        Path.home() / "scoop" / "shims",
        Path.home() / ".local" / "bin",
    ]
    if sys.executable:
        dev_roots.append(Path(sys.executable).parent / "Scripts")

    ignore_stems = {
        "pip", "pip3", "pip3.14", "easy_install", "activate", "deactivate",
        "docutils", "wheel", "virtualenv", "npm", "npx", "yarn", "pnpm", "bun",
        "conhost", "cmd", "powershell", "pwsh", "wscript", "cscript",
    }
    additional_found = set()
    for root in dev_roots:
        if root.is_dir():
            try:
                for item in root.iterdir():
                    if not item.is_file():
                        continue
                    suffix = item.suffix.lower()
                    if suffix in (".exe", ".cmd", ""):
                        stem = item.stem.lower()
                        if stem in detected_binaries or stem in ignore_stems:
                            continue
                        if stem.startswith("python") or stem.endswith("-script") or stem.endswith(".ps1"):
                            continue
                        if shutil.which(item.name):
                            additional_found.add(stem)
            except Exception:
                pass

    if additional_found:
        env_info["additional_clis"] = sorted(list(additional_found))

    return env_info


def detect_stack(project_root: Path) -> dict:
    """Inspect project manifests to infer language, test runner, linter, and monorepo services."""
    stack = {
        "language": None,
        "test_runner": None,
        "linter": None,
        "monorepo_services": [],
        "compose_services": [],
    }

    # 1. Parse Docker compose services if available
    for compose_name in ["docker-compose.yml", "docker-compose.yaml", "compose.yml", "compose.yaml"]:
        compose_file = project_root / compose_name
        if compose_file.is_file():
            text = compose_file.read_text(encoding="utf-8", errors="ignore")
            in_services = False
            for line in text.splitlines():
                if line.strip().startswith("services:"):
                    in_services = True
                    continue
                if in_services and line and not line.startswith(" ") and not line.startswith("\t") and not line.startswith("#"):
                    in_services = False
                if in_services and re.match(r"^[ ]{2}[a-zA-Z0-9_\-]+:", line):
                    stack["compose_services"].append(line.strip().rstrip(":"))
            break

    # 2. Check root manifests
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

    # 3. Detect nested monorepo services
    ignore_dirs = {".git", "node_modules", ".venv", "venv", "target", "dist", "build", ".agent", ".idea", ".vscode"}
    for p in project_root.rglob("*"):
        if p.is_file() and not any(part in ignore_dirs for part in p.parts):
            rel = p.relative_to(project_root)
            if len(rel.parts) > 4:
                continue
            posix_path = str(p.parent.relative_to(project_root)).replace("\\", "/")
            if p.name == "pom.xml" and p.parent != project_root:
                stack["monorepo_services"].append({
                    "name": p.parent.name,
                    "path": posix_path,
                    "type": "Java 21 / Spring Boot & Maven",
                    "test": f"cd {posix_path} && ./mvnw test",
                    "lint": f"cd {posix_path} && ./mvnw checkstyle:check",
                })
            elif p.name == "package.json" and p.parent != project_root:
                pkg_data = {}
                try:
                    pkg_data = json.loads(p.read_text(encoding="utf-8", errors="ignore"))
                except Exception:
                    pass
                scripts = pkg_data.get("scripts", {})
                test_cmd = "npm test" if "test" in scripts else None
                lint_cmd = "npm run lint" if "lint" in scripts else None
                tech = "React / TypeScript" if (p.parent / "tsconfig.json").is_file() else "Node.js"
                stack["monorepo_services"].append({
                    "name": p.parent.name,
                    "path": posix_path,
                    "type": tech,
                    "test": f"cd {posix_path} && {test_cmd}" if test_cmd else None,
                    "lint": f"cd {posix_path} && {lint_cmd}" if lint_cmd else None,
                })
            elif p.name == "pyproject.toml" and p.parent != project_root:
                text = p.read_text(encoding="utf-8", errors="ignore").lower()
                tech = "Python (PySide6 / Edge GUI)" if "pyside" in text else "Python"
                stack["monorepo_services"].append({
                    "name": p.parent.name,
                    "path": posix_path,
                    "type": tech,
                    "test": f"cd {posix_path} && pytest",
                    "lint": f"cd {posix_path} && ruff check .",
                })

    stack["monorepo_services"].sort(key=lambda x: x["path"])
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

        lines.append("## 1. Agent Environment Stack (Đồ nghề & Môi trường Agent vận hành)")
        lines.append("- **Host & Sandbox:** Host OS, Shell environment, Global PATH.")
        if env["tools_by_category"] or env["additional_clis"]:
            lines.append("- **Discovered Host Toolchains (Extensible Registry):**")
            for cat_label, tools in env["tools_by_category"].items():
                lines.append(f"  - **{cat_label}:** {', '.join(tools)}.")
            if env["additional_clis"]:
                additional_formatted = [f"`{c}`" for c in env["additional_clis"]]
                lines.append(f"  - **Additional Host CLIs:** {', '.join(additional_formatted)}.")
        elif env["clis"]:
            lines.append(f"- **Detected Global CLIs:** {', '.join(env['clis'])}.")
        lines.append("- **Context & Output Guard (SWE-agent Harness):**")
        lines.append("  - **Execution Wrapper (Mandatory):** `bounded_run \"<cmd>\"` (Lọc log thừa, trích xuất traceback lỗi).")
        lines.append("  - **Viewport Slicing:** `bounded_run view <file> --line <N> --window <W>` (Xem lát cắt code hẹp, chống cạn kiệt token).")
        if env["repo_map"]:
            lines.append("  - **Structural Map:** `repo_map` (Cập nhật AST toàn dự án dưới 1k tokens vào `.agent/repo_map.txt`).")
        lines.append("- **MCP Endpoints:**")
        if env["memory_mcp"]:
            lines.append("  - `memory` (Knowledge Graph MCP): Lưu các bất biến kiến trúc vĩnh viễn (`create_entities`, `read_graph`).")
        if env["ast_grep"]:
            lines.append("  - `ast-grep` (AST Syntax MCP): Truy vấn và refactor mã nguồn theo cây cú pháp ngữ nghĩa (`find_code`, `rewrite_code`).")
        lines.append("- **Memory Protocol (Separation of State):**")
        lines.append("  - **Short-term / Task State:** Lưu tiến độ, checklist và bàn giao phiên vào `.agent/tasks/<task-id>.md` (`task-handoff`).")
        lines.append("  - **Long-term / Architecture Invariants:** Lưu bất biến hệ thống, quyết định thiết kế (ADR) và schemas vào MCP `memory` (`create_entities`, `add_observations`).")
        skill_folder = ROOT / "skills"
        skill_count = len([p for p in skill_folder.iterdir() if p.is_dir() and (p / "SKILL.md").is_file()]) if skill_folder.is_dir() else 33
        lines.append(f"- **Skills Catalog:** `{skill_root}/` (Router: `using-sdlc-skills`, {skill_count} kỹ năng SDLC tải theo nhu cầu).\n")

        lines.append("## 2. Target Project Stack (Công nghệ của Dự án đang thao tác)")
        if stack["language"]:
            lines.append(f"- **Primary Root Language & Runtime:** {stack['language']}")
        if stack["compose_services"]:
            lines.append(f"- **Docker Services:** {', '.join([f'`{s}`' for s in stack['compose_services']])}")
        if stack["monorepo_services"]:
            lines.append("- **Multi-service / Monorepo Architecture:**")
            for svc in stack["monorepo_services"]:
                lines.append(f"  - **{svc['name']}** (`{svc['path']}`): {svc['type']}")
        lines.append("")

        lines.append("## 3. Mandatory Verification Commands (Always wrap via `bounded_run`)")
        if stack["test_runner"]:
            runner = stack["test_runner"]
            runner = f'bounded_run "{runner}"'
            lines.append(f"- **Root Test Command:** `{runner}`")
        if stack["linter"]:
            linter = stack["linter"]
            linter = f'bounded_run "{linter}"'
            lines.append(f"- **Root Lint / Quality Gate:** `{linter}`")
        
        if stack["monorepo_services"]:
            lines.append("- **Service-level Verification Commands:**")
            for svc in stack["monorepo_services"]:
                if svc["test"]:
                    lines.append(f"  - **{svc['name']} Test:** `bounded_run \"{svc['test']}\"`")
                if svc["lint"]:
                    lines.append(f"  - **{svc['name']} Lint:** `bounded_run \"{svc['lint']}\"`")

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
