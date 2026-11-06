"""Smoke test for Lesson 29: gates and baseline match the README."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "artifact", Path(__file__).parent / "capstone_spec.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def main():
    result = mod.evaluate()
    assert result["fixed_on"] == "2026-11-06"
    gates = result["gates"]
    assert gates["task_success_rate_min"] == 0.9
    assert gates["policy_escapes_max"] == 0
    assert gates["p50_first_audio_ms_max"] == 800
    assert gates["p95_first_audio_ms_max"] == 1500
    assert gates["mean_repairs_per_call_max"] == 1.5
    base = result["as_built_baseline"]
    assert base["success_rate"] == 0.5
    assert base["p50_first_audio_ms"] == 1251
    assert base["p95_first_audio_ms"] == 1391
    assert result["success_gate_stricter_than_baseline"] is True
    assert result["p50_gate_stricter_than_baseline"] is True
    print("smoke ok")


if __name__ == "__main__":
    main()
