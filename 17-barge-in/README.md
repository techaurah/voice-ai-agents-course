# Lesson 17: Barge-in

45 min · Intermediate · Prerequisites: Lessons 15 and 16

Callers interrupt. They interrupt because the agent is slow, because they already know the answer, because the agent is reading back something they want to correct, and sometimes because what the agent is saying is wrong. A voice system has to detect the interruption, stop playing (in this lesson's stated model, playback halts 120 ms after the caller starts speaking), and deal with the consequence nobody demos: the conversation history now claims the agent said things the caller never heard.

The lesson stages it on a spoken confirmation: "your cleaning is booked for tuesday at ten o'clock and a confirmation text is on its way", 17 words, 4,337 ms of audio by the stand-in's word timing. The caller barges in at 25, 50, and 75 percent of the line.

## Run it

```bash
python3 barge_in.py
```

At 25 percent, the caller hears 4 words. Thirteen words are phantom: present in a naive history, absent from the caller's ears, including two of the three facts the line exists to deliver (the day and the time; only the service landed). At 50 percent, 8 words are heard and all three facts have landed, but 9 phantom words remain. At 75 percent, 12 heard, 5 phantom, facts complete.

## What the code measures

Phantom history is a data-integrity bug with a conversational symptom. The agent's next turn is generated from a record that says the time was communicated; when the caller then asks "wait, what time?", a naive agent hears a confused caller rather than its own undelivered sentence, and may repeat itself, or worse, "confirm" a fact the caller never received. The fix is bookkeeping, not modelling: record what was actually played, per word or per sentence boundary, and let the history show the reply as truncated at the interrupt point. Playback position is knowable exactly in any real stack, since the player is yours.

The placement lesson is as important: the facts sit late in this line because written English puts the pleasantries first. Spoken confirmations for interrupt-prone moments should front-load the payload (time first, then the service, then the follow-up detail), because the interrupt distribution is not yours to control. At a 25 percent interrupt, front-loading is the difference between a caller who heard "ten o'clock, tuesday" and one who heard "your cleaning is booked for".

## Common failures

- Stopping playback but not truncating the history, so the transcript and the caller's memory diverge silently.
- Treating barge-in as an error state instead of a normal turn type with its own handling: the caller who interrupts a read-back is usually correcting you, which is Lesson 12's repair channel arriving early.
- Long monologue lines in interrupt-prone slots. The greeting (7,618 ms, Lesson 15) is the worst offender in this agent, and it cannot be shortened past the disclosure the policy requires, which is a genuine design tension, not a tidy-up.

## Recap checklist

- [ ] You know the heard and phantom word counts at each interrupt point
- [ ] You can explain the phantom-history bug and its fix
- [ ] You can state the front-loading rule for confirmation lines

## Resources

- Turn-taking and collision rates: [Lesson 19](../19-turn-taking/README.md)
- The greeting's length problem: [Lesson 15](../15-the-tts-standin/README.md)
