"""Smoke test for Lesson 01: the dissected turn matches the README."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "artifact", Path(__file__).parent / "anatomy.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def main():
    result = mod.evaluate()
    assert result["words"] == 10
    assert result["speech_ms"] == 3148
    assert result["pause_ms"] == 1732
    assert result["first_audio_sequential_ms"] == 1508
    assert result["first_audio_streamed_ms"] == 1198
    assert result["saving_ms"] == 310
    print("smoke ok")


if __name__ == "__main__":
    main()
