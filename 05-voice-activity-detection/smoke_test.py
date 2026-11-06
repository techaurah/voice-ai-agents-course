"""Smoke test for Lesson 05: VAD scores match the README."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "artifact", Path(__file__).parent / "vad_lab.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def main():
    result = mod.evaluate()
    assert result["raw_threshold_frame_accuracy"] == 0.9648
    assert result["clean_frame_accuracy"] == 0.7663
    assert result["accuracy_by_style"]["slow"] == 0.9754
    assert result["segments_by_style"]["slow"] == {
        "one_segment": 0, "split": 3, "missed": 0}
    noisy = result["noisy_snr8"]
    assert noisy["threshold_-32db"]["false_speech_pct"] == 40.61
    assert noisy["threshold_-18db"]["false_speech_pct"] == 22.31
    assert noisy["threshold_-32db"]["missed_speech_pct"] == 0.0
    print("smoke ok")


if __name__ == "__main__":
    main()
