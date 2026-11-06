# Lesson 15: The TTS stand-in

35 min · Beginner · Prerequisites: Lesson 00

The output side gets its stand-in in this lesson. `vox.tts` renders each word as a short tone burst whose pitch is a stable hash of the word, so a spoken reply has real samples, a real file, and a real duration, while making no claim to sound like speech. What the course measures about synthesis is timing, and the timing model is stated in the module where you can argue with it: a fixed 70 ms session cost plus 2.2 ms per character for a full one-pass render, with streaming synthesis paying the session cost once and then rendering sentence by sentence.

The artifact prices every line the booking agent can say: characters, words, rendered duration, and simulated full-render synthesis time.

## Run it

```bash
python3 tts_lab.py
```

The greeting is the outlier: 178 characters, 26 words, 7,618 ms of rendered audio, 461 ms to synthesise in one pass. Short functional lines are nothing alike: "Can I take your name?" is 21 characters and 116 ms of synthesis against 1,141 ms of audio. Across all 13 lines, mean synthesis time is 7.6 percent of rendered duration (a ratio of 0.076), which is the stand-in's way of saying synthesis is comfortably faster than real time, and the interesting constraint is never total synthesis time. It is time to first audio, which is Lesson 16.

## What the code measures

Duration grows with words; synthesis grows with characters. The two curves separate on exactly the lines a designer controls: long words and abbreviations inflate synthesis without adding spoken time, and chatty multi-clause lines inflate spoken time (the caller's wait, the platform's per-minute bill) without much synthesis cost. The greeting earns its scrutiny: at 7.6 seconds of audio it is the longest thing the agent ever says, it carries the disclosure and the consent ask, and it plays before the caller has said a word. Every second of it is a second in which the caller can hang up or talk over the agent (Lesson 17 makes that cost concrete).

There is also a discipline point: the stand-in renders tones, and the course never evaluates how it sounds. Voice quality, prosody, and pronunciation are real selection criteria for a synthesis provider and none of them are measurable here; the course's claim is only about the timing architecture, and RESEARCH.md carries the sourced provider context separately.

## Common failures

- Writing agent lines like paragraphs. Every clause is billed by the second and waited through by a human.
- Optimising total synthesis time when first-audio time is the binding constraint.
- Letting the greeting grow by accretion, one legal clause at a time, until callers routinely interrupt it, which the next lessons show corrupting the conversation history.

## Recap checklist

- [ ] You can state the stand-in's synthesis timing model
- [ ] You know the greeting's character count, duration, and synthesis time
- [ ] You can explain why duration and synthesis time follow different curves

## Resources

- Streaming the synthesis: [Lesson 16](../16-streaming-synthesis/README.md)
- Callers talking back: [Lesson 17](../17-barge-in/README.md)
- What spoken time costs: [Lesson 24](../24-cost-per-minute/README.md)
