# Contributing

Contributions are welcome: corrections, clearer explanations, new fixture calls, and translations (see `translations/README.md`).

The house rules, which pull requests are checked against:

- Every number in a lesson README, exercise, or solution must be reproducible by running that lesson's code on the bundled fixtures. Change a fixture or the `vox` package and you re-run every affected lesson and update every quoted number, including the visuals and the root README scorecard.
- The capstone gates in `29-capstone-spec/capstone/gates.json` do not move. If a change makes the capstone fail a gate, the change is wrong or the failure gets reported; the gate is never edited to fit.
- Honest negatives stay in print. A technique that measures worse keeps its result, in the lesson and in the scorecard.
- No em dashes in any file. No certificate promises. No sales calls to action inside lessons.
- Runnable code is Python standard library only: no API keys, no live model calls, no audio hardware, no new dependencies. Speech components are deterministic stand-ins and must be labelled as such.
- Latency figures inside lessons are computed by the lesson's own simulation code and labelled simulated. Real-world figures belong in RESEARCH.md with a source and a check date.
- Keep the validators green before submitting: `python3 tools/validate_course.py`, `python3 tools/check_links.py`, `python -m compileall .`, and every lesson's `smoke_test.py` run from its own folder.

For larger changes, open an issue first so the design discussion happens before the work.
