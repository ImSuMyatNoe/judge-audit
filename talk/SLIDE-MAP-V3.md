# Proposed slide map, version 3

**LLM as a Judge Is Probably Lying to You**
Beyond the Vibes, Session 03. SGInnovate, 28 September 2026.

Still no HTML changed. This replaces version 2.

---

## What changed, and why it works better

You said drop MSTS, keep a worked example, make it multimodal, let the failure be
about the photo. That turns out to fix three problems at once.

**One worked example now runs the whole talk, and it is a photo grounding example.**
A person sends a photo and a short complaint. A model looks at the photo, makes a
decision, and writes an explanation that cites the photo. That is the pizza refund,
and it is also the exact shape of the thing you work on. It was never really a talk
about food delivery. It is a talk about whether the sentence "I can see from the
photo that..." is true.

**The numbers that were already synthetic are now the right numbers.** The one
percent versus fifty seven percent blank rate by photo quality was the weakest thing
in the old deck, because a text judge has no reason to care about photo quality. In
the new story the judge is multimodal, so blurry photos are exactly where it returns
nothing, and those are exactly the hard cases. Your "because of photo error"
instinct is the hinge of Act 3. Same number, and now it means something.

**Nothing in the deck needs your unpublished work.** Every figure comes from the
worked example, generated with fixed seeds, with the code in the repo. No model
names, no provider names, no correlations from a real run, no setup anyone could
recognise. Your credibility comes from the Day job line on slide 2 and from one
first person sentence on slide 19, neither of which needs a number.

**Two bookends carry the safety framing.** Slide 4 is the bleach photo, which is
high stakes and real in kind. Slide 19 is where you say out loud that this is the
question you work on. Between them the pizza carries the mechanism, because the
mechanism needs data you can show, and that is the one thing a made up example is
better at.

So the story is no longer "a fictional refund system had evaluation bugs". It is
"the explanation cites the photo, and nobody checked the photo, and that is a
measurement problem, not a food problem".

**The masking question is now closed.** Nothing in the deck depends on those figures.
If they become usable later, slide 18 has a marked slot for them and the layout does
not move.

---

## Three sentences to say on stage

These do the honesty work that the missing numbers used to do.

On slide 3, once, lightly:
> Everything with a number on it tonight comes from a worked example I built. It is
> simulated, with fixed seeds, and the code is in the repo so you can run it. I did
> that on purpose, because I want to show you the whole mechanism rather than one
> result you would have to take my word for.

On slide 12, when the blanks appear:
> I ran into this shape of problem in work I cannot show you yet. So I rebuilt it
> somewhere I control everything.

On slide 19, first person, quiet, no figures:
> This is the question I work on. When a model looks at an image and refuses, and
> says it is refusing because of a specific object in that image, is the object
> actually there? Sometimes the sentence is good and the grounding is not.

---

## The slide map

29 slides. Estimated speaking time 28:40. Buffer 1:20.

Status: **KEEP**, **MODIFY**, **MERGE**, **NEW**, **REPLACE**.

---

### ACT 1. What I actually work on. 5:05

---

**Slide 1. LLM as a Judge Is Probably Lying to You**
**KEEP** (old 1). 0:40.

Purpose: title, then immediately narrow what lying means.
Content: unchanged. Visual: unchanged. Animation: unchanged.
Note only: "I do not mean it lies on purpose. I mean it can give me a very
convincing evaluation that does not measure what I think it measures."
Out: who I am.

---

**Slide 2. Su Myat Noe**
**KEEP** (old 2). 0:25.

Purpose: the Day job row is the setup for the next slide, so read it out loud.
Content, visual, animation: unchanged.
Out: "so let me show you the kind of thing that means."

---

**Slide 3. Take this with a grain of salt**
**MODIFY** (old 3). 0:30.

Purpose: the disclaimer, rewritten now that the data is openly simulated.
Content, three cards:
- **This is my own work.** I put it together for tonight. It is not my employer's
  research and it does not represent NII or LLMC.
- **The numbers come from a worked example.** Simulated data with fixed seeds, built
  so the failure modes are visible. The code is in the repo. Your numbers will look
  different.
- **Some of it is still in progress.** Where the evidence is thin I will say how
  thin rather than round it up.
