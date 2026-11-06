"""Smoke test for Lesson 17: barge-in counts match the README."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "artifact", Path(__file__).parent / "barge_in.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def main():
    result = mod.evaluate()
    assert result["total_words"] == 17
    assert result["line_duration_ms"] == 4337
    assert result["interrupt_25pct"]["heard_words"] == 4
    assert result["interrupt_25pct"]["phantom_words"] == 13
    assert result["interrupt_25pct"]["facts_never_heard"] == [
        "tuesday", "ten"]
    assert result["interrupt_50pct"]["heard_words"] == 8
    assert result["interrupt_75pct"]["phantom_words"] == 5
    print("smoke ok")


if __name__ == "__main__":
    main()
