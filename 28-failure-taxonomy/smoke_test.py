"""Smoke test for Lesson 28: taxonomy counts match the README."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "artifact", Path(__file__).parent / "taxonomy.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def main():
    result = mod.evaluate()
    assert result["suite_runs"] == 60
    assert result["total_failures"] == 16
    assert result["failures_by_category"] == {
        "consent_escape": 1, "payment_escape": 1,
        "repair_exhaustion": 4, "transcription_digits": 10}
    assert result["example_call_per_category"]["transcription_digits"] \
        == "call-01"
    print("smoke ok")


if __name__ == "__main__":
    main()
