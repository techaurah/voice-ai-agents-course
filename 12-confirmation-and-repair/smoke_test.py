"""Smoke test for Lesson 12: confirmation results match the README."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "artifact", Path(__file__).parent / "repair.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def main():
    result = mod.evaluate()
    off = result["adaptive_no_confirm"]
    on = result["adaptive_with_confirm"]
    assert off["success"] == 6 and off["of"] == 12
    assert off["failed_ids"] == ["call-01", "call-02", "call-04",
                                 "call-06", "call-08", "call-11"]
    assert off["mean_repairs"] == 0.0
    assert on["success"] == 12
    assert on["mean_repairs"] == 0.58
    assert on["mean_agent_turns"] == off["mean_agent_turns"] == 5.5
    print("smoke ok")


if __name__ == "__main__":
    main()
