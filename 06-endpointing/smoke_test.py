"""Smoke test for Lesson 06: endpointing results match the README."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "artifact", Path(__file__).parent / "endpointing.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def main():
    result = mod.evaluate()
    assert result["fixed_400"]["cut_offs"] == 3
    assert result["fixed_400"]["slow_cut_offs"] == 3
    assert result["fixed_800"]["cut_offs"] == 3
    assert result["adaptive_450"]["cut_offs"] == 1
    assert result["adaptive_450"]["cut_off_ids"] == ["utt-12"]
    assert result["adaptive_450"]["mean_wait_completed_ms"] == 300.0
    print("smoke ok")


if __name__ == "__main__":
    main()
