# The script

Word for word, in the speaking style of the Beyond the Vibes sessions. You can
read this out loud and it will sound like a person talking, not a person
presenting.

Two things about this style before you start.

**The "right?" is doing real work.** It is not filler. It hands the sentence back
to the room and checks they are still with you. Use it after a claim, never after
a question.

**Thinking out loud beats announcing.** Instead of "the answer is X", say "so you
would think it's X, right? But actually it's not. So then why?" The room follows
a puzzle much further than they follow a conclusion.

Speaker notes for each slide are also inside the deck. Press `N`.

---

## 1. Title

> Okay. So, my title tonight is "LLM as a Judge Is Probably Lying to You".
>
> And I want to be clear about what I mean by that, because it sounds dramatic,
> right? I don't mean the model is evil. I don't mean anybody did anything
> careless.
>
> What I mean is, the thing we use to grade our models has never itself been
> checked. And when I finally checked mine, it did not survive.
>
> So that's what the next half hour is about.

*Do not explain the structure yet. Just start.*

---

## 2. Hello

> Very quickly, who am I. I'm Su, I'm a research scientist at NII in Tokyo.
>
> I work on multimodal safety, so models that look at pictures as well as text,
> and my job is basically to check whether a model's safety behaviour is real, or
> whether it just looks real.
>
> Which, you'll see, is kind of the whole talk.
>
> That QR is my site. It comes back at the end, so don't rush for your phone yet.

*Twenty seconds. Do not linger here.*

---

## 3. Why this one matters to you

> So before anything technical, let me tell you why you should care.
>
> If you're building with AI right now, something in your stack is already being
> graded by a model. A pull request, a support reply, a summary, a refund. Right?
>
> And nobody sat down and voted on that. It just happened, quietly, over about
> eighteen months, because it was the only thing that could keep up.
>
> And that grade is what decides which version ships, which prompt wins, and
> which agent goes live on Monday.
>
> So it's already making decisions for you. That's why it matters.

---

## 4 to 7. The four words

*Keep these fast. One minute each, maximum. If you go slow here the pizza never
arrives.*

### 4. Agent

> Okay, so four words first, because half this room builds these for a living and
> half of you have never written a prompt, and I want us all in the same place.
>
> An agent. An agent is a model that takes actions on its own. Not just answering
> your question, right, but running through several steps until something is
> actually done.
>
> So it calls tools, it looks up your order, it sends a refund, or it passes the
> case to a human. It mixes your business rules with its own reasoning and picks a
> path as it goes.
>
> And the important bit for tonight is the third one. It needs a new kind of
> testing. Because you have to check the path it took, not just the sentence it
> ended up writing.

### 5. LLM as a judge

> Second word. LLM as a judge.
>
> So this is a second model that reads the first one's work and gives it a score.
> That's it. One model does the work, another model marks the homework.
>
> You feed it the photo, the order, your policy, and the reply the agent wrote.
> Sometimes the whole trace. And what comes back is a number out of ten, plus a
> paragraph explaining the number.
>
> And look at the last one there. That explanation paragraph is written to
> convince you. And nothing, anywhere, checks whether it's true.
>
> Hold on to that one. We come back to it.

### 6. Eval

> Third word, eval. Everybody in this room uses this word and I promise you
> nobody defines it the same way.
>
> An eval is the test you run on your AI to decide whether it's good enough to
> ship. So it's a benchmark, a fixed set of cases. It's a pass rate. And it's a
> gate, the line you've decided not to ship below.
>
> And the reason it matters tonight is the last line. Every single number in this
> talk came out of an eval, and that eval trusted a judge to do the scoring.

### 7. Trace and ground truth

> Last two, quickly.
>
> A trace is the full record of what the agent did, step by step, in the order it
> did it.
>
> Ground truth is what a careful human says the right answer actually was. Slow,
> expensive, and worth it.
>
> And you want both, right? Because the trace shows you where it went wrong, but
> ground truth is how you know it went wrong at all.
>
> Which gives you the line I'd like you to remember from this slide. A judge with
> no ground truth behind it is a second opinion. It is not a measurement.

