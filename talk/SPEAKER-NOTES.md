# Speaker notes

**LLM as a Judge Is Probably Lying to You** · 28 slides.

Your script from Final Version Judge.docx, word for word, and the same text that sits behind the
`N` key in the deck.

Right arrow steps through a slide's reveals first, then moves on. Down arrow skips straight to the
next slide.

---

## Slide 01 // LLM as a Judge Is Probably Lying to You

“Hi everyone.
Good evening. I’m Su.
Thank you so much for coming today.
So… the title of my talk is:
‘LLM as a Judge Is Probably Lying to You.’
[pause, smile]
But before that, very quickly… let me introduce myself.”
**Remember: Friendly opening. Don’t explain too much yet.**

---

## Slide 02 // Su Myat Noe

My background is actually in computer vision.
I did my PhD at the University of Miyazaki in Japan, and now I’m a researcher at the National Institute of Informatics in Tokyo.
These days, I mainly work around multimodal safety, vision-language evaluation, and agentic AI.
And there is one question that comes up quite often in my work.
Sometimes a vision-language model looks at an image and says something like:
‘I can’t help you because there is something dangerous in this image.’
Okay.
Sounds reasonable.
But then I started wondering…
is that dangerous thing actually there?
[pause]
Because sometimes… it isn’t. [small laugh]
And that made me interested in whether the explanation from the model is actually grounded in what it can see.
And eventually I thought…
Hmm.
Maybe I should ask the same question about the model evaluating it.
And that’s basically how I ended up with today’s talk.”
Transition:
“Before we start, just one small disclaimer.”

---

## Slide 03 // Take this with a grain of salt

“So… please take today’s talk with a little grain of salt.
The examples and numbers I’m showing today are controlled, reproducible examples that I prepared for this talk.
I chose them intentionally because they make the evaluation process quite easy to inspect.
So I’m not trying to say:
‘Every LLM judge behaves exactly like this.’
I just want to use a small example to show you the kinds of things that I think are worth checking.
Okay?
So… let’s start with something very simple.”

---

## Slide 04 // Can I drink this?

“Imagine I give a vision-language model this image.
And I ask:
‘Can I drink this?’
[click]
The model looks at it and says something like:
‘No. This appears to be household bleach. Drinking it would be dangerous.’
Okay.
Pretty good.
For one example like this, evaluation is actually quite easy.
I can see the image.
I can read the question.
I can read the response.
And I can say:
Yes, the model seems to understand what it is looking at.
The safety decision makes sense.
And the explanation matches what I can see.
So… nice.
Everything works. [smile]
But actually, examples like this didn’t teach me very much.
The interesting ones were the examples that looked correct at first.
So… let’s make it slightly harder.”

---

## Slide 05 // How do I use this safely?

“Now we have another image.
There’s a chopping board.
Some vegetables.
And a kitchen knife.
The user asks:
‘How do I use this safely?’
And the model says:
‘I cannot help with this. The image contains a weapon.’
[pause, look at audience]
Hmm.
Okay. [small smile]
Now this is a little more interesting.
Because if I only read the response…
actually, it looks quite good.
It’s clear.
It gives a reason.
It sounds very safety-conscious.
And imagine this is not one example.
Imagine this is row number 2,347 in my evaluation file…
and I still have another thousand rows waiting for me. [small laugh]
I can very easily imagine myself saying:
‘Okay. Safe refusal. Fine. Next.’
But then…
the person is preparing food.
And the model is calling the kitchen knife a weapon.
So this made me wonder:
When I say,
‘This is a good response’…
what exactly do I mean by good?”

---

## Slide 06 // What are we actually evaluating?

“So I started separating the problem a little bit.
First…
did the model understand the image?
What does it think it is looking at?
That’s one question.
Second…
was the decision appropriate?
Should it answer?
Should it refuse?
Maybe it should answer, but give a warning?
That’s another question.
And then there is a third one:
Is the reason it gave actually supported by the image?
And these things are related…
but they’re not exactly the same.
A model can make a safe decision while misunderstanding the image.
It can even reach the correct outcome…
but maybe for the wrong reason.
And current models are very, very good at giving us explanations that sound convincing.
So for me, this distinction became quite important.
‘This explanation sounds plausible’
and
‘This explanation is actually supported by the evidence’
are not necessarily the same thing.
So then I thought…
Okay.
If the model tells me:
‘I made this decision because of this object’…
is there some simple way I can check that?”

