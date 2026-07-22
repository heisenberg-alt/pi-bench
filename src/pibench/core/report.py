"""REPORT.md generator: composability ablations over committed results.

Everything is derived from ``results/*.csv`` — rerunning the command on the
same CSVs produces the same report, byte for byte.

Three analyses per (model, suite) group:

1. Ablation grid — every stack's headline metrics side by side.
2. Composition deltas — a stack is treated as a composition of another
   stack when the other's name appears as a hyphen-separated component
   prefix/infix (``spotlight-deberta`` contains ``spotlight`` and
   ``deberta``; ``spotlight-deberta-policy`` also contains
   ``spotlight-deberta``). Deltas surface second-order effects: a composed
   stack that is worse than one of its parts on any axis is a regression.
3. Pareto frontier — rows not dominated on (ASR, FPR, p95, $/1k). A row
   dominates another when it is no worse on all four and strictly better
   on at least one.
"""

from __future__ import annotations

from pathlib import Path

from pibench.core.leaderboard import aggregate_csv

_METRICS = ("asr", "fpr", "p95_ms", "usd_per_1k")


def build_report(results_dir: Path, out_path: Path) -> str:
    rows = [
        agg for p in sorted(results_dir.glob("*.csv")) if (agg := aggregate_csv(p)) is not None
    ]

    lines: list[str] = [
        "# pi-bench composability report",
        "",
        f"Auto-generated from `results/*.csv` via `pibench report`. {len(rows)} row(s).",
        "All metrics: lower is better. Pareto-front rows are marked ★.",
    ]

    for model, suite in sorted({(r["model"], r["suite"]) for r in rows}):
        group = [r for r in rows if r["model"] == model and r["suite"] == suite]
        group.sort(key=lambda r: tuple(r[m] for m in _METRICS))
        front = _pareto_front(group)

        lines += ["", f"## {model} × {suite}", ""]
        lines += _ablation_table(group, front)

        deltas = _composition_deltas(group)
        if deltas:
            lines += ["", "### Composition deltas", ""]
            lines += _delta_table(deltas)

    content = "\n".join(lines) + "\n"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding="utf-8")
    return content


def _ablation_table(group: list[dict], front: list[dict]) -> list[str]:
    out = [
        "| Stack | n | ASR ↓ | FPR ↓ | p95 (ms) ↓ | $ / 1k ↓ | Pareto |",
        "| ----- | -- | ----: | ----: | ---------: | -------: | :----: |",
    ]
    for r in group:
        star = "★" if r in front else ""
        out.append(
            f"| `{r['stack']}` | {r['n']} | {r['asr']:.3f} | {r['fpr']:.3f} | "
            f"{r['p95_ms']:.1f} | ${r['usd_per_1k']:.4f} | {star} |"
        )
    return out


def _delta_table(deltas: list[dict]) -> list[str]:
    out = [
        "| Composed | vs component | ΔASR | ΔFPR | Δp95 (ms) | Regression |",
        "| -------- | ------------ | ---: | ---: | --------: | :--------: |",
    ]
    for d in deltas:
        regression = "⚠" if d["d_asr"] > 0 or d["d_fpr"] > 0 else ""
        out.append(
            f"| `{d['composed']}` | `{d['component']}` | {d['d_asr']:+.3f} | "
            f"{d['d_fpr']:+.3f} | {d['d_p95']:+.1f} | {regression} |"
        )
    return out


def _composition_deltas(group: list[dict]) -> list[dict]:
    by_stack = {r["stack"]: r for r in group}
    deltas: list[dict] = []
    for name, row in sorted(by_stack.items()):
        for other, other_row in sorted(by_stack.items()):
            if name != other and _is_component(other, name):
                deltas.append(
                    {
                        "composed": name,
                        "component": other,
                        "d_asr": row["asr"] - other_row["asr"],
                        "d_fpr": row["fpr"] - other_row["fpr"],
                        "d_p95": row["p95_ms"] - other_row["p95_ms"],
                    }
                )
    return deltas


def _is_component(part: str, whole: str) -> bool:
    """True when ``part``'s hyphen-token sequence appears contiguously in
    ``whole``'s (and they differ). spotlight ⊂ spotlight-deberta;
    spotlight-deberta ⊂ spotlight-deberta-policy; deberta ⊄ deberta."""
    p, w = part.split("-"), whole.split("-")
    return len(p) < len(w) and any(w[i : i + len(p)] == p for i in range(len(w) - len(p) + 1))


def _pareto_front(group: list[dict]) -> list[dict]:
    def dominates(a: dict, b: dict) -> bool:
        return all(a[m] <= b[m] for m in _METRICS) and any(a[m] < b[m] for m in _METRICS)

    return [r for r in group if not any(dominates(o, r) for o in group if o is not r)]
