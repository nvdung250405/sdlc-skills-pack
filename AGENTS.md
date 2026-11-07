# Working on Universal SDLC Agent Skills

- Read `README.md`, `docs/stage-skill-map.md`, and `skills/using-sdlc-skills/SKILL.md` before changing the pack.
- The pack combines selected skills from Addy Osmani Agent Skills, Superpowers, and Anthropic Skills (all pinned SHA), plus locally adapted skills from Uxcel Product Skills, Agentic SDLC Kit, wshobson/agents, sickn33/agentic-awesome-skills and api-contract-testing. GitHub Spec Kit and BMAD are reference-only. Review `upstream.json` before adding/removing a source.
- `using-sdlc-skills` is the only default pack router. Do not introduce a competing router into the default flow.
- Prefer updating workflows, artifact contracts, templates, manifests or thin adapters over rewriting a good upstream skill.
- Upstream-synced skills must remain pinned and carry their license/notice. Derived skills are manual-review-only: never let upstream sync overwrite them; update their content hash only after a reviewed edit.
- Keep feature Story/Acceptance Criteria in one canonical `docs/features/<feature-id>/spec.md`; avoid duplicate task lists. `planning-and-task-breakdown` owns the final task list for each feature.
- Never run upstream sync into active paths unless every selected upstream has been fetched, staged and validated. `scripts/sync_upstream.py` must remain transactional.
- Do not overwrite conflicting installed skills silently. `scripts/install.py --force` must back up old content.
- Run `python scripts/lint_pack.py` during local work, then `python scripts/lint_pack.py --strict` and `python -m unittest discover -s tests -v` before release.
- Never claim cross-agent runtime compatibility unless relevant workflows have been exercised on at least two real agents.
- Use `verification-before-completion` before claiming tests or checks passed. Report commands actually run and limitations honestly.
- For token efficiency and harness execution: consult `.agent/repo_map.txt` for structural orientation, run long test/build commands via `python scripts/bounded_run.py`, and inspect code via viewports instead of reading full large files.