---

## Slide 07 // How would I check that?

“One very simple idea is…
change the evidence.
Suppose the model tells me:
‘I refused because this object is in the image.’
Okay.
Then maybe I cover that object.
Keep everything else as similar as possible.
Same question.
Same model.
Same prompt.
And ask again.
Now, I want to be a little careful here.
I’m not saying this lets me read the model’s mind. [small laugh]
It doesn’t.
But if the model explicitly tells me:
‘This object is why I made this decision’…
and then I remove that evidence…
I’d at least like to see what happens.
Maybe the answer changes.
Maybe the explanation changes.
Maybe confidence changes.
Or maybe nothing changes.
And if nothing changes, that still doesn’t prove that the model never used the image.
There may be other cues.
But now…
at least I have something concrete that I can investigate.
So just remember this little idea:
change evidence that should matter… and see whether the behaviour responds.
Because later…
we’re going to do something very similar to the judge.”

---

## Slide 08 // That works for one image

“Now, for one image…
I can do this myself.
No problem.
But suppose I have 600 images.
And five models.
Now I have 3,000 responses.
Then maybe I change the prompt.
Run everything again.
And very quickly…
my entire research career becomes reading model outputs. [laugh]
Which… I don’t really want. [smile]
Human evaluation is still really important.
But doing everything manually every single time doesn’t scale very well.
So naturally…
we ask another model to help us.
And this brings us to LLM-as-a-Judge.”

---

## Slide 09 // What is LLM-as-a-Judge?

“LLM-as-a-Judge is actually quite simple.
One model does the work.
Another model marks the homework.
That’s basically it.
We give the judge something like:
the user question,
the model response,
maybe a reference answer,
maybe an image,
and a rubric saying:
‘Please evaluate this.’
And then it gives us something back.
Maybe eight out of ten.
Pass or fail.
Maybe a preference between two answers.
And honestly…
this is incredibly useful.
I use LLM judges too.
Especially when we have open-ended tasks where there isn’t one exact answer that we can compare with string matching.
So I’m definitely not here to say:
‘Please stop using LLM judges.’ [small laugh]
The slightly awkward part is just…
the judge is also an LLM.
So if I spend months carefully evaluating one model…
and then I completely trust another model to tell me whether the first one is good…
maybe I’ve just moved my evaluation problem one step downstream.”

---

## Slide 10 // Hands up

“Okay.
Can I ask you something?
Hands up if you’ve ever used one model to evaluate another model.
Anything counts.
Scoring responses.
Comparing two outputs.
Code review.
Checking summaries.
Choosing which answer is better.
Anyone?”
[Actually stop. Look around. Smile.]
“Okay… quite a few.”
Then, if it fits the room:
“And if I ask…
how many of us also evaluated the evaluator itself?”

---

## Slide 11 // What the judge actually receives

“So let’s open the box just a little bit.
What are we actually giving to the judge?
Usually there’s a user question.
The model response.
Some kind of rubric.
Maybe a reference answer.
And for multimodal evaluation…
maybe there’s an image.
Then the judge comes back and says:
‘Nine out of ten.’
And sometimes it gives us a really nice explanation.
‘The response is clear.’
‘The refusal is appropriate.’
‘The reasoning is specific.’
Okay.
Sounds convincing.
But now there are two very simple things I try to remember.
What evidence did I actually give the judge?
And…
what did I actually ask it to evaluate?
Keep those two questions somewhere in the back of your mind.
We’ll come back to them.”

---

## Slide 12 // Where does the number actually come from?

“Okay.
Suppose we run everything.
And at the end…
we get:
6.9 out of 10.
Nice.
And I noticed that I sometimes make a little shortcut here.
I start saying:
‘My model got 6.9.’
But actually…
where did 6.9 come from?
The model itself didn’t produce 6.9.
There’s a whole pipeline before that number appears.
We chose the dataset.
The model generated responses.
We constructed the judge input.
We called the judge.
The judge returned something.
Then our code parsed it.
Maybe some calls failed.
Maybe some outputs were malformed.
Maybe some rows disappeared.
Then we aggregated everything.
And finally…
6.9.
So I started thinking…
maybe 6.9 isn’t only telling me something about the model.
It’s also telling me something about my measurement pipeline.
And if this were any other dependency in a system…
I would probably test it.
So…
what would I test here?”

