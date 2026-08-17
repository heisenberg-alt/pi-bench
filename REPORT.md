# pi-bench composability report

Auto-generated from `results/*.csv` via `pibench report`. 114 row(s).
All metrics: lower is better. Pareto-front rows are marked with an asterisk.

## llama3.1-8b × indirectrag-bench

| Stack | n | ASR ↓ | FPR ↓ | p95 (ms) ↓ | $ / 1k ↓ | Pareto |
| ----- | -- | ----: | ----: | ---------: | -------: | :----: |
| `spotlight-deberta-policy` | 500 | 0.000 | 1.000 | 176.7 | $0.0000 | * |
| `spotlight-deberta` | 500 | 0.000 | 1.000 | 176.7 | $0.0000 | * |
| `deberta` | 500 | 0.066 | 0.087 | 1152.6 | $0.0000 | * |
| `policy` | 500 | 0.080 | 0.000 | 1115.1 | $0.0000 | * |
| `spotlight` | 500 | 0.097 | 0.000 | 1239.9 | $0.0000 |  |
| `none` | 500 | 0.186 | 0.000 | 1115.1 | $0.0000 |  |

### Composition deltas

| Composed | vs component | ΔASR | ΔFPR | Δp95 (ms) | Regression |
| -------- | ------------ | ---: | ---: | --------: | :--------: |
| `spotlight-deberta` | `deberta` | -0.066 | +0.913 | -975.8 | yes |
| `spotlight-deberta` | `spotlight` | -0.097 | +1.000 | -1063.2 | yes |
| `spotlight-deberta-policy` | `deberta` | -0.066 | +0.913 | -975.8 | yes |
| `spotlight-deberta-policy` | `policy` | -0.080 | +1.000 | -938.4 | yes |
| `spotlight-deberta-policy` | `spotlight` | -0.097 | +1.000 | -1063.2 | yes |
| `spotlight-deberta-policy` | `spotlight-deberta` | +0.000 | +0.000 | +0.0 |  |

## llama3.1-8b × injecagent-full

| Stack | n | ASR ↓ | FPR ↓ | p95 (ms) ↓ | $ / 1k ↓ | Pareto |
| ----- | -- | ----: | ----: | ---------: | -------: | :----: |
| `policy` | 1064 | 0.000 | 0.000 | 1157.5 | $0.0000 | * |
| `spotlight-deberta-policy` | 1064 | 0.000 | 0.700 | 219.4 | $0.0000 | * |
| `spotlight-deberta` | 1064 | 0.000 | 0.700 | 219.4 | $0.0000 | * |
| `deberta` | 1064 | 0.055 | 0.000 | 1043.8 | $0.0000 | * |
| `spotlight` | 1064 | 0.112 | 0.000 | 1062.8 | $0.0000 |  |
| `none` | 1064 | 0.117 | 0.000 | 1157.5 | $0.0000 |  |

### Composition deltas

| Composed | vs component | ΔASR | ΔFPR | Δp95 (ms) | Regression |
| -------- | ------------ | ---: | ---: | --------: | :--------: |
| `spotlight-deberta` | `deberta` | -0.055 | +0.700 | -824.4 | yes |
| `spotlight-deberta` | `spotlight` | -0.112 | +0.700 | -843.4 | yes |
| `spotlight-deberta-policy` | `deberta` | -0.055 | +0.700 | -824.4 | yes |
| `spotlight-deberta-policy` | `policy` | +0.000 | +0.700 | -938.1 | yes |
| `spotlight-deberta-policy` | `spotlight` | -0.112 | +0.700 | -843.4 | yes |
| `spotlight-deberta-policy` | `spotlight-deberta` | +0.000 | +0.000 | +0.0 |  |

## llama3.1-8b × injecagent-full-enhanced

