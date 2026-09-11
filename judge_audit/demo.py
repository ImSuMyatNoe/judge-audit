"""The talk demo: six acts, no API keys, no network, ~6 minutes on stage.

    python -m judge_audit.demo             # all acts
    python -m judge_audit.demo --act 2     # just the survivorship act
    python -m judge_audit.demo --fast      # fewer bootstrap replicates
    python -m judge_audit.demo --export    # write data/ CSVs and figures/

Every number printed is computed at run time from the synthetic trace described
in judge_audit/simulate.py. Re-running gives identical output (fixed seeds).
"""

from __future__ import annotations

import argparse

import numpy as np
import pandas as pd

from . import metrics as M
from . import report as R
from . import simulate as S


def load(profile: S.JudgeProfile | None = None, n_items: int = 600) -> dict:
    return S.build_dataset(n_items=n_items, profile=profile)


# --------------------------------------------------------------------------- #


def act0(data: dict) -> None:
    items = data["items"]
    R.banner(
        "SYNTHETIC DATA. Nothing here is a real model's output. The simulator is "
        "calibrated to published effect sizes so the demo runs offline and "
        "reproducibly; the metrics are the reusable part -- point them at your own "
        "judge trace and the same audit runs on real data."
    )
    R.act(0, "The eval set", "What we are judging, and what the humans said about it.")
    R.table(
        [
            ("items", f"{len(items)}"),
            ("systems compared", ", ".join(sorted(items['system'].unique()))),
            ("judge passes per item", "3 (identical input each time)"),
            ("human graded score", "0-10 response quality"),
            ("human correctness", "binary agreement with the legal reference"),
            ("fluent-but-wrong items", f"{int(items['fluent_but_wrong'].sum())} "
                                       f"({items['fluent_but_wrong'].mean():.0%})"),
        ]
    )


def act1(data: dict) -> None:
    R.act(1, "Is your judge even a function?",
          "Same item, same prompt, same model, three passes. A measurement "
          "instrument returns the same reading twice.")
    rep = M.stability(data["trace"])
    R.table(rep.as_rows())
    R.note("ICC(1) is the share of score variance that comes from real "
           "differences between items rather than from the judge's own noise.")
    R.verdict(
        rep.exact_agreement > 0.90,
        f"only {rep.exact_agreement:.0%} of items got the same score all three times, "
        f"and {rep.flip_rate_at_threshold:.0%} changed their pass/fail verdict between runs",
    )
    R.takeaway(
        "If you report a single pass, a quarter of your pass/fail labels are a "
        "coin flip you did not know you were flipping. Report the score you got "
        "AND the spread across repeats, or stop calling it a measurement."
    )


def act2(data: dict) -> None:
    R.act(2, "The judge's silence is data",
          "Blank, unparseable and refused outputs are not missing at random. "
          "They cluster exactly where the answer was hard.")
    trace = data["trace"]
    rep = M.missingness(trace)
    R.table(rep.as_rows())
    print()
    strat = M.stratified(trace)
    strat = strat.rename(columns={
        "blank_rate": "blank", "r_scored_only": "r (scored)",
        "r_after_recovery": "r (recovered)", "judge_score_sd": "score SD",
    })
    R.frame(strat)
    r_easy = strat["r (scored)"].iloc[0]
    r_hard = strat["r (scored)"].iloc[-1]
    R.verdict(
        (r_easy - r_hard) < 0.10,
        f"agreement with humans runs {r_easy:.2f} on the clearest quarter and "
        f"{r_hard:.2f} on the most ambiguous quarter, where {strat['blank'].iloc[-1]:.0%} "
        "of attempts came back blank",
    )
    R.takeaway(
        "Your headline correlation is an average over a population your judge "
        "silently reshaped. It agrees with you on the items you did not need a "
        "judge for. Retry the blanks and the correlation gets worse -- that is the "
        "honest number, not a regression."
    )


