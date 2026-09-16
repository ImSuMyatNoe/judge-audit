"""Four stage scenarios, each runnable broken or fixed.

Every scenario answers the same question twice: what does this look like if you
measure it the way most harnesses do, and what does it look like once you
measure it honestly? The `--fix` flag switches between them, so a talk can show
red and green from one command.

    python -m judge_audit.scenarios 1            # broken
    python -m judge_audit.scenarios 1 --fix      # fixed
    python -m judge_audit.scenarios all --fix

Scenario 4 is the only one that needs a moment to run; it bootstraps.
"""

from __future__ import annotations

import argparse

from . import metrics as M
from . import report as R
from . import simulate as S

THRESHOLD = 7.0


def _data(n_items: int = 600):
    return S.build_dataset(n_items=n_items)


# --------------------------------------------------------------------------- #


def scenario_1(fix: bool) -> None:
    """Repeatability: one pass versus three."""
    R.act(1, "Repeatability", "Does the judge give the same answer twice?")
    data = _data()
    rep = M.stability(data["trace"], threshold=THRESHOLD)

    if not fix:
        one = data["trace"][data["trace"]["run"] == 1]["judge_score"].mean()
        R.table([
            ("what the harness reports", f"{one:.2f} / 10"),
            ("passes run", "1"),
            ("spread reported", "no"),
            ("unstable items surfaced", "no"),
        ])
        R.verdict(False,
                  "a single pass, reported as if it were a measurement -- the instability "
                  "exists, it is simply not visible from here")
        R.takeaway("Re-run this command with --fix to see what the same data looks like "
                   "when all three passes are reported.")
        return

    R.table(rep.as_rows())
    R.verdict(
        rep.exact_agreement > 0.90,
        f"three passes reported: {rep.exact_agreement:.0%} of items identical every time, "
        f"{rep.flip_rate_at_threshold:.0%} changed pass/fail verdict"
    )
    R.takeaway(
        "The fix is not a better judge. It is reporting the score AND the spread, and "
        "flagging the items whose verdict moved -- which the single-pass report silently "
        "rounded away."
    )


def scenario_2(fix: bool) -> None:
    """Hidden blanks: dropped rows versus retried rows."""
    R.act(2, "Hidden blanks", "What happens to the rows the judge never answered?")
    data = _data()
    trace = data["trace"]
    miss = M.missingness(trace)
    strat = M.stratified(trace)

    if not fix:
        R.table([
            ("rows the judge returned", f"{1 - miss.blank_rate:.0%}"),
            ("rows silently dropped", f"{miss.blank_rate:.0%}"),
            ("agreement on what survived", f"{strat['r_scored_only'].iloc[0]:.2f}"),
            ("agreement on what was dropped", "not measured"),
        ])
        R.verdict(False,
                  f"{miss.blank_rate:.0%} of attempts came back blank and were dropped before "
                  "anything was computed; the reported agreement describes only the rows the "
                  "judge was willing to score")
        R.takeaway("Re-run with --fix to retry the blanks and put them back.")
        return

    R.table(miss.as_rows())
    print()
    R.frame(strat.rename(columns={
        "blank_rate": "blank", "r_scored_only": "r (scored)",
        "r_after_recovery": "r (recovered)", "judge_score_sd": "score SD"}))
    R.verdict(
        False,
        f"blanks run {strat['blank_rate'].iloc[0]:.0%} on the clearest quarter and "
        f"{strat['blank_rate'].iloc[-1]:.0%} on the hardest; agreement across those same "
        f"quarters falls {strat['r_after_recovery'].iloc[0]:.2f} -> "
        f"{strat['r_after_recovery'].iloc[-1]:.2f}"
    )
    R.takeaway(
        "The honest number is the worse number. Publishing the post-recovery figure, and "
        "saying how many rows were recovered, is the whole fix."
    )


