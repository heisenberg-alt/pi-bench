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
(`deberta-pi + spotlighting + capability-policy in front of Qwen3-8B`).
`pi-bench` fills that gap and makes every row one-command reproducible.
Three defenses ship today (DeBERTa v3, spotlighting, capability-policy)
with the composed `spotlight-deberta` and full `spotlight-deberta-policy`
stacks defined — the model matrix lands in the rest of M3.

## Quickstart

```powershell
# install (editable, dev extras)
pip install -e ".[dev]"

# run the baseline: no-defense stack, mock model, InjecAgent seed suite
pibench bench --stack none --model mock --suite injecagent-seed

# writes results/none__mock__injecagent-seed__seed42.csv
# prints a summary table with ASR, FPR, p95 latency, $/1k
```

That baseline is the no-defense floor. Swap `--stack none` for `--stack deberta`
to see a real defense in action; both rows already sit on the leaderboard below.

## Current leaderboard

Auto-generated from `results/*.csv` via `pibench leaderboard`. Sorted by ASR ↓
then FPR ↓.

| Stack | Model | Suite | Seed | n | ASR ↓ | FPR ↓ | p95 (ms) ↓ | $ / 1k ↓ |
| ----- | ----- | ----- | ---- | -- | ----: | ----: | ---------: | -------: |
| `policy` | `mock` | `injecagent-full-enhanced` | 42 | 1064 | 0.000 | 0.000 | 5.0 | $0.0000 |
| `policy` | `mock` | `injecagent-seed` | 42 | 20 | 0.000 | 0.000 | 5.0 | $0.0000 |
| `deberta` | `mock` | `injecagent-seed` | 42 | 20 | 0.000 | 0.000 | 32.8 | $0.0000 |
| `deberta` | `mock` | `injecagent-full-enhanced` | 42 | 1064 | 0.000 | 0.000 | 53.9 | $0.0000 |
| `spotlight-deberta-policy` | `mock` | `injecagent-seed` | 42 | 20 | 0.000 | 0.700 | 40.3 | $0.0000 |
| `spotlight-deberta` | `mock` | `injecagent-seed` | 42 | 20 | 0.000 | 0.700 | 40.3 | $0.0000 |
| `spotlight-deberta-policy` | `mock` | `injecagent-full-enhanced` | 42 | 1064 | 0.000 | 0.700 | 63.1 | $0.0000 |
| `spotlight-deberta` | `mock` | `injecagent-full-enhanced` | 42 | 1064 | 0.000 | 0.700 | 63.1 | $0.0000 |
| `none` | `mock` | `injecagent-full-enhanced` | 42 | 1064 | 1.000 | 0.000 | 5.0 | $0.0000 |
| `none` | `mock` | `injecagent-seed` | 42 | 20 | 1.000 | 0.000 | 5.0 | $0.0000 |
| `spotlight` | `mock` | `injecagent-full-enhanced` | 42 | 1064 | 1.000 | 0.000 | 5.0 | $0.0000 |
| `spotlight` | `mock` | `injecagent-seed` | 42 | 20 | 1.000 | 0.000 | 5.0 | $0.0000 |

Compose finding: `spotlight-deberta` catches the same attacks as `deberta`
alone but **jumps FPR from 0.000 to 0.700** — reproduced on both the
20-case seed suite and the full 1,064-case InjecAgent suite. The
spotlight delimiters look injection-like to a PI classifier that never
saw them in training. Exactly the kind of second-order failure the
composed-defense benchmark is designed to surface.

Output-side finding: the `policy` stack blocks every attack at the
tool-call boundary with **zero input detection** — ASR 0.000, FPR 0.000,
~0 ms added latency against the mock. The caveat: it only stops attacks
with side-effects (tool misuse); text-only exfil needs the detection
layer, which is why the composed posture is the thesis.

