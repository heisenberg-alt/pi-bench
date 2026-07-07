from __future__ import annotations

from abc import ABC, abstractmethod

from pibench.core.types import Message, Verdict


class Defense(ABC):
    name: str
    version: str

    @abstractmethod
    def check(self, messages: list[Message]) -> Verdict: ...
