from __future__ import annotations

from abc import ABC, abstractmethod

from pibench.core.types import TestCase


class Suite(ABC):
    """A named collection of TestCase instances (attacks and benigns). Concrete
    subclasses register with the ``SUITES`` registry."""

    name: str
    version: str

    @abstractmethod
    def load(self) -> list[TestCase]: ...
