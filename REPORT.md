# pi-bench composability report

Auto-generated from `results/*.csv` via `pibench report`. 42 row(s).
All metrics: lower is better. Pareto-front rows are marked ★.

## llama3.1-8b × injecagent-seed

| Stack | n | ASR ↓ | FPR ↓ | p95 (ms) ↓ | $ / 1k ↓ | Pareto |
| ----- | -- | ----: | ----: | ---------: | -------: | :----: |
| `deberta` | 20 | 0.000 | 0.000 | 766.0 | $0.0000 | ★ |
| `none` | 20 | 0.000 | 0.000 | 959.9 | $0.0000 |  |
| `policy` | 20 | 0.000 | 0.000 | 959.9 | $0.0000 |  |
| `spotlight` | 20 | 0.000 | 0.000 | 1070.1 | $0.0000 |  |
| `spotlight-deberta-policy` | 20 | 0.000 | 0.700 | 766.0 | $0.0000 |  |
| `spotlight-deberta` | 20 | 0.000 | 0.700 | 766.0 | $0.0000 |  |

### Composition deltas

| Composed | vs component | ΔASR | ΔFPR | Δp95 (ms) | Regression |
| -------- | ------------ | ---: | ---: | --------: | :--------: |
| `spotlight-deberta` | `deberta` | +0.000 | +0.700 | +0.0 | ⚠ |
| `spotlight-deberta` | `spotlight` | +0.000 | +0.700 | -304.1 | ⚠ |
| `spotlight-deberta-policy` | `deberta` | +0.000 | +0.700 | +0.0 | ⚠ |
| `spotlight-deberta-policy` | `policy` | +0.000 | +0.700 | -193.9 | ⚠ |
| `spotlight-deberta-policy` | `spotlight` | +0.000 | +0.700 | -304.1 | ⚠ |
| `spotlight-deberta-policy` | `spotlight-deberta` | +0.000 | +0.000 | +0.0 |  |

## mistral-7b × injecagent-seed

| Stack | n | ASR ↓ | FPR ↓ | p95 (ms) ↓ | $ / 1k ↓ | Pareto |
| ----- | -- | ----: | ----: | ---------: | -------: | :----: |
| `deberta` | 20 | 0.000 | 0.000 | 4965.8 | $0.0000 | ★ |
| `spotlight-deberta-policy` | 20 | 0.000 | 0.700 | 3230.7 | $0.0000 | ★ |
| `spotlight-deberta` | 20 | 0.000 | 0.700 | 3230.7 | $0.0000 | ★ |
| `spotlight` | 20 | 0.700 | 0.000 | 2758.2 | $0.0000 | ★ |
| `none` | 20 | 1.000 | 0.000 | 4939.4 | $0.0000 |  |
| `policy` | 20 | 1.000 | 0.000 | 4939.4 | $0.0000 |  |

### Composition deltas

| Composed | vs component | ΔASR | ΔFPR | Δp95 (ms) | Regression |
| -------- | ------------ | ---: | ---: | --------: | :--------: |
| `spotlight-deberta` | `deberta` | +0.000 | +0.700 | -1735.1 | ⚠ |
| `spotlight-deberta` | `spotlight` | -0.700 | +0.700 | +472.5 | ⚠ |
| `spotlight-deberta-policy` | `deberta` | +0.000 | +0.700 | -1735.1 | ⚠ |
| `spotlight-deberta-policy` | `policy` | -1.000 | +0.700 | -1708.8 | ⚠ |
| `spotlight-deberta-policy` | `spotlight` | -0.700 | +0.700 | +472.5 | ⚠ |
| `spotlight-deberta-policy` | `spotlight-deberta` | +0.000 | +0.000 | +0.0 |  |

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

## qwen2.5-7b × injecagent-full

| Stack | n | ASR ↓ | FPR ↓ | p95 (ms) ↓ | $ / 1k ↓ | Pareto |
| ----- | -- | ----: | ----: | ---------: | -------: | :----: |
| `policy` | 1064 | 0.000 | 0.000 | 5635.3 | $0.0000 | ★ |
| `spotlight-deberta-policy` | 1064 | 0.000 | 0.700 | 59.3 | $0.0000 | ★ |
| `spotlight-deberta` | 1064 | 0.000 | 0.700 | 59.3 | $0.0000 | ★ |
| `deberta` | 1064 | 0.074 | 0.000 | 4580.2 | $0.0000 | ★ |
| `spotlight` | 1064 | 0.105 | 0.000 | 5870.1 | $0.0000 |  |
| `none` | 1064 | 0.146 | 0.000 | 5635.3 | $0.0000 |  |

