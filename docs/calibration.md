# Calibration: where every simulator default came from

`judge_audit/simulate.py` generates **synthetic** judge output. It is not
evidence about any real model. What makes it useful rather than arbitrary is
that each knob was set so the resulting behaviour lands in the range that
published work reports for real judges. This file is the audit trail for that
claim, so a sceptical audience member can check it, and so you can re-set any
knob you disagree with.

Full citations: `docs/references.md`.

| Knob | Default | Effect it is meant to reproduce | Source |
|---|---|---|---|
| `noise_floor` | 0.15 pts | Repeated identical passes disagree even on easy items; disagreement survives temperature 0 | Haldar et al. 2025; Lau et al. 2026 |
| `noise_slope` | 1.60 pts | Disagreement grows with item ambiguity; the demo's 21% all-passes-identical sits below Haldar's 61.3%, which is a text benchmark rather than an ambiguous multimodal one | Haldar et al. 2025 |
| `central_pull` | 0.95 | When the judge cannot tell, it regresses to a safe middling score rather than declining — scale-use pathology, not extra noise | Li et al. 2026 (DASFAA); Fujinuma et al. 2026 |
| `central_score` | 6.5 | The safe score sits above the midpoint, matching the well-documented upward skew of judge scores | Li et al. 2026 (DASFAA) |
| `blank_intercept` / `blank_slope` | −5.6 / 9.0 | Blank, unparseable and refused outputs concentrated on ambiguous items: ~1% on the clearest quartile, ~57% on the most ambiguous. Nondeterministic empty returns from hosted judges are a reported, reproducible failure | Tamba 2026; speaker's own MSTS-JP runs |
| `retry_attempts` | 3 | A retry-on-blank loop, which is what a harness does once someone notices the gaps | — |
| `verbosity_coef` | 0.30 pts / SD | Length predicts score with quality controlled for; the sign and size differ by model family, so treat this as one plausible setting rather than a constant of nature | Dubois et al. 2024; Feuer et al. 2025 |
| `fluent_wrong_inflation` | 2.80 pts | A confident, well-formatted, wrong answer scores well: judges prioritise style over correctness | Feuer et al. 2025; Zheng et al. 2023 Table 3 |
| `anchor_scores` / `anchor_pull` | (5, 7, 8) / 0.10 | Judges cluster on a few favourite values instead of using the scale | Li et al. 2026 (DASFAA) |
| `first_position_preference` | 0.62 | Preference for the first-presented candidate on a dead heat. Produces ~60% swap consistency, between Zheng's GPT-4 (65.0%) and Claude-v1 (23.8%) | Zheng et al. 2023 Table 2 |
| `pair_discrimination` | 6.0 | Real quality gaps do win out — position bias concentrates on *close* pairs | Shi et al. 2025 |
| `equiv_sensitivity` / `equiv_specificity` | 0.93 / 0.84 | A strict binary semantic-equivalence judge against a human reference: good but not perfect, and deliberately better at catching wrongness than at avoiding over-rejection | dual-judge protocol, AI for Law 2026 |

## What is *not* calibrated

- The eval set itself: 600 items, latent quality drawn from a Beta(5, 2.6), 15%
  of them fluent-but-wrong. That is a made-up population chosen so every act has
  something to show. It is not a claim about any real dataset's difficulty mix.
- The size of the two systems' true quality gap in Act 6. It is set small enough
  that the decision is genuinely hard, because a huge gap makes the act boring
  and a zero gap makes it meaningless.
- Human reference scores are generated with 0.75 points of noise. Real human
  agreement ceilings are a whole separate talk.

## Re-calibrating

Every knob lives on `JudgeProfile`. To model your own judge:

```python
from judge_audit import simulate as S, metrics as M

mine = S.JudgeProfile(name="ours", noise_floor=0.4, noise_slope=0.9,
                      blank_intercept=-6.0, blank_slope=3.0,
                      verbosity_coef=-0.1, central_pull=0.4)
data = S.build_dataset(profile=mine)
print(M.stability(data["trace"]))
```

Better still: measure the knobs from three real passes of your own harness and
compare. `judge_audit.audit` reports the same quantities on a real trace, so the
two are directly comparable — which is the honest way to use a simulator.
