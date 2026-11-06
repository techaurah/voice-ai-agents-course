"""Smoke test for Lesson 09: payload measurements match the README."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "artifact", Path(__file__).parent / "numbers_names.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def main():
    result = mod.evaluate()
    assert result["digit_utterances_exact"] == {
        "telephony": {"exact": 7, "of": 7}}
    assert result["phone_numbers"] == {
        "of": 12, "raw_exact": 5, "after_digit_correction": 12}
    assert result["spelled_names"] == {
        "of": 2, "raw_exact": 1, "after_letter_correction": 2}
    print("smoke ok")


if __name__ == "__main__":
    main()
