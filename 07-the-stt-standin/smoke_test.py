"""Smoke test for Lesson 07: STT scores match the README."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "artifact", Path(__file__).parent / "stt_lab.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def main():
    result = mod.evaluate()
    assert result["utterances"] == 24
    assert result["mean_wer"] == 0.0702
    assert result["mean_wer_clean"] == 0.0585
    assert result["mean_wer_noisy"] == 0.0867
    assert result["edit_counts"] == {
        "substitutions": 11, "deletions": 5, "insertions": 0}
    assert result["worst_three"][0] == {"id": "utt-13", "wer": 0.3333}
    print("smoke ok")


if __name__ == "__main__":
    main()