| Stack | n | ASR ↓ | FPR ↓ | p95 (ms) ↓ | $ / 1k ↓ | Pareto |
| ----- | -- | ----: | ----: | ---------: | -------: | :----: |
| `deberta` | 1064 | 0.000 | 0.000 | 185.8 | $0.0000 | * |
| `policy` | 1064 | 0.000 | 0.000 | 1078.9 | $0.0000 |  |
| `spotlight-deberta-policy` | 1064 | 0.000 | 0.700 | 218.8 | $0.0000 |  |
| `spotlight-deberta` | 1064 | 0.000 | 0.700 | 218.8 | $0.0000 |  |
| `spotlight` | 1064 | 0.110 | 0.000 | 1291.2 | $0.0000 |  |
| `none` | 1064 | 0.117 | 0.000 | 1078.9 | $0.0000 |  |

### Composition deltas

| Composed | vs component | ΔASR | ΔFPR | Δp95 (ms) | Regression |
| -------- | ------------ | ---: | ---: | --------: | :--------: |
| `spotlight-deberta` | `deberta` | +0.000 | +0.700 | +32.9 | yes |
| `spotlight-deberta` | `spotlight` | -0.110 | +0.700 | -1072.4 | yes |
| `spotlight-deberta-policy` | `deberta` | +0.000 | +0.700 | +32.9 | yes |
| `spotlight-deberta-policy` | `policy` | +0.000 | +0.700 | -860.1 | yes |
| `spotlight-deberta-policy` | `spotlight` | -0.110 | +0.700 | -1072.4 | yes |
| `spotlight-deberta-policy` | `spotlight-deberta` | +0.000 | +0.000 | +0.0 |  |

## llama3.1-8b × injecagent-seed

| Stack | n | ASR ↓ | FPR ↓ | p95 (ms) ↓ | $ / 1k ↓ | Pareto |
| ----- | -- | ----: | ----: | ---------: | -------: | :----: |
| `deberta` | 20 | 0.000 | 0.000 | 766.0 | $0.0000 | * |
| `none` | 20 | 0.000 | 0.000 | 959.9 | $0.0000 |  |
| `policy` | 20 | 0.000 | 0.000 | 959.9 | $0.0000 |  |
| `spotlight` | 20 | 0.000 | 0.000 | 1070.1 | $0.0000 |  |
| `spotlight-deberta-policy` | 20 | 0.000 | 0.700 | 766.0 | $0.0000 |  |
| `spotlight-deberta` | 20 | 0.000 | 0.700 | 766.0 | $0.0000 |  |

### Composition deltas

| Composed | vs component | ΔASR | ΔFPR | Δp95 (ms) | Regression |
| -------- | ------------ | ---: | ---: | --------: | :--------: |
| `spotlight-deberta` | `deberta` | +0.000 | +0.700 | +0.0 | yes |
| `spotlight-deberta` | `spotlight` | +0.000 | +0.700 | -304.1 | yes |
| `spotlight-deberta-policy` | `deberta` | +0.000 | +0.700 | +0.0 | yes |
| `spotlight-deberta-policy` | `policy` | +0.000 | +0.700 | -193.9 | yes |
| `spotlight-deberta-policy` | `spotlight` | +0.000 | +0.700 | -304.1 | yes |
| `spotlight-deberta-policy` | `spotlight-deberta` | +0.000 | +0.000 | +0.0 |  |

## mistral-7b × indirectrag-bench

| Stack | n | ASR ↓ | FPR ↓ | p95 (ms) ↓ | $ / 1k ↓ | Pareto |
| ----- | -- | ----: | ----: | ---------: | -------: | :----: |
| `spotlight-deberta-policy` | 500 | 0.000 | 1.000 | 360.8 | $0.0000 | * |
| `spotlight-deberta` | 500 | 0.000 | 1.000 | 360.8 | $0.0000 | * |
| `deberta` | 500 | 0.260 | 0.087 | 2519.6 | $0.0000 | * |
| `spotlight` | 500 | 0.454 | 0.000 | 2134.8 | $0.0000 | * |
| `none` | 500 | 0.723 | 0.000 | 2620.6 | $0.0000 |  |
| `policy` | 500 | 0.723 | 0.000 | 2620.6 | $0.0000 |  |

### Composition deltas

