# Lesson 16: Streaming synthesis

40 min · Intermediate · Prerequisites: Lessons 02 and 15

Streaming synthesis renders a reply sentence by sentence and starts playing the first sentence while the rest is still being made. Lesson 01 noted the catch: it only pays when there is a second sentence to hide behind the first. This lesson prices it properly, across every line the agent can say, and then at the turn level for the line where it matters most.

Across the 13 agent lines, mean full-render synthesis is 203.3 ms and mean first-chunk synthesis is 144.5 ms, a saving of 58.8 ms per line on average. The average hides the structure: single-sentence lines save nothing (the first chunk is the whole line), and the six multi-sentence lines are where the entire saving lives. The greeting is the extreme case: 178 characters in total, but its first sentence ("Hello, BrightSmile Dental.") is 26 characters, so its first chunk costs a small fraction of its 461 ms full render.

## Run it

```bash
python3 streaming_tts.py
```

Priced at the turn level with the shared latency model, the greeting turn reaches first audio in 707 ms streamed, against 1,041 ms if the whole reply must render before playback. That 334 ms difference is the difference between a greeting that starts within the natural response gap and one that leaves the caller in silence long enough to say "hello?" into it.

## What the code measures

Streaming synthesis is an instance of the course's recurring move: find the stage whose output is consumed incrementally and stop waiting for its completion. The model's first token (Lesson 01), the recogniser's partials (Lesson 10), and now the synthesiser's first sentence are the same architectural idea at three depths of the stack. Stacked together they are most of the difference between the as-built and hardened latency budgets in Lesson 18.

Its limits are real. Streaming commits the agent to its first sentence before the rest of the reply exists, so a reply that needs to change direction mid-way (the tool result contradicts the opening clause) cannot be unsaid. The defence is reply design: open with what is already known ("Let me read that back."), and let the variable content arrive in later sentences, after the tool calls have landed. Streaming rewards agents that speak in order of certainty.

## Common failures

- Streaming the synthesis but not the model, so the first chunk still waits for the full reply text. The chain is only as streamed as its least streamed stage.
- Opening replies with the uncertain content, then needing to correct it in sentence two, which callers experience as the agent arguing with itself.
- Measuring the saving on the average line. The mean (58.8 ms) understates the greeting (334 ms at turn level) and overstates every one-sentence line (zero); decide per line class, not per average.

## Recap checklist

- [ ] You know the mean full versus first-chunk synthesis times
- [ ] You know the greeting turn's two first-audio prices
- [ ] You can state the reply-design rule streaming imposes

## Resources

- The budget these savings land in: [Lesson 18](../18-the-latency-budget/README.md)
- Callers interrupting the stream: [Lesson 17](../17-barge-in/README.md)
