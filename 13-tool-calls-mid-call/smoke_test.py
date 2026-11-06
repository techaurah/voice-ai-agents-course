"""Smoke test for Lesson 13: tool-call prices match the README."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "artifact", Path(__file__).parent / "tool_calls.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def main():
    result = mod.evaluate()
    assert result["calls"] == 12
    assert result["tool_ms"] == 140
    assert result["mean_first_audio_series_streamed"] == 834.8
    assert result["mean_first_audio_series_sequential"] == 1051.0
    assert result["mean_first_audio_prefetched"] == 694.8
    assert result["prefetch_saving_ms"] == 140.0
    print("smoke ok")


if __name__ == "__main__":
    main()
