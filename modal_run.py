"""Run the remaining M3 bench matrix on Modal GPUs.

One Modal function per model, all three in parallel (A10G each), with a
shared ``pibench-data`` Volume holding Ollama weights, per-model pibench
caches, and the results CSVs. Resumable: finished (stack, suite) tuples are
skipped via their CSV on the volume, and the response cache is committed
after every tuple, so a preempted container retries almost for free.

Usage:
    .venv/bin/modal run modal_run.py                      # all 3 models
    .venv/bin/modal run modal_run.py --models llama3.1-8b # smoke-test one

Fetch artifacts when done:
    .venv/bin/modal volume get pibench-data results ./results-modal
    # then review + move CSVs into results/ and commit as usual.

Caches (Ollama weights, DeBERTa verdicts, model responses) stay on the
volume — replays on Modal are free. They are per-model sqlite trees
(``cache/<model>/``) and are not meant to be merged into the local
``.pibench-cache``.
"""

from __future__ import annotations

import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

import modal

# ── matrix ──────────────────────────────────────────────────────────────
# registry name -> Ollama tag (mirrors src/pibench/models/local_models.py)
MODEL_TAGS = {
    "llama3.1-8b": "llama3.1:8b",
    "mistral-7b": "mistral:7b",
    "qwen3-8b": "qwen3:8b",
}
STACKS = [
    "none",
    "spotlight",
    "deberta",
    "policy",
    "spotlight-deberta",
    "spotlight-deberta-policy",
]
SUITES = ["injecagent-full", "indirectrag-bench"]
SEED = 42

REPO = "/root/pi-bench"
DATA = "/data"

app = modal.App("pibench-m3")
vol = modal.Volume.from_name("pibench-data", create_if_missing=True)

image = (
    modal.Image.debian_slim(python_version="3.12")
    .apt_install("curl", "ca-certificates", "zstd")
    .run_commands("curl -fsSL https://ollama.com/install.sh | sh")
    .pip_install(
        # pibench core deps (pyproject) + deberta extra; adapter is stdlib-only
        "pydantic>=2.7",
        "pyyaml>=6.0",
        "typer>=0.12",
        "rich>=13.7",
        "diskcache>=5.6",
        "transformers>=4.44",
        "torch>=2.2",
        "sentencepiece>=0.2",
        "tiktoken>=0.7",
    )
    # repo tree last (runtime mount): src/, stacks/, datasets/
    .add_local_dir(
        Path(__file__).parent,
        remote_path=REPO,
        ignore=[".git", ".venv", ".pibench-cache", "results", "**/__pycache__"],
    )
)


def _wait_for_ollama(timeout_s: float = 120.0) -> None:
    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen("http://127.0.0.1:11434/api/version", timeout=2):
                return
        except OSError:
            time.sleep(1.0)
    raise RuntimeError("ollama serve did not come up within timeout")


@app.function(
    image=image,
    gpu="A10G",
    cpu=4.0,
    memory=16_384,
    timeout=12 * 60 * 60,
    volumes={DATA: vol},
    retries=modal.Retries(max_retries=3, initial_delay=10.0, backoff_coefficient=2.0),
)
def run_model(model_name: str) -> list[str]:
    tag = MODEL_TAGS[model_name]

    # Shared weights; per-model pibench cache (diskcache is sqlite — keep
    # concurrent containers out of each other's cache.db).
    os.environ["OLLAMA_MODELS"] = f"{DATA}/ollama/models"
    os.environ["HF_HOME"] = f"{DATA}/hf"
    os.environ["PYTHONPATH"] = f"{REPO}/src"

    results_dir = Path(DATA) / "results"
    cache_dir = Path(DATA) / "cache" / model_name
    for d in (Path(os.environ["OLLAMA_MODELS"]), results_dir, cache_dir):
        d.mkdir(parents=True, exist_ok=True)

    # cwd for pibench: stacks/ + writable results/ + per-model cache.
    work = Path("/work")
    work.mkdir(exist_ok=True)
    for link, target in {
        work / "stacks": Path(REPO) / "stacks",
        work / "results": results_dir,
        work / ".pibench-cache": cache_dir,
    }.items():
        if not link.is_symlink():
            link.symlink_to(target)

    server = subprocess.Popen(["ollama", "serve"])
    try:
        _wait_for_ollama()
        subprocess.run(["ollama", "pull", tag], check=True)
        vol.commit()  # persist weights before the long part

        done: list[str] = []
        for suite in SUITES:
            for stack in STACKS:
                csv = results_dir / f"{stack}__{model_name}__{suite}__seed{SEED}.csv"
                if csv.exists():
                    print(f"skip (exists): {csv.name}")
                    done.append(f"{csv.name} (cached)")
                    continue
                t0 = time.monotonic()
                subprocess.run(
                    [
                        sys.executable,
                        "-m",
                        "pibench.cli",
                        "bench",
                        "--stack",
                        stack,
                        "--model",
                        model_name,
                        "--suite",
                        suite,
                        "--seed",
                        str(SEED),
                    ],
                    check=True,
                    cwd=work,
                )
                vol.commit()  # CSV + response cache survive preemption
                done.append(f"{csv.name} ({time.monotonic() - t0:.0f}s)")
        return done
    finally:
        server.terminate()


@app.local_entrypoint()
def main(models: str = ",".join(MODEL_TAGS)) -> None:
    names = [m.strip() for m in models.split(",") if m.strip()]
    unknown = set(names) - set(MODEL_TAGS)
    if unknown:
        raise SystemExit(f"unknown model(s): {sorted(unknown)}; choose from {list(MODEL_TAGS)}")
    for name, rows in zip(names, run_model.map(names)):
        print(f"\n=== {name} ===")
        for row in rows:
            print(f"  {row}")
