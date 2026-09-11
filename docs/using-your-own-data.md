# Running the audit on your own judge

```
python -m judge_audit.audit --input my_trace.csv
```

Nothing is uploaded anywhere. The tool reads your CSV and prints numbers.

## The minimum file

One row per (item, judging pass). Four columns:

```csv
item_id,run,judge_score,human_score
it0001,1,8,7
it0001,2,6,7
it0001,3,,7
it0002,1,9,9
```

- `item_id` — anything stable that identifies the response being judged.
- `run` — 1, 2, 3… the pass number. **Three passes is the minimum** that makes
  the stability section meaningful; with one pass the tool will tell you so and
  skip it.
- `judge_score` — numeric. **Leave the cell empty** when the judge returned
  nothing usable: empty string, unparseable output, refusal, content filter, API
  error, timeout. Do not fill these with 0, do not drop the row. The whole audit
  is built on them.
- `human_score` — your reference score for the item, on the same scale.

Different scale? Pass `--threshold` (the score at or above which a response
counts as a pass). For a 1–5 scale, `--threshold 4`.

## Optional columns

Each one unlocks a section:

| Column | Unlocks | Notes |
|---|---|---|
| `judge_score_recovered` | survivorship gap | the score after retrying a blank; leave empty only if the retry also failed |
| `difficulty_stratum` | stratified breakdown | any grouping: annotator confidence, item length, source dataset, whether the image was occluded, model under test |
| `system` | decision risk | which system produced the response; exactly two distinct values |
| `equivalent` | dual-judge | 0/1 from a binary semantic-equivalence judge |
| `human_correct` | dual-judge | 0/1 ground truth: does the response agree with the reference |
| `fluent_but_wrong` | dual-judge detail | 0/1, the confident-wrong subset you care most about |
| `response_tokens` | verbosity probe | length of the judged response |

## Pairwise comparisons

If your judge does pairwise preference rather than pointwise scoring, pass a
second file:

```csv
pair_id,winner_ab,winner_ba
pr0001,A,A
pr0002,A,B
```

`winner_ab` is the judge's pick when A was shown first; `winner_ba` is its pick
when B was shown first. Both columns name the **candidate**, so a row where the
two disagree is a verdict that did not survive the swap.

```
python -m judge_audit.audit --input my_trace.csv --pairs my_pairs.csv
```

## Getting the file out of your harness

The shape you want is a long table, one row per attempt, written **before** any
cleaning step. Two things go wrong most often:

1. **The parser eats the evidence.** If your harness does
   `score = int(re.search(r"\d+", text).group())` inside a `try/except: continue`,
   the blanks vanish before anything can count them. Write the row with an empty
   score instead.
2. **Repeats get averaged too early.** If the harness averages three passes and
   writes one row, the stability section has nothing to measure. Write all three.

A minimal shape for a harness that already loops:

```python
rows = []
for item in items:
    for run in (1, 2, 3):
        raw = call_judge(item)                 # whatever your judge call is
        rows.append({
            "item_id": item.id,
            "run": run,
            "judge_score": parse_score(raw),   # None when unparseable -- keep the row
            "human_score": item.human_score,
            "difficulty_stratum": item.stratum,
            "response_tokens": len(item.response.split()),
        })
pd.DataFrame(rows).to_csv("my_trace.csv", index=False)
```

## Using the metrics directly

The CLI is a thin wrapper. In a notebook:

```python
import pandas as pd
from judge_audit import metrics as M

trace = pd.read_csv("my_trace.csv")
print(M.stability(trace, threshold=4))
print(M.stratified(trace))
print(M.missingness(trace))
```

Every function returns a plain dataclass or DataFrame, so the numbers go
straight into a paper table.

## Reading the output

| Section | Healthy | Worth a paragraph in your paper |
|---|---|---|
| all passes identical | >90% | <70% |
| verdict flip rate | <5% | >15% |
| ICC(1) | >0.9 | <0.75 |
| blank rate | <2% | >5%, or heavily skewed across strata |
| κ | >0.8 | <0.6, or far below raw agreement |
| position consistency | >90% | <80% |
| verbosity partial r | <0.1 | >0.25 |
| P(wrong winner) at your eval size | <5% | >10% |

These thresholds are judgement calls, not standards. The point is to publish the
numbers, not to pass them.
