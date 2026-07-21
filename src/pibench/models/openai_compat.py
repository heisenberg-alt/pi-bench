"""OpenAI-compatible chat-completions adapter — the bridge to real models.

Works against any endpoint speaking the OpenAI chat API: vLLM serve
(``vllm serve Qwen/Qwen3-8B``), llama.cpp server, or hosted providers.
Configuration comes from the constructor or environment variables so the
CLI's zero-arg instantiation works:

- ``PIBENCH_OPENAI_BASE_URL``  (default ``http://localhost:8000/v1``)
- ``PIBENCH_OPENAI_MODEL``     (default ``Qwen/Qwen3-8B``)
- ``PIBENCH_OPENAI_API_KEY``   (optional; sent as a Bearer token)

Responses are disk-cached keyed by (model, seed, params, messages) so
committed rows replay byte-identically without hitting the endpoint.
Temperature defaults to 0 and the seed is passed through for maximum
determinism on servers that honour it.

Role mapping note: ``Role.TOOL`` messages are sent as ``user`` turns with a
``[tool output]`` prefix. The strict OpenAI schema requires ``tool`` turns
to reference a prior assistant tool call, which standalone benchmark cases
don't have; the prefix keeps the untrusted provenance visible to the model
without tripping server-side validation."""

from __future__ import annotations

import json
import os
import time
import urllib.request
from collections.abc import Callable
from typing import Any

from pibench.core.cache import DiskKV, hash_input
from pibench.core.registry import MODELS
from pibench.core.types import Message, ModelResponse, Role
from pibench.models.base import Model

Transport = Callable[[str, dict, dict, float], dict]
"""(url, headers, payload, timeout_s) -> parsed response JSON."""

_DEFAULT_BASE_URL = "http://localhost:8000/v1"
_DEFAULT_MODEL = "Qwen/Qwen3-8B"


@MODELS.register("openai-compat")
class OpenAICompatModel(Model):
    name = "openai-compat"

    def __init__(
        self,
        base_url: str | None = None,
        model: str | None = None,
        temperature: float = 0.0,
        max_tokens: int = 512,
        timeout_s: float = 120.0,
        cost_per_1k_prompt_usd: float = 0.0,
        cost_per_1k_completion_usd: float = 0.0,
        cache: DiskKV | None = None,
        transport: Transport | None = None,
    ) -> None:
        self._base_url = (
            base_url or os.environ.get("PIBENCH_OPENAI_BASE_URL", _DEFAULT_BASE_URL)
        ).rstrip("/")
        self._model = model or os.environ.get("PIBENCH_OPENAI_MODEL", _DEFAULT_MODEL)
        self._temperature = temperature
        self._max_tokens = max_tokens
        self._timeout_s = timeout_s
        self._cost_prompt = cost_per_1k_prompt_usd
        self._cost_completion = cost_per_1k_completion_usd
        self._cache = cache if cache is not None else DiskKV(namespace=self.name)
        self._transport = transport if transport is not None else _http_transport
        self.version = self._model

    def complete(self, messages: list[Message], *, seed: int) -> ModelResponse:
        payload = {
            "model": self._model,
            "messages": [_to_openai(m) for m in messages],
            "temperature": self._temperature,
            "max_tokens": self._max_tokens,
            "seed": seed,
        }

        key = hash_input(self.name, payload)
        cached = self._cache.get(key)
        if cached is not None:
            return ModelResponse(**cached)

        headers = {"Content-Type": "application/json"}
        api_key = os.environ.get("PIBENCH_OPENAI_API_KEY")
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        t0 = time.perf_counter()
        raw = self._transport(
            f"{self._base_url}/chat/completions", headers, payload, self._timeout_s
        )
        latency_ms = (time.perf_counter() - t0) * 1000.0

        response = self._parse(raw, latency_ms)
        self._cache.set(key, response.model_dump())
        return response

    def _parse(self, raw: dict, latency_ms: float) -> ModelResponse:
        message = raw["choices"][0]["message"]
        usage = raw.get("usage") or {}
        cost = (
            usage.get("prompt_tokens", 0) / 1000.0 * self._cost_prompt
            + usage.get("completion_tokens", 0) / 1000.0 * self._cost_completion
        )
        return ModelResponse(
            content=message.get("content") or "",
            latency_ms=latency_ms,
            cost_usd=cost,
            tool_calls=[_to_tool_call(tc) for tc in message.get("tool_calls") or []],
            model_version=raw.get("model", self._model),
        )


def _to_openai(m: Message) -> dict:
    if m.role is Role.TOOL:
        return {"role": "user", "content": f"[tool output]\n{m.content}"}
    return {"role": m.role.value, "content": m.content}


def _to_tool_call(tc: dict) -> dict:
    fn = tc.get("function") or {}
    args_raw = fn.get("arguments", "")
    try:
        arguments: Any = json.loads(args_raw) if args_raw else {}
    except json.JSONDecodeError:
        arguments = args_raw
    return {"name": fn.get("name", "<unnamed>"), "arguments": arguments}


def _http_transport(url: str, headers: dict, payload: dict, timeout_s: float) -> dict:
    if not url.startswith(("http://", "https://")):
        raise ValueError(f"unsupported endpoint URL scheme: {url}")
    request = urllib.request.Request(  # noqa: S310 - scheme validated above
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout_s) as resp:  # noqa: S310
        return json.loads(resp.read().decode("utf-8"))