| Composed | vs component | ΔASR | ΔFPR | Δp95 (ms) | Regression |
| -------- | ------------ | ---: | ---: | --------: | :--------: |
| `spotlight-deberta` | `deberta` | -0.260 | +0.913 | -2158.9 | yes |
| `spotlight-deberta` | `spotlight` | -0.454 | +1.000 | -1774.0 | yes |
| `spotlight-deberta-policy` | `deberta` | -0.260 | +0.913 | -2158.9 | yes |
| `spotlight-deberta-policy` | `policy` | -0.723 | +1.000 | -2259.8 | yes |
| `spotlight-deberta-policy` | `spotlight` | -0.454 | +1.000 | -1774.0 | yes |
| `spotlight-deberta-policy` | `spotlight-deberta` | +0.000 | +0.000 | +0.0 |  |

## mistral-7b × injecagent-full

| Stack | n | ASR ↓ | FPR ↓ | p95 (ms) ↓ | $ / 1k ↓ | Pareto |
| ----- | -- | ----: | ----: | ---------: | -------: | :----: |
| `deberta` | 1064 | 0.000 | 0.000 | 3753.8 | $0.0000 | * |
| `none` | 1064 | 0.000 | 0.000 | 4464.8 | $0.0000 |  |
| `policy` | 1064 | 0.000 | 0.000 | 4464.8 | $0.0000 |  |
| `spotlight` | 1064 | 0.000 | 0.000 | 4942.5 | $0.0000 |  |
| `spotlight-deberta-policy` | 1064 | 0.000 | 0.700 | 455.7 | $0.0000 | * |
| `spotlight-deberta` | 1064 | 0.000 | 0.700 | 455.7 | $0.0000 | * |

### Composition deltas

| Composed | vs component | ΔASR | ΔFPR | Δp95 (ms) | Regression |
| -------- | ------------ | ---: | ---: | --------: | :--------: |
| `spotlight-deberta` | `deberta` | +0.000 | +0.700 | -3298.1 | yes |
| `spotlight-deberta` | `spotlight` | +0.000 | +0.700 | -4486.8 | yes |
| `spotlight-deberta-policy` | `deberta` | +0.000 | +0.700 | -3298.1 | yes |
| `spotlight-deberta-policy` | `policy` | +0.000 | +0.700 | -4009.0 | yes |
| `spotlight-deberta-policy` | `spotlight` | +0.000 | +0.700 | -4486.8 | yes |
| `spotlight-deberta-policy` | `spotlight-deberta` | +0.000 | +0.000 | +0.0 |  |

## mistral-7b × injecagent-full-enhanced

| Stack | n | ASR ↓ | FPR ↓ | p95 (ms) ↓ | $ / 1k ↓ | Pareto |
| ----- | -- | ----: | ----: | ---------: | -------: | :----: |
| `deberta` | 1064 | 0.000 | 0.000 | 192.3 | $0.0000 | * |
| `none` | 1064 | 0.000 | 0.000 | 5000.3 | $0.0000 |  |
| `policy` | 1064 | 0.000 | 0.000 | 5000.3 | $0.0000 |  |
| `spotlight` | 1064 | 0.000 | 0.000 | 5871.7 | $0.0000 |  |
| `spotlight-deberta-policy` | 1064 | 0.000 | 0.700 | 207.2 | $0.0000 |  |
| `spotlight-deberta` | 1064 | 0.000 | 0.700 | 207.2 | $0.0000 |  |

### Composition deltas

| Composed | vs component | ΔASR | ΔFPR | Δp95 (ms) | Regression |
| -------- | ------------ | ---: | ---: | --------: | :--------: |
| `spotlight-deberta` | `deberta` | +0.000 | +0.700 | +14.9 | yes |
| `spotlight-deberta` | `spotlight` | +0.000 | +0.700 | -5664.5 | yes |
| `spotlight-deberta-policy` | `deberta` | +0.000 | +0.700 | +14.9 | yes |
| `spotlight-deberta-policy` | `policy` | +0.000 | +0.700 | -4793.0 | yes |
| `spotlight-deberta-policy` | `spotlight` | +0.000 | +0.700 | -5664.5 | yes |
| `spotlight-deberta-policy` | `spotlight-deberta` | +0.000 | +0.000 | +0.0 |  |

## mistral-7b × injecagent-seed

