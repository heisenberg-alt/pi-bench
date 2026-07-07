from __future__ import annotations

from collections.abc import Callable
from typing import Any


class Registry(dict[str, Callable[..., Any]]):
    """Name -> factory mapping used to plug in models, defenses, and suites.
    We intentionally type the value as ``Callable[..., Any]``: each singleton
    (``MODELS``, ``DEFENSES``, ``SUITES``) narrows the return type at the call
    site via the abstract base class it stores."""

    def register(self, name: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def _inner(cls: Callable[..., Any]) -> Callable[..., Any]:
            if name in self:
                raise ValueError(f"{name!r} already registered")
            self[name] = cls
            return cls

        return _inner

    def get_or_die(self, name: str) -> Callable[..., Any]:
        if name not in self:
            raise KeyError(f"{name!r} not registered. Known: {sorted(self)}")
        return self[name]


MODELS: Registry = Registry()
DEFENSES: Registry = Registry()
SUITES: Registry = Registry()
