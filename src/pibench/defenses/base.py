from __future__ import annotations

from abc import ABC, abstractmethod

from pibench.core.types import Message, Verdict


class Defense(ABC):
    """One layer of a Stack. Inspects the message chain and returns a Verdict
    (allow / sanitize / block). Concrete subclasses register with the
    ``DEFENSES`` registry via ``@DEFENSES.register(name)``."""

    name: str
    version: str

    @abstractmethod
    def check(self, messages: list[Message]) -> Verdict: ...
