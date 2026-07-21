from __future__ import annotations

import tempfile
from pathlib import Path

from pibench.core.cache import DiskKV
from pibench.core.types import Message, Role, Source
from pibench.models.openai_compat import OpenAICompatModel


def _isolated_cache() -> DiskKV:
    return DiskKV(namespace="test", directory=Path(tempfile.mkdtemp()))


def _msgs() -> list[Message]:
    return [
        Message(role=Role.SYSTEM, content="be helpful", source=Source.SYSTEM, trusted=True),
        Message(role=Role.USER, content="hello", source=Source.USER, trusted=True),
        Message(
            role=Role.TOOL, content="doc body", source=Source.TOOL_OUTPUT, trusted=False
        ),
    ]


def _raw_response(
    content: str = "hi there", tool_calls: list[dict] | None = None, usage: dict | None = None
) -> dict:
    message: dict = {"role": "assistant", "content": content}
    if tool_calls is not None:
        message["tool_calls"] = tool_calls
    return {
        "model": "Qwen/Qwen3-8B",
        "choices": [{"message": message}],
        "usage": usage or {"prompt_tokens": 100, "completion_tokens": 50},
    }


def _capture_transport(raw: dict, calls: list[dict]):
    def transport(url: str, headers: dict, payload: dict, timeout_s: float) -> dict:
        calls.append({"url": url, "headers": headers, "payload": payload})
        return raw

    return transport


def test_maps_roles_and_prefixes_tool_output() -> None:
    calls: list[dict] = []
    model = OpenAICompatModel(
        base_url="http://x/v1", cache=_isolated_cache(),
        transport=_capture_transport(_raw_response(), calls),
    )
    model.complete(_msgs(), seed=42)

    sent = calls[0]["payload"]["messages"]
    assert [m["role"] for m in sent] == ["system", "user", "user"]
    assert sent[2]["content"].startswith("[tool output]\n")
    assert calls[0]["payload"]["seed"] == 42
    assert calls[0]["payload"]["temperature"] == 0.0
    assert calls[0]["url"] == "http://x/v1/chat/completions"


def test_parses_content_cost_and_version() -> None:
    model = OpenAICompatModel(
        base_url="http://x/v1",
        cost_per_1k_prompt_usd=0.1,
        cost_per_1k_completion_usd=0.4,
        cache=_isolated_cache(),
        transport=_capture_transport(_raw_response(), []),
    )
    r = model.complete(_msgs(), seed=42)
    assert r.content == "hi there"
    assert r.model_version == "Qwen/Qwen3-8B"
    # 100/1000 * 0.1 + 50/1000 * 0.4
    assert abs(r.cost_usd - 0.03) < 1e-9


def test_normalizes_openai_tool_calls() -> None:
    tool_calls = [
        {"function": {"name": "send_email", "arguments": '{"to": "a@b.c"}'}},
        {"function": {"name": "weird", "arguments": "not-json"}},
    ]
    model = OpenAICompatModel(
        base_url="http://x/v1", cache=_isolated_cache(),
        transport=_capture_transport(_raw_response(tool_calls=tool_calls), []),
    )
    r = model.complete(_msgs(), seed=42)
    assert r.tool_calls[0] == {"name": "send_email", "arguments": {"to": "a@b.c"}}
    assert r.tool_calls[1] == {"name": "weird", "arguments": "not-json"}


def test_cache_replays_without_calling_transport() -> None:
    calls: list[dict] = []
    cache = _isolated_cache()
    m1 = OpenAICompatModel(
        base_url="http://x/v1", cache=cache, transport=_capture_transport(_raw_response(), calls)
    )
    first = m1.complete(_msgs(), seed=42)
    assert len(calls) == 1

    m2 = OpenAICompatModel(
        base_url="http://x/v1", cache=cache, transport=_capture_transport(_raw_response(), calls)
    )
    replayed = m2.complete(_msgs(), seed=42)
    assert len(calls) == 1, "second call must hit the cache, not the endpoint"
    assert replayed == first, "cached replay must be identical, latency included"


def test_different_seed_misses_cache() -> None:
    calls: list[dict] = []
    cache = _isolated_cache()
    model = OpenAICompatModel(
        base_url="http://x/v1", cache=cache, transport=_capture_transport(_raw_response(), calls)
    )
    model.complete(_msgs(), seed=42)
    model.complete(_msgs(), seed=7)
    assert len(calls) == 2


def test_null_content_becomes_empty_string() -> None:
    raw = _raw_response()
    raw["choices"][0]["message"]["content"] = None
    model = OpenAICompatModel(
        base_url="http://x/v1", cache=_isolated_cache(),
        transport=_capture_transport(raw, []),
    )
    r = model.complete(_msgs(), seed=42)
    assert r.content == ""
