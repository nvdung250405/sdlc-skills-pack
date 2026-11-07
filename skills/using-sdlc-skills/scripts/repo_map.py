#!/usr/bin/env python3
"""Repository Structural Map Generator for Coding Agents.

Inspired by Aider's repomap architecture:
Extracts high-level definitions (classes, methods, functions, signatures)
using Tree-sitter (with fallback to Python AST) and generates a compact,
token-budgeted architectural map of the codebase for AI agents.

Usage:
  python scripts/repo_map.py
  python scripts/repo_map.py --output .agent/repo_map.txt --max-tokens 1024
"""
from __future__ import annotations

import argparse
import ast
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]

IGNORE_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".agent",
    ".gemini",
    ".idea",
    ".vscode",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    "dist",
    "build",
    ".sdlc-skill-backups",
}

IGNORE_EXTENSIONS = {
    ".pyc",
    ".pyo",
    ".pyd",
    ".lock",
    ".log",
    ".zip",
    ".tar",
    ".gz",
    ".png",
    ".jpg",
    ".svg",
    ".ico",
    ".woff",
    ".woff2",
    ".ttf",
}


def parse_python_tags_builtin(filepath: Path) -> List[str]:
    """Fallback AST parser using Python's standard library `ast`."""
    try:
        source = filepath.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(source, filename=str(filepath))
    except Exception:
        return []

    tags = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            bases = [ast.unparse(b) for b in node.bases]
            base_str = f"({', '.join(bases)})" if bases else ""
            tags.append(f"  class {node.name}{base_str}:")
            for sub in node.body:
                if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    prefix = "async def" if isinstance(sub, ast.AsyncFunctionDef) else "def"
                    args = ast.unparse(sub.args) if hasattr(ast, "unparse") else "..."
                    ret = f" -> {ast.unparse(sub.returns)}" if sub.returns and hasattr(ast, "unparse") else ""
                    tags.append(f"    {prefix} {sub.name}({args}){ret}")
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            prefix = "async def" if isinstance(node, ast.AsyncFunctionDef) else "def"
            args = ast.unparse(node.args) if hasattr(ast, "unparse") else "..."
            ret = f" -> {ast.unparse(node.returns)}" if node.returns and hasattr(ast, "unparse") else ""
            tags.append(f"  {prefix} {node.name}({args}){ret}")
    return tags


def parse_python_tags(filepath: Path) -> List[str]:
    """Parse python tags using Tree-sitter if available, else fallback."""
    try:
        import tree_sitter
        import tree_sitter_python
        lang = tree_sitter.Language(tree_sitter_python.language())
        parser = tree_sitter.Parser(lang)
        source_bytes = filepath.read_bytes()
        tree = parser.parse(source_bytes)

        lines = source_bytes.splitlines()
        tags = []

        def get_line_text(node) -> str:
            line_idx = node.start_point.row
            if line_idx < len(lines):
                return lines[line_idx].decode("utf-8", errors="replace").strip()
            return ""

        def traverse(node, indent="  "):
            for child in node.children:
                if child.type == "class_definition":
                    name_node = child.child_by_field_name("name")
                    name = name_node.text.decode("utf-8", errors="replace") if name_node else "Anonymous"
                    header = get_line_text(child).split(":")[0] + ":"
                    tags.append(f"{indent}{header}")
                    body = child.child_by_field_name("body")
                    if body:
                        traverse(body, indent + "  ")
                elif child.type in ("function_definition", "async_function_definition"):
                    header = get_line_text(child).split(":")[0]
                    tags.append(f"{indent}{header}")

        traverse(tree.root_node)
        if tags:
            return tags
    except Exception:
        pass
    return parse_python_tags_builtin(filepath)


def build_repo_map(root: Path, max_tokens: int = 1024) -> str:
    """Builds a formatted repo map fitted within max_tokens."""
    file_tags: Dict[str, List[str]] = {}

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS and not d.startswith(".")]
        for fname in sorted(filenames):
            if any(fname.endswith(ext) for ext in IGNORE_EXTENSIONS):
                continue
            fpath = Path(dirpath) / fname
            rel_path = fpath.relative_to(root).as_posix()

            if fname.endswith(".py"):
                tags = parse_python_tags(fpath)
                if tags:
                    file_tags[rel_path] = tags
            elif fname in ("package.json", "manifests/skill-map.json", "upstream.json"):
                file_tags[rel_path] = [f"  [Config/Manifest] {fname}"]

    output_lines = [
        "# Codebase Structural Map (Aider-style AST Extraction)",
        f"# Root: {root.name} | Auto-generated for token-efficient agent orientation",
        "",
    ]

    # Approximate token count: 1 token ~ 4 characters
    char_budget = max_tokens * 4

    for fpath, tags in sorted(file_tags.items()):
        file_block = [f"{fpath}:"]
        for tag in tags:
            file_block.append(tag)
        file_block.append("")

        block_str = "\n".join(file_block)
        current_len = sum(len(line) + 1 for line in output_lines)
        if current_len + len(block_str) > char_budget:
            output_lines.append(f"... (truncated {len(file_tags) - len(output_lines)} files to preserve token budget)")
            break
        output_lines.extend(file_block)

    return "\n".join(output_lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Root directory to map")
    parser.add_argument("--output", type=Path, default=ROOT / ".agent" / "repo_map.txt", help="Output file path")
    parser.add_argument("--max-tokens", type=int, default=1024, help="Token budget for map (default: 1024)")
    parser.add_argument("--stdout", action="store_true", help="Print map to stdout")
    args = parser.parse_args()

    repo_map = build_repo_map(args.root, max_tokens=args.max_tokens)

    if args.stdout:
        print(repo_map)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(repo_map, encoding="utf-8")
    token_est = len(repo_map) // 4
    print(f"SUCCESS: Generated Repo Map -> {args.output.relative_to(args.root)} (~{token_est} tokens)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

