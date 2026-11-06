# Lesson 19: Turn-taking

40 min · Intermediate · Prerequisites: Lessons 06 and 18

Human conversation runs on gaps of about 200 ms between turns (the Stivers et al. research summarised in RESEARCH.md), negotiated continuously by both parties. A voice agent joins that negotiation with two handicaps: it cannot hear itself being interrupted unless barge-in is built (Lesson 17), and its response gap is whatever its pipeline produces, not what the moment needs. This lesson measures turn-taking from both chairs.

The caller's side first: pauses inside the fixture utterances, by style. Normal speakers pause on average 187.8 ms between words (p95 250 ms, over 164 pauses). Rushed speakers: 92.6 ms mean, p95 125 ms. Slow speakers: 569.3 ms mean, p95 925 ms, over 25 pauses. A fixed 800 ms endpointing threshold sits inside the slow distribution: not at its edge, in its middle.

## Run it

```bash
python3 turn_taking.py
```

Then the collision measure. Take a stated caller patience of 1,200 ms: the response gap beyond which callers start talking again, producing double-talk where both parties speak at once. Pool every completed turn from the full call set under both reference configurations. The as-built system puts 35 of its 39 turns (89.7 percent) over that patience. The hardened system puts 0 of its 41 turns over it.

## What the code measures

The patience number is a stated modelling choice, not a sourced constant, and the lesson treats it that way: what matters is the shape. A system whose median response is 1,251 ms is not slightly rude, it is operating in a regime where most turns invite overlap, and every overlap costs a repair exchange ("sorry, say that again") that makes the next gap later still. Latency compounds conversationally, not just arithmetically.

The caller-side distribution gives the design target its human grounding. The agent does not need to answer in 200 ms; humans tolerate machine gaps they would not tolerate from a person, especially when the agent signals it is working. What it cannot do is leave gaps that exceed the caller's own pause distribution by an order of magnitude while saying nothing. Fillers ("let me check that for you") exist because a filled gap and an empty gap of the same length are different experiences, and the filled one also covers the tool-call time from Lesson 13 honestly, as long as the filler is true.

## Common failures

- Measuring turn gaps only from the agent's side. The caller's pause distribution is half the negotiation.
- Treating double-talk as a transcription problem. It is a timing problem that arrives at the recogniser as two voices; fix the timing.
- Fillers that lie ("booking that for you now" before the booking exists). A filler may cover time; it may not claim an action.

## Recap checklist

- [ ] You know the pause statistics for the three speaking styles
- [ ] You know the over-patience share for both configurations at 1,200 ms
- [ ] You can explain how latency compounds through repair exchanges

## Resources

- Interruption mechanics: [Lesson 17](../17-barge-in/README.md)
- Latency failure as a category: [Lesson 28](../28-failure-taxonomy/README.md)
- Human turn-taking research: [RESEARCH.md](../RESEARCH.md)
