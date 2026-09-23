# Refinement audit of the current 33 slide deck

No HTML changed. This is the proposal.

Result: **31 slides, 27:50 of planned content**, two slides merged away, three moved,
one mechanical addition, and the five framework words made consistent everywhere.

---

## The six things that actually matter

Everything below is detail. These six are the decisions.

**1. Slide 21 and the demo currently tell the same story twice.**
Slide 21 covers the object and the refusal does not change. Demo state 5 covers the
object and the score does not change. Right now those read as the same beat, which is
why the demo feels like a dashboard rather than a payoff.

The fix is to split the subject. Slide 21 is about **the model**: cover the object, the
model's refusal does not move. Demo state 5 is about **the judge**: cover the object,
the judge's score does not move either. Same instrument, two different things being
audited, and the second one is worse, because the judge is the thing I am using as a
measurement. That turns the demo into an escalation instead of a repeat, and it makes
evidence sensitivity the hinge that connects your research to the engineering lesson,
which is what you asked for.

**2. The five framework words are not consistent, and that is my error.**
Slide 29 currently says Repeat, Remove, Swap, Compare, Fail. Slide 31 says Repeat,
Perturb, Count, Compare, Separate. Two different frameworks, eight words, in the last
five minutes of the talk. Slide 29 gets rewritten to the five words from slide 31, with
remove and swap demoted to sub actions under Perturb, and blank, malformed and timeout
demoted under Count.

**3. The five dependency properties change.**
Slide 12 currently lists stability, availability, input contract, validity,
observability. Observability never pays off anywhere and the demo cannot show it.
It gets replaced by **evidence sensitivity**, which is the property the whole second
half is about. New five: stability, availability, input contract, evidence
sensitivity, validity. These become the demo's four labels plus validity as the
conclusion.

**4. The masking claims are too strong and need weakening in two places.**
Slide 21 currently ends "Whatever produced that sentence, it was not this object."
Slide 22 says "the object it named was not what produced the refusal." Both assert
internal causality that masking cannot establish. They become "the stated visual
reason is difficult to verify as load bearing", and slide 22 gains the reason why:
redundant cues, surrounding context and correlated features mean masking is evidence,
not proof.

**5. The deck needs in slide reveals, which it does not currently have.**
You asked for the pipeline to look clean before the failure points appear, for the
three questions to come one at a time, for the rubric to appear before what I thought
I measured. Right now everything on a slide animates in together on arrival. I propose
one small mechanical addition: the right arrow advances to the next reveal inside a
slide, and only moves to the next slide when the reveals are done. No visual change, no
new styling, roughly forty lines of JavaScript. This is the only structural addition I
am proposing and it affects six slides.

**6. Two slides come out.**
Slide 30 (quality and correctness) is absorbed into slide 31's Separate row and one
spoken line in the demo wrap up. Slide 27 (adding the evidence changed the judge's
behaviour) is absorbed into slide 26 as a fourth column. Both were saying a second
version of what the slide before them said.

---

## Slide by slide

Numbers below are the **current** deck. The new numbering is given at the end.

---

**SLIDE 1 — LLM as a Judge Is Probably Lying to You**
**KEEP**

- ROLE: title, and immediately narrow what lying means.
- PROBLEM: none.
- CHANGE: none to the slide. Note only: say the narrowing sentence before anything else.
- IN: none. OUT: who is saying this.
- TIME: 0:40. ANIMATION: unchanged.

---

**SLIDE 2 — Su Myat Noe**
**KEEP**

- ROLE: establish that the next slide is your actual job, not a hypothetical.
- PROBLEM: none.
- CHANGE: none.
- IN: from the title. OUT: the Day job row is read last and becomes slide 4.
- TIME: 0:25. ANIMATION: unchanged.

---

**SLIDE 3 — Take this with a grain of salt**
**KEEP, wording only**

- ROLE: the disclaimer, and the honest statement that the data is simulated on purpose.
- PROBLEM: the middle card says the numbers come from a worked example but does not say
  why that is a strength.
- CHANGE: middle card gains one clause: "so you can run the same checks on your own
  data". Nothing else.
- IN: from the bio. OUT: "here is the kind of example I actually work on."
- TIME: 0:25. ANIMATION: unchanged.

---

**SLIDE 4 — Can I drink this?**
**KEEP, wording only**

