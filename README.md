# pi-bench

**A composed-defense benchmark for prompt injection.** Grades entire defense
stacks — model × detectors × defenses × capability policy — not individual
detectors. Reports the four numbers that matter, always:

| ASR ↓ | FPR ↓ | p95 latency ↑ | $ / 1k requests ↑ |
| ----- | ----- | -------------- | ------------------ |

Open-weight-first for reproducibility. Hosted models included as reference rows.

## Why another benchmark?

Existing benchmarks grade single components:

- Lakera PINT → grades detectors.
- InjecAgent, AgentDojo → grade models under indirect injection.
- CyberSecEval → grades models under many attack classes.

None grade the thing practitioners actually deploy: a **stack**
(`LlamaFirewall + spotlighting + capability-policy in front of Qwen3-8B`).
`pi-bench` fills that gap and makes every row one-command reproducible.

## Quickstart

```powershell
# install (editable, dev extras)
pip install -e ".[dev]"

# run the baseline: no-defense stack, mock model, InjecAgent seed suite
pibench bench --stack none --model mock --suite injecagent-seed

# writes results/none__mock__injecagent-seed__seed42.csv
# prints a summary table with ASR, FPR, p95 latency, $/1k
```

That's M1. Every future stack, model, and suite plugs into the same command.

## What ships in M1 (this release)

- Core interfaces: `Verdict`, `Defense`, `Stack`, `Model`, `Suite`.
- One defense: `none` (baseline; passes everything through).
- One model: `mock` — deterministic, offline. Simulates a naive agent that
  complies with obvious injected instructions so the harness runs green
  without a GPU or API keys. Real open-weight adapters (Qwen3-8B via
  vLLM/HF) land in M3.
- One suite: `injecagent-seed` — 20 hand-picked cases in the InjecAgent
  indirect-injection style. Enough to demonstrate the harness end-to-end.
- Scorer with canary-token detection and benign-side FPR tracking.
- CSV output with pinned seed, model version, and defense versions.

The roadmap below lists what fills the matrix in later releases.

## Roadmap

| # | Milestone | Status |
| - | --------- | ------ |
| M1 | Vertical slice — one stack × one model × one suite, `pibench bench` prints and commits a CSV | in progress |
| M2 | Second real defense (LlamaFirewall adapter) — visible ASR drop on the leaderboard | planned |
| M3 | Full adapter set × 4 models × 3 suites | planned |
| M4 | `IndirectRAG-Bench` — own dataset, 500 examples, HF dataset card | planned |
| M5 | `REPORT.md` with composability ablations | planned |
| M6 | Launch: blog + demo video | planned |

## Non-goals

- No new detector or attack technique — we wrap and grade what exists.
- No SaaS, dashboard, or web app.
- No agent framework.

## License

MIT (planned).
