"""Smoke test for Lesson 24: cost accounting matches the README."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "artifact", Path(__file__).parent / "cost.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def main():
    result = mod.evaluate()
    as_built = result["as_built"]
    hardened = result["hardened"]
    assert as_built["total_cost_usd"] == 0.761
    assert as_built["success"] == 6
    assert as_built["wasted_on_failed_calls_usd"] == 0.4774
    assert as_built["cost_per_successful_booking"] == 0.0548
    assert hardened["total_cost_usd"] == 0.6453
    assert hardened["success"] == 12
    assert hardened["cost_per_successful_booking"] == 0.0581
    assert hardened["per_minute_rate_usd"] == 0.111
    print("smoke ok")


if __name__ == "__main__":
    main()
