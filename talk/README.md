# The talk

**LLM as a Judge Is Probably Lying to You**
Beyond the Vibes, Session 03, "Do You Trust Your AI?"
SGInnovate, 32 Carpenter St, Monday 28 September 2026, 7 to 9pm SGT.

`btv-slides.html` is the deck. Open it in any browser. No build step, no server,
no network, no API key. The photo and both QR codes are embedded in the file, so
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


## Typography

Every size on every slide comes from one scale, declared once at the top of the
stylesheet. Nothing shrinks to fit its own content.

| Token | Used for | At 1440 wide |
|---|---|---|
| `--t-h1` | title slide, question slides, part dividers | 72px |
| `--t-title` | slide titles | 56px |
| `--t-lead` | the main explanatory line, the takeaway under a diagram | 28px |
| `--t-strong` | card headings, the key column of a table | 24px |
| `--t-card` | text inside cards, process boxes, chips | 23px |
| `--t-small` | supporting text, captions, footnotes, cautions | 18px |
| `--t-micro` | eyebrows, column heads, demo readouts | 15px |

Diagram rows are CSS grid, not flex wrap. The six pipeline boxes and the six
journey boxes are `minmax(0, 1fr)` columns with `grid-auto-rows: 1fr`, so every
box has the same width, height, padding and icon box regardless of label length.
Labels carry deliberate line breaks so all six sit on the same two lines and
share a baseline. Arrows are their own grid column, vertically centred.

Verified at 1280, 1440 and 1920: no slide scrolls, and on both diagram slides
all six boxes report identical width, height and top.


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
| 31 | Close, both QR codes | 0:30 |

Demos total roughly four and a half minutes across slides 20, 22 and 29.


## Before you walk on

1. Open `btv-slides.html`, press `N` once to check the notes render, press `N`
   again to hide them, and start the clock as you begin.
2. Click through the three demos once. They are pure JavaScript with fixed data,
   so they cannot fail on stage, but muscle memory helps.
3. Scan both QR codes with your own phone in the room you will present in.


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
