# Speaker notes

Everything you need to walk on stage and give this talk without rehearsing it
six times. Read this once on the train, skim the bold lines before you go on.

The deck also carries short notes per slide. Press `N` while presenting.

---

## The whole talk in one paragraph

Teams now use one model to grade another model's work, because there is no other
way to keep up. That grading model decides which version ships. Nobody ever
checks the grading model itself. When you do check it, four specific things are
wrong with it, each of which quietly makes your numbers look better than reality.
All four are cheap to detect and cheap to fix, and you can start on Monday.

That is it. Everything else is a pizza and four demonstrations.

---

## Why this argument works

You are not saying AI is bad. You are not saying LLM judges are useless. If you
say either of those, half the room stops listening, because they use judges and
they are not idiots.

What you are saying is narrower and much harder to argue with:

> **The judge is the only part of your stack that has no tests.**

Every other component gets tested. Your API has tests. Your parser has tests.
Your retrieval has tests. The thing that decides whether all of it is any good
has no tests at all, and we all just agreed to that without discussing it.

Once someone sees that sentence, they cannot unsee it. That is your talk.

---

## The four clues, explained simply

You need to actually understand these, not just read them off the slide, because
someone will ask. Here is each one in plain words, why it happens, and the number.

### Clue one: same input, different score

You send the identical trace to the identical judge with the identical prompt,
three times. You get three different scores.

**Why this happens.** Everyone assumes temperature zero means deterministic. It
does not. Temperature zero only means "always pick the most likely next token".
The probabilities themselves shift between runs, because of how the numbers are
added up on the GPU. Floating point addition is not associative, so summing the
same values in a different order gives a slightly different total. Batch size
changes that order. Your request gets batched with whatever else arrived in the
same millisecond. On a mixture of experts model, which most frontier models now
are, the batch also changes which expert your token is routed to. You are also
probably being load balanced across replicas that are not bit identical.

So the model is deterministic in theory and stochastic in practice, and the
practice is what you are measuring.

**The numbers.** Only 21% of orders got the same score all three times. 27%
changed side of the pass line between passes. The average gap between the
highest and lowest pass was 1.2 points out of ten.

**Say this.** "If you scored your agent once, about a quarter of your pass and
fail labels were a coin toss."

**The fix.** Score three times. Report the median and the spread, not a single
number. If the spread embarrasses you, that is information, not a bug.

### Clue two: the rows that vanished

Judges do not always answer. They return an empty string, or refuse, or write a
lovely paragraph with no number in it, or emit JSON that does not parse. Your
pipeline has a `dropna()` in it somewhere and those rows quietly leave.

**Why it matters.** They are not missing at random. They are missing hardest.
The judge goes quiet exactly when the case is difficult, which is exactly when
you needed a second opinion.

**The numbers.** 22% came back blank overall. On the clearest quarter of photos,
1% blank. On the blurriest quarter, 57% blank. And where you can compare,
agreement with humans is 0.74 on the clear ones and 0.41 on the hard ones.

So the 0.74 you published came almost entirely from the easy cases.

**Say this.** "This is survivorship bias with a dropna in the middle of it."
Then ask who has written that line. Every hand goes up, including yours.

**The fix.** Retry the blanks. Report the blank rate. Break every number down by
how hard the case was. Never average across difficulty and call it one score.

**Warn them.** This is the one fix that makes your headline metric go *down*.
0.74 becomes 0.62. Say out loud that this is the right thing to do anyway,
because now the number includes the cases that matter.

### Clue three: agreement that counts lucky guesses

Your judge agrees with human reviewers 75% of the time. Sounds like it works.

**Why it does not.** Most cases are easy, and on easy cases everybody says the
same thing. A judge that approves every single order, reading literally nothing,
scores 57% on this data, because 57% of orders genuinely should be approved. So
your judge beat "approve everything" by eighteen points, not by seventy five.

Correct for the agreement you would get by luck and what is left is **0.50**.
The statistic is Cohen's kappa. Under 0.4 is poor, 0.4 to 0.6 is moderate,
above 0.8 is strong. Moderate is not a shipping gate.

