# The talk

**LLM-as-a-Judge Is Probably Lying to You** — 30 minutes, practitioner audience.

`slides.html` is the deck. Open it in any browser; no build step, no dependencies.

| Key | Does |
|---|---|
| → / space / PageDown | next slide |
| ← / PageUp | previous |
| Home / End | first / last |
| `N` | speaker notes panel (timings and delivery notes per slide) |
| a number, then Enter | jump to that slide |
| the `start` button | presenter clock; turns red past 30:00 |

The URL carries the slide number (`…/slides.html#13`), so you can reopen where
you left off. Printing gives one slide per page.

## Run of show

| Minutes | Slides | What is happening |
|---|---|---|
| 0:00–1:00 | 1 | Cold open. "Judges are not useless — unaudited judges are." |
| 1:00–4:00 | 2–3 | The 85% number, what it actually said, and the instrument framing |
| 4:00–8:00 | 4–5 | **Lie 1**: the judge is not a function. Temperature 0 is not enough |
| 8:00–13:00 | 6–8 | **Lie 2**: blanks, stratified agreement, and your own MSTS-JP result |
| 13:00–14:30 | 9 | **Lie 3**: chance correction |
| 14:30–18:00 | 10–11 | **Lie 4**: style over substance, and the dual-judge fix |
| 18:00–19:00 | 12 | Why multimodal and legal make it worse |
| 19:00–25:00 | 13–14 | **Live demo** at the terminal (~5:30) |
| 25:00–26:30 | 15 | Decision risk — the number the room can act on |
| 26:30–29:00 | 16–18 | The checklist, what to publish, before/after |
| 29:00–30:00 | 19 | Close and questions |

## Before you walk on

1. `python -m judge_audit.demo --fast` once, to warm imports and confirm the
   terminal font is big enough from the back row.
2. Have the repo cloned and the environment active in the terminal you will
   switch to. Nothing in the demo needs network or API keys.
3. Open `slides.html`, press `N` once to check the notes panel, press `N` again
   to hide it, and start the clock as you begin.
4. If the terminal fails, every demo number is already on the slides and the
   five figures are in `figures/`. Do not debug on stage.

## Trimming to 20 minutes

Cut slides 5, 12 and 18, and run only acts 1, 2 and 4 of the demo (`--act 1
--act 2 --act 4`). The argument still closes.

## Extending to 45 minutes

Add a walk through `judge_audit/metrics.py` after slide 15 — the audience for
this talk usually wants to see how `decision_risk` and `stratified` are actually
computed — and take questions between acts rather than at the end.
