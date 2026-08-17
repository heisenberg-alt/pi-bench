#!/usr/bin/env python3
"""Generate the launch-blog charts (docs/img/*.svg) from committed results.

Reads results/*.csv through the same aggregation path as leaderboard.md, so the
charts can never drift from the published tables. Stdlib only; deterministic
output (byte-identical for identical CSVs).

Usage:  python docs/make_charts.py
"""

from __future__ import annotations

import sys
from pathlib import Path

from pibench.core.leaderboard import load_rows

REPO = Path(__file__).resolve().parent.parent
IMG = REPO / "docs" / "img"

# Chart tokens (light mode, validated with the dataviz palette checker).
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
BASELINE = "#c3c2b7"
BORDER = "rgba(11,11,11,0.10)"
BLUE = "#2a78d6"  # categorical slot 1 / emphasis accent
ORANGE = "#eb6834"  # categorical slot 2
BLUE_SOFT = "#86b6ef"  # sequential step 250, for the Pareto front line
FONT = "system-ui, -apple-system, 'Segoe UI', sans-serif"

MODELS = [
    ("llama3.1-8b", "Llama 3.1 8B"),
    ("qwen3-8b", "Qwen3 8B"),
    ("qwen2.5-7b", "Qwen2.5 7B"),
    ("mistral-7b", "Mistral 7B"),
]
STACKS = ["none", "spotlight", "policy", "deberta", "spotlight-deberta", "spotlight-deberta-policy"]


def metric(rows: list[dict], stack: str, model: str, suite: str) -> dict:
    hits = [r for r in rows if (r["stack"], r["model"], r["suite"]) == (stack, model, suite)]
    if len(hits) != 1:
        sys.exit(f"expected exactly one row for ({stack}, {model}, {suite}), got {len(hits)}")
    return hits[0]


def text(x: float, y: float, s: str, *, size: float, fill: str, weight: int = 400,
         anchor: str = "start", tabular: bool = False) -> str:
    extra = " font-variant-numeric:tabular-nums;" if tabular else ""
    return (
        f'<text x="{x:g}" y="{y:g}" text-anchor="{anchor}" '
        f'style="font:{weight} {size:g}px {FONT}; fill:{fill};{extra}">{s}</text>'
    )


def rounded_top_bar(x: float, y_top: float, w: float, y_base: float, fill: str,
                    r: float = 4) -> str:
    """Column with 4px-rounded data end and a square baseline."""
    r = min(r, (y_base - y_top) / 2, w / 2)
    d = (
        f"M{x:g},{y_base:g} L{x:g},{y_top + r:g} Q{x:g},{y_top:g} {x + r:g},{y_top:g} "
        f"L{x + w - r:g},{y_top:g} Q{x + w:g},{y_top:g} {x + w:g},{y_top + r:g} "
        f"L{x + w:g},{y_base:g} Z"
    )
    return f'<path d="{d}" fill="{fill}"/>'


def ringed_dot(x: float, y: float, fill: str) -> str:
    """8px-min marker with a 2px surface ring so overlaps stay legible."""
    return (
        f'<circle cx="{x:g}" cy="{y:g}" r="7" fill="{SURFACE}"/>'
        f'<circle cx="{x:g}" cy="{y:g}" r="5" fill="{fill}"/>'
    )


def svg_shell(width: int, height: int, body: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" role="img">\n'
        f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="8" '
        f'fill="{SURFACE}" stroke="{BORDER}"/>\n'
        f"{body}\n</svg>\n"
    )


