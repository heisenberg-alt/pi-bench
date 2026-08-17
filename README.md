# pi-bench

pi-bench is a benchmark for composed prompt injection defenses. Instead of
grading a detector or a model on its own, it grades the whole stack a team
would actually deploy: a detector, prompt hardening, and an output capability
policy sitting in front of a model. Each row reports four numbers, and lower
is better for all of them: attack success rate, false positive rate, p95
latency, and cost per thousand requests.

Open-weight models come first because they keep results reproducible. The
adapter can also point at any OpenAI-compatible hosted endpoint.

## Why another benchmark

Plenty of benchmarks exist, but each grades a single component. Lakera PINT
grades detectors. InjecAgent and AgentDojo grade models under indirect
injection. CyberSecEval grades models across attack classes. What nobody
grades is the thing teams actually ship: a stack such as a DeBERTa classifier
plus spotlighting plus a capability policy in front of an 8B model. pi-bench
grades exactly that, and every row can be reproduced with a single command.

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

Four open-weight models, six stacks, three suites. Every run is pinned to
seed 42 and can be replayed from cached responses. The table shows attack
success rates with no defense in place:

| Model | `injecagent-full` (1,054 cases) | `indirectrag-bench` (500 cases) |
| --- | ---: | ---: |
| `llama3.1-8b` | 0.117 | 0.186 |
| `qwen3-8b` | 0.022 | 0.297 |
| `qwen2.5-7b` | 0.146 | 0.463 |
| `mistral-7b` | 0.000 * | 0.723 |

\* One tool call in 3,123 responses. Mistral simply does not engage the tool
channel, so this score is not evidence of robustness. The same model is the
easiest to inject through retrieved context.

Three things stood out:

- **Composition can break a defense.** Spotlighting is harmless on its own
  and DeBERTa is accurate on its own. Run spotlighting first, though, and
  DeBERTa starts flagging benign cases: FPR jumps from 0.000 to 0.700, and to
  1.000 on RAG text. The classifier reads the spotlight delimiters themselves
  as an injection.
- **Different channels need different defenses.** The capability policy is
  the only stack that fully stops real tool misuse without a single false
  positive. On RAG text it barely helps (0.463 to 0.351), because no tool
  check can stop a canary from leaving in plain response text.
- **Susceptibility depends on the channel.** A model that resists injection
  through tool outputs can still be wide open through retrieved context.
  Mistral is the clearest example.

Full data lives in [`leaderboard.md`](leaderboard.md) (every row),
[`REPORT.md`](REPORT.md) (ablations, composition deltas, Pareto fronts), and
[`docs/findings.md`](docs/findings.md) (per-suite analysis).

## Architecture

![pi-bench architecture](docs/img/architecture.svg)

The design has two enforcement points. Detection runs on inputs and is best
effort, because detectors miss. The capability policy runs on outputs and
blocks side effects even when detection fails. The findings above show why
both matter: each one covers what the other misses.

## Metrics

| Metric | Definition |
| --- | --- |
| ASR | Attack success rate on attack cases: canary exfiltration, tool misuse, or a capability policy violation. |
| FPR | Rate of benign cases wrongly blocked. A defense that blocks everything scores ASR 0 at FPR 1. |
| p95 latency (ms) | 95th percentile of added latency across stack and model, per request. |
| $ / 1k requests | Mean cost of detector and model calls, cached by seed. |

Every CSV row pins the model version, defense versions, and seed. Rerunning
the same combination produces a byte-identical file.

## Components

- **Defenses (4):** `none` (baseline), `deberta-pi` (ProtectAI
  [DeBERTa-v3 classifier](https://huggingface.co/protectai/deberta-v3-base-prompt-injection-v2),
  cached on disk), `spotlight` (Hines-style delimiter wrapping of untrusted
  content, deterministic and free), and `capability-policy` (an allowlist for
  outgoing tool calls).
- **Models (6):** `mock` (deterministic and offline, so the harness runs with
  no GPU or keys), `openai-compat` (any OpenAI-compatible endpoint via
  `PIBENCH_OPENAI_BASE_URL` / `_MODEL` / `_API_KEY`; forwards per-case tool
  schemas and caches responses to disk), and four pinned tags served through
  Ollama by default: `qwen3-8b`, `llama3.1-8b`, `mistral-7b`, `qwen2.5-7b`.
- **Suites (4):** `injecagent-seed` (20 offline cases),
  `injecagent-full` / `-enhanced` (all 1,054
  [InjecAgent](https://github.com/uiuc-kang-lab/InjecAgent) attack cases
  plus ten benign probes, pinned to a commit SHA and cached; attack success
  includes attacker tool invocation),
  and `indirectrag-bench` (500 purpose-built RAG injection cases, 350 attack
  and 150 benign with a unique canary per case, published on the
  [Hugging Face Hub](https://huggingface.co/datasets/heisenberg-88/indirectrag-bench)).
- **Commands:** `pibench bench` runs one stack, model, and suite combination;
  `pibench leaderboard` regenerates `leaderboard.md`; `pibench report`
  regenerates `REPORT.md`. GPU rows reproduce via
  [`modal_run.py`](modal_run.py).

## Extending

A new stack, defense, model, or suite is a single file:

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
| --- | --- | --- |
| M1 | Vertical slice: one stack, one model, one suite | done |
| M2 | First real defense (ProtectAI DeBERTa v3) | done; ASR 1.000 to 0.000 |
| M3 | Full matrix: 4 models, 6 stacks, 3 suites; spotlighting and capability policy | done; 72 GPU rows on Modal A10Gs, see [`docs/findings.md`](docs/findings.md) |
| M4 | IndirectRAG-Bench, a 500-case dataset with a Hugging Face card | done; [published](https://huggingface.co/datasets/heisenberg-88/indirectrag-bench) |
| M5 | `REPORT.md` with composability ablations | done |
| M6 | Launch: blog and demo video | blog drafted, publishing soon; video pending |

Backlog: none open from the original plan. The `injecagent-full-enhanced`
rows for all four real models have landed; the per-suite tables and
composition deltas are in [`REPORT.md`](REPORT.md).

## Non-goals

- No new detectors or attack techniques. pi-bench wraps and grades what
  already exists.
- No SaaS, dashboard, or web app.
- No agent framework.

## License

[MIT](LICENSE).
