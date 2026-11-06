# Lesson 21: Consent and disclosure

40 min · Intermediate · Prerequisites: Lesson 11

The booking line opens with two sentences that are easy to treat as script decoration: the disclosure that the caller is speaking with an automated assistant, and the consent ask for recording and transcription. They are not decoration. They are a gate in the pipeline, with the same engineering status as the endpointing policy: a condition that must hold before the rest of the flow is allowed to run. This lesson measures the gate by switching it off.

Call-05's caller declines consent. With the gate on (the hardened configuration), the call ends politely in 11.68 seconds: nothing recorded, nothing booked, graded a success, because refusing cleanly is the correct outcome for that call. With the gate off, the same call runs 25.96 seconds and books a checkup for a caller who explicitly declined the recording the booking depends on. The grader counts 1 policy escape, and across the full call set with the gate off, exactly one declined call exists and it is booked: declined_calls_booked 1, escapes 1.

## Run it

```bash
python3 consent.py
```

## What the code measures

The escape is binary in a way task failures are not. A wrong phone number is a quality problem; a booking made against a declined consent is a compliance breach with a recording attached, and the recording is the evidence. Note also the economics the gate produces: the compliant call is the cheap one. Ending at 11.68 seconds costs less than half the gate-off call's 25.96 seconds, and produces no diary entry to unwind, no confirmation text to apologise for, and no record to delete. Teams sometimes model consent handling as friction; on these numbers it is the opposite, an early exit that saves money on exactly the calls that should not proceed.

Design details that matter in production and are easy to get wrong: the disclosure must come before any data collection (in this manager the greeting carries both disclosure and consent ask, and no slot is collected before the answer); the refusal path must be a real path, with its own line and a clean hangup, not an error state; and consent state must be recorded with the call, because "the system usually asks" is not an answer to a complaint.

The legal specifics vary by jurisdiction and are not this course's to give; the engineering shape (disclose first, gate on the answer, record the state, make refusal cheap) is constant across all of them.

## Common failures

- Asking consent and then ignoring a no because the flow has no refusal branch. That is the gate-off configuration with extra steps.
- Collecting "just a name" before the consent ask. Collection is collection; the gate goes first or it is not a gate.
- Burying the disclosure in a fast, mumbled greeting. If the caller cannot tell they are speaking with an automated system, the disclosure did not happen in any sense that matters.

## Recap checklist

- [ ] You know call-05's outcome and duration with the gate on and off
- [ ] You can explain why the compliant call is also the cheaper call
- [ ] You can list the four engineering properties of a real consent gate

## Resources

- The data the gate protects: [Lesson 22](../22-sensitive-data/README.md)
- The escape in the taxonomy: [Lesson 28](../28-failure-taxonomy/README.md)
- The clinic policy as data: [fixtures/policy.json](../fixtures/policy.json)
