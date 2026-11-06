"""Lesson 04 artifact: what the telephone channel does to audio.

Runs a wideband rendering and test tones through the simulated
telephone channel (8 kHz sampling plus G.711 mu-law, vox.audio) and
measures three things: how much quantisation noise mu-law adds, how
much energy a 6 kHz tone loses when the band above 4 kHz is cut, and
why upsampling the result cannot bring that energy back.
"""
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from vox import audio  # noqa: E402


def goertzel(samples, rate, freq):
    """Power at one frequency, computed directly (no FFT in stdlib
    teaching code needs more than this)."""
    n = len(samples)
    k = 2 * math.pi * freq / rate
    coeff = 2 * math.cos(k)
    s1 = s2 = 0.0
    for x in samples:
        s0 = x + coeff * s1 - s2
        s2, s1 = s1, s0
    return (s1 * s1 + s2 * s2 - coeff * s1 * s2) / (n * n)


def mean_square(samples):
    return sum(s * s for s in samples) / max(1, len(samples))


def evaluate():
    data = json.loads((ROOT / "fixtures" / "transcripts.json").read_text())
    utt = data["utterances"][0]
    env = audio.envelope_for(utt["text"], utt["style"], seed=0)
    wide = audio.render(env, rate=16000, seed=0)
    chained = audio.telephony_chain(wide, 16000)
    reference_8k = audio.downsample(wide, 16000, 8000)
    err = [a - b for a, b in zip(chained, reference_8k)]
    snr_db = 10 * math.log10(mean_square(reference_8k) /
                             max(mean_square(err), 1e-12))
    results = {
        "wideband_samples": len(wide),
        "telephony_samples": len(chained),
        "mulaw_quantisation_snr_db": round(snr_db, 1),
    }
    tone1 = audio.tone(1000, 500, rate=16000)
    out1 = audio.telephony_chain(tone1, 16000)
    results["power_1000hz_wideband"] = round(goertzel(tone1, 16000, 1000), 4)
    results["power_1000hz_telephony"] = round(goertzel(out1, 8000, 1000), 4)
    tone6 = audio.tone(6000, 500, rate=16000)
    out6 = audio.telephony_chain(tone6, 16000)
    up = audio.upsample(out6, 8000, 16000)
    results["power_6000hz_wideband"] = round(goertzel(tone6, 16000, 6000), 4)
    results["power_6000hz_after_chain_and_upsample"] = round(
        goertzel(up, 16000, 6000), 6)
    results["power_2000hz_alias_in_telephony"] = round(
        goertzel(out6, 8000, 2000), 4)
    results["upsampled_length"] = len(up)
    return results


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2, sort_keys=True))
