"""Simple key-value disk cache used by defenses and (later) model adapters
to make benchmark runs cheap-to-replay and byte-identical across reruns.

Callers compute stable keys with :func:`hash_input`; values are anything
JSON/pickle-serialisable that DiskCache accepts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from diskcache import Cache

_DEFAULT_DIR = Path(".pibench-cache")


class DiskKV:
    def __init__(self, namespace: str = "default", directory: Path = _DEFAULT_DIR) -> None:
        target = directory / namespace
        target.mkdir(parents=True, exist_ok=True)
        self._cache = Cache(str(target))

    def get(self, key: str) -> Any | None:
        return self._cache.get(key)

    def set(self, key: str, value: Any) -> None:
        self._cache.set(key, value)


def hash_input(*parts: Any) -> str:
    """SHA-256 of the JSON-serialised parts. Stable across runs; safe key."""
    payload = json.dumps(list(parts), sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
