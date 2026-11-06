"""Smoke test for Lesson 25: capacity results match the README."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "artifact", Path(__file__).parent / "capacity.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def main():
    result = mod.evaluate()
    assert result["calls_in_day"] == 490
    assert result["patience_s"] == 300
    one, two, four = result["results"]
    assert one["served"] == 361 and one["abandoned"] == 129
    assert one["mean_wait_s"] == 155.7
    assert two["served"] == 460 and two["abandoned"] == 30
    assert four["served"] == 490 and four["abandoned"] == 0
    assert four["mean_wait_s"] == 38.7
    print("smoke ok")


if __name__ == "__main__":
    main()
