"""Smoke test for Lesson 02: ledger totals match the README."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "artifact", Path(__file__).parent / "ledger.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def main():
    result = mod.evaluate()
    assert result["turns"] == 24
    assert result["grand_total_ms"] == 29765
    assert result["mean_per_turn_ms"] == 1240.2
    assert result["stage_totals_ms"]["endpoint"] == 19200
    assert result["stage_shares_pct"]["endpoint"] == 64.5
    assert result["stage_totals_ms"]["llm_first_token"] == 5041
    print("smoke ok")


if __name__ == "__main__":
    main()