| Stack | n | ASR ↓ | FPR ↓ | p95 (ms) ↓ | $ / 1k ↓ | Pareto |
| ----- | -- | ----: | ----: | ---------: | -------: | :----: |
| `deberta` | 20 | 0.000 | 0.000 | 4965.8 | $0.0000 | * |
| `spotlight-deberta-policy` | 20 | 0.000 | 0.700 | 3230.7 | $0.0000 | * |
| `spotlight-deberta` | 20 | 0.000 | 0.700 | 3230.7 | $0.0000 | * |
| `spotlight` | 20 | 0.700 | 0.000 | 2758.2 | $0.0000 | * |
| `none` | 20 | 1.000 | 0.000 | 4939.4 | $0.0000 |  |
| `policy` | 20 | 1.000 | 0.000 | 4939.4 | $0.0000 |  |

### Composition deltas

| Composed | vs component | ΔASR | ΔFPR | Δp95 (ms) | Regression |
| -------- | ------------ | ---: | ---: | --------: | :--------: |
| `spotlight-deberta` | `deberta` | +0.000 | +0.700 | -1735.1 | yes |
| `spotlight-deberta` | `spotlight` | -0.700 | +0.700 | +472.5 | yes |
| `spotlight-deberta-policy` | `deberta` | +0.000 | +0.700 | -1735.1 | yes |
| `spotlight-deberta-policy` | `policy` | -1.000 | +0.700 | -1708.8 | yes |
| `spotlight-deberta-policy` | `spotlight` | -0.700 | +0.700 | +472.5 | yes |
| `spotlight-deberta-policy` | `spotlight-deberta` | +0.000 | +0.000 | +0.0 |  |

## mock × indirectrag-bench

| Stack | n | ASR ↓ | FPR ↓ | p95 (ms) ↓ | $ / 1k ↓ | Pareto |
| ----- | -- | ----: | ----: | ---------: | -------: | :----: |
| `policy` | 500 | 0.000 | 0.000 | 5.0 | $0.0000 | * |
| `spotlight-deberta-policy` | 500 | 0.000 | 1.000 | 48.3 | $0.0000 |  |
| `spotlight-deberta` | 500 | 0.000 | 1.000 | 48.3 | $0.0000 |  |
| `deberta` | 500 | 0.040 | 0.087 | 45.2 | $0.0000 |  |
| `none` | 500 | 0.234 | 0.000 | 5.0 | $0.0000 |  |
| `spotlight` | 500 | 0.234 | 0.000 | 5.0 | $0.0000 |  |

### Composition deltas

| Composed | vs component | ΔASR | ΔFPR | Δp95 (ms) | Regression |
| -------- | ------------ | ---: | ---: | --------: | :--------: |
| `spotlight-deberta` | `deberta` | -0.040 | +0.913 | +3.1 | yes |
| `spotlight-deberta` | `spotlight` | -0.234 | +1.000 | +43.3 | yes |
| `spotlight-deberta-policy` | `deberta` | -0.040 | +0.913 | +3.1 | yes |
| `spotlight-deberta-policy` | `policy` | +0.000 | +1.000 | +43.3 | yes |
| `spotlight-deberta-policy` | `spotlight` | -0.234 | +1.000 | +43.3 | yes |
| `spotlight-deberta-policy` | `spotlight-deberta` | +0.000 | +0.000 | +0.0 |  |

## mock × injecagent-full-enhanced

| Stack | n | ASR ↓ | FPR ↓ | p95 (ms) ↓ | $ / 1k ↓ | Pareto |
| ----- | -- | ----: | ----: | ---------: | -------: | :----: |
| `policy` | 1064 | 0.000 | 0.000 | 5.0 | $0.0000 | * |
| `deberta` | 1064 | 0.000 | 0.000 | 53.9 | $0.0000 |  |
| `spotlight-deberta-policy` | 1064 | 0.000 | 0.700 | 63.1 | $0.0000 |  |
| `spotlight-deberta` | 1064 | 0.000 | 0.700 | 63.1 | $0.0000 |  |
| `none` | 1064 | 1.000 | 0.000 | 5.0 | $0.0000 |  |
| `spotlight` | 1064 | 1.000 | 0.000 | 5.0 | $0.0000 |  |