The `deberta` stack wraps ProtectAI's
[`deberta-v3-base-prompt-injection-v2`](https://huggingface.co/protectai/deberta-v3-base-prompt-injection-v2)
classifier (ungated, ~184 M params, CPU-inference friendly). Against the
seed suite it eliminates every attack (ASR 1.000 → 0.000) with zero
false positives and ~30 ms of added p95 latency (~55 ms on the full
suite's longer tool responses; one-time model load is excluded via a
warm-up inference). See [`leaderboard.md`](leaderboard.md)
for the always-fresh version.

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
  - type: spotlight        # wrap untrusted content in delimiters
  - type: deberta-pi       # then classify the wrapped payload
    threshold: 0.6
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

## What ships now (M1 + M2 + partial M3)

- Core interfaces: `Verdict`, `Defense`, `Stack`, `Model`, `Suite` — with
  two enforcement points: `Defense.check()` on inputs and
  `Defense.check_output()` on model responses.
- Four defenses:
  - `none` — baseline, passes everything through.
  - `deberta-pi` — ProtectAI DeBERTa-v3 prompt-injection classifier (M2).
    Disk-cached so reruns are free and byte-identical. Threshold and
    device configurable per stack.
  - `spotlight` — Hines-style delimiter/preamble wrapping of untrusted
    content (partial M3). Deterministic, 0-cost. Its value shows up on
    instruction-respecting models; against the mock it is a null-op on
    ASR (as expected) but composing it *before* DeBERTa reveals a real
    FPR regression — see the leaderboard note above.
  - `capability-policy` — output-side tool-call allowlist (M3). Blocks
    any response whose tool calls fall outside the stack's configured
    capabilities — the safety net that works even when detection misses.
- Two models:
  - `mock` — deterministic, offline. Simulates a naive agent that
    complies with obvious injected instructions — echoing the payload *and*
    emitting an exfil `send_email` tool call — so the harness runs green
    without a GPU or API keys.
  - `openai-compat` — chat-completions adapter for any OpenAI-compatible
    endpoint (vLLM serve, llama.cpp, hosted). Configure via
    `PIBENCH_OPENAI_BASE_URL` / `PIBENCH_OPENAI_MODEL` /
    `PIBENCH_OPENAI_API_KEY`. Responses seed-cached to disk so committed
    rows replay byte-identically. First reference rows (Qwen3-8B via
    vLLM) land with the model matrix.
- Three suites:
  - `injecagent-seed` — 20 hand-picked cases in the InjecAgent
    indirect-injection style. Fast, fully offline.
  - `injecagent-full` / `injecagent-full-enhanced` — all 1,054 cases from
    [InjecAgent](https://github.com/uiuc-kang-lab/InjecAgent) (510 direct
    harm + 544 data stealing), pinned to a commit SHA and disk-cached so
    the download happens once. Attack success includes attacker-tool
    invocation, matching the source benchmark's criterion. The `enhanced`
    setting prepends the "ignore all previous instructions" hacking
    prompt; the naive mock only reacts to that marker, so base-setting
    rows become meaningful once real model adapters land.
- Scorer with canary-token detection and benign-side FPR tracking.
- `pibench leaderboard` command that regenerates `leaderboard.md` from
  every CSV under `results/`.
- `pibench report` command that regenerates [`REPORT.md`](REPORT.md) —
  per-suite ablation grids, composition deltas with regression flags, and
  Pareto-front marking — from the same CSVs.
- CSV output with pinned seed, model version, and defense versions.

The roadmap below lists what fills the matrix in later releases.

## Roadmap

| # | Milestone | Status |
| - | --------- | ------ |
| M1 | Vertical slice — one stack × one model × one suite, `pibench bench` prints and commits a CSV | done |
| M2 | Second real defense (ProtectAI DeBERTa v3 PI classifier) — visible ASR drop on the leaderboard | done — ASR 1.000 → 0.000 |
| M3 | Full adapter set × 4 models × 3 suites; spotlighting + capability-policy | in progress — spotlighting, capability-policy, openai-compat adapter, and full InjecAgent suite landed; open-weight leaderboard rows remain |
| M4 | `IndirectRAG-Bench` — own dataset, 500 examples, HF dataset card | planned |
| M5 | `REPORT.md` with composability ablations | done — `pibench report` generates ablation grids, composition deltas, Pareto front |
| M6 | Launch: blog + demo video | planned |

## Non-goals

- No new detector or attack technique — we wrap and grade what exists.
- No SaaS, dashboard, or web app.
- No agent framework.

## License

[MIT](LICENSE).