def chart_undefended_asr(rows: list[dict]) -> str:
    """Grouped columns: undefended ASR per model, tool-output vs retrieved-context."""
    tool = [metric(rows, "none", m, "injecagent-full")["asr"] for m, _ in MODELS]
    rag = [metric(rows, "none", m, "indirectrag-bench")["asr"] for m, _ in MODELS]

    w, h = 760, 448
    left, plot_w = 56, 680
    top, base = 108, 340  # y domain 0..0.8 over 232px
    y_max = 0.8
    assert max(tool + rag) <= y_max

    def sy(v: float) -> float:
        return base - (v / y_max) * (base - top)

    parts = [
        text(24, 36, "Retrieved context is the softer injection channel",
             size=16, fill=INK, weight=600),
        text(24, 58, "Undefended attack success rate (stack = none, seed 42) — "
                     "injecagent-full vs indirectrag-bench · lower is better",
             size=12.5, fill=INK_2),
        # legend (2 series)
        f'<rect x="24" y="76" width="10" height="10" rx="2" fill="{BLUE}"/>',
        text(40, 85, "Tool-output injection", size=12.5, fill=INK_2),
        f'<rect x="182" y="76" width="10" height="10" rx="2" fill="{ORANGE}"/>',
        text(198, 85, "Retrieved-context injection", size=12.5, fill=INK_2),
    ]

    # gridlines + ticks (solid hairlines, recessive)
    for i in range(5):
        v = i * 0.2
        y = sy(v)
        if v > 0:
            parts.append(f'<line x1="{left}" y1="{y:g}" x2="{left + plot_w}" y2="{y:g}" '
                         f'stroke="{GRID}" stroke-width="1"/>')
        parts.append(text(left - 8, y + 4, f"{v:.1f}", size=12, fill=MUTED,
                          anchor="end", tabular=True))
    parts.append(f'<line x1="{left}" y1="{base}" x2="{left + plot_w}" y2="{base}" '
                 f'stroke="{BASELINE}" stroke-width="1"/>')

    bar_w, gap = 22, 2
    for i, (_, label) in enumerate(MODELS):
        cx = left + i * (plot_w / 4) + (plot_w / 8)
        x1 = cx - bar_w - gap / 2
        x2 = cx + gap / 2
        if tool[i] > 0:
            parts.append(rounded_top_bar(x1, sy(tool[i]), bar_w, base, BLUE))
        if rag[i] > 0:
            parts.append(rounded_top_bar(x2, sy(rag[i]), bar_w, base, ORANGE))
        parts.append(text(cx, base + 20, label, size=13, fill=INK_2, anchor="middle"))

    # selective direct labels: the Mistral anomaly only (the table carries the rest)
    mi = len(MODELS) - 1
    cx = left + mi * (plot_w / 4) + (plot_w / 8)
    parts.append(text(cx - bar_w / 2 - gap / 2, base - 6, "0.000*", size=12, fill=INK_2,
                      anchor="middle", tabular=True))
    parts.append(text(cx + bar_w / 2 + gap / 2, sy(rag[mi]) - 7, f"{rag[mi]:.3f}", size=12,
                      fill=INK_2, anchor="middle", tabular=True))

    parts.append(text(24, 400, "* Zero measures non-engagement, not robustness: Mistral "
                               "emitted one tool call in 3,123 responses,",
                      size=11.5, fill=MUTED))
    parts.append(text(24, 416, "so it cannot invoke an attacker's tool through this channel "
                               "— yet follows 72% of retrieved-context injections.",
                      size=11.5, fill=MUTED))
    return svg_shell(w, h, "\n".join(parts))


def pareto_front(points: dict[str, tuple[float, float]]) -> set[str]:
    """Stacks not strictly dominated (another stack no worse on both, better on one)."""
    front = set()
    for name, (a, f) in points.items():
        dominated = any(
            (a2 <= a and f2 <= f) and (a2 < a or f2 < f)
            for other, (a2, f2) in points.items()
            if other != name
        )
        if not dominated:
            front.add(name)
    return front


