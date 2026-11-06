# Lesson 04: The telephone channel

40 min · Intermediate · Prerequisites: Lesson 03

Most voice agents still meet most callers on the telephone network, and the telephone network is a 1970s engineering compromise that your recogniser has to live with: audio sampled at 8 kHz, band-limited to roughly 300 to 3,400 Hz, and companded with G.711 mu-law at 64 kbit/s. This lesson simulates that channel with `vox.audio.telephony_chain` (decimation to 8 kHz plus a hand-written mu-law round trip) and measures what survives it.

Three probes. A wideband utterance goes through the chain: 78,080 samples in, 39,040 out. A 1 kHz tone, comfortably inside the band, is measured with a Goertzel filter (a single-frequency power probe, since the standard library has no FFT and one frequency is all we need). A 6 kHz tone, outside the band, gets the same treatment, plus a check of where its energy went.

## Run it

```bash
python3 telephony.py
```

The mu-law quantisation itself is gentle: measured against the decimated original, it adds noise at a signal-to-noise ratio of 37.3 dB, audible on close listening but rarely the recogniser's problem. The band limit is the violent part. The 1 kHz tone keeps its power (0.04 in, 0.0384 out). The 6 kHz tone's power at 6 kHz collapses from 0.04 to 0.000126 after the chain, even after upsampling back to 16 kHz, while a ghost of it appears at 2 kHz (power 0.0058): the energy aliased down into the band, wearing a false frequency.

## What the code measures

Upsampling adds samples, not information. Once the band above 4 kHz is discarded at sampling, no downstream processing can know what was there, which is why "the call was recorded in HD" means nothing if any leg of it was a phone call, and why recogniser features that depend on high-frequency fricatives (the difference between "fifteen" and "fifty" lives exactly there) are structurally unreliable on telephony. The STT stand-in encodes this directly: its number-word swaps only fire on the telephony channel. Lesson 07 shows the cost in word error rate; Lesson 09 shows the defence.

The alias is the subtlest part. The 6 kHz energy does not vanish politely; it reappears at 2 kHz, inside the band the recogniser trusts. Aliased content is misinformation, not absence.

## Common failures

- Blaming the recogniser for errors the channel made inevitable. If a distinction is not in the band, no model recovers it; the fix is dialogue design (confirmation), not a bigger model.
- Upsampling telephony audio to 16 kHz and reporting the pipeline as wideband. The samples double; the information does not.
- Testing only on clean wideband recordings, then shipping to phone callers. Every later lesson therefore runs both channels through everything.

## Recap checklist

- [ ] You can state the telephone band and what mu-law does
- [ ] You know the measured mu-law quantisation SNR on the fixture
- [ ] You can explain aliasing and why upsampling cannot undo it

## Resources

- The channel's fingerprint on recognition errors: [Lesson 07](../07-the-stt-standin/README.md)
- Sourced telephony facts: [RESEARCH.md](../RESEARCH.md)