---

## 8. The plan

> Okay so here's how we're going to spend the next thirty minutes.
>
> One pizza. Four clues. Three live demos, which are running right here in this
> page, so no terminal, nothing touching the network. And then five things you can
> actually do on Monday.
>
> That's the whole thing.

*Fifteen seconds. Do not read the list.*

---

## 9. Is anyone here hungry?

> Right, so quick one before anything technical. Is anybody here hungry?
>
> Keep your hand up if you ordered food on your phone this week. Supper counts.

*Genuinely ask. Genuinely wait. Three seconds of silence is fine, it is buying
you the next twenty minutes.*

> Yeah. Okay. So we're eating out for the rest of this talk. Everything tonight
> happens at this table.

---

## 10. One pizza, six hops

> So here's the example.
>
> You order on the app. The kitchen makes it. The rider brings it over. It's the
> wrong one, so you take a photo. An agent decides what to do about it. And then a
> judge gives that decision a score.
>
> And only the last box is unusual, right? The first five happen a few million
> times a day across this region already and none of us think twice about them.
>
> The last one is where tonight's trouble lives.

*Walk it left to right with your hand. Tap the last box twice.*

---

## 11. It comes, and it is not your pizza

> So twenty minutes later it turns up, and it's not your pizza.
>
> You take a photo of the bag, you say the order's wrong, you ask for your money
> back. Nothing unusual about any of that.
>
> What is unusual is that nobody is ever going to open that photo. Nine times out
> of ten a model reads it first, and it has about four seconds to make up its mind.
>
> And that's already how most refund messages get answered here. So the open
> question was never whether to automate it. The open question is who checks the
> answers.

---

## 12. Somebody has to call it

> So somebody has to call it, right? Refund you, reject the claim, or pass it to a
> human.
>
> And all three are defensible. If you refund a claim that was never true, the
> company quietly bleeds. If you reject a real one, that customer is gone for
> good. And if you send everything to a person, well, there was no point
> automating anything in the first place.
>
> So making the call is the cheap part. Knowing whether the call was any good,
> that's the expensive part. And that's basically the whole talk.

---

## 13. Six steps, four seconds

> Okay so what does this agent actually do.
>
> It reads the photo. Checks the order. Checks the policy. Decides. Writes the
> reply. Sends the money.
>
> Six steps, about four seconds. And six chances to get it wrong, right? But only
> the last one leaves a mark that anybody notices.
>
> Hold on to this picture. It comes back near the end, and by then it looks a lot
> worse.

---

## 14. So who checks the agent?

> So who checks it?
>
> Two thousand refunds a day. Nobody is sitting there reading two thousand refund
> letters, and nobody is going to be hired to do it either. We all know that.
>
> So what happens is, we hand the job to another model. We paste in the whole
> trace, we ask it to score the decision out of ten, and that number goes straight
> onto a slide.

*This is the turn. Slow right down.*

---

## 15. The thesis

> And my claim is that that number is lying to you.
>
> Not on purpose. Nobody was careless. It hands you a confident number, in the
> right format, on time. And that number does not mean what you think it means.

*Let the slide sit for a beat before you speak.*

---

## 16. A judge is an instrument

> So here's how I want you to think about it.
>
> Somewhere in your pipeline there's a thing that measures quality, and you've
> been reading whatever it prints as if it were a fact.
>
> Which makes it an instrument, right? And we've known for about four hundred
> years what you do with an instrument before you trust it. You calibrate it.

---

## 17. Three instruments you would throw out

> And none of you would accept these.
>
> A thermometer that reads differently every time you use it on the same thing. A
> weighing scale that quietly skips the heavy items and reports the average of the
> rest. A ruler that agrees with you mostly because everything you measure is the
> same length.
>
> Those all sound ridiculous, right? But all three are real failures in real
> judges. And you're going to see each one tonight, live, in this room, with no
> terminal and no API key.

---

## 18. Hands up, one

> Okay, hands up. Who here has used a model to grade another model?
>
> Scoring answers, ranking outputs, picking a winner between two prompts. All of
> it counts.

