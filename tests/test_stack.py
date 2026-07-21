from __future__ import annotations

from pathlib import Path

import pytest

from pibench.core.stack import Stack, _apply_sanitize
from pibench.core.types import Action, Message, Role, Source, Verdict
from pibench.defenses.base import Defense
from pibench.defenses.spotlight import SpotlightDefense


class _StubDefense(Defense):
    """Configurable stub: returns a fixed verdict and records what it saw."""

    version = "stub"

    def __init__(self, name: str, action: Action, modified_content: str | None = None) -> None:
        self.name = name
        self._action = action
        self._modified = modified_content
        self.seen: list[list[Message]] = []

    def check(self, messages: list[Message]) -> Verdict:
        self.seen.append(messages)
        return Verdict(
            defense=self.name,
            action=self._action,
            modified_content=self._modified,
        )


def _msg(content: str, *, trusted: bool) -> Message:
    return Message(
        role=Role.USER if trusted else Role.TOOL,
        content=content,
        source=Source.USER if trusted else Source.TOOL_OUTPUT,
        trusted=trusted,
    )


def test_block_short_circuits_downstream_defenses() -> None:
    blocker = _StubDefense("blocker", Action.BLOCK)
    downstream = _StubDefense("downstream", Action.ALLOW)
    stack = Stack(name="s", defenses=[blocker, downstream])

    _, verdicts = stack.check([_msg("payload", trusted=False)])

    assert [v.defense for v in verdicts] == ["blocker"]
    assert downstream.seen == [], "defenses after a BLOCK must not run"


def test_sanitize_rewrites_last_untrusted_for_downstream() -> None:
    sanitizer = _StubDefense("sanitizer", Action.SANITIZE, modified_content="CLEANED")
    downstream = _StubDefense("downstream", Action.ALLOW)
    stack = Stack(name="s", defenses=[sanitizer, downstream])

    msgs = [_msg("system", trusted=True), _msg("dirty payload", trusted=False)]
    sanitized, verdicts = stack.check(msgs)

    assert [v.action for v in verdicts] == [Action.SANITIZE, Action.ALLOW]
    assert sanitized[-1].content == "CLEANED"
    assert sanitized[-1].trusted is False, "sanitized content must stay untrusted"
    assert sanitized[0].content == "system", "trusted messages must be untouched"
    # downstream defense must see the sanitized chain, not the original
    assert downstream.seen[0][-1].content == "CLEANED"


def test_sanitize_without_modified_content_is_a_noop() -> None:
    sanitizer = _StubDefense("sanitizer", Action.SANITIZE, modified_content=None)
    stack = Stack(name="s", defenses=[sanitizer])

    msgs = [_msg("payload", trusted=False)]
    sanitized, _ = stack.check(msgs)
    assert sanitized[0].content == "payload"


def test_apply_sanitize_with_no_untrusted_returns_chain_unchanged() -> None:
    msgs = [_msg("a", trusted=True), _msg("b", trusted=True)]
    assert _apply_sanitize(msgs, "X") == msgs


def test_apply_sanitize_replaces_only_last_untrusted() -> None:
    msgs = [
        _msg("u1", trusted=False),
        _msg("t", trusted=True),
        _msg("u2", trusted=False),
    ]
    out = _apply_sanitize(msgs, "X")
    assert [m.content for m in out] == ["u1", "t", "X"]


def test_from_yaml_builds_configured_defenses(tmp_path: Path) -> None:
    # imported for registration side effect
    from pibench.defenses import none as _none  # noqa: F401

    yaml_path = tmp_path / "mini.yaml"
    yaml_path.write_text("name: mini\ndefenses:\n  - type: none\n", encoding="utf-8")

    stack = Stack.from_yaml(yaml_path)
    assert stack.name == "mini"
    assert [d.name for d in stack.defenses] == ["none"]


def test_from_yaml_unknown_defense_raises(tmp_path: Path) -> None:
    yaml_path = tmp_path / "bad.yaml"
    yaml_path.write_text("name: bad\ndefenses:\n  - type: does-not-exist\n", encoding="utf-8")

    with pytest.raises(KeyError, match="does-not-exist"):
        Stack.from_yaml(yaml_path)


def test_compose_spotlight_then_classifier_fpr_regression() -> None:
    """Reproduces the flagship leaderboard finding: a classifier downstream
    of spotlighting sees the delimiters/preamble and can flag benign content
    it would otherwise pass."""
    import tempfile

    from pibench.core.cache import DiskKV
    from pibench.defenses.deberta_pi import DebertaPIDefense

    def delim_sensitive_scorer(text: str) -> float:
        # stands in for a classifier that never saw spotlight delimiters
        return 0.9 if "<UNTRUSTED_INPUT>" in text else 0.0

    classifier = DebertaPIDefense(
        threshold=0.5,
        cache=DiskKV(namespace="test", directory=Path(tempfile.mkdtemp())),
        scorer_fn=delim_sensitive_scorer,
    )
    benign = [_msg("summarise this", trusted=True), _msg("Team sync at 10am.", trusted=False)]

    # classifier alone allows the benign context
    _, verdicts = Stack("deberta", [classifier]).check([m.model_copy() for m in benign])
    assert verdicts[-1].action is Action.ALLOW

    # spotlight + classifier blocks it: the FPR regression
    composed = Stack("spotlight-deberta", [SpotlightDefense(), classifier])
    _, verdicts = composed.check([m.model_copy() for m in benign])
    assert verdicts[-1].action is Action.BLOCK