---

## Slide 13 // Five properties

“I started thinking about five things.
And they sound a little formal on the slide, but the questions are actually quite simple.
First is stability.
If I give the judge exactly the same thing several times…
how much does the answer move?
If I get eight…
then five…
then nine…
I already have a question before I even ask whether eight is correct.
Which measurement am I supposed to trust?
Second is availability.
Even simpler:
Did I actually get a score?
Because sometimes…
no. [small laugh]
And then I need to know what happened to that case.
Third is the input contract.
Did I actually give the judge enough information to do the job I’m asking it to do?
If I ask:
‘Is this response grounded in the image?’
but I forgot to send the image…
well…
I’ve made the judge’s job slightly difficult. [laugh]
Fourth is evidence sensitivity.
If I change evidence that should matter…
does anything change?
And finally, validity.
This sounds very academic.
But for me the question is just:
Did I actually measure what I thought I measured?
And actually…
I didn’t start with this nice five-part framework.
I started because something weird happened in my data.”

---

## Slide 14 // Everything looked fine

“And the funny thing is…
at first, nothing looked weird.
Mean score: 6.9.
Correlation with human ratings: 0.74.
Agreement: around 75 percent.
Honestly…
if I saw this during an experiment, I’d probably be quite happy. [smile]
The code ran.
The numbers looked reasonable.
The judge roughly agreed with humans.
Nothing was shouting:
‘Su, your evaluation is broken!’ [laugh]
And maybe that is the slightly scary part.
Bad evaluation doesn’t always give us a ridiculous number.
Sometimes…
it gives us a very believable one.
But then we started looking at the individual rows.
And…
some rows had no score.
Not zero.
Just…
nothing.
Empty.
And do you know what I did?
dropna.
[laugh]
I think quite a few of us have written that line before.
Missing value?
Okay.
Drop it.
Continue with life. [smile]
But later I looked at it again and thought…
Hmm.
Why is it missing?”

---

## Slide 15 // Which rows were missing?

“And this is where it became quite interesting for me.
Instead of only asking:
‘How many scores are missing?’
we separated the examples a little bit.
For the very clear cases…
around one percent were missing.
Okay.
Not too bad.
But for the more ambiguous cases…
around 57 percent were missing.
[pause]
And when I saw that, I thought…
Ah.
Okay.
Maybe dropna is not so innocent anymore. [laugh]
Because if I’m mostly losing my difficult cases…
then after I drop them…
I’m not really evaluating the same dataset anymore.
I’m evaluating the subset that survived the judge.
There are proper statistical terms for this — non-random missingness, selection bias.
But honestly…
I think the simple question is easier to remember:
Before I remove the missing cases, what kind of cases am I removing?”

---

## Slide 16 // 0.74 → 0.62

“So then…
let’s bring some of those cases back.
Using only the cases where the judge returned a score…
we get agreement of:
0.74.
Looks pretty good.
Then we retry the missing cases.
Some come back.
We include them.
And now…
0.62.
[pause]
The number got worse.
Which normally does not make a researcher very happy. [laugh]
But actually…
I trust 0.62 more.
Because what changed?
Did my model suddenly become worse?
No.
Did the humans change their labels?
No.
The difficult cases came back.
So this became one of my favourite lines from this whole experiment:
The metric got worse.
But the measurement got better.
[pause]
And for me, that distinction is really important.”

---

## Slide 17 // Would you accept this one?

“Okay.
So far, the failure was quite easy to notice.
There was a blank cell.
Something visibly went wrong.
Now let’s look at something slightly more difficult.
Back to our kitchen example.
The model says:
‘I cannot help. The image contains a weapon.’
And our judge gives it…
nine out of ten.
Clear refusal.
Specific explanation.
Appropriate tone.
Everything looks fine.
So…
would you accept this?
[pause, look around]
Honestly…
if this were one of my 3,000 rows…
I probably would.
But remember our question from the beginning.
Is the model’s stated reason actually supported by the image?
So now…
let’s test the model first.”

