# The talk

**LLM as a Judge Is Probably Lying to You**
Beyond the Vibes, Session 03, "Do You Trust Your AI?"
SGInnovate, 32 Carpenter St, Monday 28 September 2026, 7 to 9pm SGT.

`btv-slides.html` is the deck. Open it in any browser. No build step, no server,
no network, no API key. The photo, the QR codes, the event logo and the meme are embedded in the file, so
it works from a USB stick on a laptop that has never seen this repo.

| Key | Does |
|---|---|
| right arrow / space / PageDown | next slide |
| left arrow / PageUp | previous |
| Home / End | first / last |
| `N` | speaker notes panel |
| a number, then Enter | jump to that slide |
| the `start` button | presenter clock, turns rose past 30:00 |

The URL carries the slide number (`btv-slides.html#14`), so you can reopen where
you left off, and printing gives one slide per page.


## What this talk is

One investigation, told in order, inside one domain: **multimodal safety**. The
question underneath it is whether a judge number can be trusted before the judge has
been audited.

The worked example is a simulated safety evaluation. Six hundred image and question
pairs, five models answering them, and a second model scoring every response. When a
model refuses, it names the object it is refusing because of, and that sentence is a
claim about pixels, which means it can be checked.

Two images open the talk and carry it the whole way. A bottle of household cleaner,
where the refusal is correct and nobody argues. A chopping board with a knife on it,
where the question was about vegetables and the model refuses citing a weapon. The
second one is the case the talk is about.

Slide 3 says out loud that every number comes from a simulated worked example with
fixed seeds, with the code in the repo, and that the images are drawings. That is
deliberate. Nothing in the deck depends on unpublished work, no model or provider is
named, and anybody in the room can reproduce the mechanism.

The spine: what grounded means, who checks six hundred images, where the number
really comes from, what we would test if the judge were any other dependency, the
first results looking fine, rows with no score, the debugging, the retry, the blanks
concentrating on the ambiguous images, the number falling when the hard cases come
back, a refusal that scores nine out of ten, covering the object it cited and
watching the refusal stay, what that does and does not prove, the same test in
retrieval and coding agents, the rubric I actually wrote, the judge input contract,
one demo with four failure modes, and five checks.

Slide 21 is the centre of the talk: original image, the cited object covered, and an
equal area control patch somewhere else. Slide 22 exists so slide 21 stays honest.

Nothing is revealed early. The room should arrive at each conclusion about one slide
before you say it.


## Writing register

Written the way you would say it out loud. The model sentence for the deck is on
slide 26: "A judge can only check evidence it can actually see. If the thing you care
about is not in its input, no amount of prompt wording will get it back."

Titles are questions or plain statements: "What are we actually evaluating?", "What I
mean by grounded", "So take the object out of the image and ask again", "What that
tells us, and what it does not".

No slogan titles. No uppercase labels. No emoji inside the writing. Emoji appear only
in the hands up slide and the row icons in the two interactive panels.

Cautious throughout, and slide 22 is entirely about that: the deck says "the judgment
was not grounded in the available evidence" rather than "the model hallucinated",
because the first is what was measured and the second is a story about why. Slides
17, 18, 19, 22, 26 and 27 carry their limitation in the body rather than in a
footnote. Read them out loud.

Every speaker note ends with a **Remember:** line, which is the idea to carry rather
than a sentence to memorise.


## Canvas and typography

Every slide is composed on one fixed **1920 x 1080** stage and the whole stage
is scaled to the window. Nothing reflows between a laptop, a projector and a
phone: the layout you check at home is the layout the room sees.

1920px across a 16:9 slide is 13.333 inches, so **1 point is exactly 2 pixels**
and the scale below is real points.

| Token | Used for | Points |
|---|---|---|
| `--t-h1` | cover, question slides, part dividers | 36 |
| `--t-title` | slide titles | 30 |
| `--t-lead` | main explanatory text, the takeaway under a diagram | 14 |
| `--t-strong` | card headings, key column of a table | 13 |
| `--t-card` | text inside cards and process boxes | 12 |
| `--t-small` | supporting text, captions, footnotes | 12 |
| `--t-eyebrow` | the small line above a slide title | 11 |
| `--t-micro` | column heads, demo readouts, chrome | 10 |

Deliberately light. On a 16:9 slide filling a projector, 12pt body still reads
from the back because the slide is 13 inches wide on screen and several metres
wide in the room. If it ever needs to come back up, every size lives in these
eight lines at the top of the stylesheet and they move together.

