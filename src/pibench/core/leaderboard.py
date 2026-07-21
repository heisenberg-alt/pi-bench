"""Read committed result CSVs and emit ``leaderboard.md`` — a single
sorted table of every (stack, model, suite, seed) row on disk."""

from __future__ import annotations

import csv
from pathlib import Path

from pibench.core.stats import CaseStats, headline_metrics

_HEADER = "| Stack | Model | Suite | Seed | n | ASR ↓ | FPR ↓ | p95 (ms) ↓ | $ / 1k ↓ |"
_DIV = "| ----- | ----- | ----- | ---- | -- | ----: | ----: | ---------: | -------: |"


def build_leaderboard(results_dir: Path, out_path: Path) -> str:
    rows = [
        agg for p in sorted(results_dir.glob("*.csv")) if (agg := _aggregate(p)) is not None
    ]
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


def _aggregate(csv_path: Path) -> dict | None:
    """Aggregate one result CSV into a leaderboard row, or ``None`` when the
    file is empty / header-only."""
    with csv_path.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))

    if not rows:
        return None

    cases = [
        CaseStats(
            category=r["category"],
            blocked=_truthy(r["blocked_by_defense"]),
            attack_succeeded=_truthy(r["attack_succeeded"]),
            latency_ms=float(r["total_latency_ms"]),
            cost_usd=float(r["total_cost_usd"]),
        )
        for r in rows
    ]
    head = rows[0]

    return {
        "stack": head["stack"],
        "model": head["model"],
        "suite": head["suite"],
        "seed": head["seed"],
        **headline_metrics(cases),
    }


def _truthy(x: str) -> bool:
    return x.strip().lower() in {"true", "1", "yes"}