**Say the idea before the name.** Never open with "kappa". Open with "a judge
that approves everything scores 57 percent", then name it once, then move on.

**The fix.** Always print the chance corrected number next to the always approve
baseline. The raw percentage flatters you every single time.

### Clue four: confident, beautifully written, and wrong

This is the one that costs money, and it is not a measurement error at all. It
is the wrong question.

A graded judge answers "was this handled well?". It reads the refund letter, sees
warmth, clarity, a proper apology, correct policy citation, and gives it a nine.
The letter gave away twenty two dollars for a photo of the correct pizza.

**The numbers.** The graded judge approved 89% of the confident wrong refunds.
Add a second judge that answers one yes or no question, "was this the right
call?", and that drops to 10%. False refusals stay at 36%, unchanged. You catch
almost all of the expensive errors and annoy no additional customers.

**Say this.** "A score out of ten answers one question. Nobody ever asked it
whether the answer was correct."

**The fix.** Two judges. One graded on quality, one binary on correctness.
Require both. The binary one is cheaper than the graded one, because it emits
one token instead of a paragraph.

---

## The two numbers that make people sit up

### Compounding

One step held its verdict 73 times in a hundred. That sounds survivable.

But nobody grades one step. You grade an agent, and this agent has six steps.
0.73 to the power of six is **0.15**. Fifteen orders in a hundred come out the
same way twice.

If someone asks, eight steps is 7.7%. The maths is simply `(1 - flip_rate)^k`.

### Decision risk

This is the slide to aim at whoever controls budget.

Two versions of the agent. One genuinely is better. You score a hundred orders
on each and ship the winner. **You name the wrong version one time in four.**

To get that to nine times out of ten you need about four hundred orders per
version. That is the sentence that gets eval work funded, because "our
correlation is 0.74" funds nothing.

---

## Your story, and why it belongs in the middle

Slides 20 and 21. This is the emotional centre and the only part nobody else
could give.

A model refused a request and explained itself beautifully. It named the
dangerous object in the image, said where it was sitting, declined politely.
There was no object. You had already removed it. And your evaluation scored that
refusal as correct, because it read like an excellent refusal.

**The line that lands:** "My scoring never checked whether the model was right.
It checked whether the model sounded right."

Then connect it forward, out loud: a judge that grades prose will love a
confident wrong refund for exactly the same reason. Clue four is your story
happening to somebody else's money.

Do not rush these two slides. Let the "there was no object" line sit for a full
second before you continue.

---

## Running order and timing

Thirty minutes. The clock is in the bottom bar, press `start` as you begin.

| Slides | Minutes | Notes |
|---|---|---|
| 1 to 3 | 0:00 to 2:00 | Title, twenty seconds on you, why they should care |
| 4 to 7 | 2:00 to 6:00 | Four words defined. One minute each, do not linger |
| 8 | 6:00 to 6:30 | The plan. Name the four things, do not read the slide |
| 9 to 13 | 6:30 to 10:00 | The pizza. This is where you buy their attention |
| 14 to 17 | 10:00 to 13:00 | Who checks it, the thesis, the instrument framing |
| 18 to 19 | 13:00 to 14:30 | Hands up twice. Wait properly both times |
| 20 to 21 | 14:30 to 16:30 | Your story |
| 22 to 23 | 16:30 to 17:30 | The report, and would you ship |
| 24 to 28 | 17:30 to 23:00 | Clues one and two, with two live demos |
| 29 to 31 | 23:00 to 26:00 | Clues three and four, third demo |
| 32 to 33 | 26:00 to 28:00 | Compounding, then decision risk |
| 34 to 35 | 28:00 to 30:00 | Checklist and close |

**If you are running late**, cut slides 6, 7, 12 and 17. The argument still
closes and you keep all three demos. Never cut the demos, they are the reason
this talk is different from a blog post.

**If you are running early**, slow down on 20 and 21, and take a question after
clue two.

---

## Driving the deck

