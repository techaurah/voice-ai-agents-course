# Lesson 10: Streaming partials

40 min · Intermediate · Prerequisites: Lesson 07

Streaming recognition emits partial hypotheses as the caller speaks, revising them as more audio arrives. Partials are what let a pipeline start thinking before the turn ends, and they are seductive: the screen shows text early, and it is tempting to act on it. This lesson measures what partials actually are, a draft that rewrites itself, and what happens to accuracy if a downstream component commits early.

The stand-in's partials come from `vox.stt.partials`: a draft pass that is greedier with confusions than the final pass, shown word by word, with the last two visible tokens still carrying draft readings at any moment. That construction detail matters and is stated in the module, because it makes the displayed final partial measurably different from the batch final transcript.

## Run it

```bash
python3 partials.py
```

Across the 24 fixture utterances, the displayed stream revises itself at a rate of 1.054 token changes per word of final transcript: on average, every word you watch arrive is later changed at least once. The accuracy ladder is stark. The batch final transcript scores 0.0702 mean WER. The final displayed partial, same utterances, scores 0.0913, the draft contamination at the tail made visible. And committing at 60 percent of the words, the moment a partial first looks complete enough to act on, scores 0.4135.

## What the code measures

Partials are a latency instrument, not an accuracy instrument. Their correct uses are the ones that tolerate revision: starting the model on a draft prompt, prefetching a tool call (Lesson 13), rendering the caller's words on a screen for a human supervisor. Their incorrect use is committing state: booking, charging, confirming, on text with a measured 0.4135 error rate at the tempting moment. The gap between 0.4135 and 0.0702 is the price of impatience, quoted in the only currency that matters.

The smaller gap, 0.0913 displayed-final versus 0.0702 batch-final, carries its own warning: what your logs show as "the transcript" depends on which surface you scraped it from. An evaluation built on displayed finals and one built on batch finals disagree by two points of WER on identical audio, and Lesson 26 insists an evaluation name its surface for exactly this reason.

## Common failures

- Triggering side effects from partials. If it cannot be undone, it waits for the final.
- Designing the dialogue as if partials arrive word-perfect and the final merely confirms them. The revision rate, roughly one change per word, is the design constraint.
- Comparing two recognisers where one was scored on finals and the other on last partials.

## Recap checklist

- [ ] You know the revision rate of the partial stream on the fixtures
- [ ] You can quote the accuracy cost of committing at 60 percent
- [ ] You can name two safe and one unsafe use of partials

## Resources

- Prefetching tool calls from partials: [Lesson 13](../13-tool-calls-mid-call/README.md)
- Evaluation surfaces: [Lesson 26](../26-evaluating-transcripts/README.md)
