# Lesson 29: Capstone spec

40 min · Intermediate · Prerequisites: Lessons 18 and 27

The capstone is the BrightSmile booking line, built as one system and graded as one system. This lesson is its spec, and the order of operations is the content: the gates were written down on 2026-11-06, in `capstone/gates.json` inside this lesson's folder, before the capstone code was assembled. A gate written after the results are known is a description, not a standard.

The five gates. Task success rate at least 0.9 on the twelve bundled calls. Policy escapes: zero, not a rate, zero. Simulated latency to first audio: p50 at most 800 ms and p95 at most 1,500 ms, the sourced budget from RESEARCH.md that Lesson 18 used. Mean repairs per call at most 1.5, so a system cannot pass by interrogating callers endlessly.

## Run it

```bash
python3 capstone_spec.py
```

The artifact loads the gates and recomputes the as-built baseline they were set against: success rate 0.5, p50 1,251 ms, p95 1,391 ms, escapes 0, mean repairs 0.5. It then verifies the property that makes the gates meaningful: on the two binding dimensions they are stricter than the baseline (0.9 required against 0.5 achieved; 800 ms allowed against 1,251 ms achieved). Both checks come back true.

## What the code measures

Read the gates as a contract between the course's two halves. The latency gates import the budget work (Lessons 02, 18) wholesale; nothing about them is new, which is the point: a capstone should consolidate measured standards, not invent fresh ones at the end. The success gate sits at 0.9 rather than 1.0 because a bar the fixture set's hardest call might legitimately miss is more informative than a bar tuned to be passable; the repairs gate exists because the success gate alone can be gamed by a system that asks and re-asks until callers surrender the right answer.

The baseline is part of the spec, not an embarrassment appended to it. Any future change to the system is judged against both: it must clear the gates, and it should not silently move the baseline comparisons (if the as-built numbers change, a fixture or a stand-in changed, and that is a course-level event, reviewed as such).

Lesson 30 assembles the system. Lesson 31 grades it. The gates do not move in between.

## Common failures

- Gates written after building, fitted to the results like a suit. The file's date and this lesson's baseline check exist to make that visible.
- A single success gate with no repairs or latency companions, which selects for systems that are slow, stubborn, and technically successful.
- An escapes target expressed as a percentage. On twelve calls, one escape is 8 percent and a catastrophe; zero is the only honest number.

## Recap checklist

- [ ] You can quote all five gates from memory
- [ ] You know the as-built baseline on every gated dimension
- [ ] You can explain why the gates predate the capstone code

## Resources

- The system the gates judge: [Lesson 30](../30-build-the-capstone/README.md)
- The grading run: [Lesson 31](../31-evaluate-and-harden/README.md)
- The gates file itself: [capstone/gates.json](capstone/gates.json)
