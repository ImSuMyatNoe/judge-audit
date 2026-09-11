# The judge audit checklist

One page. Run it before you let a judge make a decision for you, and again
whenever the judge model version changes.

## Before you trust the judge

**1. Run it three times on the same inputs.**
Not a sample — the whole set, three passes, identical prompts. Report the score
*and* the spread. If you only ever run once, you do not know whether you are
measuring the system or the judge.
→ `metrics.stability()`. Watch: all-passes-identical rate, verdict flip rate, ICC(1).

**2. Count the blanks, then retry them.**
Empty, unparseable, refused, errored — every one of them. Blanks are not missing
at random; they cluster on exactly the items you needed help with. Retry them,
and report the correlation *after* recovery. It will be worse. It is also the
honest one.
→ `metrics.missingness()`. Watch: blank rate, blank rate by stratum, survivorship gap.

**3. Stratify by difficulty before you believe a correlation.**
Any grouping works: annotator confidence, item ambiguity, source dataset, image
occlusion. If agreement is carried by the stratum where the answer was never in
doubt, your judge is confirming your easy cases and guessing on the rest.
→ `metrics.stratified()`.

**4. Chance-correct every agreement number.**
Raw agreement is unreadable without the majority baseline beside it. Report κ,
or report both. Expect to lose 25–40 points.
→ `metrics.agreement()`.

**5. Swap the order and re-judge.**
For every pairwise comparison. One extra call per pair, and it catches the most
embarrassing failure mode in the literature. Aggregate the two orders rather
than picking one.
→ `metrics.biases()`. Watch: position consistency, first-pick rate.

**6. Check whether length is doing the work.**
Regress judge score on response length with quality controlled for. If length
predicts the score, your leaderboard ranks verbosity.
→ `metrics.biases()`. Watch: verbosity partial r.

## Before you let the judge decide anything

**7. Pair the graded judge with a strict binary check.**
"Is this a good answer?" and "does this mean what the reference means?" are
different questions. A 0–10 judge answers only the first, and a fluent wrong
answer is precisely where that fails. Add a binary semantic-equivalence judge
against a human-curated reference and require both.
→ `metrics.dual_judge()`.

**8. Convert judge noise into decision risk.**
Nobody can act on "r = 0.7". They can act on "at our eval size, this judge names
the wrong winner one time in four". Bootstrap it.
→ `metrics.decision_risk()`.

**9. Pin, log and re-audit.**
Pin the model version, the temperature, the prompt, the score range and the
parser, and log all of them with every score. A pinned model *name* is not a
pinned model — re-run the audit when the vendor ships. Keep a held-out human-
labelled slice and re-check the judge against it on a schedule.

## What to put in the paper or the eval report

- Number of judge passes, and the spread across them.
- Blank/unparse rate, how blanks were handled, and the correlation before and
  after recovery.
- Agreement chance-corrected, with the baseline.
- Judge model version, temperature, score range, prompt, and parser.
- For pairwise results: whether both orders were judged.
- The size of your eval set, and the decision risk at that size.

## What not to do

- Do not report a single-pass number without the spread.
- Do not silently drop unparseable rows.
- Do not report raw agreement alone.
- Do not report a pooled correlation without a stratified breakdown.
- Do not use a judge that is weaker than the systems it ranks and expect the
  ranking to hold (Dorner & Hardt 2025).
- Do not let the judge be the only thing that ever looks at the output.
