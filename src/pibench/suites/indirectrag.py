"""IndirectRAG-Bench suite: 500 own-built indirect-injection cases in the
retrieval-augmented-generation style (see ``datasets/indirectrag-bench/``).

Each case is a user question plus a set of "retrieved" passages; in the 350
attack cases exactly one passage is poisoned with an instruction to the
assistant (echo a canary, or call an attacker tool). The 150 benign cases are
clean retrievals, so a defense that blocks them shows up as false positives.

The dataset ships in-repo as a pinned JSONL, so the suite is fully offline and
byte-identical across runs — the same guarantee the InjecAgent loaders give.
Regenerate it with ``python datasets/indirectrag-bench/generate.py``; publish it
to Hugging Face from ``datasets/indirectrag-bench/`` (card included)."""

from __future__ import annotations

import json
from pathlib import Path

from pibench.core.registry import SUITES
from pibench.core.types import Source, TestCase
from pibench.suites.base import Suite

_DATASET_RELPATH = ("datasets", "indirectrag-bench", "indirectrag_bench.jsonl")


def _default_dataset_path() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        candidate = parent.joinpath(*_DATASET_RELPATH)
        if candidate.exists():
            return candidate
    raise FileNotFoundError(
        "indirectrag_bench.jsonl not found; run datasets/indirectrag-bench/generate.py"
    )


@SUITES.register("indirectrag-bench")
class IndirectRAGBench(Suite):
    name = "indirectrag-bench"
    version = "indirectrag-bench-1.0"

    def __init__(self, path: Path | None = None) -> None:
        self._path = path if path is not None else _default_dataset_path()

    def load(self) -> list[TestCase]:
        lines = self._path.read_text(encoding="utf-8").splitlines()
        return [_to_case(json.loads(line)) for line in lines if line.strip()]


def _to_case(rec: dict) -> TestCase:
    passages = rec["retrieved_passages"]
    # the retrieval block the model sees: one untrusted chunk, poisoned in attacks
    injected = "\n\n".join(f"[doc {i + 1}] {p}" for i, p in enumerate(passages))
    return TestCase(
        id=rec["id"],
        suite="indirectrag-bench",
        category=rec["category"],
        user_prompt=rec["user_prompt"],
        injected_context=injected,
        injection_source=Source.RETRIEVAL,
        canary_token=rec.get("canary_token"),
        attacker_tools=list(rec.get("attacker_tools") or []),
        expected_behavior=rec.get("expected_behavior", ""),
    )