def act3(data: dict) -> None:
    R.act(3, "Agreement that does not survive chance correction",
          "Most eval items are easy, and both raters say 'fine' a lot. "
          "Raw agreement prices that in as skill.")
    pi = data["per_item"]
    rep = M.agreement(pi["graded_score"], pi["human_score"])
    R.table(rep.as_rows())
    R.verdict(
        rep.cohens_kappa > 0.80,
        f"{rep.raw_agreement:.0%} raw agreement becomes kappa = {rep.cohens_kappa:.2f} "
        f"once you subtract what you would get by always guessing the majority class "
        f"({rep.majority_baseline:.0%})",
    )
    R.takeaway(
        "Never ship a raw agreement percentage. Report chance-corrected agreement "
        "and the majority baseline next to it, or the number is unreadable."
    )


def act4(data: dict) -> None:
    R.act(4, "One number cannot answer two questions",
          "'Is this a good answer?' and 'does this mean what the reference means?' "
          "are different questions. A graded judge only ever answers the first.")
    pi = data["per_item"]
    rep = M.dual_judge(pi)
    R.table(rep.as_rows())
    R.verdict(
        rep.graded_type1_on_fluent_wrong < 0.10,
        f"the graded judge waves through {rep.graded_type1_on_fluent_wrong:.0%} of "
        f"confident-but-wrong answers; adding a binary semantic-equivalence judge "
        f"cuts that to {rep.dual_type1_on_fluent_wrong:.0%} at almost no cost in "
        f"false rejects ({rep.graded_type2:.0%} -> {rep.dual_type2:.0%})",
    )
    R.takeaway(
        "A fluent wrong answer is the one case where a graded judge is confidently "
        "useless -- and in a legally grounded task it is the only case that matters. "
        "Pair the graded judge with a strict binary check against a human reference."
    )


def act5(data: dict) -> None:
    R.act(5, "Bias probes you can run today",
          "These need no new human labels. Run them before you trust a judge, "
          "not after a reviewer asks.")
    rep = M.biases(data["trace"], data["pairs"])
    R.table(rep.as_rows())
    R.note("Position consistency is measured by asking the same pairwise question "
           "twice with the candidates swapped. Zheng et al. (2023) report 65.0% for "
           "GPT-4 and 23.8% for Claude-v1, so a low number here is the norm.")
    R.verdict(
        rep.position_consistency > 0.90 and abs(rep.verbosity_partial_r) < 0.10,
        f"{1 - rep.position_consistency:.0%} of pairwise verdicts flip when you swap "
        f"the order, and length still predicts the score at partial r = "
        f"{rep.verbosity_partial_r:+.2f} after controlling for human-judged quality",
    )
    R.takeaway(
        "Swap-and-rejudge costs you one extra API call per pair and catches the "
        "single most embarrassing failure mode in the literature."
    )


def act6(data: dict, *, fast: bool = False) -> None:
    R.act(6, "The only number your team actually needs",
          "Not 'does the judge correlate with humans' but 'how often would it "
          "hand us the wrong shipping decision?'")
    pi = data["per_item"]
    n_boot = 400 if fast else 2000
    rep = M.decision_risk(pi, judge_col="graded_single_run", n_items=100,
                          n_bootstrap=n_boot)
    R.table(rep.as_rows())
    print()
    rows = []
    for k in (25, 50, 100, 200, 400, 800):
        r = M.decision_risk(pi, judge_col="graded_single_run", n_items=k,
                            n_bootstrap=n_boot, seed=k)
        rows.append({
            "items per system": k,
            "P(correct call)": 1 - r.wrong_winner_rate - r.inconclusive_rate,
            "P(wrong winner)": r.wrong_winner_rate,
            "P(tie)": r.inconclusive_rate,
        })
    R.frame(pd.DataFrame(rows))
    R.verdict(
        rows[2]["P(correct call)"] > 0.95,
        f"at 100 items per system the judge calls the winner correctly "
        f"{rows[2]['P(correct call)']:.0%} of the time -- the true gap is "
        f"{rep.human_margin:+.2f} points and the judge measures {rep.judge_margin:+.2f}",
    )
    R.takeaway(
        "Translate the judge's noise into decision risk before you use it to pick "
        "a model. 'r = 0.7' is not a decision; 'one call in four is wrong at our "
        "eval size' is."
    )


