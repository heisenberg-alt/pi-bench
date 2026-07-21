from __future__ import annotations

from abc import ABC, abstractmethod

from pibench.core.types import Message, ModelResponse, Verdict


class Defense(ABC):
    """One layer of a Stack. Inspects the message chain and returns a Verdict
    (allow / sanitize / block). Concrete subclasses register with the
    ``DEFENSES`` registry via ``@DEFENSES.register(name)``."""

    name: str
    version: str

    @abstractmethod
    def check(self, messages: list[Message]) -> Verdict: ...

    def check_output(self, messages: list[Message], response: ModelResponse) -> Verdict | None:
        """Optional output-side enforcement point, run after the model call.
        Return ``None`` (the default) when the defense has no output check so
        the verdict trail only records defenses that actually inspected the
        response."""
        return None