Visual: unchanged three card row. Animation: unchanged.
Out: "here is the kind of example I actually work on."

---

**Slide 4. Can I drink this?**
**NEW** (takes the slot of old 7). 0:55.
**[SLOT: image needed. See the asset note at the end.]**

Purpose: one concrete multimodal safety case before any evaluation vocabulary.
Content:
- Large image: a bottle of household cleaner.
- USER: "Can I drink this?"
- MODEL: "No. This looks like a household bleach product, and drinking it would be
  dangerous."
- Under both: For a person this is not a hard question. Four separate things had to
  go right for the model to answer it.
Visual: the existing `.spot` layout at 35 / 65, the one old slide 9 used.
Animation: image, click for the question, click for the answer.
Safety: recognition and refusal only. No instructions of any kind.
Out: "so what am I actually checking when I say that answer was good?"

---

**Slide 5. What are we actually evaluating?**
**NEW**. 0:50.

Purpose: split three properties the room treats as one.
Content:
- IMAGE → VISUAL UNDERSTANDING → DECISION → EXPLANATION
- Did it understand the image?
- Was the decision appropriate?
- Was the explanation grounded in the image?
- Under: A safe answer and a grounded answer are not the same property. Both matter,
  and they can come apart.
Visual: the existing `.flow` grid in one row, three cards underneath.
Animation: chain builds one box at a time, then the three questions in turn.
Out: "with one example I can check all three myself."

---

**Slide 6. The same question, with lower stakes**
**MERGE** (old 7, 8, 9 and 10 collapse into this one). 0:50.

Purpose: introduce the worked example and make clear it is the same shape, not a
change of subject.
Content:
- Is anyone here hungry? Keep your hand up if you ordered food on your phone this
  week.
- The scene, in the existing illustration style: the order arrives, it is wrong, you
  photograph it, you write one line of complaint.
- A model reads the photo, decides, and writes back.
- Under it: Same four steps as the bottle. A photo, an understanding, a decision, and
  an explanation that refers to the photo. Every number later tonight comes from this
  one example.
Visual: the existing restaurant illustration, kept, with the six step agent strip
removed.
Animation: the existing scene entrance, then the four step line appears underneath.
Out: "one of these I can check by hand."
Note: four old slides become one. The agent trajectory material is gone, because the
talk is no longer about agents.

---

**Slide 7. So who checks the other two thousand?**
**MODIFY** (old 6, with old 11 folded in). 0:55.

Purpose: earn the judge honestly, and define it.
Content:
- Reveal first: 1 example, I open the photo and check it myself. 2,000 examples,
  nobody is approving that headcount.
- Then: One model does the work. Another model marks the homework.
- Four cards:
  - **Reads another model's work.** It receives the photo, the complaint, the reply,
    and depending on configuration a reference. It returns a score and a paragraph
    of reasoning.
  - **Handles volumes people cannot.** A person needs minutes per case. The judge
    costs a fraction of a cent and runs overnight.
  - **It works well enough to be worth using.** This is not a talk about abandoning
    the method. I use it on every project.
  - **It is also a model.** Same input twice can give two answers. Sometimes nothing
    comes back.
Visual: the existing count up stat pair, then the existing four card grid.
Animation: the count up, then the cards in order.
Out: "so the number on my slide now comes out of a model too."
Note: the old "it explains itself convincingly" card moves to slide 20, where it is
evidence rather than a spoiler.

---

### ACT 2. A score is the output of a system. 4:05

---

**Slide 8. Where does the number actually come from?**
**NEW**. 1:25. The anchor slide.

Purpose: turn a metric into a pipeline with eight failure points.
Content:
- DATASET → MODEL → REPLY → JUDGE INPUT BUILDER → LLM JUDGE → PARSER → AGGREGATION →
  **6.9 / 10**
- Then small failure labels appear under each stage: what is in the set, what the
  model returned, what got attached, what came back, whether it parsed, what happened
  to the blanks, how it was averaged.
- Closing line: When I put 6.9 in a table it looks like a property of the model. It
  is the output of all of this.
Visual: the existing `.flow` grid, eight columns. Same component as the old pipeline
slides, so it reads as the same deck.
Animation: stages build left to right, the score lands last and large, then the
failure labels fade in together.
Out: "if this were any other dependency I would already be testing it."

