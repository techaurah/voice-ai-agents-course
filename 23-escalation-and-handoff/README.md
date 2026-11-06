# Lesson 23: Escalation and handoff

45 min · Intermediate · Prerequisites: Lessons 12 and 21

Every voice agent needs a dignified way to stop being the agent. Escalation is that path, and it has more shapes than "transfer to human": a designed escalation, where the system recognises a situation outside its mandate instantly; an exhausted escalation, where repair attempts run out; and a missed escalation, where the system should have handed off and instead carried on. This lesson measures all three.

The designed path: call-09, the emergency call, under the hardened configuration. The caller's first answer mentions an emergency appointment and a swollen face; the manager escalates on that first answer, in 3 agent turns with 0 repairs spent. The policy's keyword list (emergency, swollen, bleeding, severe pain, knocked out) plus the emergency service itself make the trigger redundant on purpose: either signal alone suffices.

The exhausted path: call-11, the hard call (slow, noisy, telephony), under the as-built configuration, with the policy's repair cap swept. At a cap of 2 repairs, the call escalates after 2 repairs and 8 agent turns. At a cap of 4, it books, using exactly 4 repairs and 10 turns. At a cap of 8, it also books with 4 repairs; the higher cap is never reached, so it changes nothing.

## Run it

```bash
python3 escalation.py
```

The missed path is an ablation. A constructed variant of call-09 asks for a checkup while describing a swollen face, and is graded as the emergency it is. Under the full keyword list, the word "swollen" triggers escalation and the call grades a success. Under a reduced list containing only the word "emergency", the same call is booked as a routine checkup: 1 policy escape, graded "emergency not escalated".

## What the code measures

Escalation quality has a time dimension the outcome alone hides. The designed path costs the caller one answer; the exhausted path costs call-11's caller eight to ten turns of struggle before the same destination, and at the lower cap the system gives up on a call it could have completed. The repair cap is therefore a clinical decision, not a constant: too low and you abandon salvageable callers, too high and you torture unsalvageable ones. The sweep is how you find out which calls sit near the boundary; here, call-11 sits exactly on it, booking at cap 4 and failing at cap 2.

The ablation makes the keyword list's status clear: it is safety equipment, and its coverage is the product of someone enumerating how callers actually describe emergencies. "Swollen" is in the list because callers describe symptoms, not service categories. The reduced list fails silently, booking a tidy, valid, wrong appointment, the most dangerous failure shape in the course. A handoff also has content requirements the code gestures at: the human receiving call-09 needs the transcript and the reason, not a cold transfer and a ringing phone.

## Common failures

- Escalation as a euphemism for failure in the metrics, so teams unconsciously tune it away. Call-09's escalation is the system working perfectly.
- A repair cap copied from a tutorial. The right value is measured per call population, as the sweep shows.
- Keyword lists written from the service catalogue instead of from callers' words for their own problems.

## Recap checklist

- [ ] You can distinguish designed, exhausted, and missed escalation
- [ ] You know the repair-cap sweep results for call-11
- [ ] You know which single word removal creates the missed escalation

## Resources

- The fault-injection view: [Lesson 20](../20-voice-failure-modes/README.md)
- Repair economics: [Lesson 24](../24-cost-per-minute/README.md)