Typeface is **Poppins** throughout, with **Roboto Mono** for the running header,
captions and code. Both load from Google Fonts and fall back to Helvetica and
Menlo offline.

The Beyond the Vibes logo sits top right on the title slide only, at 64px on a
dark chip so the white wordmark holds on the cream ground. Every other slide
carries just the running title, so the logo reads as a cover mark rather than a
watermark.

Two layout variants step outside the base scale on purpose, and only these two:

- `.spot` (slide 9) is one large visual on the left and two cards on the right
  at 35 / 65. The visual is the anchor, so its card headings go to 16pt and card
  body to 14pt.
- `.connect` (slide 31) is the closing slide: the statement at 25pt with a wide
  measure, a resources list, and one QR code.

Diagram rows are CSS grid. The six pipeline boxes and the six journey boxes are
`minmax(0, 1fr)` columns with `grid-auto-rows: 1fr`, so every box has the same
width, height, padding and icon box regardless of label length. Labels carry
deliberate line breaks so all six share a baseline. Arrows are their own centred
column.

Verified at 1920, 1440 and 1280 wide: every slide composes inside the 1080 stage
with nothing clipped, and the three window sizes give byte identical layout.


## Run of show, 31 slides in 30 minutes

| Slides | Beat | Time |
|---|---|---|
| 1 to 3 | Title, who you are, the grain of salt | 1:30 |
| 4 to 7 | The bleach case, the knife case, three properties, and the test that pays off twice | 3:20 |
| 8 to 11 | Scale, what a judge is, hands up, what the judge receives | 2:35 |
| 12 to 13 | Where the number comes from, and the five dependency questions | 2:05 |
| 14 to 18 | The calm, the blanks, the debugging, the retry, the missingness | 4:45 |
| 19 | The number falls, and the bridge into the second half | 1:00 |
| 20 to 24 | Nine out of ten, cover the object, what it does not prove, the rubric, three questions | 4:55 |
| 25 to 26 | Four domains, and the judge input contract | 1:50 |
| 27 | **The demo.** One case, five states, ending on evidence sensitivity | 2:00 |
| 28 to 31 | Repeat, perturb, count, compare, separate, then the thesis and resources | 3:05 |

Total about 27:50, which leaves roughly two minutes of buffer in a 30 minute slot.

The two elastic slides are 10 (hands up) and 27 (the demo). If you are running late,
ask only the second hands up question and stop the demo after the fourth button.


## Reveals

The right arrow steps through a slide's reveals before moving to the next slide, so a
click is a beat rather than a page turn. The down arrow skips straight to the next
slide, and the bottom bar shows which step you are on. Space and PageDown behave like
the right arrow. Going backwards into a slide lands on its last step, so you can step
back into a build without replaying it.

Reveals are only on the slides where the order of the argument matters: the three
properties, the grounding test, the pipeline, the five dependency questions, the
blanks, the missingness, the metric falling, the masking panels, the rubric, the three
questions, the input contract caution, the code, and the final checklist. Everything
else appears at once.


## Before you walk on

1. Open `btv-slides.html`, press `N` once to check the notes render, press `N`
   again to hide them, and start the clock as you begin.
2. Click through the three demos once. They are pure JavaScript with fixed data,
   so they cannot fail on stage, but muscle memory helps.
3. Scan the closing QR code with your own phone in the room you will present in.


## Where the numbers come from

Every figure is from the simulated worked example in `examples/photo_refund/`,
generated by `judge_audit.simulate` with fixed seeds. The images are drawings made for
the deck. The two interactive panels on slides 19 and 27 use fixed states and say so on
the slide.

There are no unpublished results in this deck and no real model or provider names.
Slide 3 states the simulation openly, and the speaker note for slide 15 says it again.

The scientific wording is deliberate in four places. Slide 17 keeps n = 10 visible and
refuses to explain the mechanism. Slide 18 labels the rates as belonging to this worked
example. Slide 21 says the stated visual reason is difficult to verify as load bearing,
rather than claiming the object was irrelevant. Slide 22 exists entirely to say what
masking cannot establish, including redundant cues and correlated features.


## Trimming to 20 minutes

Cut slides 4, 10, 25 and 28, and stop the demo after the fourth button. Do not cut
slide 22. The investigation still closes.


## Extending to 45 minutes

Add a walk through `judge_audit/metrics.py` after slide 28, run
`python examples/photo_refund/run_audit.py` live, and take questions after slide 24 as
well as at the end.
