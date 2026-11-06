# Research: the field scan this course is built on

Checked 2026-11-06. Every external claim below names its source and the date it was checked. Numbers reported by sources are labelled as reported; they are never mixed with this course's own simulated measurements, which live in the lessons and are labelled simulated wherever they appear.

## What exists, and the gap

**Short platform courses.** DeepLearning.AI's "Building AI Voice Agents for Production" (published 2025-05-07, taught with LiveKit, ElevenLabs, and RealAvatar) is the best-known course-shaped offering: 7 lessons and 2 code examples, covering the pipeline, latency, and turn detection. It is platform-bound (LiveKit infrastructure, ElevenLabs voices, hosted keys) and short by design. DeepLearning.AI's "Building Live Voice Agents with Google's ADK" (published 2025-09-24) is similar: 9 lessons, Google ADK and Gemini throughout. Both teach one vendor's stack well; neither treats the voice problems themselves (endpointing errors, narrowband audio, spoken numbers, consent) as measurable subjects with fixtures and gates.

**Framework guides and playbooks.** Long-form builder guides (for example the LiveKit Agents or Pipecat walkthrough at ajayk.sh, checked against PyPI on 2026-10-31: LiveKit Agents 1.8.10, Pipecat 1.15.0) get a cascaded agent running and add turn detection and per-turn latency logging, but stop at "it works": no evaluation set, no failure taxonomy, no cost model, no consent design. Pipecat and LiveKit documentation is strong on knobs (see below) and silent on how to choose their values with data.

**The gap this course fills.** No offering found combines: a complete, free, offline course; framework-free, standard-library-only code; speech components as deterministic stand-ins driven by fixtures, so every claim is reproducible; latency treated as a simulated budget with distributions, not a single advertised number; voice-specific failure modes (narrowband confusions, homophones, spoken digits and names, slow speakers cut off by VAD) measured on bundled data; consent and disclosure engineered as pipeline gates; and a capstone graded against gates fixed before the build. That combination is this course.

## Architecture facts (sources checked 2026-11-06)

- Two architecture families dominate: the cascaded pipeline (VAD, STT, LLM, TTS, each swappable and inspectable) and native speech-to-speech models (OpenAI Realtime API, Gemini Live, Kyutai Moshi) that collapse the pipeline into one model. LiveKit's own pipeline guidance recommends the cascade as the production default because every stage produces text you can log, test, and audit (ajayk.sh guide, 2026; repoloot.com open-source stacks guide, 2026).
- LiveKit Agents is Apache-2.0 and bundles rooms, dispatch, SIP, a turn detector, and hosting; Pipecat is BSD-2-Clause and models the agent as a frame pipeline over a transport you supply (ajayk.sh, versions checked against PyPI 2026-10-31).
- Kyutai's Moshi (arXiv 2410.00037) is a full-duplex speech-to-speech model reporting a theoretical latency of 160 ms and about 200 ms in practice (Voice AI Engineering newsletter, hub.cissychen.com, checked 2026-11-06).

## Turn detection (sources checked 2026-11-06)

- Pipecat's Smart Turn v3 is an open-source turn-completion model: a Whisper Tiny backbone with a classifier head, distributed as an int8-quantised ONNX model of about 8 MB, analysing up to the most recent 8 seconds of the user's turn, supporting 23 languages, with CPU inference under 100 ms according to Pipecat's documentation (docs.pipecat.ai, updated 2026-10-19). Pipecat recommends running it with VAD `stop_secs` of 0.2 seconds, far below a naive silence threshold, with a silence fallback (`stop_secs` default 3.0 s in SmartTurnParams) when the model judges a turn incomplete.
- LiveKit Agents groups turn behaviour under `turn_handling`: `endpointing.min_delay` defaults to 0.5 s, or 0.3 s with the audio turn detector; `max_delay` defaults to 3.0 s, or 2.5 s with the detector (Evalgent latency comparison, verified against LiveKit docs, checked 2026-11-06).
- The design lesson both frameworks encode is the one Lesson 06 teaches with fixtures: silence duration alone is a poor completeness signal, and the field's answer is a second signal (semantic or acoustic completeness) beside VAD.

## Latency (sources checked 2026-11-06)

- Human turn-taking runs on a median gap of about 200 ms (Stivers et al., 2009, cross-linguistic turn-taking study); gaps beyond about 800 ms read as awkward and beyond 1,500 ms as broken (twig.so, "Latency Budgets for Voice AI Agents: The 800ms Rule", checked 2026-11-06).
- The same source's reported stage budget (p50) for the 800 ms total: end-of-turn detection 200 to 300 ms, final ASR 50 to 150 ms, LLM first token 200 to 400 ms, TTS first chunk 100 to 200 ms, network jitter 30 to 80 ms, with tool calls overlapped rather than sequential. This course's simulated budget (Lessons 02 and 18) is built to be compared against these reported ranges, and is labelled simulated everywhere: it is a teaching model of where time goes, not a measurement of any real platform.

## The telephone channel (sources checked 2026-11-06)

- PSTN audio is 8 kHz sampled, band-limited to roughly 300 to 3,400 Hz, and encoded with G.711 at 64 kbit/s (mu-law in North America and Japan, A-law in Europe, ITU-T G.711, first published 1972). Fricatives such as /s/ and /f/ carry distinguishing energy above that band and are simply absent (reson8.dev telephony transcription wiki, updated 2026-09-23; soniox.com Voice AI Wiki, checked 2026-11-06).
- Twilio Media Streams deliver 8 kHz mu-law audio as base64 messages over a WebSocket, in 20 ms frames (reson8.dev). Upsampling 8 kHz audio to 16 kHz adds no information; the missing band was never captured (soniox.com).
- Errors on telephony concentrate in spelled letters and digit strings, exactly the content booking and identity flows depend on (reson8.dev). Lesson 09 is built on this.

## Cost (sources checked 2026-11-06)

- Headline per-minute rates are platform fees, not totals. Third-party teardowns that read the vendors' own pricing pages in October 2026 put a US inbound minute at roughly $0.09 to $0.15 all-in on the common stacks: Vapi's advertised $0.05/min is hosting only, with STT, LLM, TTS, and telephony stacked on top (aliteq.com teardown, vendor pages read 2026-10-02; jahanzaib.ai breakdown, checked 2026-10-10). Deepgram Nova-3 streaming transcription lists at $0.0077 per minute at its regular rate (socialvik.com, updated 2026-10-25).
- This course does not quote these as its own numbers. Lesson 24 builds a component cost model whose rates are bundled teaching parameters in `fixtures/rates.json`, chosen inside the ranges these teardowns report, and every total there is computed by the lesson's code from those stated parameters.

## Safety, consent, and disclosure (sources checked 2026-11-06)

- Recording consent law varies by jurisdiction (one-party and two-party consent regimes in the US alone), and AI disclosure duties for voice bots are appearing in statute and platform policy. This course is not legal advice; it teaches the engineering pattern that survives every variant: disclose that the caller is speaking with an automated system, ask and record consent before recording or transcribing beyond the call, keep a machine-readable consent state in the dialogue, and refuse to proceed on the sensitive path without it (Lessons 21 and 22). The pattern is implemented as pipeline gates over the fixture policy, not as a paragraph in a prompt.
