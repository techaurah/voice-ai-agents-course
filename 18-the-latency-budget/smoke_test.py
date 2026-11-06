"""Smoke test for Lesson 18: design budgets match the README."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "artifact", Path(__file__).parent / "budget.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def main():
    result = mod.evaluate()
    assert result["sequential_fixed800"]["p50_ms"] == 1493
    assert result["sequential_fixed800"]["p95_ms"] == 1752
    assert result["sequential_fixed800"]["within_budget"] is False
    assert result["streamed_fixed800"]["p50_ms"] == 1251
    assert result["streamed_adaptive"]["p50_ms"] == 742
    assert result["streamed_adaptive"]["p95_ms"] == 891
    assert result["streamed_adaptive"]["within_budget"] is True
    assert result["streamed_adaptive_confirm"]["p50_ms"] == 742
    print("smoke ok")


if __name__ == "__main__":
    main()
