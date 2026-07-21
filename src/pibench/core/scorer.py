from __future__ import annotations

import csv
from pathlib import Path

from pibench.core.stats import CaseStats, headline_metrics
from pibench.core.types import RunResult


def summarize(results: list[RunResult]) -> dict:
    """Compute the four-column headline metrics for one (stack, model, suite)
    row: ASR (on attacks), FPR (on benigns), p95 latency, and mean $/1k."""
    return headline_metrics(
        [
            CaseStats(
                category=r.category,
                blocked=r.blocked_by_defense,
                attack_succeeded=bool(r.attack_succeeded),
                latency_ms=r.total_latency_ms,
                cost_usd=r.total_cost_usd,
            )
            for r in results
        ]
    )


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
        # explicit "\n": csv.writer defaults to "\r\n", which would make the
        # committed CSVs platform- and git-autocrlf-dependent
        writer = csv.writer(fh, lineterminator="\n")
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
