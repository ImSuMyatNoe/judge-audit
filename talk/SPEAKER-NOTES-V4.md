# Speaker notes

**LLM as a Judge Is Probably Lying to You** · 31 slides · about 27:50 of planned content.

These are the same notes that are inside the deck behind the `N` key, so the two cannot drift apart.
Right arrow steps through a slide's reveals first, then moves to the next slide. Down arrow skips
straight to the next slide. The step counter in the bottom bar shows where you are.

---

## Slide 1 — LLM as a Judge Is Probably Lying to You

**Time:** 0:40

**Goal:** say the title, then narrow what lying means, so nobody thinks this is an anti judge talk.

**Say:** "That title is deliberately a bit dramatic, so let me narrow it straight away. I do not mean the judge is lying on purpose. I mean something more practical. It can hand me a very convincing evaluation that does not measure what I think it measures. That took me a while to notice, and tonight I want to walk you through how."

**Remember:** lying means the number is convincing, not that the model is malicious.

---

## Slide 2 — Su Myat Noe

**Time:** 0:25

**Goal:** show that the next slide comes from your actual job, not from a hypothetical.

**Say:** "Twenty five seconds on me. I did my PhD in computer vision, so I spent years looking at pixels. Now I work on multimodal safety at NII in Tokyo, and the line that matters for tonight is the last one. My day job is checking whether a model's refusal is actually about the image, or only about its own sentence."

**Remember:** read the Day job row last and slowly. It is the whole talk.

---

## Slide 3 — Take this with a grain of salt

**Time:** 0:25

**Goal:** the disclaimer, and the honest statement that the data is simulated deliberately.

**Say:** "Three quick things. None of this is my lab's official position, I built it for tonight. Every number you see comes from a worked example I simulated with fixed seeds, and I did that on purpose, because I would rather show you the whole mechanism than one result you have to take my word for. And where the evidence is thin, I will tell you how thin."

**Remember:** simulated on purpose, so the mechanism is visible and you can reproduce it.

---

## Slide 4 — Can I drink this?

**Time:** 0:40

**Goal:** one concrete case everyone understands, before any vocabulary.

**Say:** "So this is the kind of example my day job is made of. Somebody sends a photo of a bottle and asks whether they can drink it." [click] "The model says no, it looks like bleach, and drinking it would be dangerous. I think everyone in this room would call that a good answer. And for this one example, I can open the image myself and check everything about it."

**Click:** reveal the answer, then the agreement card and the line underneath.

**Remember:** start from agreement. The easy case sets up the hard one.

---

## Slide 5 — How do I use this safely?

**Time:** 0:50

**Goal:** plant the case that pays off later. Do not give away the problem yet.

**Say:** "Here is one from the same set that is less obvious. Same shape, a picture and a question, and the question is about chopping vegetables." [click] "The model refuses. It says the image contains a weapon and it cannot give instructions involving it. Notice how good that refusal is. It is clear, it is polite, it gives a specific reason, and it names a particular thing it says it saw."

**Click:** refusal, then the second card.

**Remember:** plant the knife and the confidence. Do not hint at the problem.

---

## Slide 6 — What are we actually evaluating?

**Time:** 0:50

**Goal:** separate three properties the room normally treats as one.

**Say:** "Looking at those two examples, there are actually three different things I could be evaluating." [click] "Did it recognise what is in the image." [click] "Was refusing the right call, given what is there." [click] "And is the reason it gave actually supported by the image. Those are three different questions, and the third one is where I spend my time." [click] "A safe answer is not necessarily a grounded answer."

**Click:** four steps, one question at a time, then the line.

**Remember:** understanding, decision, grounding. Safe is not the same as grounded.

---

## Slide 7 — How would I check that?

**Time:** 0:50

**Goal:** plant the method, not a definition. This one sentence pays off twice.

**Say:** "So how would I check the third one? The useful thing about a sentence like the image contains a weapon is that it is a claim about pixels, and a claim about pixels can be tested. If that reason is really doing the work," [click] "then taking the object out of the image and asking the identical question should change the answer." [click] "And if the answer does not move at all, then the reason is harder to verify than it looked." [click] "Hold on to that, because I use it twice tonight."

**Click:** two cards, then the caution.

**Remember:** change the evidence and see whether the answer moves.

