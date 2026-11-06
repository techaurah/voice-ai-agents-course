# Notes for agents and contributors working in this repo

- Every number in a lesson README, exercise, or solution must be reproducible by running that lesson's code on the bundled fixtures. If you change a fixture or the `vox` package, re-run every affected lesson and update every quoted number, including the root README scorecard, llms.txt, and the visuals.
- The capstone gates live in `29-capstone-spec/capstone/gates.json` and do not move. If a change makes the capstone fail a gate, report the failure; never edit the gate to fit.
- Honest negatives stay in print: fixed endpointing cutting off slow speakers (Lesson 06), early commitment to partials (Lesson 10), the rejected vocabulary post-processor (Lesson 26), the middle system passing 4 of 5 gates while failing the transaction (Lesson 31), and the capstone's cost per successful booking exceeding the as-built's (Lessons 24 and 30).
- No em dashes in any file. Write around them with commas, colons, or separate sentences.
- Runnable code is Python standard library only. No API keys, no live model calls, no audio hardware, no new dependencies. Speech components are deterministic stand-ins and must be labelled as such wherever they are introduced.
- Latency figures in lessons are simulated budgets computed by the lesson's own code on the fixtures, and must be labelled simulated. Real platform figures belong in RESEARCH.md with a source and check date, never blended into the course's own measurements.
- Keep the validators green: `python3 tools/validate_course.py`, `python3 tools/check_links.py`, `python -m compileall .`, and every lesson's `smoke_test.py` run from its own folder.
- Fixtures are shared by all lessons. Call truth records must always agree with the caller-intent parse of the answers and with the schedule's free slots; the validator enforces this.
- External claims need a source and a check date in RESEARCH.md. Platform behaviour claims in particular must be re-checked before being repeated.