*Wait. Count out loud if the room is big.*

> Yeah, that's about what I expected.

---

## 19. Hands up, two

> Now keep it up if you ever checked whether that grader was any good.
>
> So, ran it twice on the same input. Compared it against people. Looked at what
> it did on the hard cases.

*Wait longer than is comfortable.*

> Right. So every room I've asked, nearly every hand goes down. And I want to be
> clear, my own hand went down too, for about two years.
>
> That gap is the reason I'm standing up here.

---

## 20. When a model saw something that was not there

> So let me tell you how I found out.
>
> Like I said, I work on multimodal safety. My models look at a picture and decide
> whether to help.
>
> And one of them refused a request, and it explained itself beautifully. It named
> the dangerous object in the image, it told me where it was sitting, and it
> declined. Very polite. Very well reasoned.
>
> There was no object. I had already removed it.

*Stop talking for one full second.*

---

## 21. It was refusing its own sentence

> So the model was declining something that existed only inside the paragraph it
> had just written.
>
> And here's the part that actually got me. My evaluation scored that refusal as
> correct. Because it read like a very good refusal.
>
> So my scoring never checked whether the model was right. It checked whether the
> model sounded right.
>
> Every number I had published was measuring writing quality, and I was calling it
> safety.
>
> And you'll see in a minute, a judge that grades prose is going to love a
> confident wrong refund for exactly the same reason. It's the same bug, it just
> costs somebody else money instead of costing me a paper.

---

## 22. Here is the report you would get

> Okay, so back to the refunds.
>
> Here's the report. Average judge score, six point nine out of ten. Correlation
> with our own human reviewers, zero point seven four. Agrees with a person
> seventy five percent of the time.
>
> Green on the dashboard. And nothing in it is false. Every one of those numbers
> was computed correctly.

---

## 23. Would you ship on that?

> So, would you ship on that?
>
> Be honest with me. Hands up if yes.

*Take hands both ways.*

> Yeah. I would have too. Most of us have shipped on a lot less than that.
>
> There are four things wrong with that report, and not one of them is visible
> from the report.

---

## 24. Part 1: The Problem

> So that's the setup. Now here's what's actually wrong with it.

*Five seconds. Do not talk over a divider.*

---

## 25. Clue one: same photo, different score

> Clue one. The thermometer.
>
> So what I did was, I sent the same six hundred orders to the same judge, with
> the same prompt, three times. Temperature at zero. Nothing changed except the
> clock.
>
> And you'd expect the same answer, right? Temperature zero, that's deterministic.
> That's what everybody assumes.
>
> But it's actually not. Only twenty one percent got the same score all three
> times. Twenty seven percent changed side of the pass line. And the average gap
> between the highest and lowest pass was one point two points out of ten.
>
> So then the question is, why? Because temperature zero really does mean "always
> pick the most likely token".
>
> The thing is, it's the probabilities themselves that move. Floating point
> addition is not associative, right, so if you add the same numbers in a
> different order you get a slightly different total. And what changes the order
> is batch size. Your request gets batched with whatever else arrived in the same
> millisecond. On a mixture of experts model, which most of the frontier models
> now are, the batch also changes which expert your token gets routed to. And
> you're probably being load balanced across replicas that aren't bit identical
> anyway.
>
> So the model is deterministic in theory and stochastic in practice. And the
> practice is what you're measuring.

---

## 26. Demo one

> Okay, so let me show you. This is running in the page, nothing is calling out to
> the network, so it can't fail because of the wifi.
>
> These are eight real orders from the example in the repo. I'm going to press
> "score them" once.

*Click.*

> Right, seven point one out of ten. That's the number I'd put in my report.
>
> Now let me score the exact same orders again.

*Click. Let them look.*

> And you can see the cells move, right? Same input, same prompt.
>
> One more time.

*Click.*

> So now, look at the readout. Thirteen percent got the same score every time.
> Fifty percent changed verdict. Average gap is one point two five points.
>
> And the number at the top is still one number. That's the problem. The wobble is
> real, it's measurable, and the way we report it hides it completely.
>
> So what should we do instead? Let me flip this.