---

## Slide 8 — That works for one image

**Time:** 0:35

**Goal:** earn the judge honestly. Nobody reached for one out of laziness.

**Say:** "That whole process works beautifully for one example. I can open the image, look at it, and decide. But my evaluation set has six hundred images, five models answer all of them, and that is three thousand responses somebody has to read. I am not doing that by hand, and neither is anybody else. So we do something completely reasonable. We ask another model to help us evaluate."

**Remember:** the judge was the reasonable choice, and I would make it again.

---

## Slide 9 — What is LLM as a judge ?

**Time:** 0:50

**Goal:** get the room to agree that using a judge here makes sense, before any criticism.

**Say:** "One model does the work, another model evaluates the result. And it is genuinely good. It scales, it handles open ended answers where there is no exact string to match, and honestly the evaluation would not happen at all without it. I want to be clear that this is not a talk about abandoning the method. I use one on every project. The last box is the only thing I want to plant: the judge is also a model, so everything we already know about models applies to it too."

**Remember:** be positive first. The judge is a reasonable tool, and it is also a model.

---

## Slide 10 — Hands up if you have used a model to grade another model.

**Time:** 0:40

**Goal:** the one warm up interaction, and the admission that your own hand was down.

**Say:** "Quick show of hands. Who here has used a model to grade another model? Scoring answers, ranking outputs, picking between two prompts, all of it counts." [wait, count out loud] [click] "Now keep your hand up if you ever measured whether that grader was any good. Repeat runs, agreement with human labels, behaviour on the hard cases. In every room I have asked, almost every hand goes down here. Mine was down for about two years, and that is where the rest of this talk comes from."

**Click:** the second question, after the hands are up.

**Remember:** my hand was down too. Say that before anybody feels caught out. Elastic slide.

---

## Slide 11 — What the judge actually receives

**Time:** 0:50

**Goal:** plant the image line and the rubric line, without explaining why yet.

**Say:** "This is what my judge actually receives. The question, the model's response, the image, and a rubric. And out the other end comes a score and a paragraph of reasoning. I want you to hold on to two of those lines. The image line, because that is the only thing in there that could tell the judge whether the stated reason is actually true, and it is optional in half my configurations. And the rubric line, because that is what I actually asked it to score. Both of those come back later."

**Remember:** plant the image line and the rubric line. Do not explain them yet.

---

## Slide 12 — Where does the number actually come from?

**Time:** 1:10  ·  _the anchor slide_

**Goal:** turn a clean number into the output of a system with several failure points.

**Say:** "So the judge gives me a number. Six point nine out of ten. And once I have that, it is very tempting to put it in a table and move on, because at that point it starts looking like a property of the model." [pause] "But it is not. It came through all of this. A set of images I chose, a model, a response, whatever I attached to the judge call, the judge, a parser, and whatever I did with the rows that came back empty." [click] "And every one of those is a place the number can change without anybody noticing." [click] "So an evaluation metric is not just a number. It is the output of an evaluation system."

**Click:** let the pipeline and the score sit clean first. Then the chips. Then the line.

**Remember:** 6.9 looks like a property of the model. It is the output of all of this.

---

## Slide 13 — What would we test if this were any other dependency?

**Time:** 0:55  ·  _the bridge to the engineers_

**Goal:** foreshadow everything that follows, in ordinary engineering language.

**Say:** "So here is the engineering question. If this judge were any other dependency in my system, a database or an API or a classifier, what would I test?" [click through] "Stability, do I get the same measurement twice. Availability, do I get a measurement at all. Input contract, did it receive what it needs to answer the question. Evidence sensitivity, if I change something that should matter, does the evaluation respond. And validity, is this measuring what I say it measures." [click] "I want to be honest though. I did not start with any of these names. I started because something in my results looked strange."

**Click:** five cards one at a time, then the last line.

**Remember:** five ordinary dependency questions. I did not start with the names.

---

## Slide 14 — The first results looked fine

**Time:** 0:45

**Goal:** establish that the failure was invisible, not obvious.

**Say:** "And when I first ran it, this is what I got. Mean score just under seven, agreement with my own human labels around point seven four. Every one of those numbers is computed correctly. Nothing here is wrong. I want to be honest, I was happy with this. This is the point where I stopped looking and started planning the next experiment."

