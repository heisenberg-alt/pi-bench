"""Numerical helpers shared by the live scorer and the on-disk leaderboard
aggregator. Kept in one place so both compute metrics the same way."""

from __future__ import annotations

from collections.abc import Iterable


def mean_rate(bools: Iterable[bool]) -> float:
    xs = list(bools)
    return sum(xs) / len(xs) if xs else 0.0


def percentile(xs: list[float], p: int) -> float:
    if not xs:
        return 0.0
    xs = sorted(xs)
    k = max(0, min(len(xs) - 1, int(round((p / 100.0) * (len(xs) - 1)))))
    return xs[k]
