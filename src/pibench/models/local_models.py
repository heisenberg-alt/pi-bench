"""Registered local open-weight reference models, served through an
OpenAI-compatible endpoint (Ollama by default: ``ollama serve`` exposes the
OpenAI ``/v1`` API on :11434). Each entry is the ``openai-compat`` adapter
pinned to one model tag, giving the 4-model matrix a stable registry name —
and therefore one CSV row and one leaderboard line — per model.

Point at vLLM / llama.cpp / a hosted provider instead by exporting
``PIBENCH_OPENAI_BASE_URL`` (and ``PIBENCH_OPENAI_API_KEY`` if needed); only
the endpoint changes, the pinned tags stay the same."""

from __future__ import annotations

import os
from collections.abc import Callable

from pibench.core.registry import MODELS
from pibench.models.openai_compat import OpenAICompatModel

_OLLAMA_DEFAULT_BASE_URL = "http://localhost:11434/v1"

# registry name -> endpoint model tag (Ollama tags by default). All four
# reliably emit OpenAI tool calls through Ollama's /v1 endpoint (Gemma3 and
# Command-R7B were dropped: the former rejects the tools API, the latter
# would not engage it).
_LOCAL_MODELS = {
    "qwen3-8b": "qwen3:8b",
    "llama3.1-8b": "llama3.1:8b",
    "mistral-7b": "mistral:7b",
    "qwen2.5-7b": "qwen2.5:7b",
}


def _factory(registry_name: str, model_tag: str) -> Callable[[], OpenAICompatModel]:
    def make() -> OpenAICompatModel:
        model = OpenAICompatModel(
            base_url=os.environ.get("PIBENCH_OPENAI_BASE_URL", _OLLAMA_DEFAULT_BASE_URL),
            model=model_tag,
        )
        model.name = registry_name  # stable identity for CSV row + leaderboard
        return model

    make.__name__ = f"make_{registry_name.replace('-', '_').replace('.', '_')}"
    return make


for _name, _tag in _LOCAL_MODELS.items():
    MODELS.register(_name)(_factory(_name, _tag))