### Composition deltas

| Composed | vs component | ΔASR | ΔFPR | Δp95 (ms) | Regression |
| -------- | ------------ | ---: | ---: | --------: | :--------: |
| `spotlight-deberta` | `deberta` | +0.000 | +0.700 | +9.2 | yes |
| `spotlight-deberta` | `spotlight` | -1.000 | +0.700 | +58.1 | yes |
| `spotlight-deberta-policy` | `deberta` | +0.000 | +0.700 | +9.2 | yes |
| `spotlight-deberta-policy` | `policy` | +0.000 | +0.700 | +58.1 | yes |
| `spotlight-deberta-policy` | `spotlight` | -1.000 | +0.700 | +58.1 | yes |
| `spotlight-deberta-policy` | `spotlight-deberta` | +0.000 | +0.000 | +0.0 |  |

## mock × injecagent-seed

| Stack | n | ASR ↓ | FPR ↓ | p95 (ms) ↓ | $ / 1k ↓ | Pareto |
| ----- | -- | ----: | ----: | ---------: | -------: | :----: |
| `policy` | 20 | 0.000 | 0.000 | 5.0 | $0.0000 | * |
| `deberta` | 20 | 0.000 | 0.000 | 32.8 | $0.0000 |  |
| `spotlight-deberta-policy` | 20 | 0.000 | 0.700 | 40.3 | $0.0000 |  |
| `spotlight-deberta` | 20 | 0.000 | 0.700 | 40.3 | $0.0000 |  |
| `none` | 20 | 1.000 | 0.000 | 5.0 | $0.0000 |  |
| `spotlight` | 20 | 1.000 | 0.000 | 5.0 | $0.0000 |  |

### Composition deltas

| Composed | vs component | ΔASR | ΔFPR | Δp95 (ms) | Regression |
| -------- | ------------ | ---: | ---: | --------: | :--------: |
| `spotlight-deberta` | `deberta` | +0.000 | +0.700 | +7.5 | yes |
| `spotlight-deberta` | `spotlight` | -1.000 | +0.700 | +35.3 | yes |
| `spotlight-deberta-policy` | `deberta` | +0.000 | +0.700 | +7.5 | yes |
| `spotlight-deberta-policy` | `policy` | +0.000 | +0.700 | +35.3 | yes |
| `spotlight-deberta-policy` | `spotlight` | -1.000 | +0.700 | +35.3 | yes |
| `spotlight-deberta-policy` | `spotlight-deberta` | +0.000 | +0.000 | +0.0 |  |

## qwen2.5-7b × indirectrag-bench

| Stack | n | ASR ↓ | FPR ↓ | p95 (ms) ↓ | $ / 1k ↓ | Pareto |
| ----- | -- | ----: | ----: | ---------: | -------: | :----: |
| `spotlight-deberta-policy` | 500 | 0.000 | 1.000 | 48.3 | $0.0000 | * |
| `spotlight-deberta` | 500 | 0.000 | 1.000 | 48.3 | $0.0000 | * |
| `deberta` | 500 | 0.100 | 0.087 | 3535.2 | $0.0000 | * |
| `policy` | 500 | 0.351 | 0.000 | 4349.0 | $0.0000 | * |
| `spotlight` | 500 | 0.363 | 0.000 | 4295.3 | $0.0000 | * |
| `none` | 500 | 0.463 | 0.000 | 4349.0 | $0.0000 |  |

### Composition deltas

| Composed | vs component | ΔASR | ΔFPR | Δp95 (ms) | Regression |
| -------- | ------------ | ---: | ---: | --------: | :--------: |
| `spotlight-deberta` | `deberta` | -0.100 | +0.913 | -3486.9 | yes |
| `spotlight-deberta` | `spotlight` | -0.363 | +1.000 | -4247.0 | yes |
| `spotlight-deberta-policy` | `deberta` | -0.100 | +0.913 | -3486.9 | yes |
| `spotlight-deberta-policy` | `policy` | -0.351 | +1.000 | -4300.7 | yes |
| `spotlight-deberta-policy` | `spotlight` | -0.363 | +1.000 | -4247.0 | yes |
| `spotlight-deberta-policy` | `spotlight-deberta` | +0.000 | +0.000 | +0.0 |  |

