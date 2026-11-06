"""Lesson 16 artifact: streaming synthesis, priced per agent line.

For every line the booking agent can say, compares the simulated
synthesis time for a full one-pass render against streaming, where
only the first sentence must finish before audio starts. Then prices
the difference at the turn level for the longest line, the greeting,
using the shared latency model.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from vox import latency, metrics, tts  # noqa: E402
from vox.dialogue import AGENT_LINES  # noqa: E402


def evaluate():
    fulls, firsts = [], []
    for line in AGENT_LINES.values():
        fulls.append(tts.synth_full_ms(line))
        firsts.append(tts.synth_first_chunk_ms(line))
    greeting = AGENT_LINES["greeting"]
    turn_full = latency.first_audio_ms(
        300, 10, 96, greeting, "wideband", design="streamed")
    # first_audio_ms already prices the first chunk; rebuild the
    # whole-reply variant by swapping the TTS term.
    turn_whole_reply = turn_full - tts.synth_first_chunk_ms(greeting) \
        + tts.synth_full_ms(greeting)
    return {
        "lines": len(fulls),
        "mean_synth_full_ms": round(metrics.mean(fulls), 1),
        "mean_synth_first_chunk_ms": round(metrics.mean(firsts), 1),
        "mean_saving_ms": round(metrics.mean(fulls) -
                                metrics.mean(firsts), 1),
        "greeting_first_sentence_chars": len(tts.first_sentence(greeting)),
        "greeting_full_chars": len(greeting),
        "greeting_turn_first_audio_streamed_ms": turn_full,
        "greeting_turn_first_audio_whole_reply_ms": turn_whole_reply,
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2, sort_keys=True))
