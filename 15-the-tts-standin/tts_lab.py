"""Lesson 15 artifact: the TTS stand-in's timing, measured.

For every line the booking agent can say, reports the character
count, the stand-in's rendered duration, and the simulated synthesis
time for a full one-pass render. The ratio the lesson cares about:
synthesis time grows with characters, utterance duration grows with
words, and the two curves decide which replies are cheap to say.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from vox import metrics, tts  # noqa: E402
from vox.dialogue import AGENT_LINES  # noqa: E402


def evaluate():
    rows = {}
    ratios = []
    for key, line in AGENT_LINES.items():
        _samples, meta = tts.render(line)
        synth = tts.synth_full_ms(line)
        ratios.append(round(synth / meta["duration_ms"], 3))
        rows[key] = {
            "chars": meta["chars"],
            "words": meta["words"],
            "duration_ms": meta["duration_ms"],
            "synth_full_ms": synth,
        }
    return {
        "lines": rows,
        "mean_synth_to_duration_ratio": round(metrics.mean(ratios), 3),
        "greeting_chars": rows["greeting"]["chars"],
        "greeting_synth_full_ms": rows["greeting"]["synth_full_ms"],
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2, sort_keys=True))
