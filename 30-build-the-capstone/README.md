# Lesson 30: Build the capstone

60 min · Advanced · Prerequisites: Lesson 29

Assembly day. The capstone system is the shared dialogue manager under the hardened configuration, packaged behind one function, `book_call`, in this lesson's artifact: adaptive endpointing (450 ms base, conditional waits to 1,100 ms), read-back confirmation with digit-level correction, name spelling with letter-level correction, the consent gate on, card storage off, streamed staging throughout. Nothing in it is new code. Every mechanism was built and measured in its own lesson; the capstone is the argument that they compose.

## Run it

```bash
python3 capstone_pipeline.py
```

The per-call table is the most satisfying output in the course, and it should be read with Lesson 11's in mind. Call-01 books, with 1 repair: the substituted phone digit is caught in read-back and corrected. Call-02 books, 1 repair, no cut-offs: the slow caller is waited for. Call-06 books with 2 repairs, the spelled name rebuilt letter by letter. Call-11, the hard call that defeated the as-built system two different ways, books with 1 repair. Call-05 ends as consent_refused and call-09 as escalated, the two non-booking outcomes that are successes. The summary: 12 of 12, success rate 1.0, 0 escapes, pooled p50 first audio 742 ms, p95 891 ms, mean repairs 0.58, cost per successful booking 0.0581 USD at the teaching rates.

## What the code measures

Composition is the claim under test. Each defence was verified against the failure it targets, in isolation: endpointing against cut-offs (Lesson 06), confirmation against wrong values (Lesson 12), the gate against the consent fault (Lesson 21). Systems fail at the seams, so the capstone run is the seam test: the same twelve calls, one configuration, graded by the independent grader. It also freezes the system's interface for Lesson 31: `book_call` takes a call fixture and returns a graded result, which is all an evaluation harness should need.

Two honest residues stay on the record. Repairs average 0.58 per call, not zero: the hardened system still mishears, it just catches it. And the cost per successful booking (0.0581) is higher than the as-built's (0.0548), for the Lesson 24 reason: the denominator now includes the hard calls. Correctness is not free; it is merely cheaper than the alternative.

## Common failures

- Assembling the capstone from fresh code "inspired by" the lessons, instead of the very components the lessons measured. Unmeasured substitutions void every earlier result.
- Freezing the configuration informally. The hardened configuration is a named constant in `vox.dialogue` precisely so that every lesson, and the grader, mean the same system.
- Reading 12 of 12 as the end of the work. The fixture set is twelve calls; Lesson 31's gate table is the claim, and it is a claim about this set, stated as such.

## Recap checklist

- [ ] You can name every element of the hardened configuration and its lesson
- [ ] You know the capstone's per-call outcomes, including the two non-bookings
- [ ] You can state the two honest residues in the summary

## Resources

- The grading: [Lesson 31](../31-evaluate-and-harden/README.md)
- The system definition: [vox/dialogue.py](../vox/dialogue.py)