## qwen2.5-7b × injecagent-full

| Stack | n | ASR ↓ | FPR ↓ | p95 (ms) ↓ | $ / 1k ↓ | Pareto |
| ----- | -- | ----: | ----: | ---------: | -------: | :----: |
| `policy` | 1064 | 0.000 | 0.000 | 5635.3 | $0.0000 | * |
| `spotlight-deberta-policy` | 1064 | 0.000 | 0.700 | 59.3 | $0.0000 | * |
| `spotlight-deberta` | 1064 | 0.000 | 0.700 | 59.3 | $0.0000 | * |
| `deberta` | 1064 | 0.074 | 0.000 | 4580.2 | $0.0000 | * |
| `spotlight` | 1064 | 0.105 | 0.000 | 5870.1 | $0.0000 |  |
| `none` | 1064 | 0.146 | 0.000 | 5635.3 | $0.0000 |  |

### Composition deltas

| Composed | vs component | ΔASR | ΔFPR | Δp95 (ms) | Regression |
| -------- | ------------ | ---: | ---: | --------: | :--------: |
| `spotlight-deberta` | `deberta` | -0.074 | +0.700 | -4520.9 | yes |
| `spotlight-deberta` | `spotlight` | -0.105 | +0.700 | -5810.8 | yes |
| `spotlight-deberta-policy` | `deberta` | -0.074 | +0.700 | -4520.9 | yes |
| `spotlight-deberta-policy` | `policy` | +0.000 | +0.700 | -5576.1 | yes |
| `spotlight-deberta-policy` | `spotlight` | -0.105 | +0.700 | -5810.8 | yes |
| `spotlight-deberta-policy` | `spotlight-deberta` | +0.000 | +0.000 | +0.0 |  |

## qwen2.5-7b × injecagent-full-enhanced

| Stack | n | ASR ↓ | FPR ↓ | p95 (ms) ↓ | $ / 1k ↓ | Pareto |
| ----- | -- | ----: | ----: | ---------: | -------: | :----: |
| `deberta` | 1064 | 0.000 | 0.000 | 175.7 | $0.0000 | * |
| `policy` | 1064 | 0.000 | 0.000 | 2667.2 | $0.0000 |  |
| `spotlight-deberta-policy` | 1064 | 0.000 | 0.700 | 221.6 | $0.0000 |  |
| `spotlight-deberta` | 1064 | 0.000 | 0.700 | 221.6 | $0.0000 |  |
| `spotlight` | 1064 | 0.114 | 0.000 | 2975.8 | $0.0000 |  |
| `none` | 1064 | 0.157 | 0.000 | 2667.2 | $0.0000 |  |

### Composition deltas

| Composed | vs component | ΔASR | ΔFPR | Δp95 (ms) | Regression |
| -------- | ------------ | ---: | ---: | --------: | :--------: |
| `spotlight-deberta` | `deberta` | +0.000 | +0.700 | +45.9 | yes |
| `spotlight-deberta` | `spotlight` | -0.114 | +0.700 | -2754.2 | yes |
| `spotlight-deberta-policy` | `deberta` | +0.000 | +0.700 | +45.9 | yes |
| `spotlight-deberta-policy` | `policy` | +0.000 | +0.700 | -2445.6 | yes |
| `spotlight-deberta-policy` | `spotlight` | -0.114 | +0.700 | -2754.2 | yes |
| `spotlight-deberta-policy` | `spotlight-deberta` | +0.000 | +0.000 | +0.0 |  |

## qwen2.5-7b × injecagent-seed

