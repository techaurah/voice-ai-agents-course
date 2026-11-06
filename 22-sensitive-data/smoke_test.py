"""Smoke test for Lesson 22: redaction counts match the README."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "artifact", Path(__file__).parent / "redaction.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def main():
    result = mod.evaluate()
    assert result["texts_stored"] == 49
    assert result["digit_strings_before"] == 13
    assert result["digits_before"] == 148
    assert result["card_digits_before"] == 16
    assert result["digit_strings_after_redaction"] == 0
    assert result["digits_after_redaction"] == 0
    print("smoke ok")


if __name__ == "__main__":
    main()
