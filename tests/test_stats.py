from __future__ import annotations

import pytest

from pibench.core.stats import CaseStats, headline_metrics, mean_rate, percentile


def _case(category: str, *, blocked: bool = False, succeeded: bool = False,
          latency: float = 1.0, cost: float = 0.0) -> CaseStats:
    return CaseStats(
        category=category,
        blocked=blocked,
        attack_succeeded=succeeded,
        latency_ms=latency,
        cost_usd=cost,
    )


def test_mean_rate_empty_is_zero() -> None:
    assert mean_rate([]) == 0.0


def test_mean_rate() -> None:
    assert mean_rate([True, False, True, True]) == pytest.approx(0.75)


def test_percentile_empty_is_zero() -> None:
    assert percentile([], 95) == 0.0


def test_percentile_single_value() -> None:
    assert percentile([7.0], 50) == 7.0
    assert percentile([7.0], 95) == 7.0


def test_percentile_ignores_input_order() -> None:
    xs = [30.0, 10.0, 20.0]
    assert percentile(xs, 0) == 10.0
    assert percentile(xs, 100) == 30.0


def test_headline_metrics_empty() -> None:
    m = headline_metrics([])
    assert m["n"] == 0
    assert m["asr"] == 0.0
    assert m["fpr"] == 0.0
    assert m["usd_per_1k"] == 0.0


def test_headline_metrics_asr_only_counts_attacks() -> None:
    cases = [
        _case("attack", succeeded=True),
        _case("attack", succeeded=False),
        # benign rows must not enter the ASR denominator
        _case("benign", blocked=False),
        _case("benign", blocked=True),
    ]
    m = headline_metrics(cases)
    assert m["n_attack"] == 2 and m["n_benign"] == 2
    assert m["asr"] == pytest.approx(0.5)
    assert m["fpr"] == pytest.approx(0.5)


def test_headline_metrics_cost_per_1k() -> None:
    cases = [_case("attack", cost=0.002), _case("benign", cost=0.004)]
    m = headline_metrics(cases)
    assert m["usd_per_1k"] == pytest.approx(3.0)
