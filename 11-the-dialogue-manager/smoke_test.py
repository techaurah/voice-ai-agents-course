"""Smoke test for Lesson 11: the three calls match the README."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "artifact", Path(__file__).parent / "dialogue_lab.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def main():
    result = mod.evaluate()
    assert result["call-01"]["success"] is False
    assert result["call-01"]["booked"]["phone"] == "07960155240"
    assert result["call-01"]["agent_turns"] == 6
    assert result["call-07"]["success"] is True
    assert result["call-12"]["success"] is True
    assert result["call-12"]["duration_s"] == 23.78
    print("smoke ok")


if __name__ == "__main__":
    main()
