# Lesson 03: Capturing audio

40 min · Beginner · Prerequisites: Lesson 00

Every voice pipeline starts with a mundane decision: how many samples per second, in what frame size, stored how. Get it wrong and everything downstream inherits the damage, because audio thrown away at capture cannot be recovered by a better recogniser later. This lesson works with the raw material directly: synthetic samples rendered from a fixture utterance, written to a real WAV file with the standard library, read back, framed, and priced for storage at the two rates that matter, 16 kHz wideband and 8 kHz telephony.

The utterance used is a slow telephony one. Rendered at 16 kHz it is 61,152 samples, 3.82 seconds of audio. Split into the 20 ms frames that telephony stacks standardised on, that is 191 frames of 320 samples each. The 20 ms frame is not an arbitrary unit: it is the packet rhythm of the telephone network, and VAD, endpointing, and streaming recognition all think in it.

## Run it

```bash
python3 capture.py
```

The WAV round trip comes back with a maximum sample difference of about 0.0000305, which is one least-significant bit of the 16-bit encoding, in other words exact for practical purposes. Storage: a minute of 16-bit mono audio costs 1,920,000 bytes at 16 kHz and 960,000 bytes at 8 kHz, a ratio of exactly 2.0. A day of calls at clinic scale is small; a platform's archive is not, and Lesson 24 returns to what retention really costs.

## What the code measures

Two things worth internalising. First, the sample rate decision is an information decision before it is a cost decision: 8 kHz sampling cannot represent anything above 4 kHz, and Lesson 04 shows what that does to the fricatives that separate "fifteen" from "fifty". Second, framing is where audio becomes data a program can reason about: once the stream is frames with energy levels, VAD (Lesson 05) and endpointing (Lesson 06) are just policies over a list of numbers.

The synthetic samples here are shaped noise, not speech, and the course never pretends otherwise. What they have is the structure the measurements need: word-sized bursts, pauses, and levels, all reproducible from a seed.

## Common failures

- Recording stereo or 32-bit float "for quality" and quadrupling storage and bandwidth for a channel that will be 8 kHz mono by the time it reaches a phone caller anyway.
- Choosing a frame size the rest of the stack does not use, then paying a resampling or reframing tax on every packet.
- Assuming capture is free because a single call is small. Multiply by concurrency (Lesson 25) and retention before deciding.

## Recap checklist

- [ ] You can compute bytes per minute for any sample rate and bit depth
- [ ] You know the frame size the rest of the course assumes, and why
- [ ] You have written and read a real WAV file with the standard library

## Resources

- What the telephone network does to this audio: [Lesson 04](../04-the-telephone-channel/README.md)
- Frames to decisions: [Lesson 05](../05-voice-activity-detection/README.md)
