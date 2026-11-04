---
name: skill-authoring
description: Use when creating, auditing, or maintaining agent skills while ensuring portability and clean provenance.
---

# Skill authoring for a curated multi-agent pack

## First prefer reuse

1. Search `manifests/skill-map.json` and `upstream.json` before writing a new skill.
2. Compare the candidates by responsibility, trigger, outputs, dependencies, maintenance, and license. Choose one authoritative upstream per responsibility.
3. Prefer vendoring the upstream skill with only documented portability patches. Integrate it through pack-level maps, workflows, templates, and adapters rather than duplicating its procedure.
4. Create a pack-owned skill only when an actual integration gap remains, such as routing, cross-agent handoff, or installation.
5. Do not copy a skill just because its name looks useful. Read `SKILL.md`, referenced files, scripts, and license before selecting it.

## Required structure

- Use `skills/<skill-name>/SKILL.md`; `SKILL.md` must be at that exact level.
- Keep the frontmatter portable: `name` and `description` by default. Add other standard fields only when their meaning is documented and portable.
- `name` must match the containing directory and use lowercase kebab-case.
- `description` must say what the skill does and the concrete situations or requests that should trigger it. Keep it concise and specific; avoid generic phrases such as “helps with software development.”
- State inputs, preconditions, ordered actions, expected outputs, verification, and stop/escalation conditions.
- Put optional details in `references/`, reusable starter files in `assets/`, and executable helpers in `scripts/`. Link every such file from `SKILL.md` with a relative path.
- Avoid mandatory vendor commands. Say “run the project's relevant test command”; describe a capability and provide a sequential fallback when sub-agents or special tools are unavailable.
- Never assume a fixed global installation path, a hidden environment variable, or an agent-specific context file unless the skill explicitly declares that limitation.

## Trigger quality and evaluation

1. Define 5–10 realistic positive prompts that should activate the skill and 5–10 negative/near-neighbor prompts that should not.
2. Include boundary cases: short request, ambiguous request, related but out-of-scope request, and a prompt that should activate a competing skill instead.
3. Review activation precision (unrelated prompts do not trigger) and recall (common in-scope phrasings do trigger). Make the description more discriminative before adding procedural detail.
4. Test on at least two target agents/models when possible. Record agent/version, prompt, whether it activated, and whether the procedure completed.
5. Treat prompt-based checks as evidence, not proof. Re-run them after changing the description, skill name, router map, or agent adapter.
6. Keep examples and tests short enough to rerun. See `references/trigger-testing.md` and `assets/SKILL-template.md`.

## Provenance and license

For every upstream-derived skill, record repository URL, source path, locked commit, license, and all local patches/exclusions in the pack manifests. Preserve required LICENSE/NOTICE files. A changed upstream skill remains upstream-derived; never relabel it as custom to avoid attribution.

## Definition of done

- One authoritative owner per responsibility, with overlap documented in `manifests/skill-map.json`.
- Frontmatter parses; name matches the directory; description contains meaningful trigger guidance.
- All relative Markdown links and referenced assets resolve in the packaged directory.
- Outputs align with the pack's artifact contracts and stable IDs when applicable.
- Irreversible, production, security-sensitive, or scope-changing actions include explicit approval gates.
- `python scripts/lint_pack.py` and `python -m unittest discover -s tests -v` pass. Release requires `python scripts/lint_pack.py --strict`.
- Cross-agent compatibility is not claimed until realistic prompts have been tried on at least two real target agents.