- ROLE: one concrete case everybody understands, before any vocabulary.
- PROBLEM: none. This slide works.
- CHANGE: the foot note becomes a cleaner hand off: "This is the case the system gets
  right. It is not the case that taught me anything."  (Already close, tighten only.)
- IN: from the Day job row. OUT: "here is one that is less obvious."
- TIME: 0:40. ANIMATION: image, click for question, click for answer. Unchanged.

---

**SLIDE 5 — How do I use this safely?**
**MODIFY**

- ROLE: plant the case that pays off at slide 20 and 21.
- PROBLEM: the second card currently says "whether it actually saw a weapon is a
  separate question", which gives away the punchline fifteen slides early. The room
  should not suspect the grounding problem yet.
- CHANGE: cut that sentence. The card says only that the refusal is confident and
  specific, and that the question was about chopping vegetables. Plant the object name,
  not the doubt.
- IN: "that one was easy. Here is one from the same evaluation set." OUT: "so what am I
  actually checking when I say a response was good?"
- TIME: 0:50. ANIMATION: unchanged.

---

**SLIDE 6 — What are we actually evaluating?**
**MODIFY, add reveal**

- ROLE: split understanding, decision and grounding into three properties.
- PROBLEM: all three questions appear at once, so the third one does not land as the
  interesting one.
- CHANGE: no content change. Add the in slide reveal: chain first, then the three
  questions one at a time. Say "a safe answer is not necessarily a grounded answer"
  on the third.
- IN: from the knife case. OUT: "let me be precise about that third one."
- TIME: 0:50. ANIMATION: chain builds, then three cards on three clicks.

---

**SLIDE 7 — What I mean by grounded**
**MODIFY**

- ROLE: currently a definition. It should be the seed of the method.
- PROBLEM: it defines grounded as a property. That is correct but inert. The sentence
  that makes the whole talk one investigation is the testable version, and right now it
  is buried inside a card.
- CHANGE: retitle to **"How would I check that?"** and make the lead the test, not the
  definition: if the stated reason is real, taking that object out of the image should
  change the answer. The two cards stay. This single sentence is what pays off at slide
  21 and again at the last demo state, so it has to be said plainly here.
- IN: "so what does grounded actually mean?" OUT: "but I cannot do that by hand at
  scale."
- TIME: 0:50. ANIMATION: lead, then two cards.

---

**SLIDE 8 — One image I can check myself**
**KEEP, wording only**

- ROLE: earn the judge honestly.
- PROBLEM: three count up numbers is one more animation than the point needs, and you
  asked to cut unnecessary counters.
- CHANGE: keep the three figures, drop the count up on the middle one so only the first
  and last animate. Foot note gains the bridge sentence: "so we do something completely
  reasonable, and ask another model to help."
- IN: from the grounding test. OUT: names the method.
- TIME: 0:35. ANIMATION: two counters, not three.

---

**SLIDE 9 — What is LLM as a judge?**
**KEEP**

- ROLE: define the method and be positive about it.
- PROBLEM: none. The four cards are in the right order.
- CHANGE: none.
- IN: from scale. OUT: straight into the hands up question.
- TIME: 0:50. ANIMATION: unchanged.

---

**SLIDE 13 — Hands up (MOVED to sit here, after slide 9)**
**KEEP, moved**

- ROLE: the one warm up interaction, and the "my hand was down too" admission.
- PROBLEM: at its current position it sits between the dependency slide and the first
  results, and it breaks the bridge "I did not start with these names, I started
  because something looked odd in my results." That bridge should be unbroken.
- CHANGE: move it to directly after slide 9. The room has just learned what a judge is,
  so asking whether they use one lands better there, and slides 10 to 12 then run
  straight into 14 and 15.
- IN: "so that is the method. Who here has used it?" OUT: "so let me show you what mine
  actually receives."
- TIME: 0:40. ANIMATION: unchanged. Elastic slide.

---

**SLIDE 10 — What the judge actually receives**
**KEEP**

- ROLE: plant the image line and the rubric line.
- PROBLEM: none, and the foot note pointing at the optional image line is doing real
  work for slide 26.
- CHANGE: none.
- IN: from hands up. OUT: "and out the other end comes a number."
- TIME: 0:50. ANIMATION: unchanged.

---

**SLIDE 11 — Where does the number actually come from?**
**MODIFY, add reveal**

