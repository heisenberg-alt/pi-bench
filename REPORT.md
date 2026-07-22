# pi-bench composability report

Auto-generated from `results/*.csv` via `pibench report`. 12 row(s).
All metrics: lower is better. Pareto-front rows are marked ★.

## mock × injecagent-full-enhanced

| Stack | n | ASR ↓ | FPR ↓ | p95 (ms) ↓ | $ / 1k ↓ | Pareto |
| ----- | -- | ----: | ----: | ---------: | -------: | :----: |
| `policy` | 1064 | 0.000 | 0.000 | 5.0 | $0.0000 | ★ |
| `deberta` | 1064 | 0.000 | 0.000 | 53.9 | $0.0000 |  |
| `spotlight-deberta-policy` | 1064 | 0.000 | 0.700 | 63.1 | $0.0000 |  |
| `spotlight-deberta` | 1064 | 0.000 | 0.700 | 63.1 | $0.0000 |  |
| `none` | 1064 | 1.000 | 0.000 | 5.0 | $0.0000 |  |
| `spotlight` | 1064 | 1.000 | 0.000 | 5.0 | $0.0000 |  |

### Composition deltas

| Composed | vs component | ΔASR | ΔFPR | Δp95 (ms) | Regression |
| -------- | ------------ | ---: | ---: | --------: | :--------: |
| `spotlight-deberta` | `deberta` | +0.000 | +0.700 | +9.2 | ⚠ |
| `spotlight-deberta` | `spotlight` | -1.000 | +0.700 | +58.1 | ⚠ |
| `spotlight-deberta-policy` | `deberta` | +0.000 | +0.700 | +9.2 | ⚠ |
| `spotlight-deberta-policy` | `policy` | +0.000 | +0.700 | +58.1 | ⚠ |
| `spotlight-deberta-policy` | `spotlight` | -1.000 | +0.700 | +58.1 | ⚠ |
| `spotlight-deberta-policy` | `spotlight-deberta` | +0.000 | +0.000 | +0.0 |  |

## mock × injecagent-seed

| Stack | n | ASR ↓ | FPR ↓ | p95 (ms) ↓ | $ / 1k ↓ | Pareto |
| ----- | -- | ----: | ----: | ---------: | -------: | :----: |
| `policy` | 20 | 0.000 | 0.000 | 5.0 | $0.0000 | ★ |
| `deberta` | 20 | 0.000 | 0.000 | 32.8 | $0.0000 |  |
| `spotlight-deberta-policy` | 20 | 0.000 | 0.700 | 40.3 | $0.0000 |  |
| `spotlight-deberta` | 20 | 0.000 | 0.700 | 40.3 | $0.0000 |  |
| `none` | 20 | 1.000 | 0.000 | 5.0 | $0.0000 |  |
| `spotlight` | 20 | 1.000 | 0.000 | 5.0 | $0.0000 |  |

### Composition deltas

| Composed | vs component | ΔASR | ΔFPR | Δp95 (ms) | Regression |
| -------- | ------------ | ---: | ---: | --------: | :--------: |
| `spotlight-deberta` | `deberta` | +0.000 | +0.700 | +7.5 | ⚠ |
| `spotlight-deberta` | `spotlight` | -1.000 | +0.700 | +35.3 | ⚠ |
| `spotlight-deberta-policy` | `deberta` | +0.000 | +0.700 | +7.5 | ⚠ |
| `spotlight-deberta-policy` | `policy` | +0.000 | +0.700 | +35.3 | ⚠ |
| `spotlight-deberta-policy` | `spotlight` | -1.000 | +0.700 | +35.3 | ⚠ |
| `spotlight-deberta-policy` | `spotlight-deberta` | +0.000 | +0.000 | +0.0 |  |