*Flip the switch.*

> Same data. Nothing changed. But now it reports the middle score with the spread
> beside it. Seven point zero, plus or minus one point three.
>
> And if that spread embarrasses you, that's information. That's not a bug.

---

## 27. Clue two: the orders the judge never scored

> Clue two. This is the weighing scale.
>
> So judges don't always answer, right? Sometimes you get an empty string.
> Sometimes it refuses. Sometimes it writes a lovely paragraph with no number in
> it. Sometimes the JSON doesn't parse.
>
> Twenty two percent of my orders came back like that. And somewhere in your
> pipeline there's a dropna, and those rows quietly leave.
>
> Now here's the part that matters. Look at the left chart. One percent of the
> clear photos went blank. Fifty seven percent of the blurry ones did.
>
> So they're not missing at random. They're missing hardest.

---

## 28. It goes quiet on exactly the orders you needed it for

> And that's the bit that stings, right?
>
> The number you publish comes from the easy ones, because the hard ones never
> made it into the calculation at all.
>
> This is survivorship bias with a dropna in the middle of it. And I'd bet money
> that everybody in this room has written that line. I certainly have.

---

## 29. Demo two

> So, same idea, live.
>
> Eight orders. Three of them came back blank. Right now we're doing what
> everybody does, we drop them, and we report zero point seven four agreement on
> the five that are left.
>
> Now watch what happens when I retry the blanks and keep them.

*Flip the switch.*

> Zero point six two.
>
> So the number went down. And I want to say this out loud, because it's the only
> slide tonight where doing the right thing makes your headline metric worse.
>
> It's still the right thing to do. Because zero point six two includes the cases
> you actually needed the judge for. Zero point seven four never did.

---

## 30. Clue three: agreement that counts lucky guesses

> Clue three. The ruler.
>
> Seventy five percent agreement with humans. Sounds like a working instrument,
> right?
>
> Except most refund calls are easy, and on easy cases everybody says the same
> thing. So a judge that just approves every single order, reading literally
> nothing, scores fifty seven percent on this data. Because fifty seven percent of
> orders genuinely should be approved.
>
> So your judge beat "approve everything" by eighteen points. Not by seventy five.
>
> And if you correct for the agreement you'd get by luck, what's left is zero point
> five zero. The statistic is called Cohen's kappa, and zero point five is
> moderate.
>
> Moderate is not a shipping gate.
>
> So whenever you report an agreement number, print the always approve baseline
> right next to it. Otherwise the raw percentage flatters you, every single time.

---

## 31. Clue four: confident, beautifully written, and wrong

> Okay, clue four. This is the expensive one, and this one is not a measurement
> error at all. This one is the wrong question.
>
> So picture a refund letter that's warm, it's clear, it apologises properly, it
> cites the right policy. And it hands over twenty two dollars for a photo of the
> correct pizza.
>
> The graded judge gives that a nine. And it's right to, on its own terms, because
> it was asked "was this handled well?".
>
> Eighty nine percent of the confident wrong refunds got approved.
>
> Now add a second judge that answers one yes or no question. Not a score. Just:
> was this the right call? That drops to ten percent.
>
> So a score out of ten answers one question. Nobody ever asked it whether the
> answer was correct.

---

## 32. Demo three

> Last one. Six refunds, and all six of them read beautifully. All of them scored
> eight or nine. All of them went through.

*Flip the switch.*

> Now with the second judge. Five of the six get stopped before the money moves.
>
> And look at the bottom row, because this is the objection you're going to give
> me. False refusals, thirty six percent, unchanged. So we're not annoying any
> extra customers. We're just not paying out on the wrong ones.
>
> And that second judge is cheaper than the first one, by the way, because it
> emits one token instead of a paragraph.

---

## 33. Six steps, and the wobble multiplies

> Okay, so now put this back into the agent.
>
> One step held its verdict seventy three times in a hundred. And when I first saw
> that I thought, yeah, that's survivable.
>
> But nobody grades one step, right? We grade agents. And this agent has six.
>
> Zero point seven three to the power of six is fifteen percent. So across all six
> steps of one pizza refund, fifteen orders in a hundred come out the same way
> twice.
>
> Agents are made of steps. That's the whole point of them.