- ROLE: the conceptual anchor of the first half.
- PROBLEM: the failure chips appear with the pipeline, so 6.9 never gets a moment of
  looking clean. You asked for the opposite order and you are right.
- CHANGE: three reveals. First the pipeline builds and the score lands, and you say the
  line about putting it in a table. Pause. Second click brings the chips. Third click
  brings the closing sentence. No content change, only sequencing.
- IN: from the judge input. OUT: "so what would I test?"
- TIME: 1:10. ANIMATION: build, pause, chips, line.

---

**SLIDE 12 — What would we test if this were any other dependency?**
**MODIFY**

- ROLE: the bridge to the engineers, and the foreshadow of everything that follows.
- PROBLEM: two things. Observability is in the list and never returns, which leaves a
  loose end. And the five read as abstract definitions rather than as things the
  audience is about to watch happen.
- CHANGE: replace observability with **evidence sensitivity**: "if I change evidence
  that should matter, does the evaluation respond?" Then add one spoken line in the
  notes: "I did not start with these names. I started because something in my results
  looked odd." That line is the bridge into the whole investigation.
- IN: from the pipeline. OUT: straight to the first results.
- TIME: 0:55. ANIMATION: five cards, one at a time.

---

**SLIDE 14 — The first results looked fine**
**KEEP**

- ROLE: establish that the failure was invisible.
- PROBLEM: none.
- CHANGE: none.
- IN: "so I went back and looked at what I already had." OUT: "and then I noticed
  something small."
- TIME: 0:45. ANIMATION: unchanged.

---

**SLIDE 15 — Then some rows came back with no score**
**KEEP**

- ROLE: the hinge, and the dropna confession.
- PROBLEM: none. This is one of the strongest slides.
- CHANGE: none.
- IN: from the calm. OUT: "so why were they missing?"
- TIME: 1:00. ANIMATION: rows, then blanks highlight, then dropna.

---

**SLIDE 16 — My first assumption was that my code was broken**
**KEEP**

- ROLE: ordinary debugging the room recognises.
- PROBLEM: none, and the strikethrough table is doing the work of three slides.
- CHANGE: none.
- IN: from the blanks. OUT: "so I tested the one that was left."
- TIME: 1:00. ANIMATION: rows cross out one at a time.

---

**SLIDE 17 — Same input. Same prompt. Retry.**
**KEEP, wording only**

- ROLE: the finding, with its limits attached.
- PROBLEM: the caution is good but the narrow claim could be sharper.
- CHANGE: the caution's last sentence becomes your wording: "in these examples, a blank
  output was not necessarily an unscorable example." Keep n = 10 prominent.
- IN: from the elimination. OUT: "but that raised a better question."
- TIME: 1:00. ANIMATION: unchanged.

---

**SLIDE 18 — The blanks were not spread evenly**
**MODIFY, wording only**

- ROLE: turn a data quality annoyance into a measurement bias.
- PROBLEM: the figures need the worked example label attached to them on the slide
  itself, not only in the notes, and the term selection bias currently appears before
  the plain English version has fully landed.
- CHANGE: the figcaption gains "in this worked example". The foot note is reordered so
  the plain sentence comes first and the term comes last: the easy images survive and
  the hard ones disappear, and the name for that is selection bias.
- IN: from the retry. OUT: "so what happens to the number when I put them back?"
- TIME: 1:00. ANIMATION: clear bar, blurry bar, pause, then the term.

---

**SLIDE 19 — When the hard cases come back**
**MODIFY**

- ROLE: the number falls, and the first half closes.
- PROBLEM: the transition out is the single most important sentence in the deck and it
  is currently only in the speaker note. It should also be on the slide, because it is
  what makes the two halves one investigation.
- CHANGE: the banner is replaced with the bridge, in two lines: these failures were
  relatively easy to notice, because something was visibly missing. The next problem
  was harder, because nothing looked broken. The caveat about a second dataset moves
  into the notes and is spoken.
- IN: from the stratification. OUT: directly into the grounding half.
- TIME: 1:00. ANIMATION: state A, click, number falls, two seconds of silence, bridge.

---

**SLIDE 20 — Would you accept this one?**
**KEEP**

- ROLE: get the room to agree with the judge before anything is revealed.
- PROBLEM: none. Interaction one of three, in the right place.
- CHANGE: none.
- IN: from the bridge. OUT: silence, then click.
- TIME: 1:00. ANIMATION: response, score, question. Then stop.

