from __future__ import annotations

from abc import ABC, abstractmethod

from pibench.core.types import Message, ModelResponse


class Model(ABC):
    name: str
    version: str

    @abstractmethod
    def complete(self, messages: list[Message], *, seed: int) -> ModelResponse: ...
