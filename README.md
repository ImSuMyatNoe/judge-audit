# judge-audit

**Your LLM judge is probably lying to you. Here is how to catch it.**

Companion code for the 30 minute talk *"LLM as a Judge Is Probably Lying to You"*,
Beyond the Vibes Session 03, SGInnovate, 28 September 2026.

Two things live here:

1. **`judge_audit/metrics.py`** — six audits you can run on **your own** judge
   output. No API calls, no dependencies beyond numpy/pandas/scipy. This is the
   part worth stealing.
2. **`judge_audit/demo.py`** — a seven-act demo that runs those audits on a
   synthetic judge trace, offline, in about twenty seconds. It exists so the talk
   can show a live failure without a network connection, an API key, or a bill.

```
pip install -r requirements.txt
python stage.py                       # live demo selector, broken vs fixed
python -m judge_audit.scenarios 1     # one scenario, measured the usual way
python -m judge_audit.scenarios 1 --fix        # the same data, measured honestly
python -m judge_audit.demo            # the full seven-act walkthrough
python -m judge_audit.audit --input my_trace.csv   # your own data
```

The talk itself lives in `talk/`, as one self contained HTML file with the
three demos built into the page.

| File | What it is |
|---|---|
| `talk/btv-slides.html` | The deck. 35 slides, three live demos you drive from the slide, speaker notes behind `N` |
| `talk/_btv_template.html` | The source it is built from. Edit this one |
| `talk/build.py` | Assembles the template plus the photo and QR codes into the deck and into `docs/index.html` |
| `talk/slides.html` | An older, longer research version of the same argument, kept for reference |
| `talk/SCRIPT.md` | The talk word for word, in a conversational speaking style, plus how to take questions mid flow |
| `talk/SPEAKER-NOTES.md` | What to say, why each number is true, the questions you will get, and what to do when something breaks on stage |

## The slides

Live at **https://imsumyatnoe.github.io/judge-audit/** once GitHub Pages is on
(see `PUBLISHING.md`). Locally, open `talk/btv-slides.html` in any browser.

Both files are built from `talk/_btv_template.html` by `python talk/build.py`,
so edit the template and rebuild rather than editing the output.


## What the demo shows

Every number below is produced by `python -m judge_audit.demo` on the default
synthetic trace (600 items, three passes, fixed seeds — you will get exactly
these numbers).

| Act | The claim | The number |
|---|---|---|
| 1 | The judge is not a function | 21% of items get the same score on all three identical passes; 27% change pass/fail verdict between passes |
| 2 | Silence is data | Blank rate runs 1% on the clearest quarter of items and 57% on the most ambiguous quarter; agreement with humans runs 0.74 and 0.41 on those same quarters |
| 3 | Agreement is inflated | 75% raw agreement becomes κ = 0.50 against a 57% majority baseline |
| 4 | One number, two questions | A graded 0–10 judge passes 89% of fluent-but-wrong responses; adding a binary semantic-equivalence judge cuts that to 10% with no extra false rejects |
| 5 | Free bias probes | 40% of pairwise verdicts flip when the two candidates are swapped; length still predicts score at partial r = +0.42 with human-judged quality controlled for |
| 6 | Decision risk | At 100 items per system the judge names the better system 74% of the time; 400 items are needed for 90% |
| 7 | What the audit buys | Same eval set, audited protocol: verdict stability 73% → 86%, blank rate 22% → 1%, fluent-wrong caught 11% → 96% |

## What this is not

**The demo data is synthetic and labelled as such in every file that touches it.**
No real model's output is shipped here, and nothing in this repository is
evidence about any specific named model. The simulator's parameters are
calibrated to effect sizes that published work reports for real judges
(`docs/calibration.md` gives the table, source by source), so the demo's *shape*
is faithful while staying reproducible on a laptop in a conference room.

If you want numbers about *your* judge, that is what `judge_audit.audit` is for.

## Running the audit on your own data

One CSV, long format, one row per (item, judging pass):

```csv
item_id,run,judge_score,human_score
it0001,1,8,7
it0001,2,6,7
it0001,3,,7
```

An empty `judge_score` means the judge returned nothing usable — blank,
unparseable, refused, API error. **Do not drop those rows.** They are the single
most informative thing in the file, and the audit is built around them.

```
python -m judge_audit.audit --input my_trace.csv --json report.json
```

Optional columns unlock further sections (`difficulty_stratum`, `system`,
`equivalent`, `human_correct`, `response_tokens`, `judge_score_recovered`); see
`docs/using-your-own-data.md`.

## The checklist

The talk ends with a one-page checklist: `docs/checklist.md`. Short version:

1. Run the judge **three times** on the same inputs, and report the spread.
2. **Count the blanks.** Retry them, and report the correlation after recovery —
   it is the honest number even though it is the worse one.
3. **Stratify.** A pooled correlation hides a judge that only agrees with you on
   easy items.
4. **Chance-correct.** Raw agreement next to a majority baseline, or κ.
5. **Swap and re-judge** every pairwise comparison.
6. **Pair the graded judge with a binary check** against a human reference.
7. **Report decision risk**, not correlation: how often would this judge pick the
   wrong system at your eval size?

## Layout

```
judge_audit/metrics.py     the audits            (the reusable part)
judge_audit/simulate.py    the synthetic judge   (clearly labelled)
judge_audit/scenarios.py   four stage scenarios, each with --fix
judge_audit/demo.py        the full walkthrough, seven acts
judge_audit/audit.py       CLI for your own CSV
judge_audit/figures.py     the talk's figures
stage.py                   live demo selector for presenting
docs/calibration.md        every simulator default, and the paper it came from
docs/using-your-own-data.md
docs/checklist.md
talk/                      two decks, speaker notes, run-of-show
tests/                     pytest suite for the metrics
```

## Tests

```
pip install pytest
pytest -q
```

The metrics are tested against cases with analytically known answers — a
perfectly stable judge, a pure-noise judge, a judge that agrees 80% of the time
by always saying "pass" — rather than against the simulator, so the tests fail
loudly if a metric is wrong rather than merely if the simulator changes.

## Citing the work behind the talk

The dual-judge protocol in Act 4 comes from:

> Su Myat Noe, Ha Thanh Nguyen, May Myo Zin, Ken Satoh.
> *Beyond Accuracy: A Dual-Judge Evaluation Protocol for Vision-Language Models
> in Legally Grounded Tasks.* AI for Law Workshop, 2026.
> Code: https://github.com/ImSuMyatNoe/dual-judge-traffic-signs

`docs/references.md` lists the literature the talk cites, with arXiv IDs.

## Licence

MIT. Take the metrics, drop the rest.
