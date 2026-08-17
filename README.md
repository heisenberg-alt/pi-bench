# pi-bench

pi-bench is a benchmark for composed prompt-injection defenses. It grades the
full stack deployed in front of a model (detector, prompt hardening, output
capability policy) rather than any single component. Every row reports four
numbers, all lower-is-better: ASR, FPR, p95 latency, and cost per 1k
requests. Open-weight models come first for reproducibility; the adapter can
also target any OpenAI-compatible hosted endpoint.

## Why another benchmark

Existing benchmarks grade single components. Lakera PINT grades detectors,
InjecAgent and AgentDojo grade models under indirect injection, and
CyberSecEval grades models across attack classes. None of them grade what
practitioners actually deploy: a stack such as `deberta-pi` plus spotlighting
plus a capability policy in front of an 8B model. pi-bench fills that gap and
makes every row reproducible with one command.

## Quickstart

```bash
# install (editable, dev extras)
pip install -e ".[dev]"

# run the baseline: no-defense stack, mock model, InjecAgent seed suite
pibench bench --stack none --model mock --suite injecagent-seed

# writes results/none__mock__injecagent-seed__seed42.csv
# prints a summary table with ASR, FPR, p95 latency, $/1k
```

Swap `--stack none` for `--stack deberta` to see a real defense in action.

## Results

Four open-weight models, six stacks, three suites, all seed-pinned and
replayable from cached responses. Undefended attack success rates:

| Model | `injecagent-full` (1,054 cases) | `indirectrag-bench` (500 cases) |
| ----- | ------------------------------: | ------------------------------: |
| `llama3.1-8b` | 0.117 | 0.186 |
| `qwen3-8b` | 0.022 | 0.297 |
| `qwen2.5-7b` | 0.146 | 0.463 |
| `mistral-7b` | 0.000 * | 0.723 |

\* One tool call in 3,123 responses. This score reflects non-engagement with
the tool channel rather than robustness; the same model is the most
injectable through retrieved context.

The composed framing surfaces three findings:

- **Composition can break a defense.** Spotlighting alone is harmless and
  DeBERTa alone is accurate, but running spotlight before DeBERTa lifts FPR
  from 0.000 to 0.700 (1.000 on RAG text) while adding no detection. The
  delimiters themselves look injection-like to the classifier.
- **Different channels need different defenses.** The output-side capability
  policy is the only stack that reaches ASR 0.000 with FPR 0.000 on real
  tool misuse, yet it barely moves RAG-text exfiltration (0.463 to 0.351).
  No tool check can catch a canary leaving through response text.
- **Susceptibility is channel-specific.** A model's rank on one injection
  surface does not predict its rank on another; see the mistral row above.

Full data: [`leaderboard.md`](leaderboard.md) has every row,
[`REPORT.md`](REPORT.md) has the ablation grids, composition deltas, and
Pareto fronts, and [`docs/findings.md`](docs/findings.md) has the per-suite
analysis.

## Architecture

![pi-bench architecture](docs/img/architecture.svg)

There are two enforcement points by design: detection on inputs, which is
best-effort because detectors miss, and a capability policy on outputs,
which blocks side effects even when detection fails. Pure classifier stacks
and pure policy stacks both underperform composed ones on the Pareto
frontier.

## Metrics

| Metric | Definition |
| ------ | ---------- |
| ASR | Attack success rate on attack cases: canary exfiltration, tool misuse, or a capability-policy violation. |
| FPR | False-positive block rate on benign cases. A defense that blocks everything scores ASR 0 at FPR 1. |
| p95 latency (ms) | 95th-percentile added latency across stack and model, per request. |
| $ / 1k requests | Mean cost of detector and model calls, seed-cached. |

Every CSV row pins the model version, defense versions, and seed. Reruns
against the same triple are byte-identical.

## Components

- **Defenses (4):** `none` (baseline), `deberta-pi` (ProtectAI
  [DeBERTa-v3 PI classifier](https://huggingface.co/protectai/deberta-v3-base-prompt-injection-v2),
  disk-cached), `spotlight` (Hines-style delimiter wrapping of untrusted
  content, deterministic and zero-cost), and `capability-policy`
  (output-side tool-call allowlist).
- **Models (6):** `mock` (deterministic and offline, so the harness runs
  green with no GPU or keys), `openai-compat` (any OpenAI-compatible
  endpoint via `PIBENCH_OPENAI_BASE_URL` / `_MODEL` / `_API_KEY`; forwards
  per-case tool schemas and seed-caches responses to disk), and four pinned
  tags served through Ollama by default: `qwen3-8b`, `llama3.1-8b`,
  `mistral-7b`, `qwen2.5-7b`.
- **Suites (4):** `injecagent-seed` (20 offline cases),
  `injecagent-full` / `-enhanced` (all 1,054
  [InjecAgent](https://github.com/uiuc-kang-lab/InjecAgent) cases, pinned to
  a commit SHA and cached; attack success includes attacker-tool
  invocation), and `indirectrag-bench` (500 purpose-built RAG-injection
  cases, 350 attack and 150 benign with a unique canary per case, published
  on the [Hugging Face Hub](https://huggingface.co/datasets/heisenberg-88/indirectrag-bench)).
- **Commands:** `pibench bench` runs one stack, model, and suite row;
  `pibench leaderboard` regenerates `leaderboard.md`; `pibench report`
  regenerates `REPORT.md`. GPU rows reproduce via
  [`modal_run.py`](modal_run.py).

## Extending

A new stack, defense, model, or suite is a single-file addition:

```yaml
# stacks/my-stack.yaml
name: my-stack
defenses:
  - type: spotlight        # wrap untrusted content in delimiters
  - type: deberta-pi       # then classify the wrapped payload
    threshold: 0.6
```

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

## Roadmap

| # | Milestone | Status |
| - | --------- | ------ |
| M1 | Vertical slice: one stack, one model, one suite | done |
| M2 | First real defense (ProtectAI DeBERTa v3) | done; ASR 1.000 to 0.000 |
| M3 | Full matrix: 4 models, 6 stacks, 3 suites; spotlighting and capability policy | done; 72 GPU rows on Modal A10Gs, see [`docs/findings.md`](docs/findings.md) |
| M4 | IndirectRAG-Bench, a 500-case dataset with an HF card | done; [published](https://huggingface.co/datasets/heisenberg-88/indirectrag-bench) |
| M5 | `REPORT.md` with composability ablations | done |
| M6 | Launch: blog and demo video | planned |

Backlog: `injecagent-full-enhanced` rows for the four real models (the
"ignore all previous instructions" escalation setting; a one-line `SUITES`
change in `modal_run.py`, roughly 5 GPU-hours).

## Non-goals

- No new detector or attack technique; we wrap and grade what exists.
- No SaaS, dashboard, or web app.
- No agent framework.

## License

[MIT](LICENSE).
