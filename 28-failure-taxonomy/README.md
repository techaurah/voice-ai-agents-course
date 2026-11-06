# Lesson 28: Failure taxonomy

40 min · Intermediate · Prerequisites: Lessons 20, 26, and 27

"The agent is unreliable" is not a diagnosis. This lesson builds the instrument that replaces it: a failure taxonomy, populated mechanically. The suite is the as-built configuration plus the four single-fault variants from Lesson 20, five configurations times twelve calls, sixty graded runs. Every failure is classified from the grader's own evidence: the field named in the failure reason becomes a transcription category, an outcome mismatch becomes repair exhaustion, and each policy escape keeps its own name.

## Run it

```bash
python3 taxonomy.py
```

Of 60 runs, 16 fail. The taxonomy: transcription_digits 10, repair_exhaustion 4, consent_escape 1, payment_escape 1. Example calls are attached per category: call-01 for digits, call-02 for repair exhaustion, call-05 for consent, call-07 for payment. Notably absent: transcription_name, which occurs in the suite (call-06 fails on its name) but is never the primary classification, because call-06 also fails on its phone number in the same runs and the classifier checks digits first. The taxonomy's priority order is documented in the artifact for exactly that reason; a classification you cannot interrogate is just a label.

## What the code measures

The counts rewrite the work plan. Ten of sixteen failures are one category, spoken digits arriving wrong and surviving into bookings, and that category has one known, measured fix (Lesson 12's confirmation), which the suite's own hardened reference proves. Repair exhaustion, the second category, is an endpointing and patience problem (Lessons 06 and 23). The two escapes are singletons by count and first-order by importance: a taxonomy that sorted purely by frequency would work on them last, which is why the taxonomy keeps escapes as named categories rather than folding them into the general failure mass. Classification serves triage, and triage weighs severity alongside frequency.

The deeper point is methodological: the taxonomy is generated, not curated. Nobody read sixty transcripts and formed impressions; a classifier over grader output produced the table, so it can be regenerated after every change and diffed. When the hardened configuration is added to the suite, its row is empty, and the diff between suite versions is the release note that matters.

## Common failures

- Taxonomies built from anecdotes: the memorable call (usually the funniest or the angriest) becomes a category with n=1 and a quarter's roadmap.
- Categories so broad they cannot be fixed ("quality issues") or so narrow every failure is unique. The grain here, mechanism-level, is chosen so each category maps to a layer of the stack and a lesson that addresses it.
- Letting the classifier's priority order stay implicit. Call-06's name failure is real and is masked by its phone failure; a team that does not know the order will one day "fix digits" and be surprised by the names waiting underneath.

## Recap checklist

- [ ] You know the suite size, failure total, and the four category counts
- [ ] You can explain why escapes stay separate despite a count of one each
- [ ] You know why transcription_name is absent, and what that reveals

## Resources

- The suite's configurations: [Lesson 20](../20-voice-failure-modes/README.md)
- The fix for the largest category: [Lesson 12](../12-confirmation-and-repair/README.md)
