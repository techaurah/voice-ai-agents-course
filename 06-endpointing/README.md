# Lesson 06: Endpointing

45 min · Intermediate · Prerequisites: Lesson 05

Endpointing is the decision that a turn is over. Get it late and the agent feels sluggish; get it early and the agent interrupts, which callers experience as rudeness and which breaks the conversation's content too, because the second half of the sentence never reaches the recogniser. This lesson walks every fixture utterance's true segment script under three policies and counts cut-offs: the policy declaring the turn finished while the caller was mid-sentence.

The policies: a fixed 400 ms silence threshold (aggressive), a fixed 800 ms threshold (the classic default), and the adaptive policy from `vox.vad`, which waits 450 ms at most boundaries but up to 1,100 ms when the words so far cannot be a finished request (fewer than three words heard, an incomplete cue word last, a digit run in progress) or when the pause fits the speaker's own established rhythm.

## Run it

```bash
python3 endpointing.py
```

Both fixed policies cut off the same 3 utterances (utt-12, utt-16, utt-19), and all three are the slow speakers: a 400 ms and an 800 ms threshold fail identically here because slow thinking pauses run 680 to 940 ms, straddling both. Their only difference is the wait on completed turns, 400 versus 800 ms, pure latency bought with nothing. The adaptive policy cuts off 1 of the 3 slow utterances, and its wait on completed turns is 300 ms, the model's decision time, because its long waits happen mid-utterance where they prevent cut-offs rather than at the end where they would only add delay.

## What the code measures

This is the honest shape of the endpointing trade. For fast and normal speakers, threshold choice is nearly free latency: their pauses are short, so any sane policy commits quickly. For slow speakers, thresholds in the usual range do not grade the damage, they merely choose it: all three slow utterances contain a pause longer than 800 ms. What fixed the slow cases in the adaptive policy was not a longer blanket wait (that is just an 1,100 ms tax on everyone) but conditional waiting: more silence demanded exactly where the utterance looks unfinished, plus learning the individual speaker's pause ceiling as they talk.

It is also why the platform numbers in RESEARCH.md look the way they do: providers pair a short minimum endpointing delay with a learned turn detector, and keep a much longer maximum delay as the fallback. The adaptive policy here is that architecture in miniature, with its rules written out where you can read them.

One cut-off survives (utt-12), and it stays in print: a caller whose first long pause arrives before the policy has learned anything about them, after words that look complete, is genuinely hard to distinguish from a finished turn.

## Common failures

- Tuning the threshold on average speakers and discovering the tail in production, where it becomes "the agent keeps interrupting my mother".
- Reporting endpointing latency without cut-off rate, or cut-off rate without latency. Either number alone can be made perfect by sacrificing the other.
- Assuming a semantic detector removes the trade. It moves the frontier; utt-12 is the reminder that a frontier remains.

## Recap checklist

- [ ] You can define a cut-off and why it is worse than a slow response
- [ ] You know the cut-off counts for the three policies on the fixture set
- [ ] You can explain the four conditions under which the adaptive policy waits longer

## Resources

- The wait these policies produce, in the budget: [Lesson 02](../02-the-latency-ledger/README.md)
- How cut-offs escalate into failed calls: [Lesson 20](../20-voice-failure-modes/README.md)
- Platform endpointing defaults: [RESEARCH.md](../RESEARCH.md)