### Composition deltas

| Composed | vs component | ΔASR | ΔFPR | Δp95 (ms) | Regression |
| -------- | ------------ | ---: | ---: | --------: | :--------: |
| `spotlight-deberta` | `deberta` | -0.074 | +0.700 | -4520.9 | ⚠ |
| `spotlight-deberta` | `spotlight` | -0.105 | +0.700 | -5810.8 | ⚠ |
| `spotlight-deberta-policy` | `deberta` | -0.074 | +0.700 | -4520.9 | ⚠ |
| `spotlight-deberta-policy` | `policy` | +0.000 | +0.700 | -5576.1 | ⚠ |
| `spotlight-deberta-policy` | `spotlight` | -0.105 | +0.700 | -5810.8 | ⚠ |
| `spotlight-deberta-policy` | `spotlight-deberta` | +0.000 | +0.000 | +0.0 |  |

## qwen2.5-7b × injecagent-seed

| Stack | n | ASR ↓ | FPR ↓ | p95 (ms) ↓ | $ / 1k ↓ | Pareto |
| ----- | -- | ----: | ----: | ---------: | -------: | :----: |
| `deberta` | 20 | 0.000 | 0.000 | 1824.9 | $0.0000 | ★ |
| `spotlight-deberta-policy` | 20 | 0.000 | 0.700 | 1824.9 | $0.0000 |  |
| `spotlight-deberta` | 20 | 0.000 | 0.700 | 1824.9 | $0.0000 |  |
| `none` | 20 | 0.300 | 0.000 | 1824.9 | $0.0000 |  |
| `policy` | 20 | 0.300 | 0.000 | 1824.9 | $0.0000 |  |
| `spotlight` | 20 | 0.300 | 0.000 | 2092.5 | $0.0000 |  |

### Composition deltas

| Composed | vs component | ΔASR | ΔFPR | Δp95 (ms) | Regression |
| -------- | ------------ | ---: | ---: | --------: | :--------: |
| `spotlight-deberta` | `deberta` | +0.000 | +0.700 | +0.0 | ⚠ |
| `spotlight-deberta` | `spotlight` | -0.300 | +0.700 | -267.7 | ⚠ |
| `spotlight-deberta-policy` | `deberta` | +0.000 | +0.700 | +0.0 | ⚠ |
| `spotlight-deberta-policy` | `policy` | -0.300 | +0.700 | +0.0 | ⚠ |
| `spotlight-deberta-policy` | `spotlight` | -0.300 | +0.700 | -267.7 | ⚠ |
| `spotlight-deberta-policy` | `spotlight-deberta` | +0.000 | +0.000 | +0.0 |  |

## qwen3-8b × injecagent-seed

| Stack | n | ASR ↓ | FPR ↓ | p95 (ms) ↓ | $ / 1k ↓ | Pareto |
| ----- | -- | ----: | ----: | ---------: | -------: | :----: |
| `deberta` | 20 | 0.000 | 0.000 | 8821.0 | $0.0000 | ★ |
| `spotlight-deberta-policy` | 20 | 0.000 | 0.700 | 5480.3 | $0.0000 | ★ |
| `spotlight-deberta` | 20 | 0.000 | 0.700 | 5480.3 | $0.0000 | ★ |
| `spotlight` | 20 | 0.400 | 0.000 | 11969.9 | $0.0000 |  |
| `none` | 20 | 0.500 | 0.000 | 12236.4 | $0.0000 |  |
| `policy` | 20 | 0.500 | 0.000 | 12236.4 | $0.0000 |  |

### Composition deltas

| Composed | vs component | ΔASR | ΔFPR | Δp95 (ms) | Regression |
| -------- | ------------ | ---: | ---: | --------: | :--------: |
| `spotlight-deberta` | `deberta` | +0.000 | +0.700 | -3340.7 | ⚠ |
| `spotlight-deberta` | `spotlight` | -0.400 | +0.700 | -6489.5 | ⚠ |
| `spotlight-deberta-policy` | `deberta` | +0.000 | +0.700 | -3340.7 | ⚠ |
| `spotlight-deberta-policy` | `policy` | -0.500 | +0.700 | -6756.1 | ⚠ |
| `spotlight-deberta-policy` | `spotlight` | -0.400 | +0.700 | -6489.5 | ⚠ |
| `spotlight-deberta-policy` | `spotlight-deberta` | +0.000 | +0.000 | +0.0 |  |
