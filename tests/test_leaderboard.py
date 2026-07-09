from __future__ import annotations

import csv
from pathlib import Path

from pibench.core.leaderboard import build_leaderboard
from pibench.core.scorer import HEADER


def _write_row(path: Path, stack: str, blocked: bool, succeeded: bool, category: str) -> None:
    row = [
        f"case-{stack}",
        "suite-x",
        category,
        stack,
        "mock",
        "mock-v1",
        "42",
        str(blocked).lower(),
        str(succeeded).lower() if category == "attack" else "",
        "5.0",
        "0.000000",
        "1",
    ]
    write_header = not path.exists()
    with path.open("a", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        if write_header:
            w.writerow(HEADER)
        w.writerow(row)


def test_leaderboard_skips_header_only_csv(tmp_path):
    results = tmp_path / "results"
    results.mkdir()

    # header-only CSV (no data rows)
    header_only = results / "empty.csv"
    with header_only.open("w", encoding="utf-8", newline="") as fh:
        csv.writer(fh).writerow(HEADER)

    out = tmp_path / "leaderboard.md"
    content = build_leaderboard(results, out)

    assert out.exists()
    assert "0 row(s)" in content


def test_leaderboard_sorts_by_asr_then_fpr(tmp_path):
    results = tmp_path / "results"
    results.mkdir()

    # 'weak' stack: attack succeeds, benign not blocked -> ASR 1.0, FPR 0.0
    weak = results / "weak.csv"
    _write_row(weak, "weak", blocked=False, succeeded=True, category="attack")
    _write_row(weak, "weak", blocked=False, succeeded=False, category="benign")

    # 'strong' stack: attack blocked, benign not blocked -> ASR 0.0, FPR 0.0
    strong = results / "strong.csv"
    _write_row(strong, "strong", blocked=True, succeeded=False, category="attack")
    _write_row(strong, "strong", blocked=False, succeeded=False, category="benign")

    out = tmp_path / "leaderboard.md"
    content = build_leaderboard(results, out)

    assert out.exists()
    # strong stack (lower ASR) must appear before weak stack
    strong_idx = content.index("`strong`")
    weak_idx = content.index("`weak`")
    assert strong_idx < weak_idx
    assert "ASR ↓" in content
