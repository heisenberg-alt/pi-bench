from __future__ import annotations

from pibench.core.registry import DEFENSES
from pibench.core.types import Action, Message, Verdict
from pibench.defenses.base import Defense


@DEFENSES.register("none")
class NoDefense(Defense):
    """Baseline: allow everything. Establishes the un-defended ASR floor."""

    name = "none"
    version = "0.1"

    def check(self, messages: list[Message]) -> Verdict:
        return Verdict(defense=self.name, action=Action.ALLOW, score=0.0, reason="baseline")
