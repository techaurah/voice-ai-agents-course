"""Smoke test for Lesson 10: partial-stream scores match the README."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "artifact", Path(__file__).parent / "partials.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def main():
    result = mod.evaluate()
    assert result["utterances"] == 24
    assert result["mean_batch_final_wer"] == 0.0702
    assert result["mean_final_wer"] == 0.0913
    assert result["mean_early_commit_wer"] == 0.4135
    assert result["token_changes_per_word"] == 1.054
    print("smoke ok")


if __name__ == "__main__":
    main()
