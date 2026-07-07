# pi-bench

**A composed-defense benchmark for prompt injection.** Grades entire defense
stacks — model × detectors × defenses × capability policy — not individual
detectors.

| ASR ↓ | FPR ↓ | p95 latency ↓ | $ / 1k requests ↓ |
| ----- | ----- | -------------- | ------------------ |

Open-weight-first for reproducibility. Hosted models included as reference rows.

## Why another benchmark?

Existing benchmarks grade single components:

- Lakera PINT → grades detectors.
- InjecAgent, AgentDojo → grade models under indirect injection.
- CyberSecEval → grades models under many attack classes.

None grade the thing practitioners actually deploy: a **stack**
(`PromptGuard + spotlighting + capability-policy in front of Qwen3-8B`).
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

## Architecture

![pi-bench architecture](docs/img/architecture.svg)

Two enforcement points on purpose: **detection** on inputs (best-effort;
detectors miss) and a **capability policy** on outputs (the safety net that
blocks side-effects even when detection fails). This layered posture is the
technical thesis of the benchmark — pure classifier stacks and pure policy
stacks both underperform composed ones on the real-world Pareto frontier.

## Metrics

Every leaderboard row reports the same four numbers. **Lower is better for
all of them.**

| Metric | Direction | Definition |
| ------ | :-------: | ---------- |
| **ASR** | ↓ | Attack success rate on attack cases: canary exfil, tool misuse, or capability-policy violation. |
| **FPR** | ↓ | False-positive block rate on benign cases — the honesty column. A defense that blocks everything scores ASR = 0 but FPR = 1. |
| **p95 latency (ms)** | ↓ | 95th-percentile added latency across stack + model per request. |
| **$ / 1k requests** | ↓ | Mean cost of embed + detector + judge + model calls, seed-cached. |

Every CSV row pins the model version, defense versions, and seed. Reruns
against the same triple are byte-identical.

## Extension points

Adding a new **stack**, **defense**, **model**, or **suite** is a single-file
addition — that is the whole point of the registry pattern.

Compose an existing set of defenses into a new stack:

```yaml
# stacks/my-stack.yaml
name: my-stack
defenses:
  - type: promptguard
    threshold: 0.6
  - type: spotlight
```

Wrap an external classifier or write a heuristic as a new defense:

```python
# src/pibench/defenses/mydefense.py
from pibench.core.registry import DEFENSES
from pibench.core.types import Message, Verdict
from pibench.defenses.base import Defense

@DEFENSES.register("mydefense")
class MyDefense(Defense):
    name = "mydefense"
    version = "0.1"
    def check(self, messages: list[Message]) -> Verdict: ...
```

Models and suites follow the same pattern under `src/pibench/models/` and
`src/pibench/suites/`.

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
| M1 | Vertical slice — one stack × one model × one suite, `pibench bench` prints and commits a CSV | done |
| M2 | Second real defense (Prompt Guard 2 adapter) — visible ASR drop on the leaderboard | next |
| M3 | Full adapter set × 4 models × 3 suites | planned |
| M4 | `IndirectRAG-Bench` — own dataset, 500 examples, HF dataset card | planned |
| M5 | `REPORT.md` with composability ablations | planned |
| M6 | Launch: blog + demo video | planned |

## Non-goals

- No new detector or attack technique — we wrap and grade what exists.
- No SaaS, dashboard, or web app.
- No agent framework.

## License

[MIT](LICENSE).
