"""A deterministic text-to-speech stand-in.

It renders each word as a short tone burst whose pitch is a stable
hash of the word, so a spoken reply has real duration, real samples,
and a WAV you can open, while making no claim to sound like speech.
What the course measures about TTS is timing: how long synthesis takes
before the first chunk can play, and how utterance duration grows with
text, and those come from the stated model below, not from the tones.

Synthesis timing model (simulated, stated so it can be disagreed
with): a fixed 70 ms session cost, plus 2.2 ms per character for a
full utterance rendered in one pass. Streaming synthesis pays the
session cost once and then renders sentence by sentence, so the first
audio is ready after the first sentence only.
"""

import hashlib

from . import audio

SESSION_MS = 70
PER_CHAR_MS = 2.2


def first_sentence(text):
    for end in (". ", "! ", "? "):
        idx = text.find(end)
        if idx != -1:
            return text[:idx + 1]
    return text


def render(text, rate=16000):
    """Render text to tone-burst samples; return (samples, meta)."""
    samples = []
    words = text.split()
    for word in words:
        digest = hashlib.sha256(word.lower().encode()).digest()
        freq = 280 + (digest[0] / 255.0) * 420
        ms = 90 + 26 * len(word.strip(".,!?"))
        samples.extend(audio.tone(freq, ms, rate, level=0.3))
        samples.extend(audio.tone(0, 55, rate, level=0.0))
    meta = {"words": len(words), "chars": len(text),
            "duration_ms": int(len(samples) / rate * 1000)}
    return samples, meta


def synth_full_ms(text):
    """Simulated milliseconds to synthesise a whole reply in one pass."""
    return int(SESSION_MS + PER_CHAR_MS * len(text))


def synth_first_chunk_ms(text):
    """Simulated milliseconds until the first audio can play when
    synthesis streams sentence by sentence."""
    return int(SESSION_MS + PER_CHAR_MS * len(first_sentence(text)))