---

## 34. One version in four, named wrong

> And here's the number I actually want you to take to your manager.
>
> Two versions of the refund agent. One of them genuinely is better. You score a
> hundred orders on each and you ship the winner.
>
> At a hundred orders, you name the wrong version one time in four.
>
> You need about four hundred to get that to nine times out of ten.
>
> And the reason I like this number is that nobody can act on a correlation.
> Right? Zero point seven four funds nothing. But "at our eval size we name the
> wrong version one time in four", that gets you budget.

---

## 35. Part 2: The Fix

> Okay. So that's the bad news. Here's the part you can actually do something
> about.

---

## 36. Five things, one afternoon

> Five things. You can do all of them before lunch on Monday.
>
> One, score everything three times, and publish the spread next to the average.
>
> Two, count what came back blank, and break it down by how hard the case was.
> Never quietly drop a row.
>
> Three, take out the luck before you celebrate. Print the always approve baseline
> beside every agreement number.
>
> Four, add a second judge that answers yes or no. Was this the right call, not
> was this nicely written. And require both to pass.
>
> Five, say what your eval size buys you. Turn the metric into a sentence about
> how often you ship the wrong thing.
>
> And all five of those are in the repo, they run on your own CSV, and you don't
> need an API key for any of it.

*Give them time to photograph this one.*

---

## 37. Close

> So, last thing.
>
> Your judge is an instrument. Calibrate it before you trust it.
>
> That QR on the left is the code. Four audits, the pizza example, and these
> slides. The one on the right is me, if you want to argue with any of this
> afterwards, which honestly I'd enjoy.
>
> Thank you.

*Then stop talking and let them scan. Silence while forty people hold up phones
is a good silence. Do not fill it.*

---

## Taking questions during the talk

He answers questions in the middle, by name, and it makes the room feel like a
conversation rather than a broadcast. If somebody asks something at slide 12, take
it at slide 12.

Three moves that make this work:

**Say the name.** "So Vincent asks about..." It costs nothing and it changes the
temperature of the room completely.

**Answer the half you can.** If you don't know, say so and say what you'd do to
find out. "I haven't audited that one. The six audits are in the repo and they
take about twenty minutes to run against it, come find me after."

**Park it if it's off the path.** "That's actually a whole other talk, and I'll
give you a proper answer at the end, but the short version is..."

---

## The questions you will get, in his register

**"Doesn't temperature zero fix it?"**

> So this is the most common one, and it's a really good question, because the
> assumption is completely reasonable. Temperature zero fixes the sampling. It
> doesn't fix the arithmetic. The logits themselves move because of batching and
> floating point ordering and expert routing. So temperature zero is not
> determinism. It just feels like it should be.

**"Wouldn't a bigger judge model solve this?"**

> Partly. It helps with clue three, and a bit with clue one. But it does nothing
> for clue four, right? Because clue four isn't a capability problem. A smarter
> model still answers "was this written well" beautifully. It's just answering the
> wrong question more fluently.

**"Human reviewers disagree too, so isn't this unfair?"**

> Yeah, and that's exactly the point, not a rebuttal. We know human agreement is
> imperfect because somebody went and measured it. So measure yours. Report kappa
> between your own reviewers. Then you've got two instruments with known error
> bars, instead of one with none.

**"Your data is synthetic, why should I believe it?"**

> You shouldn't, particularly. The trace comes from a simulator calibrated to
> effect sizes from published work, and that's all documented in the repo, source
> by source. The reason it's synthetic is so the demo runs offline and gives the
> same answer every time.
>
> But the point was never "trust my twenty one percent". The point is, run these
> six audits on your own judge output and see what number you get. That's what the
> repo is for.

**"Doesn't a second judge double my cost?"**

> No, actually the opposite. The second judge is binary, so it emits one token
> instead of a paragraph. It ends up cheaper than the graded judge it's protecting.
> It's the single highest value change on that list.