| Stack | n | ASR ↓ | FPR ↓ | p95 (ms) ↓ | $ / 1k ↓ | Pareto |
| ----- | -- | ----: | ----: | ---------: | -------: | :----: |
| `deberta` | 20 | 0.000 | 0.000 | 1824.9 | $0.0000 | * |
| `spotlight-deberta-policy` | 20 | 0.000 | 0.700 | 1824.9 | $0.0000 |  |
| `spotlight-deberta` | 20 | 0.000 | 0.700 | 1824.9 | $0.0000 |  |
| `none` | 20 | 0.300 | 0.000 | 1824.9 | $0.0000 |  |
| `policy` | 20 | 0.300 | 0.000 | 1824.9 | $0.0000 |  |
| `spotlight` | 20 | 0.300 | 0.000 | 2092.5 | $0.0000 |  |

### Composition deltas

| Composed | vs component | ΔASR | ΔFPR | Δp95 (ms) | Regression |
| -------- | ------------ | ---: | ---: | --------: | :--------: |
| `spotlight-deberta` | `deberta` | +0.000 | +0.700 | +0.0 | yes |
| `spotlight-deberta` | `spotlight` | -0.300 | +0.700 | -267.7 | yes |
| `spotlight-deberta-policy` | `deberta` | +0.000 | +0.700 | +0.0 | yes |
| `spotlight-deberta-policy` | `policy` | -0.300 | +0.700 | +0.0 | yes |
| `spotlight-deberta-policy` | `spotlight` | -0.300 | +0.700 | -267.7 | yes |
| `spotlight-deberta-policy` | `spotlight-deberta` | +0.000 | +0.000 | +0.0 |  |

## qwen3-8b × indirectrag-bench

| Stack | n | ASR ↓ | FPR ↓ | p95 (ms) ↓ | $ / 1k ↓ | Pareto |
| ----- | -- | ----: | ----: | ---------: | -------: | :----: |
| `spotlight-deberta-policy` | 500 | 0.000 | 1.000 | 154.2 | $0.0000 | * |
| `spotlight-deberta` | 500 | 0.000 | 1.000 | 154.2 | $0.0000 | * |
| `deberta` | 500 | 0.097 | 0.087 | 7006.6 | $0.0000 | * |
| `spotlight` | 500 | 0.160 | 0.000 | 6914.0 | $0.0000 | * |
| `policy` | 500 | 0.286 | 0.000 | 6961.6 | $0.0000 |  |
| `none` | 500 | 0.297 | 0.000 | 6961.6 | $0.0000 |  |

### Composition deltas

| Composed | vs component | ΔASR | ΔFPR | Δp95 (ms) | Regression |
| -------- | ------------ | ---: | ---: | --------: | :--------: |
| `spotlight-deberta` | `deberta` | -0.097 | +0.913 | -6852.4 | yes |
| `spotlight-deberta` | `spotlight` | -0.160 | +1.000 | -6759.8 | yes |
| `spotlight-deberta-policy` | `deberta` | -0.097 | +0.913 | -6852.4 | yes |
| `spotlight-deberta-policy` | `policy` | -0.286 | +1.000 | -6807.4 | yes |
| `spotlight-deberta-policy` | `spotlight` | -0.160 | +1.000 | -6759.8 | yes |
| `spotlight-deberta-policy` | `spotlight-deberta` | +0.000 | +0.000 | +0.0 |  |

## qwen3-8b × injecagent-full

| Stack | n | ASR ↓ | FPR ↓ | p95 (ms) ↓ | $ / 1k ↓ | Pareto |
| ----- | -- | ----: | ----: | ---------: | -------: | :----: |
| `policy` | 1064 | 0.000 | 0.000 | 7014.1 | $0.0000 | * |
| `spotlight-deberta-policy` | 1064 | 0.000 | 0.700 | 551.1 | $0.0000 | * |
| `spotlight-deberta` | 1064 | 0.000 | 0.700 | 551.1 | $0.0000 | * |
| `spotlight` | 1064 | 0.006 | 0.000 | 7030.9 | $0.0000 |  |
| `deberta` | 1064 | 0.006 | 0.000 | 7272.2 | $0.0000 |  |
| `none` | 1064 | 0.022 | 0.000 | 7014.1 | $0.0000 |  |

### Composition deltas

