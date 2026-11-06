# Course Design: Voice AI Agents

This document records the design as specified before the lessons were written, including the capstone gates policy. The measured outcomes live in the lessons and the root README's scorecard.

## Audience and promise

For builders who have shipped a text agent (or finished Agentic AI for Beginners) and are moving it to voice. The promise: voice treated as an engineering discipline with budgets, fixtures, and failure modes, not as a text chatbot with a microphone attached. Every design claim in the course is either measured by the lesson's own code on the bundled fixtures, or cited to a dated source in RESEARCH.md.

## Principles

1. **The pipeline is the syllabus.** A voice agent is capture, VAD, endpointing, STT, dialogue, TTS, and playback, and the hard problems live in the arrows: latency, turn-taking, interruption. The module order follows the signal.
2. **Deterministic stand-ins, labelled as such.** Speech is synthetic (tones, shaped noise, silence, generated with the standard library `wave` and `struct` modules). STT, TTS, and VAD are deterministic stand-ins driven by bundled transcript and call fixtures. Latency is a simulated budget, computed by formula from the fixture data and labelled simulated everywhere it is quoted. Nothing here calls a live model or touches audio hardware, which is exactly what makes every number reproducible.
3. **One scenario, every lesson.** The running scenario is BrightSmile Dental's appointment line (continuity with Courses 1 and 2): booking, rescheduling, and confirming appointments by phone. The capstone is that line, end to end.
4. **Failures are curriculum.** The fixture set deliberately contains the traps the field's literature names: a slow speaker whose mid-sentence pauses defeat aggressive VAD, telephony narrowband confusions (fifteen/fifty, five/nine), homophones, names that need spelling, background noise at controlled levels, a caller who declines recording consent, and a caller who tries to pay by card on a recorded line.
5. **Gates before code.** The capstone's gates were fixed in `29-capstone-spec/capstone/gates.json`, dated 2026-11-06, from the simulated latency budget and the baseline measurements of the earlier modules, before any capstone code existed. The as-built verdict and the hardening are both reported against those unchanged numbers.

## Structure

32 lessons in 10 modules:

- Module 0, Foundations (00-02): setup, what makes it voice, the latency ledger.
- Module 1, Audio in (03-06): capturing audio, the telephone channel, voice activity detection, endpointing.
- Module 2, Speech to text (07-10): the STT stand-in and WER, noise as a data problem, numbers and names, streaming partials.
- Module 3, Dialogue (11-14): the dialogue manager, confirmation and repair, tool calls mid-call, speaking output.
- Module 4, Speech out (15-17): the TTS stand-in, streaming synthesis, barge-in.
- Module 5, Real-time behaviour (18-20): the latency budget end to end, turn-taking dynamics, voice failure modes.
- Module 6, Safety and consent (21-23): consent and disclosure, sensitive data, escalation and handoff.
- Module 7, Cost and scale (24-25): cost per minute, concurrency and capacity.
- Module 8, Evaluation (26-28): evaluating transcripts, evaluating conversations, the voice failure taxonomy.
- Module 9, Capstone (29-31): spec and gates, build the BrightSmile line, evaluate and harden.

## Shared machinery

- `vox/` is the shared library: synthetic audio, VAD, the STT and TTS stand-ins, turn policies, the latency ledger, the dialogue manager, and metrics. Lessons import it so the numbers stay comparable across the course.
- `fixtures/` holds the transcript set (with channel and noise conditions), the BrightSmile schedule, the call set used by the dialogue lessons and the capstone, the clinic policy, and the cost rates used as teaching parameters.

## The honesty rules

- Simulated latency is never presented as a measurement of a real platform. The reported real-world ranges live in RESEARCH.md with sources.
- Honest negatives stay in print, including where a course technique loses: aggressive VAD against slow speakers, streaming partials against final accuracy, and whatever the capstone's as-built verdict turns out to be.
- No number appears in prose unless running the lesson's code on the fixtures produces it.
