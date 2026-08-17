# Findings: detailed results and analysis

Companion to the [README](../README.md) results summary. All numbers are
seed-42 rows regenerated from `results/*.csv`; the full grid lives in
[`leaderboard.md`](../leaderboard.md) and the ablation and Pareto view in
[`REPORT.md`](../REPORT.md).

## Seed suite: cross-model matrix (20 cases)

The four open-weight models run locally through Ollama on the seed suite,
shown as ASR per stack:

| Model | `none` | `deberta` | `spotlight` | `spotlight-deberta` | `policy` | `spotlight-deberta-policy` |
| ----- | ----: | ----: | ----: | ----: | ----: | ----: |
| `mistral-7b` | 1.000 | 0.000 | 0.700 | 0.000 | 1.000 | 0.000 |
| `qwen3-8b` | 0.500 | 0.000 | 0.400 | 0.000 | 0.500 | 0.000 |
| `qwen2.5-7b` | 0.300 | 0.000 | 0.300 | 0.000 | 0.300 | 0.000 |
| `llama3.1-8b` | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |

Every `spotlight-deberta` and `spotlight-deberta-policy` cell carries FPR
0.700 on the benign cases. That is the composition regression, reproduced on
all four models.

Naive susceptibility spans the whole range: `mistral-7b` follows every seed
injection (1.000), `qwen3-8b` half (0.500), `qwen2.5-7b` a third (0.300),
and `llama3.1-8b` resists all ten (0.000). DeBERTa collapses ASR to 0.000
for every model, so the detector's value holds across model families, not
just the mock.

## Full suite: real tool misuse (`qwen2.5-7b`, `injecagent-full`, 1,054 cases)

| Stack | ASR | FPR | p95 (ms) |
| ----- | ----: | ----: | ---------: |
| `none` | 0.146 | 0.000 | 5635.3 |
| `spotlight` | 0.105 | 0.000 | 5870.1 |
| `deberta` | 0.074 | 0.000 | 4580.2 |
| `spotlight-deberta` | 0.000 | 0.700 | 59.3 |
| `spotlight-deberta-policy` | 0.000 | 0.700 | 59.3 |
| `policy` | **0.000** | **0.000** | 5635.3 |

Unlike the seed suite, these cases carry attacker tools, so the model can
actually misuse them. Undefended, `qwen2.5-7b` invokes the attacker tool on
14.6% of the 1,054 cases. `deberta` catches about half at the input (0.074),
and the `spotlight-deberta` stacks reach ASR 0.000 only by paying FPR 0.700.
Only `policy` reaches the ASR 0.000 / FPR 0.000 corner: it blocks every
out-of-policy tool call at the output while passing every benign one. The
`spotlight-deberta` p95 collapses to roughly 59 ms because DeBERTa blocks
most cases at the input, before the model is ever called.

## IndirectRAG-Bench: retrieval-context injection (`qwen2.5-7b`, 500 cases)

| Stack | ASR | FPR | p95 (ms) |
| ----- | ----: | ----: | ---------: |
| `none` | 0.463 | 0.000 | 4349.0 |
| `spotlight` | 0.363 | 0.000 | 4295.3 |
| `policy` | 0.351 | 0.000 | 4349.0 |
| `deberta` | 0.100 | 0.087 | 3535.2 |
| `spotlight-deberta` | 0.000 | 1.000 | 48.3 |
| `spotlight-deberta-policy` | 0.000 | 1.000 | 48.3 |

[`indirectrag-bench`](https://huggingface.co/datasets/heisenberg-88/indirectrag-bench)
poisons the retrieved context instead of a tool output, and that flips the
story. `qwen2.5-7b` follows 46.3% of RAG injections, roughly three times its
InjecAgent tool-misuse rate (0.146). `policy` barely helps here (0.463 to
0.351): it guards the tool channel, but most RAG attacks exfiltrate a canary
through response text, which no output tool check can catch. `deberta` cuts
ASR to 0.100 at the cost of false-positives on 8.7% of benign passages, and
`spotlight-deberta` reaches ASR 0.000 only at FPR 1.000; the delimiter and
classifier regression is total on RAG text. On retrieval injection, no
single defense is both safe and usable. That frontier is exactly what a
composed-defense benchmark exists to expose.

## Composition finding

`spotlight-deberta` catches the same attacks as `deberta` alone but jumps
FPR from 0.000 to 0.700, reproduced across all four open-weight models and
the mock, on both the 20-case seed suite and the full 1,054-case InjecAgent
suite (and to FPR 1.000 on RAG text). The spotlight delimiters look
injection-like to a PI classifier that never saw them in training. This is
the kind of second-order failure the composed-defense framing is designed to
surface.

## Output-side finding

The two-enforcement-point thesis holds on real data. Input detection is
best-effort (`deberta` still lets 0.074 through on the full suite), but the
output-side capability policy closes the tool channel regardless of what
detection misses. It only acts on tool calls, so on the text-based seed
suite it is a no-op and matches `none`; the full suite is where it earns its
place.

## The mistral-7b caveat

`mistral-7b` emits essentially no tool calls through the tools API (1 in
3,123 responses), so its InjecAgent ASR of 0.000 reflects non-engagement
with the tool channel rather than robustness. The same model is the most
injectable through retrieved context (0.723 undefended). Susceptibility is
channel-specific: a model's rank on one injection surface does not predict
its rank on another.

## Detector details

The `deberta` stack wraps ProtectAI's
[`deberta-v3-base-prompt-injection-v2`](https://huggingface.co/protectai/deberta-v3-base-prompt-injection-v2)
classifier (ungated, roughly 184M parameters, CPU-inference friendly).
Against every model on the seed suite it eliminates every attack (ASR 0.000)
with zero false positives and about 30 ms of added p95 latency on the mock
(about 55 ms on the full suite's longer tool responses; the one-time model
load is excluded via a warm-up inference).
