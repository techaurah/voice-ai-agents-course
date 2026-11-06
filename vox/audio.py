"""Synthetic audio, standard library only.

Nothing in this course touches a microphone. Speech is rendered as
deterministic shaped noise bursts whose envelope follows a word script,
silence is a low hiss, and tones mark events. That is enough structure
to measure the things the course studies: frames, energy, VAD,
endpointing, sample rates, and the telephone channel, with full
reproducibility and no audio hardware.

A segment is a (kind, ms, level) triple with kind "speech" or "pause".
envelope_for() derives a segment script from text, so the audio lessons
and the turn-taking lessons are looking at the same utterances.
"""

import math
import random
import struct
import wave

RATES = {"wideband": 16000, "telephony": 8000}

WORD_MS = (230, 370)          # per-word speech burst range
PAUSE_MS = {"normal": (120, 260), "rushed": (60, 140), "slow": (300, 520)}
SLOW_THINK_MS = (680, 940)    # mid-utterance thinking pauses, slow style
FILLERS = {"um", "uh", "er"}


def envelope_for(text, style="normal", seed=0):
    """Derive a segment script for an utterance.

    Returns a list of (kind, ms, level, word) tuples. Speech segments
    carry the word they render; pauses carry None. Slow speakers get a
    long thinking pause before roughly one word in three after the
    second word, which is the pattern that defeats aggressive VAD in
    Lesson 05.
    """
    rng = random.Random(f"env:{seed}:{text}")
    words = text.split()
    segments = []
    for i, word in enumerate(words):
        if i > 0:
            lo, hi = PAUSE_MS[style]
            pause = rng.randint(lo, hi)
            if style == "slow" and i >= 2 and rng.random() < 0.34:
                pause = rng.randint(*SLOW_THINK_MS)
            segments.append(("pause", pause, 0.02, None))
        ms = rng.randint(*WORD_MS)
        level = 0.45 + rng.random() * 0.25
        segments.append(("speech", ms, level, word))
    return segments


def render(segments, rate=16000, seed=0):
    """Render a segment script to float samples in [-1, 1].

    Speech segments are noise bursts amplitude-modulated in 30 ms
    blocks (a crude syllable rhythm); pauses are hiss at their level.
    """
    rng = random.Random(f"render:{seed}")
    samples = []
    for kind, ms, level, _word in segments:
        n = int(rate * ms / 1000)
        if kind == "pause":
            samples.extend(rng.uniform(-level, level) for _ in range(n))
        else:
            block = max(1, int(rate * 0.03))
            for start in range(0, n, block):
                amp = level * (0.55 + rng.random() * 0.45)
                for _ in range(start, min(start + block, n)):
                    samples.append(rng.uniform(-amp, amp))
    return samples


def tone(freq_hz, ms, rate=16000, level=0.4):
    n = int(rate * ms / 1000)
    return [level * math.sin(2 * math.pi * freq_hz * i / rate)
            for i in range(n)]


def add_noise(samples, snr_db, seed=0):
    """Mix white noise into samples at a target SNR (dB)."""
    if snr_db is None:
        return list(samples)
    rng = random.Random(f"noise:{seed}")
    power = sum(s * s for s in samples) / max(1, len(samples))
    signal_rms = math.sqrt(power) if power else 0.0
    noise_rms = signal_rms / (10 ** (snr_db / 20.0)) if signal_rms else 0.0
    return [s + rng.uniform(-noise_rms, noise_rms) * 1.73
            for s in samples]


def frames(samples, rate=16000, frame_ms=20):
    """Split samples into frames; return each frame's RMS level."""
    size = int(rate * frame_ms / 1000)
    out = []
    for start in range(0, len(samples) - size + 1, size):
        chunk = samples[start:start + size]
        out.append(math.sqrt(sum(s * s for s in chunk) / size))
    return out


def to_db(rms, floor=1e-6):
    return 20 * math.log10(max(rms, floor))


def write_wav(path, samples, rate=16000):
    frames_pcm = b"".join(
        struct.pack("<h", int(max(-1.0, min(1.0, s)) * 32767))
        for s in samples)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(frames_pcm)


def read_wav(path):
    with wave.open(str(path), "rb") as w:
        rate = w.getframerate()
        raw = w.readframes(w.getnframes())
    values = struct.unpack(f"<{len(raw) // 2}h", raw)
    return [v / 32767.0 for v in values], rate


def downsample(samples, rate, target_rate):
    """Decimate to a lower rate (no anti-alias filter beyond averaging)."""
    if target_rate >= rate:
        return list(samples)
    step = rate // target_rate
    out = []
    for i in range(0, len(samples) - step + 1, step):
        out.append(sum(samples[i:i + step]) / step)
    return out


def upsample(samples, rate, target_rate):
    """Linear-interpolate to a higher rate. Adds samples, not information."""
    if target_rate <= rate:
        return list(samples)
    step = target_rate // rate
    out = []
    for i, s in enumerate(samples):
        nxt = samples[i + 1] if i + 1 < len(samples) else s
        for k in range(step):
            out.append(s + (nxt - s) * k / step)
    return out


# G.711 mu-law, implemented from the standard definition so the
# course needs no audioop (removed from the standard library).
_BIAS = 0x84
_CLIP = 32635


def mulaw_encode_sample(x):
    sample = int(max(-1.0, min(1.0, x)) * 32767)
    sign = 0x80 if sample < 0 else 0
    if sample < 0:
        sample = -sample
    sample = min(sample, _CLIP) + _BIAS
    exponent = 7
    for mask in (0x4000, 0x2000, 0x1000, 0x0800, 0x0400, 0x0200,
                 0x0100, 0x0080):
        if sample & mask:
            break
        exponent -= 1
    mantissa = (sample >> (exponent + 3)) & 0x0F
    return (~(sign | (exponent << 4) | mantissa)) & 0xFF


def mulaw_decode_sample(code):
    code = (~code) & 0xFF
    sign = code & 0x80
    exponent = (code >> 4) & 0x07
    mantissa = code & 0x0F
    sample = (((mantissa << 3) + _BIAS) << exponent) - _BIAS
    return (-sample if sign else sample) / 32768.0


def telephony_chain(samples, rate=16000):
    """Simulate the telephone channel: 8 kHz sampling plus mu-law.

    Returns the samples a recogniser on a phone call actually receives:
    decimated to 8000 samples per second and quantised by G.711 mu-law.
    """
    narrow = downsample(samples, rate, 8000)
    return [mulaw_decode_sample(mulaw_encode_sample(s)) for s in narrow]
