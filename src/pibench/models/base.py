from __future__ import annotations

from abc import ABC, abstractmethod

from pibench.core.types import Message, ModelResponse


class Model(ABC):
    """Adapter around an LLM (hosted, local, or mock). Given a message chain
    and a seed, returns the model's response with latency and cost recorded.
    Concrete subclasses register with the ``MODELS`` registry."""

    name: str
    version: str

    @abstractmethod
    def complete(self, messages: list[Message], *, seed: int) -> ModelResponse: ...
