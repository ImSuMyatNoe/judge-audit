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


## Run of show, 33 slides in 30 minutes

| Slides | Act | Beat | Time |
|---|---|---|---|
| 1 to 7 | 1 | Title, who you are, the grain of salt, the bottle, the knife, the three properties, what grounded means | 5:05 |
| 8 to 14 | 2 | Six hundred images, what a judge is, what it receives, where the number comes from, the five dependency questions, hands up, the calm | 6:05 |
| 15 to 19 | 3 | No score, the debugging, the retry, the blanks by image difficulty, the number falling | 5:00 |
| 20 to 25 | 4 | Nine out of ten, cover the object, what it does and does not prove, four domains, the rubric, three questions | 5:50 |
| 26 to 27 | 5 | The judge input contract, what changed when evidence was added | 1:45 |
| 28 | 6 | **The demo.** Five buttons, four failure modes | 2:20 |
| 29 to 30 | 7 | Five tests, quality against correctness | 1:55 |
| 31 to 33 | 8 | The checklist, the thesis, resources | 1:40 |

Total about 28:45, which leaves roughly 1:15 of buffer in a 30 minute slot.

The two elastic slides are 13 (hands up) and 28 (the demo). If you are running late,
ask only the second hands up question and stop the demo after the fourth button.
That buys two minutes without cutting an idea.


## Before you walk on

1. Open `btv-slides.html`, press `N` once to check the notes render, press `N`
   again to hide them, and start the clock as you begin.
2. Click through the three demos once. They are pure JavaScript with fixed data,
   so they cannot fail on stage, but muscle memory helps.
3. Scan the closing QR code with your own phone in the room you will present in.


## Where the numbers come from

Every figure is from the simulated worked example in `examples/photo_refund/`,
generated by `judge_audit.simulate` with fixed seeds. Run
`python examples/photo_refund/run_audit.py` and the slide numbers come back, line for
line. The two interactive panels on slides 16 and 24 use fixed subsets of the same
data and say so in the banner underneath.

There are no unpublished results in this deck, and no real model or provider names.
That is a deliberate constraint, stated on slide 3 and again in the speaker note for
slide 12. Slides 18 and 19 carry the one first person claim in the talk, which needs
no figures attached to it.


## Trimming to 20 minutes

Cut slides 4, 23, 25 and 30, and stop the demo after the fourth button. Do not cut
slide 22. The investigation still closes.


## Extending to 45 minutes

Add a walk through `judge_audit/metrics.py` after slide 29, run
`python examples/photo_refund/run_audit.py` live so the room sees the same numbers
come out of real code, and take questions after slide 25 as well as at the end.
