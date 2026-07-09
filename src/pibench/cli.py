from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from pibench.core.harness import run
from pibench.core.leaderboard import build_leaderboard
from pibench.core.registry import DEFENSES, MODELS, SUITES
from pibench.core.scorer import summarize, write_csv
from pibench.core.stack import Stack

# side-effect imports register concrete classes with the registries
from pibench.defenses import deberta_pi as _deberta_defense  # noqa: F401
from pibench.defenses import none as _none_defense  # noqa: F401
from pibench.defenses import spotlight as _spotlight_defense  # noqa: F401
from pibench.models import mock as _mock_model  # noqa: F401
from pibench.suites import injecagent as _injecagent_suite  # noqa: F401

app = typer.Typer(add_completion=False, no_args_is_help=True)
console = Console()

_STACKS_DIR = Path("stacks")
_RESULTS_DIR = Path("results")


@app.command()
def bench(
    stack: str = typer.Option(..., help="Stack name (matches stacks/<name>.yaml)."),
    model: str = typer.Option(..., help="Registered model name (e.g. 'mock', 'qwen-local')."),
    suite: str = typer.Option(..., help="Registered suite name (e.g. 'injecagent-seed')."),
    seed: int = typer.Option(42, help="Seed used for the model and pinned in the CSV."),
) -> None:
    """Run one (stack, model, suite, seed) tuple and write a results CSV."""
    stack_path = _STACKS_DIR / f"{stack}.yaml"
    if not stack_path.exists():
        console.print(f"[red]error:[/] stack file not found: {stack_path}")
        raise typer.Exit(code=1)

    stack_obj = Stack.from_yaml(stack_path)
    model_obj = MODELS.get_or_die(model)()
    suite_obj = SUITES.get_or_die(suite)()

    console.print(
        f"[bold]running[/] stack=[cyan]{stack}[/] model=[cyan]{model}[/] "
        f"suite=[cyan]{suite}[/] seed=[cyan]{seed}[/]"
    )
    results = run(suite_obj, stack_obj, model_obj, seed=seed)
    summary = summarize(results)

    _print_summary(stack, model, suite, seed, summary)

    out_path = _RESULTS_DIR / f"{stack}__{model}__{suite}__seed{seed}.csv"
    write_csv(results, out_path)
    console.print(f"\n[green]wrote[/] {out_path}")


@app.command("list")
def list_(kind: str = typer.Argument(..., help="one of: stacks, models, suites, defenses")) -> None:
    """List registered components."""
    if kind == "stacks":
        for p in sorted(_STACKS_DIR.glob("*.yaml")):
            console.print(f"- {p.stem}")
        return
    if kind == "models":
        for name in sorted(MODELS):
            console.print(f"- {name}")
        return
    if kind == "suites":
        for name in sorted(SUITES):
            console.print(f"- {name}")
        return
    if kind == "defenses":
        for name in sorted(DEFENSES):
            console.print(f"- {name}")
        return
    raise typer.BadParameter("kind must be one of: stacks, models, suites, defenses")


@app.command()
def leaderboard(
    out: Annotated[Path, typer.Option(help="Output markdown file.")] = Path("leaderboard.md"),
) -> None:
    """Regenerate leaderboard.md from every CSV in results/."""
    build_leaderboard(_RESULTS_DIR, out)
    console.print(f"[green]wrote[/] {out}")


def _print_summary(stack: str, model: str, suite: str, seed: int, summary: dict) -> None:
    table = Table(title=f"{stack} / {model} / {suite} (seed={seed})", show_lines=False)
    table.add_column("metric")
    table.add_column("value", justify="right")
    table.add_row("n attack", str(summary["n_attack"]))
    table.add_row("n benign", str(summary["n_benign"]))
    table.add_row("ASR (attacks)", f"{summary['asr']:.3f}")
    table.add_row("FPR (benigns)", f"{summary['fpr']:.3f}")
    table.add_row("p50 latency (ms)", f"{summary['p50_ms']:.1f}")
    table.add_row("p95 latency (ms)", f"{summary['p95_ms']:.1f}")
    table.add_row("$ per 1k requests", f"{summary['usd_per_1k']:.4f}")
    console.print(table)


if __name__ == "__main__":
    app()