def scenario_3(fix: bool) -> None:
    """Agreement: raw percentage versus chance-corrected."""
    R.act(3, "Agreement", "Is 75% agreement good?")
    data = _data()
    pi = data["per_item"]
    rep = M.agreement(pi["graded_score"], pi["human_score"], threshold=THRESHOLD)

    if not fix:
        R.table([
            ("raw agreement with humans", f"{rep.raw_agreement:6.1%}"),
            ("reported as", "judge agrees with humans 75% of the time"),
        ])
        R.verdict(False,
                  "a bare agreement percentage, with nothing to compare it against")
        R.takeaway("Re-run with --fix to see the same number next to the baseline it has "
                   "to beat.")
        return

    R.table(rep.as_rows())
    R.verdict(
        rep.cohens_kappa > 0.80,
        f"{rep.raw_agreement:.0%} raw becomes kappa = {rep.cohens_kappa:.2f} once you subtract "
        f"what always guessing the common answer would score ({rep.majority_baseline:.0%})"
    )
    R.takeaway(
        "Report chance-corrected agreement with the majority baseline printed beside it, "
        "or the percentage is unreadable."
    )


def scenario_4(fix: bool, *, fast: bool = False) -> None:
    """Style over substance, and what the decision actually costs."""
    R.act(4, "Confident and wrong", "Does the judge reward being right, or reading well?")
    data = _data()
    pi = data["per_item"]
    dual = M.dual_judge(pi, threshold=THRESHOLD)

    if not fix:
        R.table([
            ("fluent-but-wrong responses", f"{dual.fluent_wrong_n}"),
            ("passed by the graded judge", f"{dual.graded_type1_on_fluent_wrong:6.1%}"),
            ("second opinion asked for", "no"),
        ])
        R.verdict(False,
                  f"the graded judge waves through {dual.graded_type1_on_fluent_wrong:.0%} of "
                  "confidently wrong answers -- they are well written, and that is what it "
                  "was asked to measure")
        R.takeaway("Re-run with --fix to add a binary semantic-equivalence judge.")
        return

    R.table(dual.as_rows())
    R.verdict(
        dual.dual_type1_on_fluent_wrong < 0.10,
        f"adding a binary check cuts false accepts on fluent-but-wrong answers from "
        f"{dual.graded_type1_on_fluent_wrong:.0%} to {dual.dual_type1_on_fluent_wrong:.0%}, "
        f"with false rejects unchanged ({dual.graded_type2:.0%} -> {dual.dual_type2:.0%})"
    )
    print()
    risk = M.decision_risk(pi, judge_col="graded_single_run", n_items=100,
                           n_bootstrap=400 if fast else 2000)
    R.table(risk.as_rows())
    R.takeaway(
        "Two judges answering two different questions, and the decision risk stated at your "
        "actual eval size. That is the difference between a score and a decision."
    )


SCENARIOS = {
    1: ("Repeatability", scenario_1),
    2: ("Hidden blanks", scenario_2),
    3: ("Agreement", scenario_3),
    4: ("Confident and wrong", scenario_4),
}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("scenario", help="1, 2, 3, 4, or 'all'")
    ap.add_argument("--fix", action="store_true",
                    help="run the audited version instead of the broken one")
    ap.add_argument("--fast", action="store_true", help="fewer bootstrap replicates")
    args = ap.parse_args(argv)

    if args.scenario == "all":
        keys = sorted(SCENARIOS)
    else:
        try:
            keys = [int(args.scenario)]
        except ValueError:
            print(f"no such scenario: {args.scenario}")
            return 2
        if keys[0] not in SCENARIOS:
            print(f"no such scenario: {args.scenario}")
            return 2

    if not args.fix:
        R.banner("BROKEN MODE -- this is how most harnesses measure. Add --fix to see the "
                 "same data measured honestly.")

    for k in keys:
        _, fn = SCENARIOS[k]
        if k == 4:
            fn(args.fix, fast=args.fast)
        else:
            fn(args.fix)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