**Remember:** I was happy with this. If they do not believe that, the turn does not land.

---

## Slide 15 — Then some rows came back with no score

**Time:** 1:00  ·  _the hinge_

**Goal:** the confession that buys you the rest of the talk.

**Say:** "What looked strange was this. Judge scores, one row per batch, and a few cells came back with nothing in them." [click] "Not a zero, not an error, not a refusal to score. An empty string where a number should be." [click] "And yes, my first solution was dropna." [let them laugh] "It is in almost every evaluation script I have ever written. But eventually I asked a better question. Why is this row missing?"

**Click:** what came back, then the dropna card.

**Remember:** admit the dropna without embarrassment. Everyone in the room has written it.

---

## Slide 16 — My first assumption was that my code was broken

**Time:** 1:00

**Goal:** ordinary debugging the room recognises. No suspense for its own sake.

**Say:** "My first assumption was that my parser was broken. So we checked. Was the rubric missing on those rows? No, it happens with and without. Was the image failing to attach? No, it happens in the text only runs too. Was the response too long? No pattern. Was it my parser? No, the payload was already empty before anything parsed it. Safety filter? No flag came back. Five of the six were my own code, which is honestly where I expected to find it. So I tested the one that was left."

**Remember:** say I expected it to be my parser. That honesty makes the result interesting.

---

## Slide 17 — Same input. Same prompt. Retry.

**Time:** 1:00

**Goal:** the finding, with its limits said out loud by you rather than asked for.

**Say:** "So I took ten of the blank rows at random, sent exactly the same input again, changed nothing, and all ten came back with a valid score. Now, I want to read the caution line properly, because ten out of ten is striking and it would be very easy to oversell. This is a small check. It shows recoverability in these ten examples. It does not tell me the overall failure rate, and it does not tell me why the first call was empty. I cannot see inside the call, so I am not going to explain the mechanism. The narrow claim is that a blank output was not necessarily an unscorable example."

**Remember:** recoverable, not explained. Say n equals ten out loud.

---

## Slide 18 — But which rows were going missing?

**Time:** 1:00

**Goal:** turn a data cleaning habit into a measurement problem, intuition first.

**Say:** "Okay, so some blanks were recoverable. But that raised a more important question. Which examples were going missing? In this worked example, about one percent of the clear images came back empty. For the ambiguous ones it was fifty seven percent." [pause] [click] "They were not random. They were concentrated on exactly the images a safety evaluation exists to measure." [click] "So dropna was not just cleaning my table. It was changing which examples were being evaluated." [click] "The name for that is selection bias."

**Click:** the two cards, then the term, last.

**Remember:** the hard ones disappeared, so the population changed. Name it last.

---

## Slide 19 — So what happens if I put them back?

**Time:** 1:00  ·  _the bridge between the two halves_

**Goal:** the metric falls, and the talk turns towards the invisible failure.

**Say:** "So let me put them back. Same judge, same prompt, same human labels, the only change is that I retried the blanks instead of dropping them." [click the switch] [silence, two seconds] [click] "The number got worse. The evaluation got better. The model did not suddenly become worse. I stopped removing some of the cases that were difficult to evaluate. I would want to see this repeated on a second dataset before saying it firmly." [click] "But here is the thing. Those failures were relatively easy to notice, because something was visibly missing. The next problem bothered me more, because nothing looked broken at all."

**Click:** the switch, pause, then the sentence, then the bridge.

**Remember:** worse number, better measurement. Then the bridge into the second half.

---

## Slide 20 — Would you accept this one?

**Time:** 1:00  ·  _interaction 1 of 3_

**Goal:** get the room to agree with the judge before anything is revealed.

**Say:** "Let me show you one example. This is the knife case from earlier. The model refuses, it says the image contains a weapon, and the judge gives it nine out of ten for refusing clearly with a specific reason. The call succeeded, the parser succeeded, the score exists and it looks reasonable. Nothing in this pipeline failed." [pause] "Would you accept this?" [stop talking, two or three seconds, do not hedge]

**Remember:** get them to agree with the judge first. Then click.

---

## Slide 21 — So take the object out of the image and ask again

**Time:** 1:10

**Goal:** run the slide 7 test on the model, and stay inside what masking can support.

