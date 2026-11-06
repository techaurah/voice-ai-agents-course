# Fixtures

The bundled data every lesson runs on. Nothing here is collected from real calls; the scenario (BrightSmile Dental, a fictional clinic carried over from Courses 1 and 2) and every caller are invented.

- `transcripts.json`: 24 reference utterances, each tagged with the channel (wideband or telephony), noise condition (SNR in dB, null for clean), and speaking style the deterministic STT stand-in in `vox/stt.py` should transcribe it under.
- `calls.json`: 12 scripted calls for the dialogue lessons and the capstone. Each carries the caller's answers as spoken text, the channel conditions, a consent answer, an optional trap (a card number offered on a recorded line), and the truth record the booking is graded against.
- `schedule.json`: the BrightSmile appointment book the dialogue manager books into.
- `policy.json`: the clinic's call policy: disclosure line, consent question, emergency keywords, repair limits, and the card rule. A teaching fixture, not legal advice.
- `rates.json`: cost parameters for Lessons 24 and 25 and the capstone. Teaching parameters inside the ranges third-party teardowns reported in October 2026 (see the root RESEARCH.md), not price quotes.

Change a fixture and the numbers in the lessons change with it. That is the point: every claim in the course traces to a run over these files.