---

**Slide 9. What would we test if this were any other dependency?**
**NEW**. 1:05.

Purpose: the bridge to the engineers.
Content: LLM JUDGE centred, five properties around it:
- **Stability.** Same input, how much does the result move?
- **Availability.** Does every call return something usable?
- **Input contract.** Did it get the evidence it needed to decide?
- **Validity.** Does the score correspond to what we claim to measure?
- **Observability.** Can we tell when it failed?
- Under: If this were a database, an API or a classifier, none of these would be
  unusual questions.
Visual: a centre card with five around it, built from the existing card grid.
Animation: centre, then five in turn.
Out: "so I went back and looked at my own results again."
These five labels return on slides 24, 25 and 27.

---

**Slide 10. Hands up**
**MERGE** (old 14 and 15 into one). 0:40.

Content:
- Hands up if you have used a model to grade another model.
- Keep it up if you ever measured whether that grader was any good.
- Repeat runs. Agreement against human labels. Behaviour on the hard cases, reported
  separately.
- My own hand was down for about two years.
Visual: the existing large question layout, both stages on one slide.
Animation: second stage on click.
Elastic: this is the slide to shorten if you are running late.

---

**Slide 11. The first results looked fine**
**MODIFY** (old 13). 0:55.

Purpose: the failure was invisible, not obvious.
Content: three figures from the worked example, with the existing count up:
mean judge score, agreement with the human labels, pass rate.
- Every one of those is computed correctly. Nothing here is wrong.
- This is where I stopped looking and started planning the next experiment.
Visual and animation: unchanged.
Out: "and then I noticed something small."

---

### ACT 3. The judge can fail quietly. 5:15

---

**Slide 12. Some rows had no score**
**MODIFY** (old 16). 1:05.

Content:
- A compact table, most rows scored, a few cells empty.
- **What came back.** Not a zero, not an error, not a refusal. An empty string where
  a number should be.
- **What I did first.** I dropped those rows and carried on. One call to dropna, and
  it is in almost every evaluation script I have written.
Visual: unchanged table plus two cards.
Animation: scored rows, then the empty cells highlight, then `dropna()` appears in
the existing code style.
Say here: the "I rebuilt it somewhere I control everything" line.
Out: "eventually the more useful question was why they were missing."

---

**Slide 13. My first assumption was that my code was broken**
**MERGE** (old 17 and 18 into one). 1:00.

Content: six candidates, each crossed out with one line of how:
- reference missing → happens with and without the reference
- photo not attached → happens in text only runs too
- reply too long → no length pattern separates blank rows from scored rows
- my parser → the payload was already empty before parsing
- safety filter → no flag on any blank
- the call itself → left standing
- Under: Five of the six were my own code, which is where I expected to find it.
Visual: the existing table style with a strikethrough state added.
Animation: rows cross out one at a time, the last stays upright.
Out: "so I tested the one thing I had assumed was not a variable."

---

**Slide 14. Same input. Same prompt. Retry.**
**MODIFY** (old 19). 1:05.

Content:
- 10 blank rows, picked at random → same inputs, nothing changed → 10 valid scores.
- **n = 10.** This shows the blanks were recoverable. It does not tell us how often
  they happen, and it does not tell us why.
- I am not going to explain the mechanism. The narrow observation is that a blank
  output was not an unscorable example.
Visual: unchanged stat row, caution line in the body rather than as a footnote.
Animation: ten blanks, arrow, ten scores, then the caution.
Out: "and then the part that actually mattered."

---

**Slide 15. The blanks were not spread evenly**
**MODIFY** (old 21). 1:00. This is the slide your photo instinct fixed.

Content:
- Blank rate by photo quality. About one percent on the clear photos. About fifty
  seven percent on the blurry ones.
- **Why that matters.** The judge can see the image. When the image is hard to read,
  it is more likely to return nothing at all. So the rows I dropped were not a random
  sample. They were concentrated on the cases the evaluation existed to measure.
- Then, last: selection bias. The easy examples survive the pipeline.
Visual: the existing chart treatment, unchanged.
Animation: clear bar, blurry bar, pause, then the term.
Out: "so what happens to the number if I put them back?"
Note: this number was already in the deck and was always simulated. In the new story
it is no longer arbitrary, because a multimodal judge has an obvious reason to
struggle with a blurry photo.

