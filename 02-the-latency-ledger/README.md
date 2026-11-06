# Lesson 02: The latency ledger

35 min · Beginner · Prerequisites: Lessons 00 and 01

One turn can mislead. A budget built from one turn inherits that turn's word count, its channel, and its speaker's pace, and none of those are yours to choose in production. So this lesson builds the ledger properly: every one of the 24 fixture utterances is priced through the streamed pipeline model, stage by stage, with the endpointing stage taken from each utterance's own simulated end-of-turn wait rather than a flat constant. Slow speakers cost more in this ledger, exactly as they do on a real line, because the wait at the end of their turns is priced from their actual pauses.

The five stages are the ones from Lesson 01: endpointing, transcription finalisation, the model's first token, synthesis of the first chunk, and channel jitter. The prompt given to the model grows across each simulated call, the way a real prompt accumulates slot state turn by turn.

## Run it

```bash
python3 ledger.py
```

Across 24 turns the ledger totals 29,765 ms, a mean of 1,240.2 ms per turn. The shares are the lesson: endpointing takes 19,200 ms, 64.5 percent of all latency. The model's first token is second at 5,041 ms (16.9 percent), synthesis of the first chunk third at 3,157 ms (10.6 percent), transcription finalisation 1,407 ms (4.7 percent), and jitter 960 ms (3.2 percent).

## What the code measures

Two thirds of the caller's perceived wait is a policy decision: how much silence the system demands before it believes a turn has ended. It is not compute, it is not the model, and no faster provider fixes it. This is the single most transferable fact in the course, and it matches the sourced budgets in RESEARCH.md, where end-of-turn detection is also the largest reported stage. Everything in Modules 1 and 5 follows from it: capture and endpointing are not plumbing, they are the product's responsiveness.

The ledger also shows why vendor latency claims are hard to compare: each of these stages is a distribution in real systems, not a number, and providers quote different stages. When you build your own ledger first, their numbers have somewhere to land.

## Common failures

- Optimising the model stage because it is the fashionable one. Here it is worth 16.9 percent; halving it saves less than trimming 100 ms of endpointing silence.
- Averaging away the slow speakers. The mean turn is 1,240.2 ms, but the wait is not evenly shared: it concentrates on exactly the callers who pause longest, which Lesson 19 quantifies.
- Quoting a single total. A budget you cannot decompose by stage cannot be negotiated with a provider or defended in a design review.

## Recap checklist

- [ ] You can reproduce the five stage totals and their shares
- [ ] You know which stage dominates and roughly by how much
- [ ] You can explain why endpointing is a policy, not a component

## Resources

- Where the endpointing wait comes from: [Lesson 06](../06-endpointing/README.md)
- The budget the capstone is graded against: [Lesson 18](../18-the-latency-budget/README.md)
- Sourced comparisons: [RESEARCH.md](../RESEARCH.md)
