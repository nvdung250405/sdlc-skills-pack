# SDLC Pack Live Agent Execution Benchmarks

This directory archives empirical execution transcripts, token measurements, and evaluation runs of coding agents executing the 11 golden task fixtures (`evals/*.json`).

---

## Structure

```
evals/
├── *.json                    # 11 Golden evaluation fixtures (verified by scripts/run_evals.py)
└── results/
    ├── BENCHMARK_METHODOLOGY.md   # Comparative A/B evaluation protocol
    ├── sample-run-claude.json     # Sample benchmark transcript schema
    └── <runtime>/                 # Agent execution logs (claude-code, antigravity, cursor, etc.)
```

## Schema for Benchmark Execution Transcripts

Each JSON transcript in `evals/results/` records:
- `fixture_id`: Golden fixture identifier (e.g. `eval-feature-loop-01`)
- `runtime`: Agent platform (`claude-code`, `antigravity-ide`, `cursor`, etc.)
- `model`: Exact model version (e.g. `claude-3-7-sonnet`, `gemini-2.5-pro`)
- `profile`: Pack installation profile used (`eager-lean`, `core`, `core+web`, `full`)
- `tokens`: Prompt, completion, and total tokens
- `skills_invoked`: Sequence of skills loaded during the task
- `artifacts_produced`: List of relative paths and schema validation status
- `verification_passed`: Boolean indicating empirical test gate status
- `limitations`: Observations, manual fallbacks triggered, or edge cases