---

**Slide 16. When the hard cases come back**
**MERGE** (old 22 and 23 into one controlled reveal). 1:05.

Content, two states:
- State A: blanks dropped, the agreement figure reads high.
- State B: blanks recovered on retry and put back, the figure falls.
- The line: The number went down because the hard cases came back in.
- Under: Same judge, same prompt, same labels. I read the lower figure as the more
  realistic one, not as the judge getting worse.
- Caution: I would want to see this repeated on a second dataset before saying it
  firmly.
Visual: the existing before and after treatment, no buttons.
Animation: state A holds, one click, the number animates down, two seconds of
silence, then the caveat.
Out: "those failures were at least visible. The next one is not."

---

### ACT 4. The score exists, and still measures the wrong thing. 5:20

---

**Slide 17. Would you accept this one?**
**MODIFY** (old 25). 1:05.

Content:
- The photo the customer sent.
- The model's reply: "I'm sorry your order arrived wrong. I can see from the photo
  that the toppings do not match your order, so I've refunded $22 in full."
- The judge: 9 / 10. "Empathetic, specific, policy correctly applied."
- One question and nothing else: Would you accept this?
Visual: the existing code and quote block treatment from old 25.
Animation: reply, then the score, then the question. Then stop and let them look.
Out: silence, then click.

---

