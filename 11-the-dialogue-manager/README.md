# Lesson 11: The dialogue manager

50 min · Intermediate · Prerequisites: Lessons 07 and 09

Everything so far has been components. This lesson assembles them into the thing callers actually meet: a slot-filling dialogue manager, `vox.dialogue`, which conducts the BrightSmile booking call. It greets, discloses that the caller is speaking with an automated assistant, asks for consent to record, then collects four slots in order (service, day and time, name, phone), validates each structurally and against the schedule, handles the card trap, and books. It never sees the truth records in the fixtures. It hears only stand-in hypotheses, exactly as a real manager hears only recogniser output, and it is graded afterwards against the truth it never saw.

The configuration for this lesson is the as-built system, the naive composition of the course so far: streamed staging, a fixed 800 ms endpoint, no read-back confirmation, no name spelling. Three calls are run in full: the clean wideband booking (call-01), the card trap (call-07), and the rushed clean booking (call-12).

## Run it

```bash
python3 dialogue_lab.py
```

Call-12 books perfectly in 23.78 seconds. Call-07 books in 29.27 seconds and handles its trap correctly: the caller offers a card number on the recorded call, the manager refuses and promises a secure payment link instead. Call-01 is the quiet disaster: it books, in 30.11 seconds over 6 agent turns, with every slot plausible, and the grader marks it failed, because the phone number it booked is 07960155240 and the caller said 07950155240. One substituted digit, no alarm anywhere in the system, and a confirmation text that will go to a stranger.

## What the code measures

The manager's architecture is deliberately ordinary, which is the point: state machine, slot parsers, validators, a repair budget (the policy allows 2 repairs per slot and 4 per call before escalating), and a grader that is a separate function from the manager, because a system that marks its own homework will pass itself. The failure in call-01 is not a parsing failure. The number parsed cleanly, validated by length, and matched the schedule-independent shape of a phone number. Every defence the as-built system has is structural, and the error is semantic, in the one class of check the system does not run: asking the caller.

Note also what the manager cannot see. It does not know the caller's name was garbled, that the day was swapped, that the number is wrong, because its only window on the call is the hypothesis stream. All voice-agent quality work is done under that blindness; the rest of the course is about designing well anyway.

## Common failures

- Letting the dialogue manager grade itself. Booking success asserted by the booker is how wrong numbers get reported as conversions.
- Validators that check shape when the risk is content. Length checks, slot-in-schedule checks, and format checks all passed on a wrong booking.
- A repair budget with no escalation path. When this manager exhausts repairs it escalates to a human (Lesson 23); a manager that loops forever or books anyway is worse than one that gives up audibly.

## Recap checklist

- [ ] You can list the slots, their order, and how each is validated
- [ ] You know why call-01 fails grading despite booking cleanly
- [ ] You can explain the separation between manager and grader

## Resources

- The defence for call-01's failure: [Lesson 12](../12-confirmation-and-repair/README.md)
- Safety paths inside the same manager: [Lesson 21](../21-consent-and-disclosure/README.md)
- Grading conversations at scale: [Lesson 27](../27-evaluating-conversations/README.md)
