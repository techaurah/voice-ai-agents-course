# Lesson 00: Course setup and the synthetic lab

20 min · Beginner · Prerequisites: none, just Python 3.10 or newer

This course builds voice agents without touching a microphone, a telephony account, or an API key. Everything runs on synthetic audio and deterministic stand-ins that live in the `vox/` package at the repo root, driven by the fixtures in `fixtures/`. That is a deliberate design choice, not a shortcut: a stand-in whose behaviour is written down in code can be measured, argued with, and re-run by anyone, which is more than can be said for a demo against a live platform. This first lesson proves the lab works on your machine.

The scenario running through the course is BrightSmile Dental, a fictional clinic whose appointment line you will build, measure, break, and harden. The fixtures hold 24 reference utterances, 12 scripted calls, a 19-slot appointment book, the clinic policy, and a set of teaching rates for the cost lessons.

## Run it

```bash
python3 check_environment.py
```

It prints your Python version, renders a one-second 440 Hz tone to a real WAV file with the standard library `wave` module, reads it back, and counts the fixtures. On the reference machine (Python 3.12.3) it reports 16,000 samples read back at 16,000 Hz, 24 transcripts, 12 calls, 19 schedule slots, and the clinic name BrightSmile Dental.

## What the code measures

Nothing here is a benchmark. The checks exist to catch the three ways a fresh clone usually fails: a Python too old for the syntax the course uses, a broken import of the shared `vox` package, and a fixtures folder that did not survive the download. The WAV round trip matters for a subtler reason: later lessons generate audio with `wave` and `struct` and then measure it, so the write and read path has to be exact before anything built on it can be trusted.

## Common failures

- Running the script from the repo root instead of the lesson folder. The artifact finds the repo root itself, but your editor's working directory habits will bite in later lessons; get used to running from the lesson folder now.
- A `python3` older than 3.10. The course uses current standard library behaviour; upgrade rather than patching around it.
- Editing a fixture to see what happens and forgetting. Every number in this course is computed from the fixtures as shipped; change one and your numbers will quietly stop matching the lessons.

## Recap checklist

- [ ] `check_environment.py` runs and reports 24 transcripts and 12 calls
- [ ] You can name what the `vox` package and the `fixtures` folder are for
- [ ] You know the course scenario: the BrightSmile Dental appointment line

## Resources

- The fixture guide: [fixtures/README.md](../fixtures/README.md)
- The shared library guide: [vox/README.md](../vox/README.md)
- Why the course is built this way: [DESIGN.md](../DESIGN.md)
