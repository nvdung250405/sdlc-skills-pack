from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


def run_script(script: str, *args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [PYTHON, str(ROOT / "scripts" / script), *args],
        cwd=cwd or ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
    )


class PackStaticTests(unittest.TestCase):
    def test_offline_linter_accepts_partial_or_complete_distribution(self) -> None:
        result = run_script("lint_pack.py")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Checked", result.stdout)
        if run_script("lint_pack.py", "--strict").returncode == 0:
            self.assertIn("Pack structure, upstream selection, resources and provenance are valid.", result.stdout)
        else:
            self.assertTrue("WARNING:" in result.stdout or "partial" in result.stdout.lower())

    def test_strict_lint_matches_upstream_sync_state(self) -> None:
        result = run_script("lint_pack.py", "--strict")
        if result.returncode == 0:
            self.assertIn("Pack structure, upstream selection, resources and provenance are valid.", result.stdout)
        else:
            self.assertIn("Pack validation FAILED.", result.stdout)
            self.assertTrue((ROOT / "manifests" / "upstream-lock.json").exists() is False or "ERROR:" in result.stdout)

    def test_handoff_template_and_skill_authoring_assets_exist(self) -> None:
        handoff = ROOT / "skills" / "task-handoff" / "assets" / "task-template.md"
        self.assertTrue(handoff.is_file(), "task-handoff links an asset that must ship with the skill")
        authoring = ROOT / "extras" / "skill-authoring"
        self.assertTrue((authoring / "assets" / "SKILL-template.md").is_file())
        self.assertTrue((authoring / "references" / "trigger-testing.md").is_file())

    def test_antigravity_profiles_are_configured(self) -> None:
        adapters = json.loads((ROOT / "adapters" / "agents.json").read_text(encoding="utf-8"))["agents"]
        self.assertEqual(adapters["antigravity"]["project"], ".agents/skills")
        self.assertEqual(adapters["antigravity"]["global"], "~/.gemini/config/skills")
        self.assertEqual(adapters["antigravity-cli"]["project"], ".agents/skills")
        self.assertEqual(adapters["antigravity-cli"]["global"], "~/.gemini/antigravity-cli/skills")

    def test_pack_has_only_one_default_router(self) -> None:
        manifest = json.loads((ROOT / "upstream.json").read_text(encoding="utf-8"))
        matches = [item for upstream in manifest["upstreams"] for item in upstream.get("items", [])
                   if item.get("name", Path(item["src"]).name) in {"using-sdlc-skills", "using-agent-skills"}]
        self.assertEqual(matches, [], "Routers are pack-owned policy; upstream routers must not compete by default.")
        router = (ROOT / "skills" / "using-sdlc-skills" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("name: using-sdlc-skills", router)
        self.assertIn("only default pack-level router", router.lower())

    def test_selected_skill_map_has_no_unknown_or_duplicate_skill(self) -> None:
        manifest = json.loads((ROOT / "upstream.json").read_text(encoding="utf-8"))
        skill_map = json.loads((ROOT / "manifests" / "skill-map.json").read_text(encoding="utf-8"))
        known = {"using-sdlc-skills", "task-handoff", "skill-authoring"}
        for upstream in manifest["upstreams"]:
            for item in upstream.get("items", []):
                name = item.get("name", Path(item["src"]).name)
                known.add(name)
        for item in manifest.get("derived_skills", []):
            known.add(item["name"])
        groups = skill_map["groups"]
        entries = [name for members in groups.values() for name in members]
        self.assertEqual(len(entries), len(set(entries)), "A skill should appear in one group only.")
        self.assertEqual(set(entries) - known, set(), "Skill map contains unknown skills.")

    def test_skill_inventory_counts_match_materialized_directories(self) -> None:
        manifest = json.loads((ROOT / "upstream.json").read_text(encoding="utf-8"))
        skill_dirs = {path.name for path in (ROOT / "skills").iterdir() if path.is_dir()}
        extra_dirs = {path.name for path in (ROOT / "extras").iterdir() if path.is_dir()}
        self.assertEqual(len(skill_dirs), 29)
        self.assertEqual(len(extra_dirs), 34)
        for item in manifest.get("derived_skills", []):
            self.assertIn(item["name"], skill_dirs if item.get("tier") == "skills" else extra_dirs)

    def test_feature_spec_has_canonical_story_and_gherkin_contract(self) -> None:
        template = (ROOT / "templates" / "specs" / "feature-spec.md").read_text(encoding="utf-8")
        self.assertIn("canonical feature artifact", template.lower())
        self.assertIn("US-FEAT-NNN-001", template)
        self.assertIn("AC-FEAT-NNN-001", template)
        for marker in ("Given:", "When:", "Then:"):
            self.assertIn(marker, template)

    def test_all_11_workflows_and_templates_exist_and_have_standard_headers(self) -> None:
        templates = sorted([p for p in (ROOT / "templates").rglob("*.md") if p.name != "README.md"])
        self.assertEqual(len(templates), 23, f"Expected 23 markdown templates, found {len(templates)}")
        for t in templates:
            text = t.read_text(encoding="utf-8")
            self.assertIn("> **Document type:** Canonical Artifact Contract", text, f"{t.name} missing header")

        workflows = sorted(list((ROOT / "workflows").glob("*.md")))
        self.assertEqual(len(workflows), 11, f"Expected 11 workflows, found {len(workflows)}")
        for w in workflows:
            text = w.read_text(encoding="utf-8")
            self.assertIn("> **Document type:** Standardized Workflow Definition", text, f"{w.name} missing header")

    def test_router_bundled_assets_are_in_sync_with_root(self) -> None:
        router_tmpl_dir = ROOT / "skills" / "using-sdlc-skills" / "assets" / "templates"
        for t in (ROOT / "templates").rglob("*"):
            if t.is_file() and t.name != "README.md":
                rel = t.relative_to(ROOT / "templates")
                bundled = router_tmpl_dir / rel
                self.assertTrue(bundled.is_file(), f"Missing bundled template {rel}")
                self.assertEqual(t.read_bytes(), bundled.read_bytes(), f"Bundled template {rel} out of sync")

        router_wf_dir = ROOT / "skills" / "using-sdlc-skills" / "assets" / "workflows"
        for w in (ROOT / "workflows").glob("*.md"):
            bundled = router_wf_dir / w.name
            self.assertTrue(bundled.is_file(), f"Missing bundled workflow {w.name}")
            self.assertEqual(w.read_bytes(), bundled.read_bytes(), f"Bundled workflow {w.name} out of sync")

        router_script_dir = ROOT / "skills" / "using-sdlc-skills" / "scripts"
        for script_name in ["scaffold.py", "bounded_run.py", "verify_contracts.py"]:
            src = ROOT / "scripts" / script_name
            bundled = router_script_dir / script_name
            self.assertTrue(bundled.is_file(), f"Missing bundled script {script_name}")
            self.assertEqual(src.read_bytes(), bundled.read_bytes(), f"Bundled script {script_name} out of sync")

        res_check = run_script("build_assets.py", "--check")
        self.assertEqual(res_check.returncode, 0, f"build_assets.py --check failed: {res_check.stderr}")

    def test_scaffold_all_32_artifact_aliases(self) -> None:
        from scripts.scaffold import ARTIFACT_MAP
        self.assertEqual(len(ARTIFACT_MAP), 32)
        with tempfile.TemporaryDirectory() as temp:
            dest_dir = Path(temp)
            for alias, (tmpl_file, dest_pattern) in ARTIFACT_MAP.items():
                target = dest_dir / tmpl_file
                res = run_script("scaffold.py", alias, "--id", "test-feat", "--target", str(target))
                self.assertEqual(res.returncode, 0, f"Scaffold failed for {alias}: {res.stderr}")
                self.assertTrue(target.is_file(), f"Target file was not created for {alias}")
                content = target.read_text(encoding="utf-8")
                if tmpl_file.endswith(".md"):
                    self.assertIn("> **Document type:** Canonical Artifact Contract", content, f"{alias} missing contract header")
                else:
                    self.assertGreater(len(content), 10, f"{alias} file is empty or too short")

    def test_verify_contracts_gate_detects_invalid_yaml_and_structural_errors(self) -> None:
        # 1. Canonical contracts in templates/contracts must all pass
        res = run_script("verify_contracts.py", "--dir", "templates/contracts")
        self.assertEqual(res.returncode, 0, f"Canonical templates failed verification: {res.stdout}")

        # 2. Corrupted YAML or garbage syntax must fail with non-zero exit code
        with tempfile.TemporaryDirectory() as temp:
            bad_dir = Path(temp)
            # Garbage syntax
            (bad_dir / "openapi.yaml").write_text("invalid: [unclosed bracket", encoding="utf-8")
            res_bad = run_script("verify_contracts.py", "--dir", str(bad_dir))
            self.assertNotEqual(res_bad.returncode, 0, "Corrupted YAML must fail verification gate")
            self.assertIn("FAILED", res_bad.stdout + res_bad.stderr)

            # Non-mapping YAML
            (bad_dir / "openapi.yaml").write_text("- item1\n- item2", encoding="utf-8")
            res_list = run_script("verify_contracts.py", "--dir", str(bad_dir))
            self.assertNotEqual(res_list.returncode, 0, "Non-mapping YAML must fail verification gate")
            self.assertIn("FAILED", res_list.stdout + res_list.stderr)

            # Missing required fields (empty document)
            (bad_dir / "openapi.yaml").write_text("some_random_key: true\n", encoding="utf-8")
            res_missing = run_script("verify_contracts.py", "--dir", str(bad_dir))
            self.assertNotEqual(res_missing.returncode, 0, "OpenAPI missing version must fail verification gate")
            self.assertIn("FAILED", res_missing.stdout + res_missing.stderr)

    def test_linter_strict_guardrails_detect_metric_mismatch_broken_paths_and_hygiene(self) -> None:
        from scripts.lint_pack import check_doc_metrics, check_doc_path_references, check_distribution_hygiene
        
        # 1. Broken path reference detection
        test_errors: list[str] = []
        dummy_wf = ROOT / "workflows" / "tmp_broken_ref_test.md"
        try:
            dummy_wf.write_text("See [broken](templates/specs/nonexistent-spec-file.md) for details.", encoding="utf-8")
            check_doc_path_references(test_errors)
            self.assertTrue(any("nonexistent-spec-file.md" in e for e in test_errors), "Linter must catch broken template references")
        finally:
            dummy_wf.unlink(missing_ok=True)

        # 2. Hygiene violation detection
        test_hygiene_errors: list[str] = []
        junk_file = ROOT / "templates" / "junk.pyc"
        try:
            junk_file.write_bytes(b"\0\0")
            check_distribution_hygiene(test_hygiene_errors)
            self.assertTrue(any("junk.pyc" in e for e in test_hygiene_errors), "Linter must catch compiled bytecode in distribution folders")
        finally:
            junk_file.unlink(missing_ok=True)

    def test_installer_requires_verified_pack_unless_partial_is_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            dest = Path(temp) / "new-skills"
            is_complete = run_script("lint_pack.py", "--strict").returncode == 0
            result = run_script("install.py", "custom", "--dest", str(dest))
            if is_complete:
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertTrue(dest.is_dir())
            else:
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertFalse(dest.exists())

    def test_installer_preflight_backup_and_force(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            dest = Path(temp) / "new-skills"
            initial = run_script("install.py", "custom", "--dest", str(dest), "--allow-partial")
            self.assertEqual(initial.returncode, 0, initial.stdout + initial.stderr)

            selected = "using-sdlc-skills"
            installed = dest / selected / "SKILL.md"
            original_text = installed.read_text(encoding="utf-8")
            installed.write_text(original_text + "\n# user change\n", encoding="utf-8")

            conflict = run_script("install.py", "custom", "--dest", str(dest), "--allow-partial")
            self.assertEqual(conflict.returncode, 3, conflict.stdout + conflict.stderr)
            self.assertIn("user change", installed.read_text(encoding="utf-8"))

            forced = run_script("install.py", "custom", "--dest", str(dest), "--allow-partial", "--force")
            self.assertEqual(forced.returncode, 0, forced.stdout + forced.stderr)
            self.assertEqual(installed.read_text(encoding="utf-8"), original_text)
            backups = list(Path(temp).rglob(".sdlc-skill-backups/**/using-sdlc-skills/SKILL.md"))
            if not backups:
                backups = list(Path(temp).rglob(".sdlc-skill-backups/**/SKILL.md"))
            self.assertTrue(backups, "--force should preserve replaced skill content in a backup.")
            self.assertTrue(any("user change" in file.read_text(encoding="utf-8") for file in backups))

    def test_agents_md_does_not_overwrite_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            target = root / "AGENTS.md"
            target.write_text("Do not overwrite me\n", encoding="utf-8")
            refused = run_script("install.py", "agents-md", cwd=root)
            self.assertEqual(refused.returncode, 3, refused.stdout + refused.stderr)
            self.assertEqual(target.read_text(encoding="utf-8"), "Do not overwrite me\n")
            shutil.copytree(ROOT / "skills", root / "skills")
            shutil.copytree(ROOT / "workflows", root / "workflows")
            shutil.copytree(ROOT / "templates", root / "templates")

            forced = run_script("install.py", "agents-md", "--force", cwd=root)
            self.assertEqual(forced.returncode, 0, forced.stdout + forced.stderr)
            self.assertIn("portable index", target.read_text(encoding="utf-8").lower())
            backups = list(root.rglob(".sdlc-skill-backups/**/AGENTS.md"))
            self.assertTrue(backups)
            self.assertEqual(backups[0].read_text(encoding="utf-8"), "Do not overwrite me\n")

    def test_eval_fixtures_are_valid_and_executable(self) -> None:
        result = run_script("run_evals.py")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Successfully verified 4 golden evaluation fixtures", result.stdout)


@unittest.skipUnless(shutil.which("git"), "Git is required for local sync transaction tests")
class SyncTransactionTests(unittest.TestCase):
    def _fixture(self, root: Path) -> tuple[Path, Path]:
        source = root / "source-repo"
        source.mkdir()
        subprocess.run(["git", "init", "-b", "main"], cwd=source, check=True, capture_output=True, text=True)
        subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=source, check=True)
        subprocess.run(["git", "config", "user.name", "Test Fixture"], cwd=source, check=True)
        skill_dir = source / "skills" / "demo-skill"
        skill_dir.mkdir(parents=True)
        (source / "references").mkdir(parents=True)
        (source / "references" / "common.md").write_text("# Shared reference\n", encoding="utf-8")
        (skill_dir / "SKILL.md").write_text(
            "---\nname: demo-skill\ndescription: A local sync fixture skill.\n---\n\n# Demo\n\n[Common](../../references/common.md)\n",
            encoding="utf-8",
        )
        (skill_dir / "docs").mkdir()
        (skill_dir / "docs" / "nested.md").write_text(
            "# Nested\n\n[Common](../../../references/common.md)\n", encoding="utf-8"
        )
        (source / "LICENSE").write_text("test license\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=source, check=True)
        subprocess.run(["git", "commit", "-m", "fixture"], cwd=source, check=True, capture_output=True, text=True)

        pack = root / "pack"
        (pack / "scripts").mkdir(parents=True)
        (pack / "manifests").mkdir()
        shutil.copy2(ROOT / "scripts" / "sync_upstream.py", pack / "scripts" / "sync_upstream.py")
        manifest = {
            "schema_version": 2,
            "upstreams": [{
                "id": "fixture-source",
                "url": str(source),
                "ref": "main",
                "license": "MIT-test",
                "license_file": "LICENSE",
                "shared_refs_dir": "references",
                "items": [{"src": "skills/demo-skill", "tier": "skills"}],
            }],
        }
        (pack / "upstream.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        return pack, source

    def test_sync_succeeds_from_local_git_source_and_writes_lock(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            pack, _ = self._fixture(Path(temp))
            result = subprocess.run(
                [PYTHON, str(pack / "scripts" / "sync_upstream.py")],
                cwd=pack, text=True, encoding="utf-8", errors="replace", capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue((pack / "skills" / "demo-skill" / "SKILL.md").is_file())
            self.assertTrue((pack / "third_party" / "fixture-source" / "LICENSE").is_file())
            self.assertTrue((pack / "manifests" / "upstream-lock.json").is_file())
            self.assertTrue((pack / "skills" / "demo-skill" / "references" / "common.md").is_file())
            root_skill = (pack / "skills" / "demo-skill" / "SKILL.md").read_text(encoding="utf-8")
            nested_skill = (pack / "skills" / "demo-skill" / "docs" / "nested.md").read_text(encoding="utf-8")
            self.assertIn("[Common](references/common.md)", root_skill)
            self.assertIn("[Common](../references/common.md)", nested_skill)
            provenance = json.loads((pack / "manifests" / "skill-provenance.json").read_text(encoding="utf-8"))
            self.assertIn("skills/demo-skill", provenance["skills"])

    def test_sync_failure_does_not_modify_existing_materialized_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            pack, _ = self._fixture(Path(temp))
            script = pack / "scripts" / "sync_upstream.py"
            first = subprocess.run([PYTHON, str(script)], cwd=pack, text=True, capture_output=True)
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            existing = pack / "skills" / "demo-skill" / "SKILL.md"
            existing.write_text("last-known-good\n", encoding="utf-8")

            manifest_path = pack / "upstream.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["upstreams"][0]["items"].append({"src": "skills/does-not-exist", "tier": "skills"})
            manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
            failed = subprocess.run([PYTHON, str(script)], cwd=pack, text=True, capture_output=True)
            self.assertNotEqual(failed.returncode, 0, failed.stdout + failed.stderr)
            self.assertEqual(existing.read_text(encoding="utf-8"), "last-known-good\n")

    def test_sync_retains_removed_skills_unless_prune_archives_them(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            pack, _ = self._fixture(Path(temp))
            script = pack / "scripts" / "sync_upstream.py"
            first = subprocess.run([PYTHON, str(script)], cwd=pack, text=True, capture_output=True)
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)

            manifest_path = pack / "upstream.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["upstreams"][0]["items"] = []
            manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

            ordinary = subprocess.run([PYTHON, str(script)], cwd=pack, text=True, capture_output=True)
            self.assertEqual(ordinary.returncode, 0, ordinary.stdout + ordinary.stderr)
            skill = pack / "skills" / "demo-skill"
            self.assertTrue(skill.is_dir(), "Ordinary sync must retain an obsolete path for review.")
            lock = json.loads((pack / "manifests" / "upstream-lock.json").read_text(encoding="utf-8"))
            self.assertIn("skills/demo-skill", lock["retired_paths"])

            pruned = subprocess.run([PYTHON, str(script), "--prune"], cwd=pack, text=True, capture_output=True)
            self.assertEqual(pruned.returncode, 0, pruned.stdout + pruned.stderr)
            self.assertFalse(skill.exists(), "Pruned skill should leave active path.")
            lock = json.loads((pack / "manifests" / "upstream-lock.json").read_text(encoding="utf-8"))
            self.assertEqual(lock["retired_paths"], [])
            backups = list((pack / ".sdlc-upstream-backups").rglob("SKILL.md"))
            self.assertTrue(backups, "Pruned content must be archived, not deleted.")
            self.assertEqual(backups[0].read_text(encoding="utf-8").strip(), "---\nname: demo-skill\ndescription: A local sync fixture skill.\n---\n\n# Demo\n\n[Common](references/common.md)")


if __name__ == "__main__":
    unittest.main(verbosity=2)
