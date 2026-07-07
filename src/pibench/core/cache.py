from __future__ import annotations

import hashlib
import json
from pathlib import Path

from diskcache import Cache

_DEFAULT_DIR = Path(".pibench-cache")


class ResponseCache:
    """Deterministic-replay cache keyed by (model_version, seed, messages)."""

    def __init__(self, directory: Path = _DEFAULT_DIR) -> None:
        directory.mkdir(parents=True, exist_ok=True)
        self._cache = Cache(str(directory))

    def _key(self, model_version: str, seed: int, messages: list[dict]) -> str:
        payload = json.dumps(
            {"m": model_version, "s": seed, "msgs": messages},
            sort_keys=True,
            ensure_ascii=False,
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def get(self, model_version: str, seed: int, messages: list[dict]) -> dict | None:
        return self._cache.get(self._key(model_version, seed, messages))

    def set(self, model_version: str, seed: int, messages: list[dict], value: dict) -> None:
        self._cache.set(self._key(model_version, seed, messages), value)
