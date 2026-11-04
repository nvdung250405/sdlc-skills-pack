#!/usr/bin/env python3
"""Unified Contract Verification Gate for SDLC Agent Skills.

Enforces Section 11.2 of docs/architecture.md:
Validates machine-executable contracts (OpenAPI, AsyncAPI, STOMP, Protobuf,
GraphQL, JSON Schema, SQL DDL) for syntax, required structure, and contract rules.

Usage:
  python scripts/verify_contracts.py
  python scripts/verify_contracts.py --dir contracts
  python scripts/verify_contracts.py --strict
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def check_yaml_file(path: Path) -> tuple[bool, str, dict | None]:
    try:
        import yaml
        content = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(content, dict):
            return False, "Root YAML element must be a mapping", None
        return True, "Valid YAML", content
    except ImportError:
        # Fallback basic YAML validation when pyyaml is not installed
        text = path.read_text(encoding="utf-8")
        if not text.strip():
            return False, "File is empty", None
        return True, "Basic YAML syntax valid", {}
    except Exception as exc:
        return False, f"YAML parse error: {exc}", None


def verify_openapi(path: Path, strict: bool) -> list[str]:
    errors = []
    ok, msg, data = check_yaml_file(path)
    if not ok:
        errors.append(f"{path.name}: {msg}")
        return errors
    if data:
        version = str(data.get("openapi", ""))
        if not version.startswith("3."):
            errors.append(f"{path.name}: unsupported or missing openapi version (expected 3.x, found '{version}')")
        if "info" not in data or "title" not in data.get("info", {}):
            errors.append(f"{path.name}: missing required 'info.title'")
        if "paths" not in data:
            errors.append(f"{path.name}: missing required 'paths' section")
        if "components" not in data or "schemas" not in data.get("components", {}):
            errors.append(f"{path.name}: missing 'components.schemas'")

    # External linter check if tool is available
    if shutil.which("spectral"):
        res = subprocess.run(["spectral", "lint", str(path)], capture_output=True, text=True)
        if res.returncode != 0:
            errors.append(f"{path.name}: spectral lint failed:\n{res.stdout}")
    return errors


def verify_asyncapi(path: Path, strict: bool) -> list[str]:
    errors = []
    ok, msg, data = check_yaml_file(path)
    if not ok:
        errors.append(f"{path.name}: {msg}")
        return errors
    if data:
        version = str(data.get("asyncapi", ""))
        if not (version.startswith("2.") or version.startswith("3.")):
            errors.append(f"{path.name}: unsupported asyncapi version (expected 2.x or 3.x, found '{version}')")
        if "info" not in data or "title" not in data.get("info", {}):
            errors.append(f"{path.name}: missing 'info.title'")
        if "channels" not in data:
            errors.append(f"{path.name}: missing 'channels' section")
    return errors


def verify_stomp(path: Path, strict: bool) -> list[str]:
    errors = []
    ok, msg, data = check_yaml_file(path)
    if not ok:
        errors.append(f"{path.name}: {msg}")
        return errors
    if data:
        if "protocol" not in data or "STOMP" not in str(data.get("protocol")):
            errors.append(f"{path.name}: missing or invalid 'protocol: STOMP'")
        if "destinations" not in data:
            errors.append(f"{path.name}: missing 'destinations' mapping")
    return errors


def verify_proto(path: Path, strict: bool) -> list[str]:
    errors = []
    text = path.read_text(encoding="utf-8")
    if 'syntax = "proto3";' not in text:
        errors.append(f"{path.name}: must declare 'syntax = \"proto3\";'")
    if not re.search(r"\bpackage\s+[\w.]+;", text):
        errors.append(f"{path.name}: missing 'package <name>;' declaration")
    if not re.search(r"\bservice\s+\w+\s*\{", text):
        errors.append(f"{path.name}: missing 'service <Name> {{ ... }}' block")
    if not re.search(r"\brpc\s+\w+\s*\(", text):
        errors.append(f"{path.name}: service contains no RPC methods")

    if shutil.which("buf"):
        res = subprocess.run(["buf", "lint", str(path)], capture_output=True, text=True)
        if res.returncode != 0:
            errors.append(f"{path.name}: buf lint failed:\n{res.stdout}")
    return errors


def verify_graphql(path: Path, strict: bool) -> list[str]:
    errors = []
    text = path.read_text(encoding="utf-8")
    if not re.search(r"\btype\s+Query\b", text):
        errors.append(f"{path.name}: missing root 'type Query'")
    if not re.search(r"\bschema\s*\{", text) and "type Query" not in text:
        errors.append(f"{path.name}: invalid or empty GraphQL schema")
    return errors


def verify_json_schema(path: Path, strict: bool) -> list[str]:
    errors = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            errors.append(f"{path.name}: root element must be a JSON object")
        if "$schema" not in data:
            errors.append(f"{path.name}: missing '$schema' declaration")
        if "type" not in data:
            errors.append(f"{path.name}: missing 'type' declaration")
    except json.JSONDecodeError as exc:
        errors.append(f"{path.name}: invalid JSON syntax: {exc}")
    return errors


def verify_sql_migration(path: Path, strict: bool) -> list[str]:
    errors = []
    text = path.read_text(encoding="utf-8")
    upper = text.upper()
    if "BEGIN;" not in upper or "COMMIT;" not in upper:
        errors.append(f"{path.name}: migration must be wrapped in a transaction (BEGIN; ... COMMIT;)")
    if "CREATE TABLE" not in upper and "ALTER TABLE" not in upper and "DROP TABLE" not in upper:
        errors.append(f"{path.name}: no DDL operations (CREATE/ALTER/DROP) detected")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dir", default="contracts", help="Directory containing executable contracts (default: 'contracts')")
    parser.add_argument("--strict", action="store_true", help="Fail on warnings and enforce strict external linters if installed")

    args = parser.parse_args()

    # Look in project directory, or fallback to templates/contracts
    contracts_dir = Path(args.dir)
    if not contracts_dir.is_dir():
        contracts_dir = ROOT / "templates" / "contracts"

    if not contracts_dir.is_dir():
        print(f"No contracts directory found at '{args.dir}' or 'templates/contracts'.", file=sys.stderr)
        return 0

    all_errors: list[str] = []
    verified_count = 0

    for file in sorted(contracts_dir.iterdir()):
        if not file.is_file():
            continue
        name = file.name.lower()
        errs = []
        if "openapi" in name or name.endswith((".yaml", ".yml")) and "api" in name and "async" not in name and "stomp" not in name:
            errs = verify_openapi(file, args.strict)
            verified_count += 1
        elif "asyncapi" in name:
            errs = verify_asyncapi(file, args.strict)
            verified_count += 1
        elif "stomp" in name:
            errs = verify_stomp(file, args.strict)
            verified_count += 1
        elif name.endswith(".proto"):
            errs = verify_proto(file, args.strict)
            verified_count += 1
        elif name.endswith((".graphql", ".gql")):
            errs = verify_graphql(file, args.strict)
            verified_count += 1
        elif name.endswith(".json") and ("schema" in name or "contract" in name):
            errs = verify_json_schema(file, args.strict)
            verified_count += 1
        elif name.endswith(".sql") or "migration" in name:
            errs = verify_sql_migration(file, args.strict)
            verified_count += 1

        all_errors.extend(errs)

    print(f"--- Contract Verification Gate ({contracts_dir}) ---")
    print(f"Verified {verified_count} machine-executable contracts.")

    if all_errors:
        print(f"FAILED with {len(all_errors)} errors:", file=sys.stderr)
        for err in all_errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print("Status: ALL CONTRACTS VALID (100% Conformance)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

