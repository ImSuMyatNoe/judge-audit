"""Figures for the talk. Matplotlib, no seaborn, no styles beyond what is set here.

    python -m judge_audit.demo --figures

Colours come from a validated categorical palette (blue / orange / red, with
grey chrome), used at most three at a time so the charts survive colour-vision
deficiency and greyscale printing. Every chart is also direct-labelled, so no
reading depends on colour alone.
"""

from __future__ import annotations

import pathlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from . import metrics as M  # noqa: E402
from . import simulate as S  # noqa: E402

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
BLUE = "#2a78d6"
ORANGE = "#eb6834"
RED = "#d03b3b"
GREEN = "#0ca30c"

FIG_DIR = pathlib.Path("figures")


def _style(ax, *, ylabel: str = "", title: str = "", subtitle: str = "") -> None:
    ax.set_facecolor(SURFACE)
    ax.figure.set_facecolor(SURFACE)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color("#c3c2b7")
        ax.spines[side].set_linewidth(0.8)
    ax.tick_params(colors=MUTED, labelsize=9, length=3)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    if ylabel:
        ax.set_ylabel(ylabel, color=INK_2, fontsize=9)
    if title:
        ax.set_title(title, color=INK, fontsize=12, fontweight="bold", loc="left", pad=16)
    if subtitle:
        ax.text(0, 1.02, subtitle, transform=ax.transAxes, color=INK_2,
                fontsize=9, va="bottom")


def _save(fig, name: str) -> pathlib.Path:
    FIG_DIR.mkdir(exist_ok=True)
    path = FIG_DIR / name
    fig.savefig(path, dpi=200, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)
    return path


# --------------------------------------------------------------------------- #


def fig_stability(data: dict) -> pathlib.Path:
    """Three passes over the same 40 items: the range each item's score covers."""
    trace = data["trace"]
    wide = trace.pivot_table(index="item_id", columns="run", values="judge_score")
    wide = wide.dropna().head(40)
    order = wide.mean(axis=1).sort_values().index
    wide = wide.loc[order]
    x = np.arange(len(wide))

    fig, ax = plt.subplots(figsize=(9, 3.4))
    lo, hi = wide.min(axis=1).to_numpy(), wide.max(axis=1).to_numpy()
    ax.vlines(x, lo, hi, color=GRID, linewidth=6, zorder=1)
    for i, run in enumerate(wide.columns):
        ax.scatter(x, wide[run], s=26, zorder=3,
                   color=[BLUE, ORANGE, RED][i % 3],
                   label=f"pass {run}", edgecolor=SURFACE, linewidth=1.2)
    unstable = (hi - lo) >= 2
    ax.scatter(x[unstable], np.full(unstable.sum(), 11.4), marker="v", s=22,
               color=RED, zorder=4)
    _style(ax, ylabel="judge score (0-10)",
           title="The same item, judged three times",
           subtitle="40 items, identical prompt each pass. Markers show the three "
                    "scores; the bar is the range. Arrows: 2+ points of spread.")
    ax.set_xticks([])
    ax.set_xlabel("items, ordered by mean score", color=INK_2, fontsize=9)
    ax.set_ylim(0, 12.2)
    ax.set_yticks([0, 2, 4, 6, 8, 10])
    ax.legend(frameon=False, fontsize=9, labelcolor=INK_2, ncol=3,
              loc="lower right", bbox_to_anchor=(1.0, -0.02))
    return _save(fig, "01_stability.png")


def fig_stratified(data: dict) -> pathlib.Path:
    """Two panels, one scale each -- never a second y-axis on one plot."""
    strat = M.stratified(data["trace"])
    labels = [s.replace(" ", "\n", 1) for s in strat["stratum"]]
    x = np.arange(len(strat))

    fig, axes = plt.subplots(1, 2, figsize=(9.5, 3.6))
    ax = axes[0]
    bars = ax.bar(x, strat["blank_rate"], color=ORANGE, width=0.62)
    for b, v in zip(bars, strat["blank_rate"]):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.015, f"{v:.0%}",
                ha="center", color=INK, fontsize=9, fontweight="bold")
    _style(ax, ylabel="blank / unparseable rate",
           title="Where the judge goes quiet")
    ax.set_xticks(x, labels, color=INK_2)
    ax.set_ylim(0, max(strat["blank_rate"]) * 1.25)
    ax.yaxis.set_major_formatter(lambda v, _: f"{v:.0%}")

    ax = axes[1]
    bars = ax.bar(x, strat["r_after_recovery"], color=BLUE, width=0.62)
    for b, v in zip(bars, strat["r_after_recovery"]):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.02, f"{v:.2f}",
                ha="center", color=INK, fontsize=9, fontweight="bold")
    _style(ax, ylabel="r (judge, human)",
           title="...and where its agreement lives")
    ax.set_xticks(x, labels, color=INK_2)
    ax.set_ylim(0, 0.95)
    fig.text(0, -0.04, "Items split into quartiles by ambiguity. Same eval set, "
                       "same judge, same prompt.", color=INK_2, fontsize=9)
    fig.tight_layout()
    return _save(fig, "02_stratified.png")