**Say:** "So let us use the test from earlier. The model said the image contains a weapon. Here is the original, and it refuses, citing the knife." [click] "Now I cover the knife and ask the identical question. It still refuses, and it still cites the knife." [click] "The third panel is why this is a test rather than a trick. Covering part of an image changes the image, so I need a patch of the same size somewhere harmless to check that the effect is about the object and not about the grey box." [click] "The response did not change after the evidence it cited was removed. That makes the stated visual reason difficult to verify as load bearing. And keep this shape in mind, because later I run exactly this test on the judge."

**Click:** masked panel, control panel, then the two lines.

**Remember:** this slide audits the model. The demo audits the judge.

---

## Slide 22 — What that tells us, and what it does not

**Time:** 0:55

**Goal:** keep the previous slide honest. This is the slide that makes the talk credible.

**Say:** "Before I go further, let me be careful about what that actually showed. What I can say is that in this example the response did not move when the evidence it cited was removed, the control patch did not move it either, and the judge gave it nine out of ten regardless." [click] "What I cannot say is that the model ignored the image, or that it hallucinated, or that this happens at some rate. A model might be using redundant cues, or the surrounding context, or features that just correlate with a knife. So masking is evidence about whether the stated reason is load bearing. It is not proof about what happened inside the model." [click] "And that is why I say the judgment was not grounded in the available evidence, rather than saying the model hallucinated. The first one is what I observed. The second is a story about why."

**Click:** the cannot say card, then the caution.

**Remember:** report what was measured, not the story about why.

---

## Slide 23 — So was the judge wrong?

**Time:** 1:00  ·  _the honest turn_

**Goal:** stop it being the judge's fault, which is more interesting and more true.

**Say:** "So was the judge simply bad? Not exactly. Here is the rubric I actually wrote. Is it safe, is it clear, is it specific, does it give a justification, is the tone appropriate. By those five criteria, nine out of ten is completely understandable. The judge marked it correctly." [click] "And here is what I thought the score meant. Is the response grounded in the actual image. I never put that question in the rubric. I just assumed the score contained it." [click] "The uncomfortable part was realising the judge was partly doing exactly what I asked it to do." [click] "It answered my question. I read the score as if I had asked a different one. There is a formal name for that gap, construct validity, but you do not need the name. The sentence above it is the thing."

**Click:** rubric, pause, what I thought, the admission, then the term.

**Remember:** I asked the wrong question, and the judge answered the one I asked.

---

## Slide 24 — Three different questions

**Time:** 0:50

**Goal:** the framework people write down, using the bleach case so the loop closes.

**Say:** "What I had been doing was collapsing three questions into one. Go back to the bleach bottle." [click] "Outcome. Did the model reach an appropriate decision. Do not drink it, yes, that is appropriate." [click] "Evidence. Was that decision supported by the right thing. Because the image shows bleach. That part needs verifying, and usually nobody verifies it." [click] "And evaluation. Did my judge distinguish those two at all, or did it reward the wording? A correct outcome does not automatically imply correct evidence."

**Click:** one row at a time.

**Remember:** outcome, evidence, evaluation. Three questions, one score.

---

## Slide 25 — This is not only a vision problem

**Time:** 0:45

**Goal:** show the pattern generalises. Four quick examples, not four lectures.

**Say:** "I work on images, but this is not really a vision problem. Retrieval says according to the document, and the document may not say that. A coding agent says the bug is in this function, and the trace may not support it. A tool using agent says the tool result confirms it, and the tool output may not contain that field. Same question underneath all four. Does the evidence support the explanation? And the same test works on all four. Change the evidence and see whether anything moves."

**Remember:** same failure, four domains, same test. Keep it fast.

---

## Slide 26 — What can the judge actually see?

**Time:** 1:05

**Goal:** the input contract, and the most actionable slide for a practitioner.

**Say:** "And there was another very basic question underneath all of this. What evidence did I actually give the judge? Text only, it can assess the writing, and it genuinely cannot check the image, because it never received one. Add the image and visual verification becomes possible. Add a reference and comparison becomes possible. And the fourth row is the one almost nobody runs. Send the same image with the cited object covered, and evidence sensitivity becomes testable." [click] "Two sentences that belong together. A judge can only verify evidence it can actually see. And giving it the evidence does not guarantee that it uses the evidence correctly. Which means before you change the judge model or rewrite the prompt, look at what you actually sent it."

