from __future__ import annotations

import csv
from collections.abc import Iterable
from pathlib import Path

from pibench.core.types import RunResult


def summarize(results: list[RunResult]) -> dict:
    """Compute the four-column headline metrics for one (stack, model, suite)
    row: ASR (on attacks), FPR (on benigns), p95 latency, and mean $/1k."""
    attacks = [r for r in results if r.category == "attack"]
    benigns = [r for r in results if r.category == "benign"]

    asr = _rate([bool(r.attack_succeeded) for r in attacks])
    fpr = _rate([r.blocked_by_defense for r in benigns])
    latencies = [r.total_latency_ms for r in results]
    p50 = _pct(latencies, 50)
    p95 = _pct(latencies, 95)
    mean_cost_per_1k = 1000.0 * (sum(r.total_cost_usd for r in results) / max(len(results), 1))

    return {
        "n_attack": len(attacks),
        "n_benign": len(benigns),
        "asr": asr,
        "fpr": fpr,
        "p50_ms": p50,
        "p95_ms": p95,
        "usd_per_1k": mean_cost_per_1k,
    }


def _rate(bools: Iterable[bool]) -> float:
    xs = list(bools)
    return sum(xs) / len(xs) if xs else 0.0


def _pct(xs: list[float], p: int) -> float:
    if not xs:
        return 0.0
    xs = sorted(xs)
    k = max(0, min(len(xs) - 1, int(round((p / 100.0) * (len(xs) - 1)))))
    return xs[k]


HEADER = [
    "case_id",
    "suite",
    "category",
    "stack",
    "model",
    "model_version",
    "seed",
    "blocked_by_defense",
    "attack_succeeded",
    "total_latency_ms",
    "total_cost_usd",
    "n_verdicts",
]


def write_csv(results: list[RunResult], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(HEADER)
        for r in results:
            writer.writerow(
                [
                    r.case_id,
                    r.suite,
                    r.category,
                    r.stack,
                    r.model,
                    r.model_version,
                    r.seed,
                    r.blocked_by_defense,
                    r.attack_succeeded if r.attack_succeeded is not None else "",
                    f"{r.total_latency_ms:.2f}",
                    f"{r.total_cost_usd:.6f}",
                    len(r.verdicts),
                ]
            )
