# Lesson 27: Evaluating conversations

45 min · Intermediate · Prerequisites: Lessons 12 and 20

Transcript scores say how well the system hears. Conversation scores say whether callers got their appointments. This lesson evaluates the second kind properly: not as one success rate, but per call family, where a family is a set of calls built to probe one weakness. Families overlap on purpose; call-11 is both a slow-speaker call and a noisy-line call, because real calls do not fail one variable at a time.

The families: clean bookings (call-01, call-12), slow speakers (call-02, call-11), noisy lines (call-03, call-11), names and spelling (call-06, call-10), spoken number chunks (call-04), safety paths (call-05, call-07, call-09), and reschedule (call-08).

## Run it

```bash
python3 eval_conversations.py
```

As-built, overall 6 of 12, and the families localise the damage: slow speakers 0 of 2, spoken number chunks 0 of 1, reschedule 0 of 1, clean bookings 1 of 2, names and spelling 1 of 2, noisy lines 1 of 2, and safety paths a clean 3 of 3. Hardened: 12 of 12 overall, every family at full marks.

## What the code measures

The single most instructive cell is clean bookings at 1 of 2. The as-built system fails a clean wideband call (call-01's substituted phone digit) for a reason no amount of audio quality fixes, and a team evaluating only hard conditions would never see it. Families force the evaluation to include the calls the system is supposed to find easy, which is where silent data corruption lives.

The safety family's perfect as-built score teaches the complementary lesson: some subsystems are already right, and evaluation should say so, because hardening effort spent re-proving the consent gate is effort not spent on slow speakers at 0 of 2. A family table is a work-allocation document. It also ages well: when a future change regresses reschedule from 1 of 1 to 0 of 1 while the overall rate stays flat (some other family improved), the table shows the trade instead of hiding it in the wash.

Grading itself stays where Lesson 11 put it: in a separate function, against truth records the manager never saw, with escapes counted apart from failures. A conversation evaluation that the system can influence is marketing.

## Common failures

- One aggregate success rate for a system whose failures cluster. The cluster is the information.
- Families designed after the failures are known, so every family passes. These families were implicit in the fixture design from the start.
- Dropping the easy calls from evaluation as "already handled". Call-01 is the standing refutation.

## Recap checklist

- [ ] You can quote the as-built score for every family
- [ ] You know why clean bookings at 1 of 2 is the most important cell
- [ ] You can explain what a family table allocates

## Resources

- The fault table behind the families: [Lesson 20](../20-voice-failure-modes/README.md)
- Naming the failure classes: [Lesson 28](../28-failure-taxonomy/README.md)