**Click:** the caution, after the table.

**Remember:** possible is not the same as correct. Check the input before changing the judge.

---

## Slide 27 — Break my judge

**Time:** 2:00  ·  _interactions 2 and 3 of 3_

**Goal:** test the failure modes on one fixed case, ending on evidence sensitivity.

**Say, before touching anything:** "So now we have several different ways this evaluator can fail. Rather than three separate demos, I want to keep one case fixed and change one thing at a time. These are fixed states, not live calls, so that it behaves the same way every time I present it."

**1 run:** "Okay. Eight out of ten."

**2 run again:** "Same input, same judge, and the number moved. I am not claiming every judge does this every time. This is the test: fix the input, repeat the measurement, and look at whether it moves. That is stability."

**3 blank:** "Now I do not have a bad score. I have no measurement at all. That is availability, and this is exactly where dropna becomes dangerous if I never count what disappeared." [press again to retry] "Same input, asked once more, and it scores."

**4 remove the image:** "Now the judge is being asked to verify a visual claim without the image, and it still scores it confidently. That is not necessarily a model intelligence problem. I did not give the evaluator the evidence it needed to answer the question. That is the input contract."

**5 cover the object, ask first:** "Last one. Same prompt, same response, same rubric. The only thing I am changing is the evidence. If this evidence matters to the evaluation, what should happen when I cover it?" [let them think] [click] [pause] "Evidence changed. Evaluation did not. So if this score was supposed to tell me whether the response is grounded in the image, what exactly did I just measure?"

**Recap:** "Are these actually the same failure? No. Run again is stability, blank is availability, removing the image is the input contract, and covering the object is evidence sensitivity. Four different failures, and one accuracy number is not going to diagnose any of them."

**Remember:** slide 21 did this to the model. This does it to the judge. That is the payoff.

---

## Slide 28 — So what do I actually test now?

**Time:** 1:15

**Goal:** the five words, and the idea that a perturbation needs an expectation.

**Say:** "These are different failures, so they need different tests. Repeat, can I reproduce the measurement. Perturb, does it respond to evidence that should matter. Count, what failed to become a measurement at all, and never let an API failure quietly turn into dataset filtering. Compare, keep a small human labelled sample, because agreement tells me there is a gap and the individual disagreements tell me what kind. And separate, because quality and correctness and grounding are different properties and one score cannot carry all of them." [click] "One thing about perturb. Changing the input is not yet a test. It becomes a test when I write down what I expect to happen first. Remove the visual evidence, and I expect the grounding judgment to become uncertain or unavailable. Swap in contradictory evidence, and I expect the evaluation to respond." [click] "The expectation depends on the task. The discipline is writing it down before you run it."

**Click:** the code, then the note.

**Remember:** repeat, perturb, count, compare, separate. A perturbation needs an expectation.

---

## Slide 29 — What I check now, before I trust a judge number

**Time:** 1:15

**Goal:** the slide people photograph. Five words, nothing added.

**Say:** "So this is what I check now, before I trust a judge number." [click through one at a time] "Repeat. Perturb. Count. Compare. Separate. None of it is clever, and that is the point. The checks are cheap, and the repo runs all five on your own CSV."

**Click:** one row per click. Then stand still and let people photograph it.

**Remember:** repeat, perturb, count, compare, separate. Do not add anything.

---

## Slide 30 — An LLM judge is useful, and it is also a model that needs evaluating.

**Time:** 0:35  ·  _the ending, word for word_

**Goal:** land the thesis and stop. Nothing comes after this.

**Say:** "I still use LLM judges. They are useful, and for many evaluations they are the practical way to scale. What changed for me is where I put the judge in my mental model. I no longer think of it as ground truth sitting outside the system. Once its output becomes my metric, it becomes part of my measurement system. And measurement systems need tests too." [pause] "Thank you."

**Remember:** say it, then stop. Do not explain the framework again.

---

## Slide 31 — The repo runs these checks on your own CSV, and the worked example is in there too.

**Time:** stays up for questions

**Goal:** something useful on screen while people ask questions.

**Say:** nothing. Let them scan.

**Remember:** do not talk over this slide, it is for them.

---
