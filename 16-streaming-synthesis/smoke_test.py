"""Smoke test for Lesson 16: streaming prices match the README."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "artifact", Path(__file__).parent / "streaming_tts.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def main():
    result = mod.evaluate()
    assert result["lines"] == 13
    assert result["mean_synth_full_ms"] == 203.3
    assert result["mean_synth_first_chunk_ms"] == 144.5
    assert result["mean_saving_ms"] == 58.8
    assert result["greeting_first_sentence_chars"] == 26
    assert result["greeting_full_chars"] == 178
    assert result["greeting_turn_first_audio_streamed_ms"] == 707
    assert result["greeting_turn_first_audio_whole_reply_ms"] == 1041
    print("smoke ok")


if __name__ == "__main__":
    main()
