"""ProtectAI DeBERTa-v3 prompt-injection classifier as a pi-bench defense.

Model card: https://huggingface.co/protectai/deberta-v3-base-prompt-injection-v2
The model returns two logits; index 1 is the INJECTION class. Threshold at
0.5 by default; tune per stack via ``stacks/*.yaml``.

The classifier call is injected via ``scorer_fn`` so unit tests can run
without downloading ~750 MB of weights. Production callers leave it
``None``; the adapter lazy-loads the real HF pipeline the first time
``check()`` runs. Verdicts (score, action, latency) are disk-cached keyed
by ``(model_id, threshold, untrusted_text)`` so reruns are free and
byte-identical."""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import Any

from pibench.core.cache import DiskKV, hash_input
from pibench.core.registry import DEFENSES
from pibench.core.types import Action, Message, Verdict
from pibench.defenses.base import Defense

_DEFAULT_MODEL_ID = "protectai/deberta-v3-base-prompt-injection-v2"


@DEFENSES.register("deberta-pi")
class DebertaPIDefense(Defense):
    name = "deberta-pi"
    version = "protectai-v2-1.0"

    def __init__(
        self,
        threshold: float = 0.5,
        model_id: str = _DEFAULT_MODEL_ID,
        device: str = "cpu",
        cache: DiskKV | None = None,
        scorer_fn: Callable[[str], float] | None = None,
    ) -> None:
        self._threshold = float(threshold)
        self._model_id = model_id
        self._device = device
        self._cache = cache if cache is not None else DiskKV(namespace=self.name)
        self._scorer_fn = scorer_fn
        self._pipe: Any | None = None

    def check(self, messages: list[Message]) -> Verdict:
        untrusted = "\n\n".join(m.content for m in messages if not m.trusted)
        if not untrusted:
            return Verdict(
                defense=self.name,
                action=Action.ALLOW,
                score=0.0,
                reason="no untrusted content",
            )

        key = hash_input(self.version, self._model_id, self._threshold, untrusted)
        cached = self._cache.get(key)
        if cached is not None:
            return Verdict(**cached)

        t0 = time.perf_counter()
        score = self._score(untrusted)
        latency_ms = (time.perf_counter() - t0) * 1000.0

        action = Action.BLOCK if score >= self._threshold else Action.ALLOW
        verdict = Verdict(
            defense=self.name,
            action=action,
            score=score,
            reason=f"pi_prob={score:.3f} thr={self._threshold:.2f}",
            latency_ms=latency_ms,
            cost_usd=0.0,
        )
        self._cache.set(key, verdict.model_dump())
        return verdict

    def _score(self, text: str) -> float:
        if self._scorer_fn is not None:
            return float(self._scorer_fn(text))
        if self._pipe is None:
            self._pipe = _build_pipeline(self._model_id, self._device)
        result = self._pipe(text, truncation=True, max_length=512, top_k=None)
        entries = result[0] if isinstance(result[0], list) else result
        for entry in entries:
            if entry["label"].upper() == "INJECTION":
                return float(entry["score"])
        return 0.0


def _build_pipeline(model_id: str, device: str) -> Any:
    from transformers import (
        AutoModelForSequenceClassification,
        AutoTokenizer,
        pipeline,
    )

    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForSequenceClassification.from_pretrained(model_id)
    pipe = pipeline(
        "text-classification",
        model=model,
        tokenizer=tokenizer,
        device=device,
        top_k=None,
    )
    # Warm-up inference so one-time model-load / graph-compile cost is not
    # attributed to (and cached into) the first case's verdict latency.
    pipe("warm-up", truncation=True, max_length=512)
    return pipe
