# References

Everything the talk cites, with the specific finding it is cited for. arXiv IDs
were checked against the arXiv abstract page (title + first author); where a
venue could not be confirmed the entry says so rather than guessing.

## The case for LLM-as-a-judge

- **Zheng et al. (2023)**, *Judging LLM-as-a-Judge with MT-Bench and Chatbot
  Arena*, NeurIPS 2023 D&B, [arXiv:2306.05685](https://arxiv.org/abs/2306.05685).
  GPT-4 agrees with human preference on 85% of non-tie MT-Bench pairs, against
  81–82% human–human agreement — **but only 66% once ties are counted**.
- **Liu et al. (2023)**, *G-Eval*, EMNLP 2023,
  [arXiv:2303.16634](https://arxiv.org/abs/2303.16634).
  The widely cited summarization result is **Spearman 0.514** with humans, not 0.9.
- **Bavaresco et al. (2025)**, *LLMs instead of Human Judges?*, ACL 2025 (short),
  [arXiv:2406.18403](https://arxiv.org/abs/2406.18403).
  11 judges × 20 human-annotated datasets: agreement swings with the property
  judged, annotator expertise, and whether the text was human- or model-generated.

## Position bias

- **Wang et al. (2023)**, *Large Language Models are not Fair Evaluators*,
  [arXiv:2305.17926](https://arxiv.org/abs/2305.17926) (venue unconfirmed).
  Reordering the two candidates makes Vicuna-13B "beat" ChatGPT on **66 of 80**
  queries (82.5%).
- **Zheng et al. (2023)**, Table 2. Position consistency under swap:
  **GPT-4 65.0%, GPT-3.5 46.2%, Claude-v1 23.8%**; Claude-v1 picks the first
  answer 75% of the time.
- **Shi et al. (2025)**, *Judging the Judges: A Systematic Study of Position Bias*,
  AACL-IJCNLP 2025, [arXiv:2406.07791](https://arxiv.org/abs/2406.07791).
  >150,000 instances: position bias is systematic, not noise, and is driven by
  the **quality gap** — close pairs flip most.

## Style over substance

- **Zheng et al. (2023)**, Table 3. A "repetitive list" attack — same content,
  padded and reformatted — fools GPT-3.5 and Claude-v1 **91.3%** of the time.
- **Dubois et al. (2024)**, *Length-Controlled AlpacaEval*,
  [arXiv:2404.04475](https://arxiv.org/abs/2404.04475) (venue unconfirmed).
  Win rates need explicit length control before they say anything about quality.
- **Feuer et al. (2025)**, *Style Outweighs Substance*, ICLR 2025,
  [arXiv:2409.15268](https://arxiv.org/abs/2409.15268).
  Judge preference does **not** correlate with measured safety, world knowledge,
  or instruction following.

## Self-preference

- **Panickssery et al. (2024)**, *LLM Evaluators Recognize and Favor Their Own
  Generations*, NeurIPS 2024,
  [arXiv:2404.13076](https://arxiv.org/abs/2404.13076).
  Self-recognition ability and self-preference strength are **linearly** related
  under fine-tuning — causal, not incidental.
- **Zheng et al. (2023)**. GPT-4 favours its own outputs by ~10 points of win
  rate; Claude-v1 by ~25.
- **Chen et al. (2025)**, *Do LLM Evaluators Prefer Themselves for a Reason?*,
  [arXiv:2504.03846](https://arxiv.org/abs/2504.03846) (venue unconfirmed).
  On verifiable tasks much self-preference is legitimate — but the *harmful*
  part concentrates on items the judge itself got wrong.

## Instability and scale-use

- **Haldar et al. (2025)**, *Rating Roulette: Self-Inconsistency in
  LLM-As-A-Judge Frameworks*, EMNLP 2025,
  [arXiv:2510.27106](https://arxiv.org/abs/2510.27106).
  Intra-rater Krippendorff α across repeated runs, all below the 0.8 threshold
  (Llama 3.1 0.265, DeepSeek-R1 0.507, Qwen-3 0.563); Qwen-3 gives the same
  verdict on all three runs for only **61.3%** of cases.
- **Lau et al. (2026)**, *Same Input, Different Scores*,
  [arXiv:2603.04417](https://arxiv.org/abs/2603.04417) (venue unconfirmed).
  Score variability persists **at temperature 0** across five hosted judges.
- **Tamba (2026)**, *Necessary but Not Sufficient: Temperature Control and
  Reproducibility in LLM-as-Judge Safety Evaluations*,
  [arXiv:2606.26185](https://arxiv.org/abs/2606.26185) (venue unconfirmed).
  Unset temperature → provider default 1.0 → up to ~**50%** per-item pass/fail
  disagreement over 20 identical runs. Recommends logging grader disagreement as
  a first-class eval health metric.
- **Fujinuma et al. (2026)**, *Contrastive Decoding Mitigates Score Range Bias*,
  ACL 2026, [arXiv:2510.18196](https://arxiv.org/abs/2510.18196).
  Judges are highly sensitive to the declared score range (1–5 vs 1–10 vs 0–100).
- **Li et al. (2026)**, *Evaluating Scoring Bias in LLM-as-a-Judge*, DASFAA 2026,
  [arXiv:2506.22316](https://arxiv.org/abs/2506.22316).
  Rubric-order bias, score-ID bias, reference-answer score bias — present in
  frontier models.

## Why a correlation can mislead

- **Gao et al. (2025)**, *Analyzing and Evaluating Correlation Measures in NLG
  Meta-Evaluation*, NAACL 2025,
  [arXiv:2410.16834](https://arxiv.org/abs/2410.16834).
  12 correlation measures × 6 datasets × 32 metrics: the measure you pick changes
  the conclusion.
- **Dorner & Hardt (2025)**, *Limits to scalable evaluation at the frontier:
  LLM as Judge won't beat twice the data*, ICLR 2025,
  [arXiv:2410.13341](https://arxiv.org/abs/2410.13341).
  When the judge is no more accurate than the model under test, **no** debiasing
  method can cut the required ground-truth labels by more than half.
- **Norman et al. (2026)**, *Reliability without Validity*,
  [arXiv:2606.19544](https://arxiv.org/abs/2606.19544) (venue unconfirmed).
  ~541,000 judgments: chance-correcting raw agreement deflates it by **33–41
  points of κ** on MT-Bench; judge rankings move by up to 14 positions depending
  on the benchmark. Two production judges show test-retest reliability >0.95
  **and** position bias >0.10 — stable is not the same as unbiased.
- **Chen et al. (2026)**, *A Judge Should Know What Changed*,
  [arXiv:2608.24419](https://arxiv.org/abs/2608.24419) (venue unconfirmed).
  Judges are stable under meaning-*preserving* edits (S = 0.945) but catch only
  ~1/3 of meaning-*changing* ones (R = 0.319); surface-only predictors reproduce
  **67.4% of MT-Bench human votes**.

## Judges on objectively checkable tasks

- **Tan et al. (2025)**, *JudgeBench*, ICLR 2025,
  [arXiv:2410.12784](https://arxiv.org/abs/2410.12784).
  On pairs with verifiable factual/logical correctness, a vanilla GPT-4o judge
  scores **50.86%** against a 50% random baseline — while the same judges score
  70–90% on preference benchmarks.
- **Chen et al. (2024)**, *MLLM-as-a-Judge*, ICML 2024 (oral),
  [arXiv:2402.04788](https://arxiv.org/abs/2402.04788).
  Multimodal judges look human-like on pairwise comparison but diverge sharply
  on pointwise scoring, with hallucinated justifications.
- **Lee et al. (2026)**, *MM-JudgeBias*, ACL 2026 Main,
  [arXiv:2604.18164](https://arxiv.org/abs/2604.18164).
  26 MLLMs, 9 bias types: systematic **modality neglect** — judges ignore the
  image or the text when evidence is missing or conflicting.

## Drift

- **Chen, Zaharia & Zou (2023)**, *How is ChatGPT's behavior changing over time?*,
  [arXiv:2307.09009](https://arxiv.org/abs/2307.09009); also in Harvard Data
  Science Review 6.2 (DOI unconfirmed).
  Same endpoint, same prompts: GPT-4 accuracy on one task fell **84% → 51%**
  between March and June 2023. A pinned model *name* is not a pinned model.

## Surveys

- **Gu et al.**, *A Survey on LLM-as-a-Judge*, The Innovation 7(6),
  DOI 10.1016/j.xinn.2025.101253; preprint
  [arXiv:2411.15594](https://arxiv.org/abs/2411.15594).
- **Li et al. (2025)**, *From Generation to Judgment*, EMNLP 2025,
  [arXiv:2411.16594](https://arxiv.org/abs/2411.16594).

## The speaker's own work

- Su Myat Noe, Ha Thanh Nguyen, May Myo Zin, Ken Satoh, *Beyond Accuracy: A
  Dual-Judge Evaluation Protocol for Vision-Language Models in Legally Grounded
  Tasks*, AI for Law Workshop, 2026.
  Code: https://github.com/ImSuMyatNoe/dual-judge-traffic-signs
