from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel

from pibench.core.registry import DEFENSES
from pibench.core.types import Action, Message, ModelResponse, Verdict
from pibench.defenses.base import Defense


class StackConfig(BaseModel):
    name: str
    defenses: list[dict]


class Stack:
    """A composed defense pipeline. Runs each defense in order on the input
    messages. First BLOCK short-circuits; SANITIZE mutates the message chain
    for downstream defenses and the model."""

    def __init__(self, name: str, defenses: list[Defense]) -> None:
        self.name = name
        self.defenses = defenses

    @classmethod
    def from_yaml(cls, path: Path) -> Stack:
        config = StackConfig(**yaml.safe_load(path.read_text(encoding="utf-8")))
        defenses = [
            DEFENSES.get_or_die(entry["type"])(**{k: v for k, v in entry.items() if k != "type"})
            for entry in config.defenses
        ]
        return cls(name=config.name, defenses=defenses)

    def check(self, messages: list[Message]) -> tuple[list[Message], list[Verdict]]:
        """Run every defense on the message chain. Return the (possibly
        sanitized) chain plus the verdict trail. First BLOCK stops the pipe."""
        verdicts: list[Verdict] = []
        current = list(messages)
        for defense in self.defenses:
            v = defense.check(current)
            verdicts.append(v)
            if v.action is Action.BLOCK:
                return current, verdicts
            if v.action is Action.SANITIZE and v.modified_content is not None:
                current = _apply_sanitize(current, v.modified_content)
        return current, verdicts

    def check_output(self, messages: list[Message], response: ModelResponse) -> list[Verdict]:
        """Run every defense's output-side check on the model response.
        Defenses without an output check contribute no verdict. First BLOCK
        stops the pipe."""
        verdicts: list[Verdict] = []
        for defense in self.defenses:
            v = defense.check_output(messages, response)
            if v is None:
                continue
            verdicts.append(v)
            if v.action is Action.BLOCK:
                break
        return verdicts


def _apply_sanitize(messages: list[Message], replacement: str) -> list[Message]:
    """Replace the last untrusted message's content with the sanitized value.
    Trivial for M1; richer scoping (per-source, per-span) lands with real
    defenses that emit structured patches."""
    for i in range(len(messages) - 1, -1, -1):
        if not messages[i].trusted:
            new = messages[:i] + [messages[i].model_copy(update={"content": replacement})]
            new.extend(messages[i + 1 :])
            return new
    return messages