---

**SLIDE 21 — So take the object out of the image and ask again**
**MODIFY**

- ROLE: the intellectual turning point, and the visual that makes it concrete.
- PROBLEM: the closing line asserts internal causality that masking cannot establish,
  and the slide is currently ambiguous about whether it is auditing the model or the
  judge.
- CHANGE: two things. First, make explicit that this slide is about **the model's
  response**, so the demo can later do the same thing to **the judge's score**. Second,
  replace the closing line with: the response did not change after the evidence it
  cited was removed, which makes the stated visual reason difficult to verify as load
  bearing.
- IN: from the room accepting the answer. OUT: "before I go further, what does that
  actually prove?"
- TIME: 1:10. ANIMATION: original, click for masked, click for control.

---

**SLIDE 22 — What that tells us, and what it does not**
**MODIFY**

- ROLE: keep slide 21 honest. This is the slide that makes the talk credible.
- PROBLEM: the left card still says the object "was not what produced the refusal",
  which is the claim the slide exists to avoid. And the reason masking is not proof is
  missing.
- CHANGE: left card becomes what we can observe: the response and the score did not
  move when the cited evidence was removed. Right card gains the mechanism caveat: a
  model may be using redundant cues, surrounding context or correlated features, so
  masking is evidence about whether the stated reason is load bearing, not proof about
  what happened inside the model. The caution line keeps the hallucination wording
  point, which is good as it stands.
- IN: from the reveal. OUT: "so was the judge simply wrong?"
- TIME: 0:55. ANIMATION: two cards, then the caution.

---

**SLIDE 24 — Was the judge actually wrong?**
**MODIFY, add reveal**

- ROLE: the honest turn back on yourself, and the best slide in the deck.
- PROBLEM: the rubric and what you thought you measured appear together, so the
  realisation has no beat.
- CHANGE: no content change except one added line. Add the reveal: rubric first, pause,
  then what you thought you were measuring, then the admission line. Construct validity
  stays in the foot note, after the plain English version, and the notes say plainly
  that the room does not need to remember the term.
- IN: from the caution. OUT: "which means I had been collapsing several questions into
  one."
- TIME: 1:00. ANIMATION: rubric, pause, intent, admission, term.

---

**SLIDE 25 — Three different questions**
**MODIFY, add reveal**

- ROLE: the framework the room writes down.
- PROBLEM: three cards at once, and the bleach callback is only in the notes.
- CHANGE: reveal one at a time, and put the bleach example into the cards themselves so
  the loop visibly closes: do not drink it is the outcome, the image has to actually
  show bleach is the evidence, did the judge check either is the evaluation.
- IN: from the rubric. OUT: "and this is not only a vision problem."
- TIME: 0:50. ANIMATION: three cards on three clicks.

---

**SLIDE 23 — This is not only a vision problem (MOVED to sit here, after 25)**
**KEEP, moved**

- ROLE: hand the pattern to people who do not work on vision.
- PROBLEM: only its position. It currently sits between the masking caution and the
  rubric, which interrupts the chain from the reveal to the honest turn.
- CHANGE: move to after the three questions, which is where your outline puts it and
  where it reads as a generalisation rather than a detour.
- IN: from the three questions. OUT: "and there is a more basic question underneath all
  of this."
- TIME: 0:45. ANIMATION: four cards, then the shared line.

---

**SLIDE 26 — What can the judge actually see?**
**MODIFY, absorbs slide 27**

- ROLE: the input contract, and the most actionable slide for a practitioner.
- PROBLEM: slide 27 immediately afterwards says a second version of the same thing with
  a second table. Two tables in a row about configurations is where the room's
  attention goes.
- CHANGE: one table with four rows and a fourth column carrying what was observed, so
  capability and observation sit on one line each. The counterfactual row stays as the
  fourth row, because it is the row that sets up the demo. The caution keeps both
  halves together: a judge can only verify evidence it can see, and giving it the
  evidence does not guarantee it uses the evidence correctly.
- IN: from the four domains. OUT: "so now we have several ways this can fail. Let me
  test them on one case."
- TIME: 1:05. ANIMATION: rows one at a time, then the caution.

---

**SLIDE 27 — Adding the evidence changed the judge's behaviour**
**MERGE into 26. Slide removed.**

- Its four observations become the fourth column of slide 26. Its practical closing
  sentence, look at what the judge was actually sent before you change the judge, moves
  to slide 26's notes and is spoken.