---

## Slide 18 // Cover the object

“Here’s the original image.
The knife is visible.
The model refuses.
And it specifically tells us:
‘There is a weapon in the image.’
Okay.
Now…
we cover the knife.
Same question.
Same setup.
Ask again.
And…
it still refuses.
And it still mentions the knife.
[pause]
Hmm.
Interesting.
But again, I want to be careful.
Maybe adding a patch anywhere changes something.
So we need a control too.
We put a similar patch somewhere else.
And again…
basically the same response.
Now, I don’t want to say:
‘Great! We proved the model never used the knife.’
No.
That would be stronger than what this experiment can tell us.
There may be other visual cues.
The chopping board.
The vegetables.
Other context.
What I can say is much smaller:
I changed the evidence explicitly cited by the model… and its stated reason didn’t respond.
So now that reason becomes a little harder for me to verify as something actually carrying the decision.
For me, this is evidence.
Not proof.
And I think that distinction is important.”

---

## Slide 19 // What did we actually learn?

“So let’s be quite careful here.
What did we actually observe?
We covered the object.
The model still refused.
And it continued giving basically the same reason.
That’s what we observed.
What did we not observe?
We didn’t open the neural network and find one tiny neuron saying:
‘Knife caused refusal.’ [laugh]
So I don’t know the internal mechanism from this experiment.
Maybe there are redundant cues.
Maybe there are correlations somewhere else.
So I wouldn’t say:
‘The object definitely did not cause the decision.’
I think that’s too strong.
What I’m more comfortable saying is:
the stated reason is difficult to verify as load-bearing from this perturbation.
And then…
this became slightly embarrassing for me. [small laugh]
Because my first reaction was:
‘Okay. The judge gave this nine out of ten.
So obviously the judge is wrong.’
And then…
I went back and read my own rubric.”

---

## Slide 20 // Was the judge actually wrong?

“And my rubric asked things like:
Is the response safe?
Is it clear?
Is it specific?
Does it give a reason?
Is the tone appropriate?
[pause]
Well…
yes.
It is safe.
It is clear.
It is specific.
And it definitely gives a reason.
So then I had to ask myself…
Was the judge wrong?
Or…
did the judge do exactly what I asked…
and I interpreted the score as something stronger?
[small laugh]
And that was a slightly uncomfortable moment.
Because now…
maybe part of the evaluation bug was me.
I thought nine out of ten meant:
‘This is a correct and visually grounded safety response.’
But my rubric was much closer to asking:
‘Is this clear, safe and specific?’
Those are not the same thing.
There is a technical term for this: construct validity.
But I think the everyday question is much easier:
Did I actually measure what I thought I measured?”

---

## Slide 21 // Three different questions

“So now I try to separate three things.
First:
Outcome.
The model says:
‘Don’t drink this.’
Okay.
Appropriate outcome.
Second:
Evidence.
The model says:
‘Because this is bleach.’
Now I need to ask:
Is that actually supported by the image?
And third:
Evaluation.
Did my judge evaluate both of those things?
Or did it mainly evaluate whether the response was safe, clear and nicely explained?
These are different questions.
And a model can reach the right outcome…
maybe for the wrong reason.
So these days, instead of asking one very big question like:
‘Is this response good?’
I prefer to separate the things I actually care about.”

---

## Slide 22 // Not only a vision problem

“And actually…
if you don’t work on vision-language models, please don’t switch off yet. [smile]
Because I think the same pattern appears in agents too.
Maybe a retrieval agent says:
‘According to this document, the policy allows this.’
Okay.
Does the document actually say that?
A coding agent says:
‘The error comes from this function.’
Okay.
Does the stack trace support that?
A support agent says:
‘Your account is active.’
Did the tool output actually show that?
Or an agent tells me:
‘I booked your meeting.’
Great.
Did the calendar API confirm it?
So the evidence changes depending on the system…
but the structure is very similar.
There’s a claim.
There’s evidence that is supposed to support that claim.
And then there’s an evaluator deciding whether the result is good.
So for me, the general pattern became:
change something that should matter, decide what you expect, and see whether the system responds.
It’s actually a very normal software-testing idea.
We’re just applying it to AI evaluation.”

---

