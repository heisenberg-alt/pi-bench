from __future__ import annotations

import pibench.models.local_models as _local  # noqa: F401
from pibench.core.registry import MODELS
from pibench.models.openai_compat import OpenAICompatModel

_EXPECTED = {
    "qwen3-8b": "qwen3:8b",
    "llama3.1-8b": "llama3.1:8b",
    "mistral-7b": "mistral:7b",
    "qwen2.5-7b": "qwen2.5:7b",
}


def test_all_local_models_registered() -> None:
    for name in _EXPECTED:
        assert name in MODELS


def test_factory_builds_openai_compat_with_pinned_tag() -> None:
    for name, tag in _EXPECTED.items():
        model = MODELS.get_or_die(name)()
        assert isinstance(model, OpenAICompatModel)
        assert model.name == name  # stable identity for the CSV row
        assert model.version == tag  # endpoint model tag


def test_base_url_override(monkeypatch) -> None:
    monkeypatch.setenv("PIBENCH_OPENAI_BASE_URL", "http://vllm:8000/v1")
    model = MODELS.get_or_die("qwen3-8b")()
    assert model._base_url == "http://vllm:8000/v1"
