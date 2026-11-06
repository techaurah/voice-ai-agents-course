# Resources

Print these next to the lessons. Every claim in them traces to the course's fixtures or to a dated source in the root RESEARCH.md.

## The one-page decision card

- Endpointing first. Two thirds of simulated turn latency is the end-of-turn wait (Lesson 02: 64.5 percent of the ledger). No model upgrade outruns a silence threshold.
- Fixed thresholds fail slow speakers at every setting in the usual range (Lesson 06: 400 and 800 ms cut the same three utterances). Make the wait depend on what has been said and who is saying it.
- Confirm the payload, not the conversation. Phone numbers arrive exactly right 5 times in 12 unconfirmed (Lesson 09); read-back with digit-level correction makes it 12 of 12 (Lesson 12).
- Never commit state on a partial transcript. Committing at 60 percent of the words costs 0.4135 WER against the final's 0.0702 (Lesson 10). Prefetch reads from partials; never prefetch writes (Lesson 13).
- Escapes are not failures with worse PR. They are a separate currency: two of the four injected faults score 11 of 12 while committing the only unforgivable errors in the table (Lesson 20).
- Failed calls are the majority of a bad system's bill: 63 percent of the as-built spend went to calls that failed (Lesson 24).
- Capacity is burst shape, not volume. The same 490-call day is trivial spread evenly and loses 129 calls clustered, on one line (Lesson 25).

## Reading list (all checked 2026-11-06, see RESEARCH.md)

- LiveKit documentation: endpointing configuration (`min_delay` 0.5 s default, 0.3 s with the audio turn detector; `max_delay` 3.0 s, 2.5 s with the detector).
- Pipecat documentation: Smart Turn v3, an open-source turn-completion model (Whisper Tiny backbone, int8 ONNX around 8 MB, up to 8 seconds of audio, CPU inference under 100 ms per the docs).
- Stivers, T. et al. (2009). Universals and cultural variation in turn-taking in conversation. PNAS. The roughly 200 ms median human turn gap used in Lesson 19.
- twig.so, "Latency Budgets for Voice AI Agents: The 800ms Rule" (checked 2026-11-06). Reported per-stage p50 ranges, and the framing that gaps beyond about 800 ms feel awkward and beyond 1,500 ms feel broken.
- DeepLearning.AI short courses on production voice agents (2025): platform-bound and short by design; this course is the long, offline, framework-free counterpart (see RESEARCH.md for the gap analysis).
- Telephony references in RESEARCH.md: PSTN 8 kHz sampling, the 300 to 3,400 Hz band, G.711 companding, and 20 ms media frames.

## Glossary

- **Endpointing**: deciding that a caller's turn has ended. The largest single term in the latency ledger.
- **Cut-off**: an endpointing decision made while the caller was mid-sentence.
- **First audio**: the moment the agent's response becomes audible; the latency this course budgets.
- **Partial**: a streaming transcript hypothesis that may still revise itself.
- **Stand-in**: a deterministic local model of a speech component, labelled as such, whose stated rules produce measurable behaviour without a live service.
- **Escape**: a policy violation that leaves the system: a booking against declined consent, card digits stored, an emergency not escalated. Counted separately from task failures, always.
- **Repair**: one correction exchange: a re-ask, a read-back correction, a spelled letter. The currency confirmation is paid in.
- **Family**: a set of test calls probing one weakness; families may overlap.
