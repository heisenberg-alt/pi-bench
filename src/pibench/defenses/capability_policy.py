"""Capability policy: output-side enforcement. The safety net of the
two-enforcement-point architecture — even when input detection misses an
injection, side-effects are stopped at the tool-call boundary.

This defense is a no-op on inputs. After the model responds, every tool
call is checked against an explicit allowlist; any call to a tool outside
it blocks the response. Deterministic and 0-cost, like ``spotlight``."""

from __future__ import annotations

from pibench.core.registry import DEFENSES
from pibench.core.types import Action, Message, ModelResponse, Verdict
from pibench.defenses.base import Defense


@DEFENSES.register("capability-policy")
class CapabilityPolicyDefense(Defense):
    name = "capability-policy"
    version = "capability-policy-v1"

    def __init__(self, allowed_tools: list[str] | None = None) -> None:
        self._allowed = frozenset(allowed_tools or [])

    def check(self, messages: list[Message]) -> Verdict:
        return Verdict(
            defense=self.name,
            action=Action.ALLOW,
            score=0.0,
            reason="output-side defense; no input check",
        )

    def check_output(self, messages: list[Message], response: ModelResponse) -> Verdict | None:
        disallowed = sorted(
            {
                name
                for call in response.tool_calls
                if (name := str(call.get("name", "<unnamed>"))) not in self._allowed
            }
        )
        if disallowed:
            return Verdict(
                defense=self.name,
                action=Action.BLOCK,
                score=1.0,
                reason=f"tool call(s) outside capability allowlist: {', '.join(disallowed)}",
                latency_ms=0.0,
                cost_usd=0.0,
            )
        return Verdict(
            defense=self.name,
            action=Action.ALLOW,
            score=0.0,
            reason="all tool calls within capability allowlist",
            latency_ms=0.0,
            cost_usd=0.0,
        )
