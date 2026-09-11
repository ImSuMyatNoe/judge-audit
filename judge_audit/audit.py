"""Run the audit on your own judge trace.

    python -m judge_audit.audit --input my_trace.csv
    python -m judge_audit.audit --input my_trace.csv --threshold 4 --scale 5
    python -m judge_audit.audit --input my_trace.csv --pairs my_pairs.csv --json out.json

Your CSV needs one row per (item, judging pass):

    item_id,run,judge_score,human_score
    it0001,1,8,7
    it0001,2,6,7
    it0001,3,,7          <- leave the cell EMPTY for a blank/unparseable/refused output

Optional columns, each unlocking one more section of the report:

    judge_score_recovered   the score after retrying a blank (survivorship check)
    difficulty_stratum      any grouping you like (stratified check)
    system                  which system produced the response (decision-risk check)
    equivalent              0/1 from a binary semantic-equivalence judge (dual-judge check)
    human_correct           0/1 ground-truth correctness (dual-judge check)
    fluent_but_wrong        0/1 flag for confident-but-wrong responses
    response_tokens         response length (verbosity check)

`--pairs` takes a second CSV with `winner_ab` and `winner_ba`: the judge's pick
with the two candidates presented in each order.

Nothing is uploaded anywhere; this reads your file and prints numbers.
"""

from __future__ import annotations

import argparse
import json
import sys

import pandas as pd

from . import metrics as M
from . import report as R

REQUIRED = ("item_id", "run", "judge_score", "human_score")


def run(
    trace: pd.DataFrame,
    pairs: pd.DataFrame | None = None,
    *,
    threshold: float = 7.0,
) -> dict:
    out: dict = {}

    R.act("A", "Stability", "Same input, repeated passes.")
    if trace["run"].nunique() < 2:
        R.note("Only one pass per item in this file -- re-run your harness at least "
               "3 times on the same inputs to get this section. It is the cheapest "
               "check in the report and the one most likely to change your mind.")
    else:
        s = M.stability(trace, threshold=threshold)
        R.table(s.as_rows())
        out["stability"] = s.__dict__

    R.act("B", "Missingness", "What the judge refused to score, and what that hides.")
    m = M.missingness(trace)
    R.table(m.as_rows())
    out["missingness"] = {k: v for k, v in m.__dict__.items()
                          if k != "blank_rate_by_stratum"}
    if "difficulty_stratum" in trace.columns:
        print()
        strat = M.stratified(trace)
        R.frame(strat)
        out["stratified"] = strat.to_dict(orient="records")
    else:
        R.note("Add a `difficulty_stratum` column to see where agreement actually "
               "lives. Any grouping works: annotator confidence, item length, "
               "source dataset, whether the image was occluded.")

    R.act("C", "Agreement", "Chance-corrected, next to the baseline it has to beat.")
    per_item = trace.groupby("item_id").agg(
        judge=("judge_score_recovered" if "judge_score_recovered" in trace.columns
               else "judge_score", "mean"),
        human=("human_score", "first"),
    )
    a = M.agreement(per_item["judge"], per_item["human"], threshold=threshold)
    R.table(a.as_rows())
    out["agreement"] = a.__dict__

    if {"equivalent", "human_correct"} <= set(trace.columns):
        R.act("D", "Dual judge", "Graded score alone vs graded + binary equivalence.")
        pi = trace.groupby("item_id").agg(
            graded_score=("judge_score_recovered" if "judge_score_recovered" in trace.columns
                          else "judge_score", "mean"),
            equivalent=("equivalent", lambda s: bool(s.mean() >= 0.5)),
            human_correct=("human_correct", "first"),
            fluent_but_wrong=("fluent_but_wrong", "first")
            if "fluent_but_wrong" in trace.columns else ("human_correct", "first"),
        ).reset_index()
        d = M.dual_judge(pi, threshold=threshold)
        R.table(d.as_rows())
        out["dual_judge"] = d.__dict__

    R.act("E", "Bias probes", "No new human labels needed.")
    b = M.biases(trace, pairs)
    R.table(b.as_rows())
    out["biases"] = b.__dict__

    if "system" in trace.columns and trace["system"].nunique() == 2:
        R.act("F", "Decision risk", "How often would this judge pick the wrong system?")
        pi = trace.groupby(["item_id", "system"], as_index=False).agg(
            judge_score=("judge_score", "mean"), human_score=("human_score", "first"))
        try:
            dr = M.decision_risk(pi)
            R.table(dr.as_rows())
            out["decision_risk"] = dr.__dict__
        except ValueError as exc:
            R.note(str(exc))

    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", required=True, help="CSV of judge scores (long format)")
    ap.add_argument("--pairs", help="CSV of pairwise comparisons judged in both orders")
    ap.add_argument("--threshold", type=float, default=7.0,
                    help="score at or above which a response counts as a pass")
    ap.add_argument("--json", help="also write the full report as JSON")
    args = ap.parse_args(argv)

    trace = pd.read_csv(args.input)
    missing = [c for c in REQUIRED if c not in trace.columns]
    if missing:
        print(f"error: {args.input} is missing required column(s): {', '.join(missing)}",
              file=sys.stderr)
        print(__doc__, file=sys.stderr)
        return 2

    pairs = pd.read_csv(args.pairs) if args.pairs else None
    out = run(trace, pairs, threshold=args.threshold)

    if args.json:
        with open(args.json, "w") as fh:
            json.dump(out, fh, indent=2, default=str)
        print(f"\nwrote {args.json}")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
