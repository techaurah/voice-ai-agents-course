"""Smoke test for Lesson 26: fix verdict matches the README."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "artifact", Path(__file__).parent / "eval_transcripts.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def main():
    result = mod.evaluate()
    assert result["mean_wer_before"] == 0.0702
    assert result["mean_wer_after"] == 0.0744
    assert result["utterances_helped"] == 1
    assert result["utterances_hurt"] == 2
    assert result["utterances_unchanged"] == 21
    assert result["by_tag"]["plain"] == {"before": 0.0333, "after": 0.0667}
    print("smoke ok")


if __name__ == "__main__":
    main()
