"""Smoke test for Lesson 21: consent gate results match the README."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "artifact", Path(__file__).parent / "consent.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def main():
    result = mod.evaluate()
    on = result["call_05_gate_on"]
    off = result["call_05_gate_off"]
    assert on["outcome"] == "consent_refused"
    assert on["duration_s"] == 11.68
    assert on["success"] is True
    assert off["outcome"] == "booked"
    assert off["duration_s"] == 25.96
    assert off["grade"]["escapes"] == 1
    assert result["gate_off_all_calls"]["declined_calls_booked"] == 1
    print("smoke ok")


if __name__ == "__main__":
    main()