- Saves 0:50.

---

**SLIDE 28 — Break my judge**
**MODIFY. This is the biggest change.**

- ROLE: not a demonstration of a tool. One case, several hypotheses, one variable at a
  time, ending on the result that matters.
- PROBLEM: four of them. The button order puts remove image before blank. The final
  state repeats slide 21 rather than escalating it. The labels include validity but not
  evidence sensitivity. And there is no moment where the room predicts before you click.
- CHANGE:
  - Button order becomes **run, run again, blank response, remove the image, cover the
    object**.
  - State 5 is reframed as the escalation: slide 21 covered the object and the model's
    answer did not move. Now the same move is made against the judge, and the score
    does not move either. Readout shows the before and after score side by side with
    **evidence changed / evaluation did not**.
  - Before state 5, you ask the room: if this evidence matters to the evaluation, what
    should happen when I remove it? That is interaction two of three.
  - Labels become stability, availability, input contract, evidence sensitivity. The
    recap asks are these actually the same failure, which is interaction three, and
    then answers no, four different failures, so one accuracy number cannot diagnose
    all four.
  - The banner says plainly that these are fixed demo states, chosen so the behaviour
    is reproducible on stage, and not live calls.
- IN: "rather than three demos, one case, one variable at a time." OUT: "different
  failures need different tests."
- TIME: 2:00. ANIMATION: state changes only, reset returns to state 1.

---

**SLIDE 29 — What I would test before trusting a judge**
**MODIFY**

- ROLE: turn the talk into something they can do on Monday.
- PROBLEM: the five rows are Repeat, Remove, Swap, Compare, Fail, which competes with
  the five words on slide 31. And the code asserts that a judge must score two images
  differently, which is too strong to put on a slide.
- CHANGE:
  - Rows become **Repeat, Perturb, Count, Compare, Separate**, the same five words as
    slide 31 and the same five you say in the conclusion. Remove and swap become
    examples inside the Perturb row. Blank, malformed and timeout become examples
    inside Count.
  - Perturb gains the part that makes it a test rather than a poke: write down the
    expected behaviour before running it. The row carries one test and one expectation.
  - The code becomes conceptual, with no universal assertion:
    `before = judge(original)` / `after = judge(counterfactual)` /
    `inspect_delta(before, after, expectation)`.
  - The foot note says the expectation depends on the task, and the point is that it is
    written down first.
- IN: from the demo recap. OUT: "and one of those five is the one I got wrong."
- TIME: 1:15. ANIMATION: rows one at a time, code last.

---

**SLIDE 30 — Quality and correctness are different questions**
**MERGE into 31. Slide removed.**

- ROLE it was playing: the decomposition argument.
- PROBLEM: it repeats slide 25's structure and slide 31's Separate row, in the last
  four minutes, when the room is already holding two frameworks.
- CHANGE: the five properties chip row moves into slide 31's Separate row as a single
  line, and the line about not solving it by running five judges moves into the demo
  wrap up, which is where somebody will actually ask the question.
- Saves 0:45.

---

**SLIDE 31 — What I check now, before I trust a judge number**
**MODIFY, add reveal**

- ROLE: the slide people photograph.
- PROBLEM: five rows arriving together, and Separate is currently one line where it now
  has to carry slide 30's content.
- CHANGE: reveal one word at a time. Separate's row gains the list of properties that
  one score is usually asked to carry. Everything else stays.
- IN: from the test suite. OUT: the closing statement.
- TIME: 1:15. ANIMATION: five rows, one per click.

---

**SLIDE 32 — An LLM judge is useful, and it is also a model that needs evaluating**
**KEEP**

- ROLE: the thesis, alone on the slide.
- PROBLEM: none.
- CHANGE: the notes carry your ending verbatim, so the last thirty seconds are not
  improvised. Nothing is added after it.
- IN: from the checklist. OUT: thank you.
- TIME: 0:35. ANIMATION: none.

---

**SLIDE 33 — Resources**
**KEEP**

- ROLE: something useful on screen during questions.
- CHANGE: none. TIME: 0:00.

---

## A. Unchanged

1, 2, 9, 10, 14, 15, 16, 20, 32, 33.
Ten slides. Roughly a third of the deck is already doing its job.

## B. Wording only

3, 4, 17, 18.
Four slides, small edits, no layout or reveal changes.

