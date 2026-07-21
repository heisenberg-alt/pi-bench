from __future__ import annotations

from pathlib import Path

from pibench.core.harness import run
from pibench.core.registry import MODELS, SUITES
from pibench.core.scorer import summarize
from pibench.core.stack import Stack
from pibench.core.types import Action, Message, ModelResponse, Role, Source
from pibench.defenses import capability_policy as _cp  # noqa: F401
from pibench.defenses.capability_policy import CapabilityPolicyDefense
from pibench.models import mock as _mock  # noqa: F401
from pibench.suites import injecagent as _inj  # noqa: F401

REPO = Path(__file__).resolve().parents[1]


def _user_msg(content: str = "hi") -> Message:
    return Message(role=Role.USER, content=content, source=Source.USER, trusted=True)


def _resp(tool_calls: list[dict]) -> ModelResponse:
    return ModelResponse(content="ok", latency_ms=1.0, cost_usd=0.0, tool_calls=tool_calls)


def test_input_check_is_allow_noop() -> None:
    v = CapabilityPolicyDefense(allowed_tools=[]).check([_user_msg()])
    assert v.action is Action.ALLOW


def test_blocks_tool_call_outside_allowlist() -> None:
    d = CapabilityPolicyDefense(allowed_tools=["search"])
    v = d.check_output([_user_msg()], _resp([{"name": "send_email", "arguments": {}}]))
    assert v is not None and v.action is Action.BLOCK
    assert "send_email" in v.reason


def test_allows_tool_calls_inside_allowlist() -> None:
    d = CapabilityPolicyDefense(allowed_tools=["search"])
    v = d.check_output([_user_msg()], _resp([{"name": "search", "arguments": {}}]))
    assert v is not None and v.action is Action.ALLOW


def test_allows_response_with_no_tool_calls() -> None:
    d = CapabilityPolicyDefense(allowed_tools=[])
    v = d.check_output([_user_msg()], _resp([]))
    assert v is not None and v.action is Action.ALLOW


def test_unnamed_tool_call_is_never_allowed() -> None:
    d = CapabilityPolicyDefense(allowed_tools=["search"])
    v = d.check_output([_user_msg()], _resp([{"arguments": {}}]))
    assert v is not None and v.action is Action.BLOCK


def test_policy_stack_end_to_end_on_mock() -> None:
    """The output-side safety net: no input detection at all, yet every
    attack is stopped at the tool-call boundary with zero benign blocks."""
    stack = Stack.from_yaml(REPO / "stacks" / "policy.yaml")
    model = MODELS.get_or_die("mock")()
    suite = SUITES.get_or_die("injecagent-seed")()

    summary = summarize(run(suite, stack, model, seed=42))
    assert summary["asr"] == 0.0, "capability policy must block the mock's exfil tool calls"
    assert summary["fpr"] == 0.0, "benign responses carry no tool calls; none may be blocked"


def test_policy_output_verdict_recorded_in_run_results() -> None:
    stack = Stack.from_yaml(REPO / "stacks" / "policy.yaml")
    model = MODELS.get_or_die("mock")()
    suite = SUITES.get_or_die("injecagent-seed")()

    results = run(suite, stack, model, seed=42)
    attack = next(r for r in results if r.category == "attack")
    assert attack.blocked_by_defense is True
    assert attack.attack_succeeded is False
    # verdict trail: input no-op ALLOW + output BLOCK
    assert [v.action for v in attack.verdicts] == [Action.ALLOW, Action.BLOCK]
    # blocked at the output boundary: the response existed but must not count
    assert attack.response is not None