def act7(data: dict) -> None:
    R.act(7, "What the audit buys you",
          "Same eval set, same metrics, a judge built with a rubric, a reference "
          "answer, a retry-on-blank loop, repeated passes and a binary second judge.")
    careful = load(S.CAREFUL_PROFILE, n_items=len(data["items"]))
    a, b = data, careful

    sa, sb = M.stability(a["trace"]), M.stability(b["trace"])
    ma, mb = M.missingness(a["trace"]), M.missingness(b["trace"])
    da, db = M.dual_judge(a["per_item"]), M.dual_judge(b["per_item"])
    ba, bb = M.biases(a["trace"], a["pairs"]), M.biases(b["trace"], b["pairs"])

    R.compare(
        "as shipped", "after audit",
        [
            ("all 3 runs identical", f"{sa.exact_agreement:.0%}", f"{sb.exact_agreement:.0%}"),
            ("verdict flip rate", f"{sa.flip_rate_at_threshold:.0%}", f"{sb.flip_rate_at_threshold:.0%}"),
            ("ICC(1)", f"{sa.icc1:.2f}", f"{sb.icc1:.2f}"),
            ("blank rate", f"{ma.blank_rate:.0%}", f"{mb.blank_rate:.0%}"),
            ("r after recovery", f"{ma.r_after_recovery:.2f}", f"{mb.r_after_recovery:.2f}"),
            ("false accept, fluent-wrong", f"{da.graded_type1_on_fluent_wrong:.0%}", f"{db.dual_type1_on_fluent_wrong:.0%}"),
            ("position consistency", f"{ba.position_consistency:.0%}", f"{bb.position_consistency:.0%}"),
            ("length partial r", f"{ba.verbosity_partial_r:+.2f}", f"{bb.verbosity_partial_r:+.2f}"),
        ],
    )
    R.takeaway(
        "None of this makes the judge honest. It makes the judge's dishonesty "
        "measurable, which is the most you can ask of an instrument."
    )


ACTS = {0: act0, 1: act1, 2: act2, 3: act3, 4: act4, 5: act5, 6: act6, 7: act7}


def export(data: dict, out_dir: str = "data") -> None:
    import pathlib

    d = pathlib.Path(out_dir)
    d.mkdir(parents=True, exist_ok=True)
    for name in ("items", "trace", "pairs", "per_item"):
        data[name].to_csv(d / f"{name}.csv", index=False)
    M.stratified(data["trace"]).to_csv(d / "stratified.csv", index=False)
    print(f"\nwrote {out_dir}/items.csv, trace.csv, pairs.csv, per_item.csv, stratified.csv")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--act", type=int, action="append",
                    help="run only this act (repeatable); default is all of them")
    ap.add_argument("--items", type=int, default=600, help="eval set size")
    ap.add_argument("--fast", action="store_true", help="fewer bootstrap replicates")
    ap.add_argument("--export", action="store_true", help="write data/ CSVs")
    ap.add_argument("--figures", action="store_true", help="write figures/ PNGs")
    args = ap.parse_args(argv)

    np.set_printoptions(suppress=True)
    pd.set_option("display.width", 100)

    data = load(n_items=args.items)
    wanted = args.act or sorted(ACTS)
    for n in wanted:
        fn = ACTS.get(n)
        if fn is None:
            print(f"no such act: {n}")
            continue
        if n == 6:
            fn(data, fast=args.fast)
        else:
            fn(data)

    if args.export:
        export(data)
    if args.figures:
        from .figures import build_all

        build_all(data)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
