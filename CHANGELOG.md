# Changelog

## v1.0.0, 2026-11-06

First complete release.

- 32 lessons in 10 modules: foundations, audio capture and the telephone channel, VAD and endpointing, a deterministic STT stand-in, noise and payload evaluation, the slot-filling dialogue manager, confirmation and repair, tool calls, spoken output normalisation, a TTS stand-in, streaming synthesis, barge-in, latency budgets, turn-taking, failure modes, consent, sensitive data, escalation, cost per minute, concurrency, transcript and conversation evaluation, failure taxonomy, and the capstone.
- Shared `vox` package: synthetic audio (wave and struct), an energy VAD with fixed and adaptive endpointing policies, a confusion-model STT stand-in, a tone-burst TTS stand-in, a simulated latency ledger, metrics, and the BrightSmile dialogue manager with an independent grader.
- Fixtures: 24 reference utterances, 12 scripted calls, a 19-slot appointment book, clinic policy, and teaching rates. Nothing collected from real calls.
- Capstone: gates fixed in writing on 2026-11-06 before the capstone was assembled. As-built system passes 3 of 5 gates (success 0.5, p50 first audio 1,251 ms); the hardened capstone passes 5 of 5 (success 1.0, 0 escapes, p50 742 ms, p95 891 ms, mean repairs 0.58).
- Honest negatives kept in print, among them: fixed endpointing at 400 and 800 ms cuts off all three slow fixture utterances; early commitment to streaming partials scores 0.4135 WER against the final's 0.0702; a domain-vocabulary post-processor makes WER worse overall (0.0702 to 0.0744) and is rejected by its own evaluation; the hardened system's cost per successful booking is higher than the as-built's even though its total spend is lower.
