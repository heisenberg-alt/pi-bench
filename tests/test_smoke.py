from __future__ import annotations

from pathlib import Path

from pibench.core.harness import run
from pibench.core.registry import MODELS, SUITES
from pibench.core.scorer import summarize, write_csv
from pibench.core.stack import Stack
from pibench.defenses import none as _none  # noqa: F401
from pibench.models import mock as _mock  # noqa: F401
from pibench.suites import injecagent as _inj  # noqa: F401

REPO = Path(__file__).resolve().parents[1]


def test_baseline_row_end_to_end(tmp_path):
    stack = Stack.from_yaml(REPO / "stacks" / "none.yaml")
    model = MODELS.get_or_die("mock")()
    suite = SUITES.get_or_die("injecagent-seed")()

    results = run(suite, stack, model, seed=42)
    assert results, "harness produced zero results"

    attacks = [r for r in results if r.category == "attack"]
    benigns = [r for r in results if r.category == "benign"]
    assert attacks and benigns, "seed suite must include both attacks and benigns"

    summary = summarize(results)
    assert summary["n_attack"] == len(attacks)
    assert summary["n_benign"] == len(benigns)

    # With no defense in front of a naive model, the seed suite should show
    # a clearly non-zero ASR — otherwise the fixture is broken.
    assert summary["asr"] > 0.5, f"expected baseline ASR > 0.5 on mock, got {summary['asr']}"
    assert summary["fpr"] == 0.0, "no-defense stack must never block, so FPR must be zero"

    out_path = tmp_path / "row.csv"
    write_csv(results, out_path)
    content = out_path.read_text(encoding="utf-8")
    assert "case_id" in content and "attack_succeeded" in content
