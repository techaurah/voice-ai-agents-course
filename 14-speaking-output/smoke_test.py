"""Smoke test for Lesson 14: spoken-form counts match the README."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "artifact", Path(__file__).parent / "spoken_forms.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def main():
    result = mod.evaluate()
    assert result["sentences"] == 15
    assert result["unspeakable_tokens_before"] == 45
    assert result["unspeakable_tokens_after"] == 0
    assert "nine o'clock" in result["example_after"]
    assert "fifty pounds" in result["example_after"]
    print("smoke ok")


if __name__ == "__main__":
    main()
