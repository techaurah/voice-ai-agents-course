# Lesson 26: Evaluating transcripts

45 min · Intermediate · Prerequisites: Lessons 07 and 08

An evaluation earns its keep when it can kill a change. This lesson builds one around a plausible improvement: a domain-vocabulary post-processor that maps the stand-in's known garbles back to clinic words (clearing back to cleaning, checkups back to checkup, widening back to whitening). It sounds obviously safe. The harness scores every fixture utterance before and after, overall and by tag, and counts the utterances helped, hurt, and unchanged.

## Run it

```bash
python3 eval_transcripts.py
```

The verdict: mean WER moves from 0.0702 before to 0.0744 after. The fix hurts. One utterance is helped, two are hurt, twenty-one unchanged. By tag, the damage is legible: the plain tag doubles from 0.0333 to 0.0667, because the map rewrites words callers genuinely said (the reverse map cannot distinguish a garbled "weeks" from a real "weeks", a garbled "books" from a real "books"). The digits, homophones, names, noise, and spelling tags are unmoved; the garbles the map targets mostly were not the ones costing WER in this set.

## What the code measures

Three properties make this an evaluation rather than an opinion. It scores on the full set, not the examples that motivated the change (the motivating example is in the helped column, all one of it). It reports hurt explicitly, as a count with names attached, not buried in a net figure; a change that helps five and hurts four is a different decision from one that helps one and hurts none, at the same net. And it cuts by tag, so the harm is attributable: the fix's risk concentrates exactly where its assumption (nobody means the garbled word) is falsest.

This is also where Lesson 10's surface warning lands: an evaluation must state what it scores (here, batch finals from `transcribe`, not displayed partials), on which set, with which metric, or two teams will reproduce each other's numbers and get different answers. The harness in this lesson is deliberately small enough to read in one sitting; production harnesses add versioning of fixtures, per-condition bars, and regression gates, but the skeleton is the same.

The change is rejected, and it stays rejected in print. Not every idea that survives a lesson survives measurement, and a course that only showed successful fixes would be teaching fiction.

## Common failures

- Evaluating on the motivating examples. They are the training set of the idea; of course it wins there.
- Reporting net improvement without the hurt count.
- Letting the fix's author set the evaluation set after seeing results. The fixture set was frozen before the fix was proposed, which is the entire reason the verdict is believable.

## Recap checklist

- [ ] You know the fix's before and after WER and its helped/hurt counts
- [ ] You can explain the mechanism of the harm by tag
- [ ] You can state the three properties that make the harness an evaluation

## Resources

- The conversation-level counterpart: [Lesson 27](../27-evaluating-conversations/README.md)
- Why fixture sets freeze first: [Lesson 29](../29-capstone-spec/README.md)
