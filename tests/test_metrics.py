"""Tests for the audit metrics.

The metrics are the part of this repo anyone might run on real data, so they are
tested against cases whose answers are known analytically -- a perfectly stable
judge, a pure-noise judge, a judge that agrees with humans only by always saying
"pass" -- rather than against the simulator's output.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from judge_audit import metrics as M
from judge_audit import simulate as S


def _trace(scores_by_run: dict[int, list[float]], human: list[float]) -> pd.DataFrame:
    rows = []
    for run, scores in scores_by_run.items():
        for i, s in enumerate(scores):
            rows.append({"item_id": f"it{i}", "run": run, "judge_score": s,
                         "human_score": human[i]})
    return pd.DataFrame(rows)


# --- stability ------------------------------------------------------------- #


def test_perfect_stability():
    scores = [3, 5, 7, 9, 10, 2, 6, 8]
    t = _trace({1: scores, 2: scores, 3: scores}, human=scores)
    rep = M.stability(t)
    assert rep.exact_agreement == 1.0
    assert rep.mean_spread == 0.0
    assert rep.flip_rate_at_threshold == 0.0
    assert rep.icc1 == pytest.approx(1.0, abs=1e-9)


def test_pure_noise_has_no_signal():
    rng = np.random.default_rng(0)
    n = 400
    t = _trace(
        {r: list(rng.integers(0, 11, n).astype(float)) for r in (1, 2, 3)},
        human=list(rng.integers(0, 11, n).astype(float)),
    )
    rep = M.stability(t)
    assert abs(rep.icc1) < 0.15          # no between-item signal to find
    assert rep.exact_agreement < 0.10


def test_spread_and_flip_rate_are_counted():
    # item 0 is stable and passing; item 1 straddles the threshold.
    t = _trace({1: [9, 8], 2: [9, 6], 3: [9, 7]}, human=[9, 7])
    rep = M.stability(t, threshold=7.0)
    assert rep.flip_rate_at_threshold == 0.5
    assert rep.mean_spread == pytest.approx(1.0)


def test_stability_counts_items_that_are_always_blank():
    t = _trace({1: [5, np.nan], 2: [5, np.nan], 3: [5, np.nan]}, human=[5, 5])
    assert M.stability(t).n_items == 2


# --- missingness ----------------------------------------------------------- #


def test_blank_rate_and_partial_items():
    t = _trace({1: [5, np.nan, 7], 2: [5, np.nan, np.nan], 3: [5, np.nan, 7]},
               human=[5, 5, 7])
    rep = M.missingness(t)
    assert rep.blank_rate == pytest.approx(4 / 9)
    assert rep.items_never_scored == pytest.approx(1 / 3)
    assert rep.items_partially_scored == pytest.approx(1 / 3)


def test_survivorship_gap_is_positive_when_blanks_hide_hard_items():
    """Drop the items the judge scores worst and the correlation must improve."""
    rng = np.random.default_rng(3)
    n = 300
    human = rng.integers(0, 11, n).astype(float)
    easy = human[: n // 2] + rng.normal(0, 0.4, n // 2)          # judged well
    hard = rng.normal(6.5, 0.5, n - n // 2)                      # judged as noise
    judged = np.concatenate([easy, hard])
    blanked = judged.copy()
    blanked[n // 2:] = np.nan                                    # blanks on the hard half
    rows = []
    for i in range(n):
        rows.append({"item_id": f"it{i}", "run": 1, "judge_score": blanked[i],
                     "judge_score_recovered": judged[i], "human_score": human[i]})
    rep = M.missingness(pd.DataFrame(rows))
    assert rep.survivorship_gap > 0.2


# --- agreement ------------------------------------------------------------- #


def test_kappa_is_zero_for_a_constant_rater():
    """A judge that says "pass" to everything agrees a lot and knows nothing."""
    human = [9] * 80 + [2] * 20
    judge = [9] * 100
    rep = M.agreement(judge, human)
    assert rep.raw_agreement == pytest.approx(0.80)
    assert rep.cohens_kappa == pytest.approx(0.0, abs=1e-9)
    assert rep.majority_baseline == pytest.approx(0.80)


def test_kappa_is_one_for_a_perfect_rater():
    human = [9, 8, 2, 3, 10, 1]
    rep = M.agreement(human, human)
    assert rep.cohens_kappa == pytest.approx(1.0)
    assert rep.raw_agreement == 1.0


# --- dual judge ------------------------------------------------------------ #


def test_dual_judge_cannot_increase_false_accepts():
    """Adding an AND-ed second judge can only remove passes, never add them."""
    data = S.build_dataset(n_items=300)
    rep = M.dual_judge(data["per_item"])
    assert rep.dual_type1 <= rep.graded_type1 + 1e-9
    assert rep.dual_type2 >= rep.graded_type2 - 1e-9


def test_dual_judge_catches_fluent_wrong():
    df = pd.DataFrame({
        "graded_score": [9, 9, 9, 2],
        "equivalent": [False, False, True, True],
        "human_correct": [False, False, True, True],
        "fluent_but_wrong": [True, True, False, False],
    })
    rep = M.dual_judge(df)
    assert rep.graded_type1_on_fluent_wrong == pytest.approx(1.0)
    assert rep.dual_type1_on_fluent_wrong == pytest.approx(0.0)


# --- biases ---------------------------------------------------------------- #


def test_position_consistency_is_one_when_order_does_not_matter():
    pairs = pd.DataFrame({"winner_ab": ["A", "B", "A"], "winner_ba": ["A", "B", "A"]})
    trace = _trace({1: [5, 6, 7]}, human=[5, 6, 7])
    rep = M.biases(trace, pairs)
    assert rep.position_consistency == pytest.approx(1.0)


def test_verbosity_slope_detects_length_preference():
    rng = np.random.default_rng(1)
    n = 400
    quality = rng.uniform(0, 10, n)
    length = rng.normal(200, 50, n)
    score = quality + 0.02 * (length - 200) + rng.normal(0, 0.2, n)
    trace = pd.DataFrame({
        "item_id": [f"it{i}" for i in range(n)], "run": 1,
        "judge_score": score, "human_score": quality, "response_tokens": length,
    })
    rep = M.biases(trace)
    assert rep.verbosity_partial_r > 0.5


def test_scale_entropy_is_zero_for_a_one_score_judge():
    trace = _trace({1: [7] * 50}, human=[5] * 50)
    assert M.biases(trace).scale_entropy == pytest.approx(0.0)


# --- decision risk --------------------------------------------------------- #


def test_decision_risk_is_zero_when_the_judge_is_the_truth():
    df = pd.DataFrame({
        "system": ["a"] * 200 + ["b"] * 200,
        "judge_score": list(np.linspace(5, 10, 200)) + list(np.linspace(0, 5, 200)),
    })
    df["human_score"] = df["judge_score"]
    rep = M.decision_risk(df, n_items=100, n_bootstrap=300)
    assert rep.wrong_winner_rate == 0.0


def test_decision_risk_rejects_more_than_two_systems():
    df = pd.DataFrame({"system": ["a", "b", "c"], "judge_score": [1, 2, 3],
                       "human_score": [1, 2, 3]})
    with pytest.raises(ValueError):
        M.decision_risk(df)


# --- simulator contract ---------------------------------------------------- #


def test_simulation_is_deterministic():
    a = S.build_dataset(n_items=120)
    b = S.build_dataset(n_items=120)
    pd.testing.assert_frame_equal(a["trace"], b["trace"])


def test_careful_profile_is_actually_better():
    base = S.build_dataset(n_items=400)
    careful = S.build_dataset(n_items=400, profile=S.CAREFUL_PROFILE)
    assert M.stability(careful["trace"]).icc1 > M.stability(base["trace"]).icc1
    assert M.missingness(careful["trace"]).blank_rate < M.missingness(base["trace"]).blank_rate
