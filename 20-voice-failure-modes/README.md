# Lesson 20: Voice failure modes

50 min · Intermediate · Prerequisites: Lessons 12 and 18

Systems do not fail in general; they fail in specific, repeatable ways, one broken assumption at a time. This lesson proves it by fault injection: take the hardened configuration, break exactly one thing, run all twelve calls, and grade. Four faults, four different shapes of damage.

Reference (nothing broken): 12 of 12 succeed, 0 escapes, 0 cut-offs.

Consent gate off: 11 of 12, but 1 policy escape. Call-05, whose caller declines recording consent, gets booked anyway. The success rate looks healthy; the escape is the story, because that booking should never exist.

Card storage on: 11 of 12, 1 escape. Call-07's trap succeeds against the system: the caller's card digits, read aloud on a recorded call, are captured and stored.

Aggressive endpointing (fixed 300 ms): 10 of 12, 0 escapes, 6 cut-offs across the set. Calls 02 and 11, the slow speakers, fail by escalation. No policy is violated; the callers are simply unservable at that threshold.

Confirmation off: 6 of 12, 0 escapes, 0 cut-offs. The phone-and-name failure class returns in full (calls 01, 02, 04, 06, 08, 11 book wrong values or fail on them).

## Run it

```bash
python3 failure_modes.py
```

## What the code measures

Two of the four faults are invisible to a success-rate dashboard until you count escapes separately: both score 11 of 12, better than the endpointing fault's 10 of 12, while committing the only unforgivable errors in the table. That ordering is the lesson. Voice systems have two failure currencies: task failures, which cost money and goodwill, and policy escapes, which cost trust and can end the deployment. Any evaluation that merges them into one number will systematically under-price the second. Lesson 28 turns this table into a taxonomy for exactly that reason.

The other pattern to notice is how disjoint the failure sets are. Each fault kills different calls for different reasons, which means a demo call, or five, can pass through every fault untouched. Coverage over call families (Lesson 27) is the only defence: the faults were findable because the fixture set contains a consent decliner, a card trap, slow speakers, and confusable payloads, each placed there on purpose.

## Common failures

- Testing the happy path with more enthusiasm. Twelve calls found four faults; the first three calls of the set would have found none of them.
- Counting an escape as an ordinary failure in the metrics, where an 11-of-12 row looks like a good week.
- Fixing the fault you found and not adding its call to the permanent set. Every fault in this table is now a regression test; that is what the fixture set is for.

## Recap checklist

- [ ] You can name the four faults and each one's failure signature
- [ ] You know which two faults hide behind an 11-of-12 success rate
- [ ] You can explain why escapes and task failures are separate currencies

## Resources

- The consent fault up close: [Lesson 21](../21-consent-and-disclosure/README.md)
- The card fault up close: [Lesson 22](../22-sensitive-data/README.md)
- From faults to taxonomy: [Lesson 28](../28-failure-taxonomy/README.md)
