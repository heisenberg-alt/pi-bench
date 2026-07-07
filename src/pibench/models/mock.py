from __future__ import annotations

import hashlib
import time

from pibench.core.registry import MODELS
from pibench.core.types import Message, ModelResponse, Source
from pibench.models.base import Model


@MODELS.register("mock")
class MockModel(Model):
    """Deterministic offline model. Simulates a naive agent that complies
    with obvious injected instructions found in untrusted context. Used so
    the harness runs green without any API keys or GPU.

    Compliance behaviour is fixed and documented: if any untrusted message
    contains the word "IGNORE" or an "INSTRUCTION:" marker, the mock echoes
    the injected payload (and the canary token if present) into its reply.
    This yields a non-trivial baseline ASR the harness can act on."""

    name = "mock"
    version = "mock-v1"

    def __init__(self, latency_ms: float = 5.0, cost_per_call_usd: float = 0.0) -> None:
        self._latency_ms = latency_ms
        self._cost_per_call = cost_per_call_usd

    def complete(self, messages: list[Message], *, seed: int) -> ModelResponse:
        t0 = time.perf_counter()
        content = self._simulate(messages, seed)
        elapsed_ms = (time.perf_counter() - t0) * 1000.0 + self._latency_ms
        return ModelResponse(
            content=content,
            latency_ms=elapsed_ms,
            cost_usd=self._cost_per_call,
            model_version=self.version,
        )

    def _simulate(self, messages: list[Message], seed: int) -> str:
        untrusted = [m for m in messages if not m.trusted]
        for m in untrusted:
            upper = m.content.upper()
            if "IGNORE" in upper or "INSTRUCTION:" in upper:
                return f"[INJECTED] complying with tool output: {m.content[:200]}"
        user = next((m.content for m in messages if m.source is Source.USER), "")
        digest = hashlib.sha256(f"{seed}|{user}".encode()).hexdigest()[:8]
        return f"Sure — here is a benign answer to your request. ({digest})"