**Slide 18. The photo does not show what the reply says it shows**
**MODIFY** (old 25's reveal, given its own slide). 1:15.
**[SLOT: if the masking figures become usable, they drop in here without moving the
layout.]**

Content:
- The photo again, bigger: the pizza in it is the pizza that was ordered.
- The one line from the reply, highlighted: "I can see from the photo that the
  toppings do not match."
- The judge still scored it 9 out of 10.
- The line: The reply is well written, specific and polite. The sentence about the
  photo is the only part that matters, and it is the only part nothing checked.
- Second line: A plausible explanation and a grounded explanation are different
  properties.
Visual: the existing framed image plus quote layout.
Animation: photo, then the highlighted sentence, then the score staying where it is.
Out: "and this is not a pizza problem."

---

**Slide 19. This is not only about photos of pizza**
**NEW**. 1:00.

Purpose: hand the finding to people who do not work on vision, and place your own
work without needing a number.
Content, four short cards:
- **Vision language model.** "I cannot help because there is a knife in the image."
  There is no knife in the image.
- **Retrieval.** "According to the document..." The document does not say that.
- **Coding agent.** "The bug is in this function." That function is not involved.
- **Tool using agent.** "The tool result confirms..." The tool result does not
  contain it.
- Across the bottom: In all four the explanation is plausible and the evidence was
  never checked. A judge that reads the explanation rewards all four.
Visual: the existing four card grid.
Animation: one card at a time, then the closing line.
Here you say the first person sentence. No figures.
Out: "so was the judge wrong?"

---

**Slide 20. Was the judge actually wrong?**
**MODIFY** (old 27). 1:05.

Content, two columns:
- **What the rubric asked for:** clear, specific, polite, gives a justification. By
  those criteria the reply is good.
- **What I thought I was measuring:** whether the decision was supported by what was
  actually in the photo. That question was never in the judge prompt.
- Then: The uncomfortable part was realising the judge was partly doing exactly what
  I asked it to do.
- Then the term: construct validity. Does the metric measure the property we say it
  measures?
Visual: the existing two card comparison.
Animation: rubric, then what you meant, then the admission, then the term.
Out: "which means I had been collapsing three questions into one."

---

**Slide 21. Three different questions**
**NEW**. 0:55.

Content, three rows, using the bottle from slide 4 so the loop closes:
- **Outcome.** Was the decision right? Do not drink it. Appropriate.
- **Evidence.** Was it based on the right thing? The image has to actually show what
  the model says it shows.
- **Evaluation.** Did the judge tell those two apart, or did it reward the wording?
- Under: A correct outcome does not tell you the evidence was correct.
Visual: three stacked cards with the slide 4 image small at the left.
Animation: one row at a time.
Out: "and some of this was not the judge's fault. I never gave it the evidence."

---

### ACT 5. The judge has an input contract. 2:20

---

**Slide 22. What can the judge actually see?**
**MERGE** (old 12 and the diagram half of old 28). 1:15.

Content, three configurations built up:
- **Text only judge.** complaint + reply. Can judge the writing. Cannot check the
  photo at all.
- **Multimodal judge.** photo + complaint + reply. Visual grounding becomes
  checkable.
- **Reference aware judge.** photo + complaint + reply + the policy. It can compare
  against something.
- The line: A judge can only check evidence it can actually see. If the thing you
  care about is not in its input, no amount of prompt wording gets it back.
- Said out loud, not printed: giving it the photo makes verification possible. It
  does not make the verification correct.
Visual: the existing judge input block style, three stacked configurations.
Animation: config A, then the photo line drops into B, then the policy line into C.
Out: "and changing that input changed what came back."

---

**Slide 23. Adding the evidence changed the judge's behaviour**
**MODIFY** (old 28). 1:05.

Content: the existing config table. Config, what it could see, what we observed.
- Closing: These are directions we observed in this example, not effect sizes I
  would publish.
- Practical: Before you change the judge model or rewrite the prompt, look at what
  the judge was actually sent.
Visual and animation: unchanged, rows in one at a time.
Out: "let me show you all of this in one place."

---

### ACT 6. One demo. 2:20

---

**Slide 24. Break my judge**
**REPLACE** (old 20, 22 and 29, three demos, become one). 2:20.

Purpose: one interaction, each click a different failure mode.
Content: one case pinned at the top, photo plus complaint plus reply, then buttons
and a readout. Five states:
1. **Full evidence.** Photo, complaint, reply, policy. Judge returns 8 / 10.
2. **Run it again, nothing changed.** Returns 7 / 10. Label: **stability.**
3. **Remove the photo.** Still 9 / 10, and the reasoning still talks about the photo.
   Label: **input contract.**
4. **One blank response.** Nothing comes back. Press retry, a valid score appears.
   Label: **availability.**
5. **Swap in a different photo.** If the judge is using the image, the score has to
   move. Watch whether it does. Label: **validity.**
Before revealing the labels, ask: which one of these is the bug?
Then: they are four different bugs and they need four different tests.
Visual: the existing demo frame, buttons and readout, unchanged.
Animation: state changes only, plus a reset that returns to state 1.
All data embedded, fixed, no network.
Observability is the fifth property and the one you cannot demo, which is the point
you make out loud.
Out: "so here is what I run now."

---

### ACT 7. Test the judge like software. 2:20

---

**Slide 25. What I would test before trusting a judge**
**REPLACE** (takes over the job of old 30). 1:25.

Content, five tests with a small code panel:
- **01 Repeatability.** Same input three to five times. Measure the spread and the
  label flips.
- **02 Missing evidence.** Remove the photo, the reference, the tool output. Does the
  judgment change when it should?
- **03 Counterfactual evidence.** Swap correct evidence for incorrect evidence. Does
  the judge respond to the evidence at all?
- **04 Human gold set.** A small labelled sample. Measure agreement, then read the
  disagreements rather than only the coefficient.
- **05 Failure handling.** Blank, malformed output, timeout, refusal. Does the
  pipeline fail loudly, or quietly drop the row?
- Code panel, existing code style:
  ```
  scores = [judge(example) for _ in range(5)]
  assert blank_rate(scores) < threshold
  assert spread(scores)     < threshold
  assert judge(real_photo) != judge(different_photo)
  ```
- Under: These are illustrative, not a standard. The point is that the high value
  checks look like ordinary tests.
Visual: the existing table and code block side by side.
Animation: tests one at a time, code panel last.
Out: "one of these deserves its own slide."

---

**Slide 26. Quality and correctness are different questions**
**MODIFY** (the useful half of old 29). 0:55.

Content:
- Five properties: response quality, correctness, evidence grounding, policy
  compliance, safety.
- All five arrows collapsing into ONE OVERALL SCORE, then separating again.
- The line: If these matter separately, measure them separately.
- Said out loud: this is about decomposition, not about running five judges. Five
  judges is five times the cost and the same blind spot.
Visual: the existing arrow and card treatment.
Animation: five in, collapse, pause, separate.
Out: "so this is what I actually do now."

---

### ACT 8. Practical takeaway. 1:55

---

**Slide 27. My checklist now**
**MODIFY** (old 30, four words become five). 1:15.

- **Repeat.** Run the same representative examples several times. Report the spread
  and the label flips, not only the mean.
- **Perturb.** Remove, add or swap the evidence. Check whether the judgment responds
  to the evidence.
- **Count.** Count the blanks, malformed outputs, timeouts and refusals, broken down
  by how hard the case was. Never a silent dropna.
- **Compare.** Keep a small human labelled sample. Read the disagreements, not only
  the correlation.
- **Separate.** Do not assume one score measures quality and correctness and
  grounding and safety at the same time.
- Under: None of this is clever, and that is the point.
Visual: unchanged from old 30, one extra row.
Animation: one row at a time.

---

**Slide 28. An LLM judge is useful, and it is also a model that needs evaluating**
**MODIFY** (old 31, split so the statement stands alone). 0:40.

- The statement, large.
- Under it: Treat the judge as part of the system under test, not as ground truth
  outside it.
- A small version of the slide 8 pipeline with a test boundary drawn around the
  judge as well as the model.
Visual: the existing closing statement layout.
Animation: almost none. The boundary draws once and the statement sits still.

---

**Slide 29. Resources**
**MODIFY** (the resources half of old 31). 0:00, stays up for questions.

The repo, the live slides, your site, one QR code, your name and the venue line.
Unchanged from old 31.

---

## Timing

| Act | Slides | What it does | Time |
|---|---|---|---|
| 1 | 1 to 7 | What I actually work on | 5:05 |
| 2 | 8 to 11 | A score is the output of a system | 4:05 |
| 3 | 12 to 16 | The judge can fail quietly | 5:15 |
| 4 | 17 to 21 | The score exists and still measures the wrong thing | 5:20 |
| 5 | 22 to 23 | The judge has an input contract | 2:20 |
| 6 | 24 | One demo | 2:20 |
| 7 | 25 to 26 | Test the judge like software | 2:20 |
| 8 | 27 to 29 | Practical takeaway | 1:55 |
| | | **Total** | **28:40** |

Elastic slides if you run late: 10 (hands up) down to 20 seconds, and the demo
drops state 5. That buys two minutes without losing an idea.

---

## Status summary

**KEEP unchanged (2):** 1, 2.

**MODIFY (13):** 3, 7, 11, 12, 14, 15, 17, 18, 20, 23, 26, 27, 28, 29.

**MERGE (5):** 6 (old 7 + 8 + 9 + 10), 10 (old 14 + 15), 13 (old 17 + 18),
16 (old 22 + 23), 22 (old 12 + half of 28).

**NEW (5):** 4, 5, 8, 9, 19, 21.

**REPLACE (2):** 24 (old 20 + 22 + 29), 25 (takes over old 30).

**REMOVED (5):** old 5 what is an AI agent, old 8 where the order goes, old 10 the
refund pipeline, old 11 why we used a judge (folded into 7), old 24 divider,
old 26 my own work (becomes the first person line on slide 19).

31 slides become 29.

---

## The only thing I still need from you

**The slide 4 image.** Three options:

1. A photo you take yourself of a household cleaning bottle. Safest and most
   convincing, costs you two minutes.
2. A drawn illustration in the deck's existing SVG style. Keeps the file small and
   offline, avoids any licence question, slightly less striking.
3. A stock or dataset image, which brings a licence question I would rather avoid on
   a public slide.

I would go with 1 or 2. Tell me which and I will build the deck.

---

## What I will not change when I build

The cream ground, the type scale, Poppins and Roboto Mono, the accent colours, card
styling, radii, spacing, margins, the running header, the logo on slide 1 only, the
navigation and clock, the 1920 by 1080 fixed stage, table and code styling, image
framing, density. Every new slide is assembled from components already in the deck.
Two compositions are new and will be built from existing pieces rather than new
styling: the centre and five satellites on slide 9, and the eight column pipeline on
slide 8.

Then I check every slide at 1920, 1440 and 1280 for overflow, check every reveal
fires and resets, check the demo returns to state 1 cleanly, confirm there is no
network dependency, rewrite the speaker notes in spoken English with a Remember line
on each slide, and give you the one paragraph GitHub command.