| Key | Does |
|---|---|
| right arrow, space, or page down | next slide |
| left arrow | previous |
| `N` | speaker notes panel on and off |
| a number then Enter | jump to that slide |
| `start` button | the clock, turns rose past 30:00 |

**The three demos.**

- **Slide 25.** Press "Score them" once, read the average out loud as if it were
  real. Press again, and let them watch the cells change colour. Press a third
  time. Then flip the switch on the right to "what to do", and the same data
  reports itself with its spread.
- **Slide 28.** Flip between "drop the blanks" and "ask again, keep them". Point
  at the big number going down. That is the honest number.
- **Slide 31.** Flip to "add a second". Point at the false refusal row staying
  at 36%, because that is the objection you will get.

All three run entirely inside the page. No terminal, no API key, no network. They
cannot fail because of the venue wifi.

---

## Questions you will get, and answers

**"Doesn't temperature zero fix the instability?"**
No, and this is the most common misconception in the room. Temperature zero
fixes the sampling, not the arithmetic. Batching, GPU floating point ordering,
expert routing and load balancing across replicas all move the logits. Say it
plainly: temperature zero is not determinism.

**"Wouldn't a bigger judge model solve this?"**
It helps with clue three and a little with clue one. It does nothing for clue
four, because clue four is not a capability problem, it is asking the wrong
question. A smarter model still answers "was this written well" beautifully.

**"Human reviewers disagree too, so isn't this unfair?"**
Yes, and that is exactly the point, not a rebuttal. We know human agreement is
imperfect because somebody measured it. Report kappa between your humans too.
Then you have two instruments with known error bars instead of one with none.

**"Your data is synthetic. Why should I believe the numbers?"**
Be completely straight about this. The trace comes from a simulator whose
parameters are calibrated to effect sizes reported in published work, source by
source, in `docs/calibration.md`. The numbers are there so the demo runs offline
and reproducibly. The point is not "trust my 21%". The point is "run these six
audits on your own judge output and see what you get". That is what the repo is
for.

**"Doesn't a second judge double my cost?"**
No. The second judge is binary. It emits one token, not a paragraph. In practice
it costs less than the graded judge it is protecting, and it is the single
highest value change on the checklist.

**"How many runs is enough?"**
Three is the minimum that tells you anything. If your decision threshold sits
inside the spread you measured, you need more runs or a better protocol, and
that is itself the finding.

**"What about position bias and length bias?"**
Real, measurable, and in the repo. Pairwise verdicts flip about 40% of the time
when you swap which candidate comes first. Length still predicts score after
controlling for human judged quality. You cut them from the talk for time, and
you can say so honestly.

---

## Things that could go wrong, and what to do

**The projector washes out the cream background.** The deck still reads. Every
broken and fixed state carries a word and a glyph as well as a colour, precisely
so it survives bad projectors and colour blindness.

**No wifi and the fonts do not load.** It falls back to Georgia and Helvetica
and still works. Nothing else in the page needs the network.

**A demo does not respond.** You clicked faster than the animation. Click once
more. If it still will not, every number is already printed on the slide before
it, so just say the number and move on. Never debug on stage.

**Someone wants to talk about a specific vendor's judge.** Do not get pulled
into it. "I have not audited that one. The six audits are in the repo and they
take about twenty minutes to run against it. Come and find me after and we can
look together." That answer makes you look generous and moves the talk on.

**Somebody senior pushes back hard.** Agree with the half that is true. "You are
right that this is cheap and fast and that is why I use judges too. My claim is
only that we should measure the thing before we trust it." Almost nobody argues
with that.

---

## Four things to have in your pocket

Lines worth having ready, because they are the ones people write down.

1. "Temperature zero is not determinism."
2. "The judge is the only part of the stack with no tests."
3. "A second opinion is not a measurement."
4. "Nobody can act on a correlation. Everybody can act on: at our eval size we
   name the wrong version one time in four."

---

## The last thirty seconds

Land on the sentence, not the QR codes.

> Your judge is an instrument. Calibrate it before you trust it.

Then stop talking and let them scan. Silence while forty people hold up their
phones is a good silence. Do not fill it.