def chart_asr_vs_fpr(rows: list[dict]) -> str:
    """Emphasis scatter: all six stacks on indirectrag-bench with Qwen2.5 7B."""
    pts = {
        s: (
            metric(rows, s, "qwen2.5-7b", "indirectrag-bench")["asr"],
            metric(rows, s, "qwen2.5-7b", "indirectrag-bench")["fpr"],
        )
        for s in STACKS
    }
    front = pareto_front(pts)

    w, h = 760, 484
    left, right, top, base = 64, 720, 128, 396  # x 0..0.5, y 0..1.0
    x_max, y_max = 0.5, 1.0
    assert max(a for a, _ in pts.values()) <= x_max

    def sx(v: float) -> float:
        return left + (v / x_max) * (right - left)

    def sy(v: float) -> float:
        return base - (v / y_max) * (base - top)

    parts = [
        text(24, 36, "No stack is both safe and usable against retrieved-context injection",
             size=16, fill=INK, weight=600),
        text(24, 58, "All six stacks on indirectrag-bench, Qwen2.5 7B, seed 42 · "
                     "closer to the origin is better",
             size=12.5, fill=INK_2),
        # legend (2 series)
        f'<circle cx="29" cy="81" r="5" fill="{BLUE}"/>',
        text(40, 85, "On the Pareto front", size=12.5, fill=INK_2),
        f'<circle cx="187" cy="81" r="5" fill="{MUTED}"/>',
        text(198, 85, "Dominated by another stack", size=12.5, fill=INK_2),
        text(left, 114, "FPR — share of benign traffic blocked", size=12, fill=MUTED),
    ]

    for i in range(5):
        v = i * 0.25
        y = sy(v)
        if v > 0:
            parts.append(f'<line x1="{left}" y1="{y:g}" x2="{right}" y2="{y:g}" '
                         f'stroke="{GRID}" stroke-width="1"/>')
        parts.append(text(left - 8, y + 4, f"{v:.2f}", size=12, fill=MUTED,
                          anchor="end", tabular=True))
    for i in range(6):
        v = i * 0.1
        x = sx(v)
        if v > 0:
            parts.append(f'<line x1="{x:g}" y1="{top}" x2="{x:g}" y2="{base}" '
                         f'stroke="{GRID}" stroke-width="1"/>')
        parts.append(text(x, base + 18, f"{v:.1f}", size=12, fill=MUTED,
                          anchor="middle", tabular=True))
    parts.append(f'<line x1="{left}" y1="{base}" x2="{right}" y2="{base}" '
                 f'stroke="{BASELINE}" stroke-width="1"/>')
    parts.append(text((left + right) / 2, base + 40, "ASR — share of attacks that succeed",
                      size=12, fill=MUTED, anchor="middle"))

    # Pareto front line beneath the dots
    front_xy = sorted((pts[s] for s in front), key=lambda p: p[0])
    line = " ".join(f"{sx(a):g},{sy(f):g}" for a, f in front_xy)
    parts.append(f'<polyline points="{line}" fill="none" stroke="{BLUE_SOFT}" '
                 f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')

    # one dot per distinct point; coincident stacks share a dot and a label block
    for (a, f) in sorted(set(pts.values())):
        names = [s for s in STACKS if pts[s] == (a, f)]
        on_front = names[0] in front
        parts.append(ringed_dot(sx(a), sy(f), BLUE if on_front else MUTED))

    ink = {True: INK, False: INK_2}
    wt = {True: 600, False: 400}
    x0, y0 = sx(0.0), sy(1.0)  # spotlight-deberta and spotlight-deberta-policy coincide
    parts += [
        text(x0 + 14, y0 - 2, "spotlight-deberta and", size=13, fill=ink[True], weight=wt[True]),
        text(x0 + 14, y0 + 14, "spotlight-deberta-policy", size=13, fill=ink[True],
             weight=wt[True]),
        text(x0 + 24, y0 + 30, "(coincident: every benign case blocked)", size=11.5, fill=MUTED),
        text(sx(pts["deberta"][0]) + 12, sy(pts["deberta"][1]) - 10, "deberta",
             size=13, fill=ink["deberta" in front], weight=wt["deberta" in front]),
        text(sx(pts["policy"][0]) - 9, base - 13, "policy",
             size=13, fill=ink["policy" in front], weight=wt["policy" in front], anchor="end"),
        text(sx(pts["spotlight"][0]) + 9, base - 13, "spotlight",
             size=13, fill=ink["spotlight" in front], weight=wt["spotlight" in front]),
        text(sx(pts["none"][0]), base - 15, "none",
             size=13, fill=ink["none" in front], weight=wt["none" in front], anchor="middle"),
    ]
    return svg_shell(w, h, "\n".join(parts))


def main() -> None:
    rows = load_rows(REPO / "results")
    rows = [r for r in rows if r["seed"] == "42" and r["model"] != "mock"]
    IMG.mkdir(parents=True, exist_ok=True)
    (IMG / "undefended-asr.svg").write_text(chart_undefended_asr(rows), encoding="utf-8")
    (IMG / "asr-vs-fpr-indirectrag.svg").write_text(chart_asr_vs_fpr(rows), encoding="utf-8")
    print(f"wrote {IMG / 'undefended-asr.svg'}")
    print(f"wrote {IMG / 'asr-vs-fpr-indirectrag.svg'}")


if __name__ == "__main__":
    main()
