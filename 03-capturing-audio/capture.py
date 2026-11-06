"""Lesson 03 artifact: capturing audio with the standard library.

Renders one fixture utterance as synthetic samples, writes and reads
a real WAV file, and prices storage and framing at the two sample
rates that matter for voice agents: 16 kHz wideband and 8 kHz
telephony. Frame size is 20 ms, the packet size telephony stacks
standardised on.
"""
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from vox import audio  # noqa: E402


def evaluate():
    data = json.loads((ROOT / "fixtures" / "transcripts.json").read_text())
    utt = data["utterances"][2]  # a slow telephony utterance
    env = audio.envelope_for(utt["text"], utt["style"], seed=0)
    rate = 16000
    samples = audio.render(env, rate=rate, seed=0)
    with tempfile.TemporaryDirectory() as tmp:
        path = str(Path(tmp) / "capture.wav")
        audio.write_wav(path, samples, rate)
        back, back_rate = audio.read_wav(path)
    max_diff = max(abs(a - b) for a, b in zip(samples, back))
    frame_len = int(rate * 0.020)
    frame_levels = audio.frames(samples, rate)
    return {
        "utterance_samples": len(samples),
        "utterance_seconds": round(len(samples) / rate, 2),
        "wav_roundtrip_max_diff": max_diff,
        "frame_ms": 20,
        "samples_per_frame": frame_len,
        "frames_in_utterance": len(frame_levels),
        "bytes_per_minute_16k": 16000 * 2 * 60,
        "bytes_per_minute_8k": 8000 * 2 * 60,
        "storage_ratio_16k_over_8k": (16000 * 2 * 60) / (8000 * 2 * 60),
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2, sort_keys=True))
