"""Lesson 00 artifact: verify the course environment end to end.

Checks the Python version, renders a synthetic tone to a real WAV
file with the standard library and reads it back, imports the shared
stand-in library, and counts the bundled fixtures. Nothing here needs
a network, an API key, or audio hardware.
"""
import json
import sys
import tempfile
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from vox import audio  # noqa: E402


def load(name):
    return json.loads((ROOT / "fixtures" / name).read_text())


def evaluate():
    transcripts = load("transcripts.json")["utterances"]
    calls = load("calls.json")["calls"]
    schedule = load("schedule.json")
    slots = len(schedule["slots"])
    samples = audio.tone(440, 1000, rate=16000)
    with tempfile.TemporaryDirectory() as tmp:
        path = str(Path(tmp) / "tone.wav")
        audio.write_wav(path, samples, 16000)
        with wave.open(path) as handle:
            frames = handle.getnframes()
            rate = handle.getframerate()
    return {
        "python": sys.version.split()[0],
        "python_ok": sys.version_info >= (3, 10),
        "wav_roundtrip_samples": frames,
        "wav_rate": rate,
        "transcripts": len(transcripts),
        "calls": len(calls),
        "schedule_slots": slots,
        "clinic": load("policy.json")["clinic"],
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2, sort_keys=True))