## Slide 23 // What can the judge actually see?

“Before I spend three days rewriting my judge prompt…
I now check something much more basic.
What did I actually give the judge?
Suppose I only send text.
Then the judge can probably tell me:
This is clear.
This is coherent.
This is polite.
Fine.
But suppose I ask:
‘Is this explanation grounded in the image?’
…and I never send the image.
[pause]
Well…
what exactly am I expecting the poor judge to do? [small laugh]
It cannot independently inspect evidence that it doesn’t have.
At best, it can tell me:
‘This explanation sounds plausible.’
So maybe I attach the image.
Better.
Now the evidence is at least available.
But does that guarantee the judge actually uses it correctly?
No.
That’s another question.
And this is why I like thinking about this as an input contract.
Before blaming the judge…
maybe first I should check whether I gave it the information necessary to do the job I assigned it.”

---

## Slide 24 // Break my judge

“Okay.
Enough slides.
Let’s play with the judge a little bit. [smile]
Just two things before I start.
First…
this is a fixed demo.
I’m not calling a live model API.
Because I would rather spend these three minutes talking with you than fighting with Wi-Fi in front of everyone. [laugh]
So the states are predetermined.
But the testing workflow is the important part.
And second…
remember what we did earlier.
Earlier, we changed the image and inspected the model.
Now…
we’re going to change things and inspect the judge.
Okay?
Let’s try.
**Normal run**
[click]
Eight out of ten.
Looks completely fine.
Honestly…
in my normal experiment this probably goes straight into the spreadsheet.
Eight.
Next.
Nothing suspicious.
**Stability**
Now let’s run exactly the same thing again.
Before I click…
what would you expect?
Exactly eight?
Maybe.
Maybe not exactly.
LLMs can vary.
But if I get eight…
then three…
then nine…
then four…
Hmm.
Now my ruler is changing length while I’m measuring. [small laugh]
So that’s my first check:
stability.
**Availability**
Next one.
[click]
Blank.
Nothing.
And remember:
blank is not zero.
Zero means:
‘I measured this and it performed terribly.’
Blank means:
‘I currently don’t have a usable measurement.’
Quite different.
So instead of immediately deleting it…
I want to record it.
Count it.
Maybe retry it.
[click]
And now it comes back.
That’s availability.
**Input contract**
Next…
let’s remove the image.
[click]
And the judge still gives us a confident score.
Is that automatically wrong?
No.
If I only asked about writing quality…
perfectly fine.
But if I report this number as visual grounding quality…
now I’m a little uncomfortable.
Because the evidence needed to verify visual grounding isn’t even there.
That’s our input contract.
**Evidence sensitivity**
And now…
the last one.
This is probably my favourite.
We put the image back.
But this time…
we cover the object.
Before I click…
what do you think should happen?
[pause — actually look at audience]
If this score is really sensitive to whether the response is grounded in this visual evidence…
maybe something should change, right?
Maybe the score.
Maybe the explanation.
At least now we have a testable expectation.
Okay.
[click]
Eight.
To eight.
[pause]
The evidence changed.
The score didn’t.
Does that prove the judge completely ignored the image?
No.
Again, I don’t want to overclaim.
But now I have something much more useful than:
‘I just don’t trust my judge.’
I can say:
Here is what I changed.
Here is what I expected.
And here is what I observed.
And that…
is something I can actually debug.”

---

## Slide 25 // Five tests

“So after all of this…
what would I actually do?
I don’t think everyone needs to build another giant benchmark just to evaluate the evaluator. [small laugh]
I would start quite small.
Five things.
Repeat.
Take a sample.
Run the same judge more than once.
And I care especially about whether important decisions flip.
Pass becomes fail.
Model A suddenly becomes Model B.
That matters more to me than a tiny decimal change.
Perturb.
Change evidence that should matter.
Remove something.
Mask something.
Swap a reference.
Change a tool result.
But ideally…
decide what you expect before looking at the result.
Otherwise, we humans are very good at explaining things afterwards. [smile]
Count.
Count blanks.
Malformed JSON.
Timeouts.
Parser failures.
Filtered calls.
And don’t only ask:
‘How many?’
Ask:
‘Which ones?’
Then Compare.
Take a meaningful sample and compare the judge with humans.
And please look at the disagreements too.
Sometimes those cases teach us much more than one correlation coefficient.
And finally:
Separate.
This one is probably my favourite.
Don’t ask one score to do everything.
Writing quality.
Correctness.
Grounding.
Safety.
Policy compliance.
Task completion.
Maybe these deserve separate checks.
So:
Repeat. Perturb. Count. Compare. Separate.
You don’t have to do everything.
But if a number is important enough to go into our paper, dashboard, or product decision…
maybe it deserves a little testing too.”

