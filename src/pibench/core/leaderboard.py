"""Read committed result CSVs and emit ``leaderboard.md`` — a single
sorted table of every (stack, model, suite, seed) row on disk."""

from __future__ import annotations

import csv
from pathlib import Path

_HEADER = "| Stack | Model | Suite | Seed | n | ASR ↓ | FPR ↓ | p95 (ms) ↓ | $ / 1k ↓ |"
_DIV = "| ----- | ----- | ----- | ---- | -- | ----: | ----: | ---------: | -------: |"


def build_leaderboard(results_dir: Path, out_path: Path) -> str:
    rows = [_aggregate(p) for p in sorted(results_dir.glob("*.csv")) if p.stat().st_size > 0]
    rows.sort(key=lambda r: (r["asr"], r["fpr"], r["p95_ms"], r["usd_per_1k"]))

    lines = [
        "# pi-bench leaderboard",
        "",
        f"Auto-generated from `results/*.csv`. Sorted by ASR ↓ then FPR ↓. "
        f"{len(rows)} row(s).",
        "",
        _HEADER,
        _DIV,
    ]
    for r in rows:
        lines.append(
            f"| `{r['stack']}` | `{r['model']}` | `{r['suite']}` | {r['seed']} | "
            f"{r['n']} | {r['asr']:.3f} | {r['fpr']:.3f} | "
            f"{r['p95_ms']:.1f} | ${r['usd_per_1k']:.4f} |"
        )
    content = "\n".join(lines) + "\n"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding="utf-8")
    return content


def _aggregate(csv_path: Path) -> dict:
    with csv_path.open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))

    attacks = [r for r in rows if r["category"] == "attack"]
    benigns = [r for r in rows if r["category"] == "benign"]
    latencies = [float(r["total_latency_ms"]) for r in rows]
    costs = [float(r["total_cost_usd"]) for r in rows]

    asr = _rate(_truthy(r["attack_succeeded"]) for r in attacks)
    fpr = _rate(_truthy(r["blocked_by_defense"]) for r in benigns)
    n = len(rows)

    return {
        "stack": rows[0]["stack"] if rows else csv_path.stem,
        "model": rows[0]["model"] if rows else "",
        "suite": rows[0]["suite"] if rows else "",
        "seed": rows[0]["seed"] if rows else "",
        "n": n,
        "asr": asr,
        "fpr": fpr,
        "p95_ms": _pct(latencies, 95),
        "usd_per_1k": 1000.0 * (sum(costs) / max(n, 1)),
    }


def _truthy(x: str) -> bool:
    return x.strip().lower() in {"true", "1", "yes"}


def _rate(xs) -> float:
    xs = list(xs)
    return sum(xs) / len(xs) if xs else 0.0


def _pct(xs: list[float], p: int) -> float:
    if not xs:
        return 0.0
    xs = sorted(xs)
    k = max(0, min(len(xs) - 1, int(round((p / 100.0) * (len(xs) - 1)))))
    return xs[k]
