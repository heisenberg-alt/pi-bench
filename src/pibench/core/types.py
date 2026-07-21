from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field


class Role(StrEnum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class Source(StrEnum):
    """Where a message chunk originated. Untrusted sources are what defenses
    must scrutinise; trusted sources are the app's own instructions."""

    SYSTEM = "system"
    USER = "user"
    RETRIEVAL = "retrieval"
    TOOL_OUTPUT = "tool_output"


class Message(BaseModel):
    role: Role
    content: str
    source: Source = Source.USER
    trusted: bool = True


class Action(StrEnum):
    ALLOW = "allow"
    SANITIZE = "sanitize"
    BLOCK = "block"


class Verdict(BaseModel):
    """Result of one defense checking one message (or a bundle of messages)."""

    defense: str
    action: Action
    score: float = Field(ge=0.0, le=1.0, default=0.0)
    reason: str = ""
    latency_ms: float = 0.0
    cost_usd: float = 0.0
    modified_content: str | None = None


class TestCase(BaseModel):
    id: str
    suite: str
    category: Literal["attack", "benign"]
    user_prompt: str
    injected_context: str | None = None
    injection_source: Source | None = None
    canary_token: str | None = None
    attacker_tools: list[str] = Field(default_factory=list)
    expected_behavior: str = ""


class ModelResponse(BaseModel):
    content: str
    latency_ms: float
    cost_usd: float
    tool_calls: list[dict] = Field(default_factory=list)
    model_version: str = ""


class RunResult(BaseModel):
    case_id: str
    suite: str
    category: Literal["attack", "benign"]
    stack: str
    model: str
    model_version: str
    seed: int
    verdicts: list[Verdict]
    response: ModelResponse | None = None
    blocked_by_defense: bool
    attack_succeeded: bool | None = None
    total_latency_ms: float
    total_cost_usd: float