| Composed | vs component | ΔASR | ΔFPR | Δp95 (ms) | Regression |
| -------- | ------------ | ---: | ---: | --------: | :--------: |
| `spotlight-deberta` | `deberta` | -0.006 | +0.700 | -6721.1 | yes |
| `spotlight-deberta` | `spotlight` | -0.006 | +0.700 | -6479.8 | yes |
| `spotlight-deberta-policy` | `deberta` | -0.006 | +0.700 | -6721.1 | yes |
| `spotlight-deberta-policy` | `policy` | +0.000 | +0.700 | -6463.1 | yes |
| `spotlight-deberta-policy` | `spotlight` | -0.006 | +0.700 | -6479.8 | yes |
| `spotlight-deberta-policy` | `spotlight-deberta` | +0.000 | +0.000 | +0.0 |  |

## qwen3-8b × injecagent-full-enhanced

| Stack | n | ASR ↓ | FPR ↓ | p95 (ms) ↓ | $ / 1k ↓ | Pareto |
| ----- | -- | ----: | ----: | ---------: | -------: | :----: |
| `deberta` | 1064 | 0.000 | 0.000 | 197.3 | $0.0000 | * |
| `policy` | 1064 | 0.000 | 0.000 | 7079.9 | $0.0000 |  |
| `spotlight-deberta-policy` | 1064 | 0.000 | 0.700 | 244.1 | $0.0000 |  |
| `spotlight-deberta` | 1064 | 0.000 | 0.700 | 244.1 | $0.0000 |  |
| `spotlight` | 1064 | 0.004 | 0.000 | 7105.9 | $0.0000 |  |
| `none` | 1064 | 0.046 | 0.000 | 7079.9 | $0.0000 |  |

### Composition deltas

| Composed | vs component | ΔASR | ΔFPR | Δp95 (ms) | Regression |
| -------- | ------------ | ---: | ---: | --------: | :--------: |
| `spotlight-deberta` | `deberta` | +0.000 | +0.700 | +46.8 | yes |
| `spotlight-deberta` | `spotlight` | -0.004 | +0.700 | -6861.7 | yes |
| `spotlight-deberta-policy` | `deberta` | +0.000 | +0.700 | +46.8 | yes |
| `spotlight-deberta-policy` | `policy` | +0.000 | +0.700 | -6835.8 | yes |
| `spotlight-deberta-policy` | `spotlight` | -0.004 | +0.700 | -6861.7 | yes |
| `spotlight-deberta-policy` | `spotlight-deberta` | +0.000 | +0.000 | +0.0 |  |

## qwen3-8b × injecagent-seed

| Stack | n | ASR ↓ | FPR ↓ | p95 (ms) ↓ | $ / 1k ↓ | Pareto |
| ----- | -- | ----: | ----: | ---------: | -------: | :----: |
| `deberta` | 20 | 0.000 | 0.000 | 8821.0 | $0.0000 | * |
| `spotlight-deberta-policy` | 20 | 0.000 | 0.700 | 5480.3 | $0.0000 | * |
| `spotlight-deberta` | 20 | 0.000 | 0.700 | 5480.3 | $0.0000 | * |
| `spotlight` | 20 | 0.400 | 0.000 | 11969.9 | $0.0000 |  |
| `none` | 20 | 0.500 | 0.000 | 12236.4 | $0.0000 |  |
| `policy` | 20 | 0.500 | 0.000 | 12236.4 | $0.0000 |  |

### Composition deltas

| Composed | vs component | ΔASR | ΔFPR | Δp95 (ms) | Regression |
| -------- | ------------ | ---: | ---: | --------: | :--------: |
| `spotlight-deberta` | `deberta` | +0.000 | +0.700 | -3340.7 | yes |
| `spotlight-deberta` | `spotlight` | -0.400 | +0.700 | -6489.5 | yes |
| `spotlight-deberta-policy` | `deberta` | +0.000 | +0.700 | -3340.7 | yes |
| `spotlight-deberta-policy` | `policy` | -0.500 | +0.700 | -6756.1 | yes |
| `spotlight-deberta-policy` | `spotlight` | -0.400 | +0.700 | -6489.5 | yes |
| `spotlight-deberta-policy` | `spotlight-deberta` | +0.000 | +0.000 | +0.0 |  |
