from __future__ import annotations

from abc import ABC, abstractmethod

from pibench.core.types import TestCase


class Suite(ABC):
    name: str
    version: str

    @abstractmethod
    def load(self) -> list[TestCase]: ...
