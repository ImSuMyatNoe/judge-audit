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

One investigation, told in order, around a single question: **can we trust an
LLM judge before we audit the judge?**

Slide 3 is the disclaimer: this is her own work, prepared for the talk, not her
lab's research. The worked example is the pizza refund, all the way through. Why a judge at all,
the report you would ship on, some rows coming back empty, six candidate causes,
five ruled out, the retry, the number moving, the confident wrong refund, what
changed when the judge could see the policy and the photo, and the four checks
that came out of it.

Nothing is revealed early. The room should arrive at each conclusion about one
slide before you say it.


## Writing register

Written the way you would say it out loud. The model sentence for the whole
deck is the one under the pipeline on slide 8: "We monitor the first five steps.
But the final score comes from the judge, so how do we know the judge is right?"
Complete sentences, spoken rhythm, a question where a question moves the story on.

Titles are questions or plain statements: "What happens before the refund?",
"Then we noticed some rows had no score", "Adding the reference changed the
judge's behavior".

No slogan titles. Nothing built as "Six steps. Four seconds." or "Looks right.
Isn't." Those read as copywriting rather than as a person talking.

Explanation slides use four boxes with short sentence case headings and two or
three plain sentences each. No uppercase labels, no emoji inside the writing.
Emoji appear only in diagrams and navigation: the restaurant scene, the six hop
strip, the refund pipeline, and the two hands up slides.

Cautious throughout: we observed, in this run, one explanation that fits, this
does not tell us how common that is. Slide 19 carries its limitation in the body.
Read it out loud.


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

The Beyond the Vibes logo sits top right on every slide at a uniform 46px on a
dark chip, so it holds on the cream ground.

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
| 1 to 2 | Title, then twenty seconds of who you are | 1:00 |
| 3 | Take this with a grain of salt. Say it lightly | 0:30 |
| 4 | The question the talk is about. Do not answer it | 0:20 |
| 5 | What is an AI agent, four boxes | 1:00 |
| 6 | What is LLM as a judge, four boxes | 1:00 |
| 7 to 9 | Ask who is hungry, where the order goes, it arrives wrong | 2:15 |
| 10 | What happens before the refund. The pipeline and the question | 1:00 |
| 11 to 12 | Why we used a judge, and what the judge receives | 1:45 |
| 13 | The first results looked fine | 0:45 |
| 14 to 15 | Hands up twice. Almost every hand goes down on the second | 1:10 |
| 16 | **The turn.** Some rows had no score | 1:00 |
| 17 to 18 | Six candidate causes, five ruled out | 1:40 |
| 19 | Ten inputs sent again, ten scored. Read the caution line | 1:00 |
| 20 | **Demo 1.** The same eight orders, three times | 1:30 |
| 21 | The missing scores were not spread evenly | 1:00 |
| 22 | **Demo 2.** What happens when we drop the blanks | 1:30 |
| 23 | The number went down because the hard cases came back | 0:40 |
| 24 | Divider. Where were the disagreements? | 0:15 |
| 25 to 26 | One example, then the same thing in my own work | 2:30 |
| 27 | What the judge was actually rewarding | 1:00 |
| 28 | Adding the reference changed the judge's behavior | 1:30 |
| 29 | **Demo 3.** What a second judge catches | 1:30 |
| 30 | What we check before trusting a judge number | 1:30 |
| 31 | Close. One QR code, the repo | 0:30 |

Demos total roughly four and a half minutes across slides 20, 22 and 29.


## Before you walk on

1. Open `btv-slides.html`, press `N` once to check the notes render, press `N`
   again to hide them, and start the clock as you begin.
2. Click through the three demos once. They are pure JavaScript with fixed data,
   so they cannot fail on stage, but muscle memory helps.
3. Scan the closing QR code with your own phone in the room you will present in.


## Where the numbers come from

Every figure comes from `examples/photo_refund/`, which is synthetic data
generated by `judge_audit.simulate` with fixed seeds. Run
`python examples/photo_refund/run_audit.py` and you get the slide numbers back,
line for line. The demos use fixed subsets of the same data and say so in the
banner under each one.

Slide 26 is the one real anecdote: the mis grounded refusal from your own
multimodal safety work. No figures attached to it, so nothing unpublished is on
a public slide.


## Trimming to 20 minutes

Cut slides 9, 17, 26 and 28, and run only demos 1 and 3. The investigation
still closes.


## Extending to 45 minutes

Add a walk through `judge_audit/metrics.py` after slide 30, run
`python examples/photo_refund/run_audit.py` live so the room sees the same
numbers come out of real code, and take questions at slide 24 as well as at the end.
