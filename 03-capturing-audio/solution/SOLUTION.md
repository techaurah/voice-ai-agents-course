# Solution, Lesson 03

At 24 kHz, 16-bit mono audio costs 24,000 × 2 × 60 = 2,880,000 bytes per minute. At a 10 ms frame size the lesson's utterance produces 382 frames instead of 191, exactly double.

Doubling the frame count doubles every per-frame loop's work: VAD decisions, level computations, and endpointing checks all run twice as often for the same audio, which is why frame size is a stack-wide agreement and not a per-component preference. And 24 kHz capture buys a telephone caller nothing at all: the call itself is band-limited to roughly 300 to 3,400 Hz (Lesson 04), so the extra samples record a wider band than the channel ever carried, at 1.5 times the storage of 16 kHz.