def fig_dual_judge(data: dict) -> pathlib.Path:
    rep = M.dual_judge(data["per_item"])
    labels = ["graded judge\nalone", "graded + binary\nequivalence judge"]
    vals = [rep.graded_type1_on_fluent_wrong, rep.dual_type1_on_fluent_wrong]
    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    bars = ax.bar(labels, vals, color=[RED, GREEN], width=0.5)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.02, f"{v:.0%}",
                ha="center", color=INK, fontsize=13, fontweight="bold")
    _style(ax, ylabel="false-accept rate",
           title="Confident, fluent, and wrong",
           subtitle=f"Share of the {rep.fluent_wrong_n} fluent-but-wrong responses "
                    f"that each protocol passes as acceptable.")
    ax.set_ylim(0, 1.05)
    ax.yaxis.set_major_formatter(lambda v, _: f"{v:.0%}")
    ax.tick_params(axis="x", labelcolor=INK_2, labelsize=10)
    return _save(fig, "03_dual_judge.png")


def fig_decision_risk(data: dict, n_bootstrap: int = 2000) -> pathlib.Path:
    sizes = [25, 50, 100, 200, 400, 800]
    correct = []
    for k in sizes:
        r = M.decision_risk(data["per_item"], judge_col="graded_single_run",
                            n_items=k, n_bootstrap=n_bootstrap, seed=k)
        correct.append(1 - r.wrong_winner_rate - r.inconclusive_rate)

    fig, ax = plt.subplots(figsize=(7, 3.6))
    ax.axhline(0.90, color=MUTED, linewidth=1, linestyle=(0, (4, 3)))
    ax.text(sizes[0], 0.905, "90% of calls correct", color=INK_2, fontsize=9, va="bottom")
    ax.plot(sizes, correct, color=BLUE, linewidth=2, marker="o", markersize=7,
            markeredgecolor=SURFACE, markeredgewidth=1.4)
    for k, v in zip(sizes, correct):
        if k in (25, 100, 800):
            ax.annotate(f"{v:.0%}", (k, v), textcoords="offset points",
                        xytext=(0, 10), ha="center", color=INK,
                        fontsize=10, fontweight="bold")
    _style(ax, ylabel="P(judge picks the better system)",
           title="How big does your eval set have to be to trust the verdict?",
           subtitle="Bootstrap over items; the two systems really do differ, "
                    "and the judge has to find it.")
    ax.set_xscale("log")
    ax.set_xticks(sizes, [str(s) for s in sizes], color=INK_2)
    ax.set_xlabel("items per system", color=INK_2, fontsize=9)
    ax.set_ylim(0.4, 1.03)
    ax.yaxis.set_major_formatter(lambda v, _: f"{v:.0%}")
    return _save(fig, "04_decision_risk.png")


def fig_before_after(data: dict) -> pathlib.Path:
    careful = S.build_dataset(n_items=len(data["items"]), profile=S.CAREFUL_PROFILE)
    pairs = [
        ("all 3 passes identical",
         M.stability(data["trace"]).exact_agreement,
         M.stability(careful["trace"]).exact_agreement),
        ("verdict stable across passes",
         1 - M.stability(data["trace"]).flip_rate_at_threshold,
         1 - M.stability(careful["trace"]).flip_rate_at_threshold),
        ("items scored, not blank",
         1 - M.missingness(data["trace"]).blank_rate,
         1 - M.missingness(careful["trace"]).blank_rate),
        ("fluent-wrong caught",
         1 - M.dual_judge(data["per_item"]).graded_type1_on_fluent_wrong,
         1 - M.dual_judge(careful["per_item"]).dual_type1_on_fluent_wrong),
    ]
    labels = [p[0] for p in pairs]
    before = [p[1] for p in pairs]
    after = [p[2] for p in pairs]
    y = np.arange(len(pairs))
    h = 0.34

    fig, ax = plt.subplots(figsize=(8, 3.6))
    ax.barh(y + h / 2, before, height=h, color=ORANGE, label="as shipped")
    ax.barh(y - h / 2, after, height=h, color=BLUE, label="after the audit")
    for yy, v in zip(y + h / 2, before):
        ax.text(v + 0.015, yy, f"{v:.0%}", va="center", color=INK, fontsize=9)
    for yy, v in zip(y - h / 2, after):
        ax.text(v + 0.015, yy, f"{v:.0%}", va="center", color=INK, fontsize=9,
                fontweight="bold")
    _style(ax, title="What the audit buys you",
           subtitle="Same eval set and metrics; a judge with a rubric, a reference "
                    "answer, retries, repeats and a second binary judge.")
    ax.set_yticks(y, labels, color=INK_2)
    ax.set_xlim(0, 1.15)
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.xaxis.set_major_formatter(lambda v, _: f"{v:.0%}")
    ax.legend(frameon=False, fontsize=9, labelcolor=INK_2, loc="lower right")
    return _save(fig, "05_before_after.png")


def build_all(data: dict | None = None) -> list[pathlib.Path]:
    data = data or S.build_dataset()
    paths = [
        fig_stability(data),
        fig_stratified(data),
        fig_dual_judge(data),
        fig_decision_risk(data),
        fig_before_after(data),
    ]
    print("\nwrote " + ", ".join(str(p) for p in paths))
    return paths


if __name__ == "__main__":
    build_all()
