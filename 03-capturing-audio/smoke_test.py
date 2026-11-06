"""Smoke test for Lesson 03: capture numbers match the README."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "artifact", Path(__file__).parent / "capture.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def main():
    result = mod.evaluate()
    assert result["utterance_samples"] == 61152
    assert result["utterance_seconds"] == 3.82
    assert result["samples_per_frame"] == 320
    assert result["frames_in_utterance"] == 191
    assert result["bytes_per_minute_16k"] == 1920000
    assert result["bytes_per_minute_8k"] == 960000
    assert result["storage_ratio_16k_over_8k"] == 2.0
    assert result["wav_roundtrip_max_diff"] < 0.0001
    print("smoke ok")


if __name__ == "__main__":
    main()