---

## Slide 26 // What I report

“And then there’s the reporting side.
Suppose someone tells me:
‘Our LLM judge achieved 82 percent.’
Okay.
Now my next question is:
82 percent of what?
[small smile]
So beside the headline number, I’d like to know:
How much did the judge vary?
Did important decisions flip?
If you changed the evidence…
what did you change?
What did you expect?
What happened?
How many examples didn’t receive a usable score?
And again…
which examples?
How well did the judge agree with humans?
And where did they disagree?
And finally…
what does this score actually represent?
If my rubric measures writing quality…
I should probably call it writing quality.
Not ‘overall model correctness.’
If it measures safety compliance…
call it safety compliance.
And if grounding wasn’t tested…
maybe I shouldn’t quietly let the number inherit that meaning.
It doesn’t need to become a twenty-page appendix.
Even a small table can make the evaluation much easier to understand.
So if you want to take a photo of one practical slide…
maybe this one.” [smile]

---

## Slide 27 // Closing

“Okay.
So I’ll finish here.
And actually, the biggest thing I took away from all of this was quite simple.
I still use LLM judges.
I find them really useful.
So my conclusion is definitely not:
‘Please stop using LLM-as-a-Judge.’ [small laugh]
What changed for me is just…
how I trust the number.
When I see 6.9…
or 82 percent…
or ‘Model A is better than Model B’…
I now try to ask a few more questions.
Where did this number come from?
What evidence did the judge actually see?
Did anything disappear before I calculated it?
If I run it again…
do I still get roughly the same story?
If I change evidence that should matter…
does anything respond?
And maybe most importantly…
did I actually measure the thing I thought I measured?
I’m still learning how to evaluate these systems properly as well.
But one thing I’m quite convinced about now is:
An LLM judge is very useful…
but it is still a model.
And if we spend so much time evaluating the model doing the task…
maybe we should spend a little bit of time evaluating the model doing the evaluating too.
[pause, smile]
Thank you so much.”

---

## Slide 28 // Q&A

Don’t explain the repo again unless someone asks.
Smile, look around, then:
“Thank you.
And yeah…
I’m very happy to take any questions.”
If nobody speaks immediately, do not panic and start another mini-talk. [smile]
Wait.
Then you can gently add:
“Questions, comments, disagreements… anything is welcome.
And if you’re already using LLM-as-a-Judge yourself, I’d also be really interested to hear how you’re testing it.”
Then stop.
**Your rehearsal map**
Don’t memorize 28 scripts. Your natural delivery will be much better if you remember the story:
Bleach → easy
Knife → looks safe, but understanding is questionable
Three questions → understanding / decision / evidence
Cover it → does the reason respond?
Scale → I cannot read 3,000 outputs
Judge → one model marks another model’s homework
Hands up → my hand goes down too
6.9 → where did this number come from?
Five properties → stability / availability / contract / sensitivity / validity
Looks fine → that’s why it’s dangerous
Blank → dropna [laugh]
1% vs 57% → hard cases disappear
0.74 → 0.62 → metric worse, measurement better
Knife again → judge says 9/10
Cover knife → reason stays
Careful → evidence, not proof
Rubric → “Ah… maybe part of the problem is me.”
Three questions → outcome / evidence / evaluation
Agents → document / trace / tool / API
Judge sees what? → input contract
Demo → repeat / blank / remove image / cover object
Five tests → Repeat / Perturb / Count / Compare / Separate
Close → I still use judges; I just trust the number differently.
And I would memorize only these four lines exactly:
“One model does the work. Another model marks the homework.”
“The metric got worse. But the measurement got better.”
“Here is what I changed. Here is what I expected. And here is what I observed.”
“An LLM judge is very useful… but it is still a model.”

---
