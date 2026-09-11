"""Audit metrics for LLM-as-a-judge output.

Nothing in this module knows or cares where the scores came from. Point it at
your own judge traces (see docs/using-your-own-data.md) and it will compute the
same numbers the talk demo computes.

Conventions
-----------
A *trace* is a long-format table with one row per (item, run):

    item_id, run, judge_score, human_score, [blank], [system], ...

`judge_score` may be NaN, which means the judge produced nothing usable on that
attempt (empty string, unparseable output, refusal, API error). Those rows are
the most informative rows in the file and this module never silently drops them.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

import numpy as np
import pandas as pd

# --------------------------------------------------------------------------- #
# 1. Stability: is the judge even a function?
# --------------------------------------------------------------------------- #


@dataclass
class StabilityReport:
    n_items: int
    n_runs: int
    exact_agreement: float          # share of items where all runs agree exactly
    within_one: float               # share of items where max-min <= 1
    mean_spread: float              # mean (max - min) per item
    p95_spread: float
    mean_within_item_sd: float
    icc1: float                     # ICC(1): share of variance that is signal
    flip_rate_at_threshold: float   # share of items whose pass/fail verdict changes
    threshold: float

    def as_rows(self) -> list[tuple[str, str]]:
        return [
            ("items x runs", f"{self.n_items} x {self.n_runs}"),
            ("all runs identical", f"{self.exact_agreement:6.1%}"),
            ("all runs within 1 point", f"{self.within_one:6.1%}"),
            ("mean spread (max-min)", f"{self.mean_spread:6.2f} pts"),
            ("95th pct spread", f"{self.p95_spread:6.2f} pts"),
            ("mean within-item SD", f"{self.mean_within_item_sd:6.2f} pts"),
            ("ICC(1) signal share", f"{self.icc1:6.3f}"),
            (f"verdict flips at >={self.threshold:g}", f"{self.flip_rate_at_threshold:6.1%}"),
        ]


def icc1(wide: pd.DataFrame) -> float:
    """ICC(1) from a one-way random-effects ANOVA.

    `wide` is items x runs. Returns the share of total variance attributable to
    real between-item differences. 1.0 = the judge is a function of the item;
    0.0 = the score is a coin flip that happens to live on a 0-10 scale.

    Rows with any missing value are dropped (documented, not silent: callers
    should report the blank rate alongside this number).
    """
    m = wide.dropna(axis=0, how="any").to_numpy(dtype=float)
    n, k = m.shape
    if n < 2 or k < 2:
        return float("nan")
    grand = m.mean()
    row_means = m.mean(axis=1)
    # Between-item and within-item mean squares.
    ms_between = k * ((row_means - grand) ** 2).sum() / (n - 1)
    ms_within = ((m - row_means[:, None]) ** 2).sum() / (n * (k - 1))
    denom = ms_between + (k - 1) * ms_within
    if denom == 0:
        return float("nan")
    return float((ms_between - ms_within) / denom)


def stability(
    trace: pd.DataFrame,
    *,
    item_col: str = "item_id",
    run_col: str = "run",
    score_col: str = "judge_score",
    threshold: float = 7.0,
) -> StabilityReport:
    """Run-to-run behaviour of a judge scored repeatedly on identical input."""
    wide = trace.pivot_table(index=item_col, columns=run_col, values=score_col, dropna=False)
    complete = wide.dropna(axis=0, how="any")
    spread = (complete.max(axis=1) - complete.min(axis=1))
    passes = (complete >= threshold)
    flips = passes.nunique(axis=1) > 1
    return StabilityReport(
        n_items=int(wide.shape[0]),
        n_runs=int(wide.shape[1]),
        exact_agreement=float((spread == 0).mean()) if len(spread) else float("nan"),
        within_one=float((spread <= 1).mean()) if len(spread) else float("nan"),
        mean_spread=float(spread.mean()) if len(spread) else float("nan"),
        p95_spread=float(spread.quantile(0.95)) if len(spread) else float("nan"),
        mean_within_item_sd=float(complete.std(axis=1, ddof=1).mean()) if len(complete) else float("nan"),
        icc1=icc1(wide),
        flip_rate_at_threshold=float(flips.mean()) if len(flips) else float("nan"),
        threshold=threshold,
    )


# --------------------------------------------------------------------------- #
# 2. Missingness: the judge's silence is data
# --------------------------------------------------------------------------- #


@dataclass
class MissingnessReport:
    blank_rate: float
    blank_rate_by_stratum: pd.Series
    items_never_scored: float
    items_partially_scored: float
    r_complete_only: float          # judge-human correlation on always-parseable items
    r_after_recovery: float         # ... after the blanks are retried and recovered
    n_complete_only: int
    n_after_recovery: int

    @property
    def survivorship_gap(self) -> float:
        return self.r_complete_only - self.r_after_recovery

    def as_rows(self) -> list[tuple[str, str]]:
        return [
            ("blank / unparseable rate", f"{self.blank_rate:6.1%}"),
            ("items blank on every run", f"{self.items_never_scored:6.1%}"),
            ("items blank on some runs", f"{self.items_partially_scored:6.1%}"),
            ("r(judge, human), complete-only", f"{self.r_complete_only:6.3f}  (n={self.n_complete_only})"),
            ("r(judge, human), after recovery", f"{self.r_after_recovery:6.3f}  (n={self.n_after_recovery})"),
            ("survivorship gap", f"{self.survivorship_gap:+6.3f}"),
        ]


def _pearson(a: Sequence[float], b: Sequence[float]) -> float:
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    ok = ~(np.isnan(a) | np.isnan(b))
    if ok.sum() < 3:
        return float("nan")
    a, b = a[ok], b[ok]
    if a.std() == 0 or b.std() == 0:
        return float("nan")
    return float(np.corrcoef(a, b)[0, 1])


def missingness(
    trace: pd.DataFrame,
    *,
    item_col: str = "item_id",
    run_col: str = "run",
    score_col: str = "judge_score",
    human_col: str = "human_score",
    recovered_col: str | None = "judge_score_recovered",
    stratum_col: str | None = "difficulty_stratum",
) -> MissingnessReport:
    """Quantify what the judge refuses to answer, and what that refusal buys it.

    The headline pair is `r_complete_only` vs `r_after_recovery`: the first is
    the number most eval reports publish, the second is the number after you go
    back and get a score for the items the judge originally choked on.
    """
    wide = trace.pivot_table(index=item_col, columns=run_col, values=score_col, dropna=False)
    per_item_blank = wide.isna()
    n_items = len(wide)

    by_stratum = pd.Series(dtype=float)
    if stratum_col and stratum_col in trace.columns:
        by_stratum = trace.groupby(stratum_col)[score_col].apply(lambda s: float(s.isna().mean()))

    human = trace.groupby(item_col)[human_col].first()
    complete_items = per_item_blank.sum(axis=1) == 0

    # Both correlations are computed the way a single pass of your harness would
    # compute them -- one score per item, not an average over repeats -- and then
    # averaged across the passes you happen to have. Averaging runs first would
    # cancel exactly the noise this comparison is trying to expose.
    r_per_run, n_per_run = [], []
    for run in wide.columns:
        col = wide[run]
        ok = col.notna()
        r_per_run.append(_pearson(col[ok], human[ok]))
        n_per_run.append(int(ok.sum()))
    valid = [r for r in r_per_run if not np.isnan(r)]
    r_complete = float(np.mean(valid)) if valid else float("nan")
    n_complete = int(np.mean(n_per_run)) if n_per_run else 0

    if recovered_col and recovered_col in trace.columns:
        rec_wide = trace.pivot_table(index=item_col, columns=run_col, values=recovered_col, dropna=False)
        rr, nn = [], []
        for run in rec_wide.columns:
            col = rec_wide[run]
            ok = col.notna()
            rr.append(_pearson(col[ok], human[ok]))
            nn.append(int(ok.sum()))
        valid_rr = [r for r in rr if not np.isnan(r)]
        r_recovered = float(np.mean(valid_rr)) if valid_rr else float("nan")
        n_recovered = int(np.mean(nn)) if nn else 0
    else:
        r_recovered = float("nan")
        n_recovered = 0

    return MissingnessReport(
        blank_rate=float(trace[score_col].isna().mean()),
        blank_rate_by_stratum=by_stratum,
        items_never_scored=float((per_item_blank.all(axis=1)).mean()) if n_items else float("nan"),
        items_partially_scored=float(
            ((per_item_blank.any(axis=1)) & (~per_item_blank.all(axis=1))).mean()
        ) if n_items else float("nan"),
        r_complete_only=r_complete,
        r_after_recovery=r_recovered,
        n_complete_only=n_complete,
        n_after_recovery=n_recovered,
    )


def stratified(
    trace: pd.DataFrame,
    *,
    stratum_col: str = "difficulty_stratum",
    item_col: str = "item_id",
    score_col: str = "judge_score",
    recovered_col: str = "judge_score_recovered",
    human_col: str = "human_score",
) -> pd.DataFrame:
    """Blank rate and judge-human correlation, per difficulty stratum.

    This is the table that decides whether an aggregate correlation means
    anything. If agreement is carried by the stratum where the answer was never
    in doubt, the judge is confirming your easy cases and guessing on the rest --
    and the single pooled number cannot tell you that.
    """
    rows = []
    for name, g in trace.groupby(stratum_col, observed=True):
        n_items = g[item_col].nunique()
        rows.append(
            {
                "stratum": name,
                "items": n_items,
                "blank_rate": float(g[score_col].isna().mean()),
                "r_scored_only": _pearson(g[score_col], g[human_col]),
                "r_after_recovery": (
                    _pearson(g[recovered_col], g[human_col])
                    if recovered_col in g.columns else float("nan")
                ),
                "judge_score_sd": float(g[recovered_col].std())
                if recovered_col in g.columns else float("nan"),
            }
        )
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------- #
# 3. Agreement that survives chance correction
# --------------------------------------------------------------------------- #


@dataclass
class AgreementReport:
    raw_agreement: float
    cohens_kappa: float
    majority_baseline: float
    pearson: float
    spearman: float
    kendall_tau_b: float

    @property
    def kappa_deflation(self) -> float:
        return self.raw_agreement - self.cohens_kappa

    def as_rows(self) -> list[tuple[str, str]]:
        return [
            ("raw exact agreement", f"{self.raw_agreement:6.1%}"),
            ("always-guess-majority baseline", f"{self.majority_baseline:6.1%}"),
            ("Cohen's kappa", f"{self.cohens_kappa:6.3f}"),
            ("deflation (raw - kappa)", f"{self.kappa_deflation:+6.1%}"),
            ("Pearson r", f"{self.pearson:6.3f}"),
            ("Spearman rho", f"{self.spearman:6.3f}"),
            ("Kendall tau-b", f"{self.kendall_tau_b:6.3f}"),
        ]


def cohens_kappa(a: Sequence, b: Sequence) -> float:
    a = pd.Series(list(a))
    b = pd.Series(list(b))
    ok = a.notna() & b.notna()
    a, b = a[ok], b[ok]
    if len(a) == 0:
        return float("nan")
    labels = sorted(set(a) | set(b))
    idx = {lab: i for i, lab in enumerate(labels)}
    n = len(a)
    obs = sum(1 for x, y in zip(a, b) if x == y) / n
    pa = a.value_counts(normalize=True)
    pb = b.value_counts(normalize=True)
    exp = sum(pa.get(lab, 0.0) * pb.get(lab, 0.0) for lab in labels)
    if exp >= 1.0:
        return float("nan")
    return float((obs - exp) / (1 - exp))


def agreement(
    judge: Sequence[float],
    human: Sequence[float],
    *,
    threshold: float = 7.0,
) -> AgreementReport:
    """Instance-level agreement, reported the way it should be reported.

    Raw agreement is the number that looks good in a slide; kappa is the number
    that survives the observation that most items are easy and both raters are
    saying "fine" a lot.
    """
    j = pd.Series(list(judge), dtype=float)
    h = pd.Series(list(human), dtype=float)
    ok = j.notna() & h.notna()
    j, h = j[ok], h[ok]
    jb = (j >= threshold)
    hb = (h >= threshold)
    maj = max(hb.mean(), 1 - hb.mean())
    from scipy import stats  # local import keeps module importable without scipy

    return AgreementReport(
        raw_agreement=float((jb == hb).mean()),
        cohens_kappa=cohens_kappa(jb, hb),
        majority_baseline=float(maj),
        pearson=_pearson(j, h),
        spearman=float(stats.spearmanr(j, h).statistic),
        kendall_tau_b=float(stats.kendalltau(j, h, variant="b").statistic),
    )


# --------------------------------------------------------------------------- #
# 4. Dual judge: one number cannot see two failure modes
# --------------------------------------------------------------------------- #


@dataclass
class DualJudgeReport:
    n: int
    graded_pass_rate: float
    binary_pass_rate: float
    human_pass_rate: float
    graded_type1: float             # judge passes it, reference says wrong
    graded_type2: float             # judge fails it, reference says right
    dual_type1: float
    dual_type2: float
    fluent_wrong_n: int
    graded_type1_on_fluent_wrong: float
    dual_type1_on_fluent_wrong: float

    def as_rows(self) -> list[tuple[str, str]]:
        return [
            ("items", f"{self.n}"),
            ("graded judge pass rate", f"{self.graded_pass_rate:6.1%}"),
            ("equivalence judge pass rate", f"{self.binary_pass_rate:6.1%}"),
            ("human reference pass rate", f"{self.human_pass_rate:6.1%}"),
            ("graded-only  false accept (Type I)", f"{self.graded_type1:6.1%}"),
            ("graded-only  false reject (Type II)", f"{self.graded_type2:6.1%}"),
            ("dual-judge   false accept (Type I)", f"{self.dual_type1:6.1%}"),
            ("dual-judge   false reject (Type II)", f"{self.dual_type2:6.1%}"),
            (f"-- on the {self.fluent_wrong_n} fluent-but-wrong items --", ""),
            ("graded-only false accept", f"{self.graded_type1_on_fluent_wrong:6.1%}"),
            ("dual-judge  false accept", f"{self.dual_type1_on_fluent_wrong:6.1%}"),
        ]


def dual_judge(
    df: pd.DataFrame,
    *,
    graded_col: str = "graded_score",
    binary_col: str = "equivalent",
    human_col: str = "human_correct",
    fluent_wrong_col: str = "fluent_but_wrong",
    threshold: float = 7.0,
) -> DualJudgeReport:
    """Compare a graded 0-10 judge against a graded + binary-equivalence pair.

    The graded judge answers "is this a good answer?". The binary judge answers
    "does this mean the same thing as the reference?". Those are different
    questions, and a response can score 8/10 on the first while failing the
    second outright -- which is exactly the case that matters in a legally
    grounded task, where a confident wrong reading is worse than a hedge.
    """
    d = df.dropna(subset=[graded_col, binary_col, human_col])
    graded_pass = d[graded_col] >= threshold
    binary_pass = d[binary_col].astype(bool)
    dual_pass = graded_pass & binary_pass
    truth = d[human_col].astype(bool)

    def t1(pred):  # false accept: predicted pass, actually wrong
        neg = ~truth
        return float((pred & neg).sum() / neg.sum()) if neg.sum() else float("nan")

    def t2(pred):  # false reject: predicted fail, actually right
        pos = truth
        return float(((~pred) & pos).sum() / pos.sum()) if pos.sum() else float("nan")

    fw = d[fluent_wrong_col].astype(bool) if fluent_wrong_col in d.columns else pd.Series(False, index=d.index)
    fw_n = int(fw.sum())

    def t1_on(pred, mask):
        sub = mask & (~truth)
        return float((pred & sub).sum() / sub.sum()) if sub.sum() else float("nan")

    return DualJudgeReport(
        n=len(d),
        graded_pass_rate=float(graded_pass.mean()),
        binary_pass_rate=float(binary_pass.mean()),
        human_pass_rate=float(truth.mean()),
        graded_type1=t1(graded_pass),
        graded_type2=t2(graded_pass),
        dual_type1=t1(dual_pass),
        dual_type2=t2(dual_pass),
        fluent_wrong_n=fw_n,
        graded_type1_on_fluent_wrong=t1_on(graded_pass, fw),
        dual_type1_on_fluent_wrong=t1_on(dual_pass, fw),
    )


# --------------------------------------------------------------------------- #
# 5. The only question a practitioner actually has
# --------------------------------------------------------------------------- #


@dataclass
class DecisionRiskReport:
    n_items: int
    n_bootstrap: int
    human_margin: float             # system A minus system B, human scores
    judge_margin: float
    wrong_winner_rate: float        # P(judge ranks the worse system first)
    inconclusive_rate: float        # P(judge sees a dead heat)
    items_needed_for_90pct: int | None

    def as_rows(self) -> list[tuple[str, str]]:
        rows = [
            ("items per system", f"{self.n_items}"),
            ("bootstrap replicates", f"{self.n_bootstrap}"),
            ("true margin (human)", f"{self.human_margin:+6.2f} pts"),
            ("measured margin (judge)", f"{self.judge_margin:+6.2f} pts"),
            ("P(judge picks the worse system)", f"{self.wrong_winner_rate:6.1%}"),
            ("P(judge calls it a tie)", f"{self.inconclusive_rate:6.1%}"),
        ]
        rows.append((
            "items for 90% correct calls",
            f"{self.items_needed_for_90pct}" if self.items_needed_for_90pct else "not reached in range",
        ))
        return rows


def decision_risk(
    df: pd.DataFrame,
    *,
    system_col: str = "system",
    judge_col: str = "judge_score",
    human_col: str = "human_score",
    n_items: int | None = None,
    n_bootstrap: int = 2000,
    tie_band: float = 0.05,
    seed: int = 0,
    sample_sizes: Iterable[int] = (25, 50, 100, 200, 400, 800, 1600),
) -> DecisionRiskReport:
    """How often would this judge hand you the wrong shipping decision?

    Bootstrap-resample items, recompute each system's mean judge score, and count
    how often the judge's winner disagrees with the human winner. This converts
    "our judge correlates 0.8 with humans" into the number a team can act on.
    """
    rng = np.random.default_rng(seed)
    systems = sorted(df[system_col].dropna().unique())
    if len(systems) != 2:
        raise ValueError(f"decision_risk compares exactly two systems, got {systems}")
    a, b = systems
    da = df[df[system_col] == a]
    db = df[df[system_col] == b]

    human_margin = da[human_col].mean() - db[human_col].mean()
    judge_margin = da[judge_col].mean() - db[judge_col].mean()
    true_winner = a if human_margin > 0 else b

    def simulate(k: int) -> tuple[float, float]:
        wrong = 0
        tie = 0
        ja = da[judge_col].dropna().to_numpy()
        jb = db[judge_col].dropna().to_numpy()
        for _ in range(n_bootstrap):
            sa = rng.choice(ja, size=k, replace=True).mean()
            sb = rng.choice(jb, size=k, replace=True).mean()
            diff = sa - sb
            if abs(diff) < tie_band:
                tie += 1
            elif (a if diff > 0 else b) != true_winner:
                wrong += 1
        return wrong / n_bootstrap, tie / n_bootstrap

    k0 = n_items or min(len(da), len(db))
    wrong_rate, tie_rate = simulate(k0)

    needed = None
    for k in sorted(sample_sizes):
        w, t = simulate(k)
        if (1 - w - t) >= 0.90:
            needed = k
            break

    return DecisionRiskReport(
        n_items=k0,
        n_bootstrap=n_bootstrap,
        human_margin=float(human_margin),
        judge_margin=float(judge_margin),
        wrong_winner_rate=wrong_rate,
        inconclusive_rate=tie_rate,
        items_needed_for_90pct=needed,
    )


# --------------------------------------------------------------------------- #
# 6. Known biases you can test for without any ground truth
# --------------------------------------------------------------------------- #


@dataclass
class BiasReport:
    position_consistency: float     # share of pairs whose winner survives a swap
    position_first_pick_rate: float
    verbosity_slope: float          # judge points per SD of response length, quality held out
    verbosity_partial_r: float
    scale_entropy: float            # 0 = one score forever, 1 = uniform use of the scale
    top_two_score_share: float

    def as_rows(self) -> list[tuple[str, str]]:
        return [
            ("position consistency under swap", f"{self.position_consistency:6.1%}"),
            ("picks the first option", f"{self.position_first_pick_rate:6.1%}"),
            ("verbosity slope (pts / SD length)", f"{self.verbosity_slope:+6.2f}"),
            ("length-score partial r | quality", f"{self.verbosity_partial_r:+6.3f}"),
            ("scale-use entropy (0-1)", f"{self.scale_entropy:6.3f}"),
            ("share on 2 most-used scores", f"{self.top_two_score_share:6.1%}"),
        ]


def _residualize(y: np.ndarray, x: np.ndarray) -> np.ndarray:
    """Residuals of y after removing a linear fit on x."""
    x1 = np.column_stack([np.ones_like(x), x])
    beta, *_ = np.linalg.lstsq(x1, y, rcond=None)
    return y - x1 @ beta


def biases(
    trace: pd.DataFrame,
    pairs: pd.DataFrame | None = None,
    *,
    score_col: str = "judge_score",
    length_col: str = "response_tokens",
    quality_col: str = "human_score",
) -> BiasReport:
    """Bias probes that need no human labels except for the verbosity control.

    `pairs` (optional) has one row per pairwise comparison with columns
    `winner_ab` and `winner_ba`: the judge's pick with the two orders presented
    forwards and backwards. Position consistency is the share where the same
    candidate wins both ways -- Zheng et al. (2023) report 65% for GPT-4 and
    23.8% for Claude-v1, so anything under ~80% here is normal, not a bug in
    your harness.
    """
    d = trace.dropna(subset=[score_col])
    counts = d[score_col].value_counts(normalize=True)
    p = counts.to_numpy()
    k = max(len(p), 2)
    ent = float(-(p * np.log(p)).sum() / np.log(k))

    slope = float("nan")
    partial = float("nan")
    if length_col in d.columns and quality_col in d.columns:
        sub = d.dropna(subset=[length_col, quality_col])
        if len(sub) > 10:
            length_z = (sub[length_col] - sub[length_col].mean()) / sub[length_col].std()
            sr = _residualize(sub[score_col].to_numpy(float), sub[quality_col].to_numpy(float))
            lr = _residualize(length_z.to_numpy(float), sub[quality_col].to_numpy(float))
            if lr.std() > 0:
                slope = float(np.polyfit(lr, sr, 1)[0])
                partial = _pearson(sr, lr)

    consistency = float("nan")
    first_pick = float("nan")
    if pairs is not None and {"winner_ab", "winner_ba"} <= set(pairs.columns):
        consistency = float((pairs["winner_ab"] == pairs["winner_ba"]).mean())
        first_pick = float(
            ((pairs["winner_ab"] == "A").astype(int) + (pairs["winner_ba"] == "B").astype(int)).sum()
            / (2 * len(pairs))
        )

    return BiasReport(
        position_consistency=consistency,
        position_first_pick_rate=first_pick,
        verbosity_slope=slope,
        verbosity_partial_r=partial,
        scale_entropy=ent,
        top_two_score_share=float(counts.head(2).sum()),
    )
