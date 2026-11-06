# Lesson 31: Evaluate and harden

50 min · Advanced · Prerequisites: Lesson 30

The last lesson runs the grading the whole course has pointed at: both reference configurations, the same twelve calls, the gates fixed in Lesson 29 before the capstone existed. The ship verdict belongs to the capstone's row, but the as-built row stays in the table, because a gate report that only shows the passing system teaches nothing about the gates.

## Run it

```bash
python3 evaluate_capstone.py
```

As-built: success rate 0.5 (gate 0.9, fail), escapes 0 (gate 0, pass), p50 1,251 ms (gate 800, fail), p95 1,391 ms (gate 1,500, pass), mean repairs 0.5 (gate 1.5, pass). Three of five gates.

Capstone: success rate 1.0, escapes 0, p50 742 ms, p95 891 ms, mean repairs 0.58. Five of five gates. Ship: true.

## What the code measures

The two failing as-built gates are the course in miniature: it fails on outcomes (half the calls) and on median responsiveness (a fixed 800 ms wait inside every turn), while passing on the tail latency, the repairs budget it never spends, and the policy escapes it does not commit. That profile is worth dwelling on, because it describes many real first versions: safe, polite, and not good enough at the core transaction. The hardening that closed the gap was not more model or more spend; it was endpointing that respects callers, confirmation that respects arithmetic, and a spelling channel for names, each measured before it was adopted.

The hardening loop this lesson names is the transferable asset: fix gates before building, measure the baseline, change one layer at a time (Lessons 12, 18, 20), evaluate on frozen families (Lesson 27), classify the failures that remain (Lesson 28), and only then re-grade. Whatever stack you build on next, that loop survives the platform choices, which is fortunate, because the platforms will change under you and the loop is the part that is yours.

What the verdict does not claim: that the system is ready for real callers. The fixtures are twelve scripted calls, the recogniser and synthesiser are stand-ins, and the latency figures are simulated budgets. The course's claim is narrower and stronger: on a frozen, graded set, against gates set in advance from sourced budgets, the hardened design passes and the naive design measurably does not, and every number in that sentence can be reproduced by running the code in this repo.

## Common failures

- Moving the gates at grading time. They are in a file with a date on it; the date is the discipline.
- Shipping on the overall rate while a family (Lesson 27) still fails. The gates here are necessary; the family table is where sufficiency gets argued.
- Treating the capstone as a finish line rather than a baseline. The next fixture set, with accents, crosstalk, and mid-call topic changes this one lacks, is where the loop runs next.

## Recap checklist

- [ ] You can quote both rows of the gate table
- [ ] You know which two gates the as-built system fails
- [ ] You can state the hardening loop in order

## Resources

- The gates file: [29-capstone-spec/capstone/gates.json](../29-capstone-spec/capstone/gates.json)
- The full course map: [README.md](../README.md)
- Where the budget numbers came from: [RESEARCH.md](../RESEARCH.md)
