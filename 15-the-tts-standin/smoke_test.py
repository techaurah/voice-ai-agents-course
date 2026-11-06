"""Smoke test for Lesson 15: TTS timing matches the README."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "artifact", Path(__file__).parent / "tts_lab.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def main():
    result = mod.evaluate()
    assert result["greeting_chars"] == 178
    assert result["greeting_synth_full_ms"] == 461
    assert result["lines"]["greeting"]["duration_ms"] == 7618
    assert result["lines"]["ask_name"]["synth_full_ms"] == 116
    assert result["mean_synth_to_duration_ratio"] == 0.076
    assert len(result["lines"]) == 13
    print("smoke ok")


if __name__ == "__main__":
    main()
