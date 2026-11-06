# vox: the shared machinery

Standard-library-only stand-ins for every stage of a voice pipeline. Each module is labelled for what it models and what it does not.

- `audio.py`: synthetic audio. Segment scripts derived from text, rendered to samples with the `wave` and `struct` modules; frame energies; downsampling; a from-scratch G.711 mu-law codec; the simulated telephone chain.
- `vad.py`: an energy VAD over frame levels, and endpointing policies (fixed silence threshold, plus an adaptive variant that waits longer after incomplete cue words) graded against the true segment script.
- `stt.py`: a deterministic confusion-model stand-in for speech-to-text: homophones, telephony number and letter confusions, unknown names, and noise-driven drops and garbles, all seeded by utterance and attempt. Plus the spoken-form parsers (digit words, days, times) the dialogue lessons use.
- `tts.py`: a deterministic TTS stand-in: tone-burst renderings with real durations, and the stated synthesis timing model (session cost plus per-character cost, sentence-streamed first chunk).
- `latency.py`: the simulated latency ledger: stage cost formulas, first-audio computation for sequential and streamed designs, percentiles. Simulated budgets for teaching, never measurements of real platforms.
- `dialogue.py`: the BrightSmile slot-filling dialogue manager and its grader. The manager hears only STT hypotheses; the grader, in a separate function, compares outcomes with the truth records.
- `metrics.py`: word error rate with a substitution/deletion/insertion breakdown, and small statistics helpers.

Lessons import from here so that a number measured in Lesson 05 means the same thing in Lesson 27.
