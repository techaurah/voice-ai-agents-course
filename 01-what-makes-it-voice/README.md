# Lesson 01: What makes it voice

30 min · Beginner · Prerequisites: Lesson 00

A text agent and a voice agent can share the same brain and still be different products, because voice adds three things text never has: the caller's words arrive as audio that must be captured and recognised, the agent's words must be synthesised and played, and everything happens against a clock the caller can feel. A two-second pause in a chat window is nothing. On a phone call it is an eternity, and the caller starts talking again, or hangs up.

This lesson dissects one spoken turn. The utterance is the first fixture: "I would like to book a cleaning on tuesday morning", ten words. Its synthetic envelope holds 3,148 ms of speech and 1,732 ms of internal pauses, which is the first surprise for most builders: even a short, fluent sentence is more than a third silence, and every one of those pauses is a place where a naive system can decide the caller has finished.

## Run it

```bash
python3 anatomy.py
```

It prices the turn through the course's simulated latency ledger (in `vox/latency.py`, every figure a stated formula, labelled simulated throughout the course) under two designs. Sequential, where each stage waits for the last: 1,508 ms to first audio, made of 800 ms of endpointing silence, 300 ms of batch transcription finalisation, 265 ms for the model to produce its full reply, 118 ms to synthesise that reply in one pass, and 25 ms of wideband jitter. Streamed, where stages overlap: 1,198 ms, because the transcription final drops to 60 ms and the model only has to reach its first token (195 ms) before synthesis of the first chunk can start.

## What the code measures

The 310 ms saving is real but it is not the headline. The headline is the 800 ms sitting at the front of both designs: the silence the system waits before it believes the turn is over. Streaming optimises the stages engineers like to benchmark and leaves the largest one untouched. Lesson 02 totals this up across every fixture turn, and Module 5 is devoted to attacking that 800 ms properly.

Notice what the streamed design did not change: the synthesis term is 118 ms in both, because the reply used here ("Let me read that back.") is a single sentence, so the first chunk is the whole reply. Streaming only pays when there is a second sentence to hide behind the first, which is Lesson 16's measurement.

## Common failures

- Comparing designs on a single short turn and generalising. Turn shape matters: word counts, reply length, and channel all move the totals. That is why the course always re-measures on the full fixture set before drawing a conclusion.
- Treating the ledger numbers as platform measurements. They are simulated budgets from stated formulas. RESEARCH.md holds the real-world ranges reported by platforms and writers, kept separate on purpose.
- Forgetting the jitter term. It is small here (25 ms wideband, 55 ms on telephony) and it is the only term that gets worse exactly when your callers are on the worst connections.

## Recap checklist

- [ ] You can list the stages between a caller's last word and the agent's first audio
- [ ] You know why the endpointing wait dominates a single turn
- [ ] You can explain when streaming synthesis does and does not save time

## Resources

- The full ledger across all fixture turns: [Lesson 02](../02-the-latency-ledger/README.md)
- Sourced real-world latency budgets: [RESEARCH.md](../RESEARCH.md)
