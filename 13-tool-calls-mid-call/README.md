# Lesson 13: Tool calls mid-call

40 min · Intermediate · Prerequisites: Lessons 02 and 11

A voice agent that cannot act is a very polite answering machine. The booking manager's one real-world action in this course is the schedule lookup on the "when" turn: the caller names a day and time, and before the agent can respond it must check the diary. In the latency model that lookup is a simulated 140 ms, synchronous. This lesson prices three ways of paying it, across the when-turn of all twelve bundled calls.

In series in a streamed design: the lookup happens after the transcript finalises and before the model speaks, mean first audio 834.8 ms. In series in a sequential design: 1,051.0 ms. Prefetched: the lookup is started while the caller is still speaking, triggered by the partial transcript naming a day (Lesson 10's one safe superpower), so by the time the turn ends the answer is already there, and the tool adds nothing: 694.8 ms.

## Run it

```bash
python3 tool_calls.py
```

The prefetch saving is exactly 140.0 ms, the tool's full cost, because in this model prefetching hides all of it. Real prefetches hide less: the partial may name the wrong day, the lookup may need the service slot too, and some tools cannot be speculatively executed at all. The model states its assumption (the lookup depends only on what the caller is currently saying) so you can disagree with it precisely.

## What the code measures

Tool latency in a voice pipeline is not like tool latency in a web app, where 140 ms is beneath notice. It sits inside the turn gap, the most scrutinised 800 ms in the product, and it stacks with everything else in the ledger. The sequential column shows the compounding: batch transcription, full-reply generation, and the tool in series push the when-turn past a second, into the range where Lesson 19 shows callers start talking over the agent.

Prefetching deserves its safety note. A read-only lookup (is this slot free?) is the ideal speculative call: worst case, you looked up the wrong slot and throw the result away. A write (hold this slot) is not, because speculation with side effects creates phantom holds and double bookings. The rule the course follows: prefetch reads freely, never prefetch writes, and let the confirmation layer (Lesson 12) be the only path to a write.

## Common failures

- Putting a slow tool in series on the critical path because the code was simpler that way, then trying to buy the latency back with a faster model.
- Prefetching on the first partial that mentions a day, without checking how often partials revise the day (Lesson 10 measured 1.054 token changes per word; days get revised too).
- Timing out tools silently and letting the agent improvise an answer. An agent that says "that slot is free" because the lookup timed out is worse than one that asks the caller to wait.

## Recap checklist

- [ ] You know the three prices of the schedule lookup on the when-turn
- [ ] You can state the prefetch rule: reads yes, writes no
- [ ] You can explain why tool latency matters more in voice than in web

## Resources

- Partials and their revision rate: [Lesson 10](../10-streaming-partials/README.md)
- Where the when-turn sits in the budget: [Lesson 18](../18-the-latency-budget/README.md)
