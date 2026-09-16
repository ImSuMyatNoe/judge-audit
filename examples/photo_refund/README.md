# The photo-refund example

A customer photographs the meal that arrived, says it's wrong, and asks for a
refund. An agent looks at the photo, checks the order, and decides: **refund,
reject, or escalate**. Then an LLM judge reads the trace and scores the decision
out of ten.

That judge is what this example audits.

```
python examples/photo_refund/run_audit.py
python examples/photo_refund/run_audit.py --clue 2     # just the missing rows
```

## The four clues

Run it and you get, in order:

| Clue | What a normal report says | What the audit finds |
|---|---|---|
| 1 | the agent scores 6.9 / 10 | only **21%** of orders got the same score on all three passes, and **27%** changed pass/fail |
| 2 | the judge agrees with humans at **0.74** | it went blank on **22%** of orders — 1% of clear photos, **57%** of barely-readable ones. Agreement on those: **0.41** |
| 3 | **75%** agreement with human reviewers | always guessing the common answer scores 57%. Chance-corrected, it's **κ = 0.50** |
| 4 | the judge catches bad refunds | it approves **89%** of the confident-but-wrong ones. A second, binary judge cuts that to **10%** |

And then the number a team can act on: at 100 orders per agent version, the
judge names the **wrong version one time in four**.

## The files

| File | What's in it |
|---|---|
| `traces.csv` | one row per order — dish, complaint, the agent's decision, the refund amount, and two human judgements |
| `judged.csv` | one row per (order, judge pass) — three passes each, blanks left blank |
| `make_data.py` | regenerates both, deterministically |
| `run_audit.py` | the four clues |

The two human columns are deliberately separate, and that separation is the
point of clue 4:

- `human_score` — was this **handled well**? Clear reasoning, right tone, sensible escalation.
- `human_correct` — was it the **right call**? Should this customer have got their money back?

A graded judge answers the first question. Only the first. A refund decision
that reads beautifully and gives away $24 for a photo of the correct meal
scores 9/10 on handling and is still wrong.

## This data is synthetic

No real customers, no real photos, no real model output. The trace is generated
by `judge_audit.simulate`, whose parameters are calibrated to effect sizes that
published work reports for real judges — see `docs/calibration.md`, source by
source. That's why the numbers above are reproducible on a laptop with no API
key, and why they match the talk exactly.

For numbers about *your* judge, put your own trace through the same audits:

```
python -m judge_audit.audit --input my_trace.csv
```

`docs/using-your-own-data.md` describes the two columns everyone gets wrong —
the blank rows you must not drop, and the repeated passes you must not average
before scoring.
