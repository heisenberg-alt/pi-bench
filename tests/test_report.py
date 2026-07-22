from __future__ import annotations

import csv
from pathlib import Path

from pibench.core.report import _is_component, _pareto_front, build_report
from pibench.core.scorer import HEADER


def _write_rows(path: Path, stack: str, rows: list[tuple[str, bool, bool, float]]) -> None:
    """rows: (category, blocked, succeeded, latency_ms)"""
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(HEADER)
        for i, (category, blocked, succeeded, latency) in enumerate(rows):
            w.writerow(
                [
                    f"case-{i}",
                    "suite-x",
                    category,
                    stack,
                    "mock",
                    "mock-v2",
                    "42",
                    str(blocked),
                    str(succeeded) if category == "attack" else "",
                    f"{latency:.2f}",
                    "0.000000",
                    "1",
                ]
            )


def _results_dir(tmp_path: Path) -> Path:
    d = tmp_path / "results"
    d.mkdir()
    # component A: blocks the attack, no benign block, slow
    _write_rows(
        d / "a.csv", "deberta",
        [("attack", True, False, 30.0), ("benign", False, False, 30.0)],
    )
    # component B: misses the attack, fast
    _write_rows(
        d / "b.csv", "spotlight",
        [("attack", False, True, 5.0), ("benign", False, False, 5.0)],
    )
    # composed: same ASR as A but blocks the benign case -> FPR regression
    _write_rows(
        d / "ab.csv", "spotlight-deberta",
        [("attack", True, False, 40.0), ("benign", True, False, 40.0)],
    )
    return d


def test_is_component_token_semantics() -> None:
    assert _is_component("spotlight", "spotlight-deberta")
    assert _is_component("deberta", "spotlight-deberta")
    assert _is_component("spotlight-deberta", "spotlight-deberta-policy")
    assert not _is_component("spotlight-deberta", "spotlight-deberta")  # not itself
    assert not _is_component("light", "spotlight-deberta")  # token, not substring
    assert not _is_component("spotlight-policy", "spotlight-deberta-policy")  # not contiguous


def test_pareto_front_marks_non_dominated_rows() -> None:
    a = {"asr": 0.0, "fpr": 0.0, "p95_ms": 30.0, "usd_per_1k": 0.0}
    b = {"asr": 1.0, "fpr": 0.0, "p95_ms": 5.0, "usd_per_1k": 0.0}
    c = {"asr": 0.0, "fpr": 0.7, "p95_ms": 40.0, "usd_per_1k": 0.0}  # dominated by a
    front = _pareto_front([a, b, c])
    assert a in front and b in front and c not in front


def test_report_surfaces_fpr_regression(tmp_path: Path) -> None:
    out = tmp_path / "REPORT.md"
    content = build_report(_results_dir(tmp_path), out)

    assert out.exists()
    assert "## mock × suite-x" in content
    # composed vs deberta: ΔFPR +1.000 flagged as regression
    assert "| `spotlight-deberta` | `deberta` | +0.000 | +1.000 | +10.0 | ⚠ |" in content
    # composed vs spotlight: ASR improved, FPR regressed -> still flagged
    assert "| `spotlight-deberta` | `spotlight` | -1.000 | +1.000 | +35.0 | ⚠ |" in content


def test_report_is_deterministic(tmp_path: Path) -> None:
    d = _results_dir(tmp_path)
    first = build_report(d, tmp_path / "r1.md")
    second = build_report(d, tmp_path / "r2.md")
    assert first == second


def test_report_pareto_column(tmp_path: Path) -> None:
    content = build_report(_results_dir(tmp_path), tmp_path / "REPORT.md")
    ablation = content.split("### Composition deltas")[0]
    lines = {
        line.split("|")[1].strip(): line
        for line in ablation.splitlines()
        if line.startswith("| `")
    }
    assert lines["`deberta`"].rstrip().endswith("★ |")
    assert lines["`spotlight`"].rstrip().endswith("★ |")
    # composed row is dominated by deberta -> no star
    assert lines["`spotlight-deberta`"].rstrip().endswith("|  |")