## C. Structural

5 (cut the giveaway), 6 (reveal), 7 (retitle and reframe as the test), 8 (drop one
counter), 11 (three stage reveal), 12 (swap observability for evidence sensitivity),
19 (bridge onto the slide), 21 (weaken the claim, make it about the model), 22 (add
the redundant cues caveat), 24 (reveal), 25 (reveal plus bleach callback), 26 (absorb
27), 28 (demo rebuild), 29 (five words plus safer code), 31 (reveal plus absorb 30).
Fifteen slides.

## D. Merged, removed, or moved

- **Merged away:** 27 into 26, 30 into 31.
- **Moved:** 13 to after 9, and 23 to after 25.
- Nothing is deleted outright. 33 slides become 31.

## E. Demo changes

| Was | Becomes |
|---|---|
| run, run again, remove image, blank, different photo | run, run again, blank, remove image, cover the object |
| state 5 repeats slide 21 | state 5 audits the judge, where slide 21 audited the model |
| labels: stability, input contract, availability, validity | stability, availability, input contract, evidence sensitivity |
| no prediction moment | the room is asked what should happen before state 5 |
| banner describes the data | banner says plainly these are fixed states, not live calls |
| 2:20 | 2:00 |

## F. Timing

| Act | Slides (new numbering) | Time |
|---|---|---|
| Who and what the problem is | 1 to 7 | 4:50 |
| Scale, the judge, the pipeline, the five properties | 8 to 13 | 5:20 |
| The visible failures | 14 to 18 | 4:45 |
| The bridge | 19 | 1:00 |
| The invisible failure | 20 to 24 | 4:50 |
| Input contract | 25 | 1:05 |
| The demo | 26 | 2:00 |
| Test suite, checklist, close | 27 to 31 | 4:00 |
| | **Total** | **27:50** |

Buffer in a 30 minute slot: 2:10, which is what you asked for.

Elastic if you are behind: the hands up slide drops to 20 seconds, and the demo stops
after the fourth button. That is another two minutes.

---

## New numbering, after the moves and merges

1 title, 2 bio, 3 grain of salt, 4 bleach, 5 knife, 6 what are we evaluating,
7 how would I check that, 8 scale, 9 what is a judge, 10 hands up, 11 what the judge
receives, 12 where the number comes from, 13 the five properties, 14 first results
looked fine, 15 no score, 16 debugging, 17 retry, 18 not spread evenly, 19 hard cases
come back plus the bridge, 20 would you accept this, 21 take the object out, 22 what it
does and does not tell us, 23 was the judge wrong, 24 three questions, 25 not only
vision, 26 what can the judge see, 27 break my judge, 28 what I would test, 29 my
checklist, 30 thesis, 31 resources.

---

## The six questions your audience should be able to answer

1. **Why did she need a judge?** Slide 8. One image is checkable by hand, three
   thousand responses are not.
2. **Why is a clean score not automatically trustworthy?** Slide 12. The number is the
   output of eight stages, and it looks like a property of the model.
3. **Why does dropping failed calls bias an evaluation?** Slides 18 and 19. The blanks
   were concentrated on the ambiguous images, so dropna changed which examples were
   being measured, and the metric moved when they came back.
4. **Why can a good response be unsupported by the evidence?** Slides 20 to 22. The
   refusal is clear, specific and well justified, and the sentence about the image is
   the only part nothing checked.
5. **Why does changing the evidence audit the evaluator?** Slide 7 plants it, slide 21
   does it to the model, the demo does it to the judge. If the stated reason is load
   bearing, removing it should move something.
6. **What five things do I test?** Slides 28 and 29. Repeat, perturb, count, compare,
   separate, in those words, three times.

Question five is the one the deck currently answers weakest, because slide 21 and the
demo overlap instead of building. That is what change one fixes.

---

## What I need from you

Approve, or tell me which of the six decisions at the top you want differently. The one
I would most like a yes or no on is number five, the in slide reveals, because it is
the only mechanical change and it touches six slides. Without it, the pipeline cannot
show 6.9 as clean before showing the failure points, and the rubric cannot land before
what you thought you were measuring.

After approval I will rebuild, verify slide count, overflow at three widths, every
reveal, the demo states and reset, offline behaviour and readability, and then write
the full speaker notes against the final numbering in the TIME, GOAL, SAY, CLICK,
REMEMBER format.
