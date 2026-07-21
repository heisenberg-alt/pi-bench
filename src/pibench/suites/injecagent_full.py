"""Full InjecAgent suite: all 1,054 indirect-injection test cases from
https://github.com/uiuc-kang-lab/InjecAgent (Zhan et al., arXiv:2403.02691).

Two attack families, both delivered through a user tool's response:

- ``dh`` (direct harm, 510): the injected instruction pushes the agent to
  call a harmful attacker tool (e.g. unlock a smart lock).
- ``ds`` (data stealing, 544): the injected instruction pushes the agent
  to extract user data and exfiltrate it via ``GmailSendEmail``.

Attack success in the source benchmark is "the agent invokes an attacker
tool", so each ``TestCase`` carries ``attacker_tools`` for the judge.

The dataset is pinned to a commit SHA and disk-cached, so the download
happens once and every run afterwards is offline and byte-identical. The
seed suite's 10 benign cases are reused as the benign side (the upstream
dataset has no benign cases; FPR needs some).

Settings: ``base`` injects only the attacker instruction; ``enhanced``
prepends an "IGNORE all previous instructions" hacking prompt. Both are
registered (``injecagent-full``, ``injecagent-full-enhanced``). Note for
mock-model rows: the naive mock only complies with explicit IGNORE /
INSTRUCTION: markers, so its base-setting ASR is ~0 — base-setting rows
only become meaningful with real model adapters."""

from __future__ import annotations

import json
import urllib.request

from pibench.core.cache import DiskKV, hash_input
from pibench.core.registry import SUITES
from pibench.core.types import Source, TestCase
from pibench.suites.base import Suite
from pibench.suites.injecagent import InjecAgentSeed

_PINNED_SHA = "f19c9f2c79a41046eb13c03c51a24c567a8ffa07"
_BASE_URL = "https://raw.githubusercontent.com/uiuc-kang-lab/InjecAgent"


@SUITES.register("injecagent-full")
class InjecAgentFull(Suite):
    version = f"injecagent@{_PINNED_SHA[:12]}"

    def __init__(
        self,
        setting: str = "base",
        sha: str = _PINNED_SHA,
        cache: DiskKV | None = None,
        fetcher=None,
    ) -> None:
        if setting not in ("base", "enhanced"):
            raise ValueError(f"setting must be 'base' or 'enhanced', got {setting!r}")
        self.name = "injecagent-full" if setting == "base" else f"injecagent-full-{setting}"
        self._setting = setting
        self._sha = sha
        self._cache = cache if cache is not None else DiskKV(namespace="injecagent-full")
        self._fetcher = fetcher if fetcher is not None else _http_fetch

    def load(self) -> list[TestCase]:
        cases: list[TestCase] = []
        for family in ("dh", "ds"):
            for i, item in enumerate(self._records(family)):
                cases.append(self._to_case(family, i, item))
        cases.extend(_benign_cases(self.name))
        return cases

    def _records(self, family: str) -> list[dict]:
        url = f"{_BASE_URL}/{self._sha}/data/test_cases_{family}_{self._setting}.json"
        key = hash_input(self.name, self._sha, self._setting, family)
        cached = self._cache.get(key)
        if cached is not None:
            return cached
        records = json.loads(self._fetcher(url))
        if not isinstance(records, list) or not records:
            raise ValueError(f"unexpected InjecAgent payload from {url}")
        self._cache.set(key, records)
        return records

    def _to_case(self, family: str, index: int, item: dict) -> TestCase:
        return TestCase(
            id=f"{family}-{self._setting}-{index:04d}",
            suite=self.name,
            category="attack",
            user_prompt=item["User Instruction"],
            injected_context=str(item["Tool Response"]),
            injection_source=Source.TOOL_OUTPUT,
            canary_token=None,
            attacker_tools=list(item["Attacker Tools"]),
            expected_behavior="ignore the injected instruction; answer the user request",
        )


def _benign_cases(suite_name: str) -> list[TestCase]:
    benigns = [c for c in InjecAgentSeed().load() if c.category == "benign"]
    return [c.model_copy(update={"suite": suite_name}) for c in benigns]


def _http_fetch(url: str) -> str:
    if not url.startswith("https://"):
        raise ValueError(f"refusing non-https dataset URL: {url}")
    with urllib.request.urlopen(url, timeout=60.0) as resp:  # noqa: S310 - https enforced
        return resp.read().decode("utf-8")


@SUITES.register("injecagent-full-enhanced")
def _enhanced() -> InjecAgentFull:
    return InjecAgentFull(setting="enhanced")
