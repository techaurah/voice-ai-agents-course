"""Lesson 01 artifact: dissect one spoken turn.

Takes the first fixture utterance, measures its speech and pause
structure, then prices the turn through the simulated latency ledger
two ways: a sequential design (every stage waits for the previous
one) and a streamed design (stages overlap). All numbers are computed
here, on the fixture, by the shared stand-in library.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from vox import audio, latency, tts  # noqa: E402
from vox.dialogue import AGENT_LINES  # noqa: E402


def evaluate():
    data = json.loads((ROOT / "fixtures" / "transcripts.json").read_text())
    utt = data["utterances"][0]
    text = utt["text"]
    env = audio.envelope_for(text, utt["style"], seed=0)
    speech_ms = sum(ms for kind, ms, _l, _w in env if kind == "speech")
    pause_ms = sum(ms for kind, ms, _l, _w in env if kind == "pause")
    words = len(text.split())
    reply = AGENT_LINES["confirm"]
    reply_words = len(reply.split())
    prompt_words = 96  # a mid-call prompt, slot state included
    jitter = latency.JITTER_MS[utt["channel"]]
    sequential = {
        "endpoint_silence": 800,
        "stt_final_batch": latency.stt_final_ms(words, streaming=False),
        "llm_full_reply": latency.llm_full_ms(prompt_words, reply_words),
        "tts_full_reply": tts.synth_full_ms(reply),
        "network_jitter": jitter,
    }
    streamed = {
        "endpoint_silence": 800,
        "stt_final_streaming": latency.stt_final_ms(words, streaming=True),
        "llm_first_token": latency.llm_first_token_ms(prompt_words),
        "tts_first_chunk": tts.synth_first_chunk_ms(reply),
        "network_jitter": jitter,
    }
    seq_total = sum(sequential.values())
    str_total = sum(streamed.values())
    return {
        "utterance": text,
        "words": words,
        "speech_ms": speech_ms,
        "pause_ms": pause_ms,
        "stages_sequential": sequential,
        "stages_streamed": streamed,
        "first_audio_sequential_ms": seq_total,
        "first_audio_streamed_ms": str_total,
        "saving_ms": seq_total - str_total,
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2, sort_keys=True))
