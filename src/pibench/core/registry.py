from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


class Registry(dict[str, Callable[..., T]]):
    def register(self, name: str) -> Callable[[Callable[..., T]], Callable[..., T]]:
        def _inner(cls: Callable[..., T]) -> Callable[..., T]:
            if name in self:
                raise ValueError(f"{name!r} already registered")
            self[name] = cls
            return cls

        return _inner

    def get_or_die(self, name: str) -> Callable[..., T]:
        if name not in self:
            raise KeyError(f"{name!r} not registered. Known: {sorted(self)}")
        return self[name]


MODELS: Registry = Registry()
DEFENSES: Registry = Registry()
SUITES: Registry = Registry()
