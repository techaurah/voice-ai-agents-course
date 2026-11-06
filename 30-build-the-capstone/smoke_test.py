"""Smoke test for Lesson 30: capstone summary matches the README."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "artifact", Path(__file__).parent / "capstone_pipeline.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def main():
    result = mod.evaluate()
    summary = result["summary"]
    assert summary["success"] == 12 and summary["of"] == 12
    assert summary["success_rate"] == 1.0
    assert summary["escapes"] == 0
    assert summary["p50_first_audio_ms"] == 742
    assert summary["p95_first_audio_ms"] == 891
    assert summary["mean_repairs"] == 0.58
    assert summary["cost_per_successful_booking"] == 0.0581
    assert result["per_call"]["call-05"]["outcome"] == "consent_refused"
    assert result["per_call"]["call-09"]["outcome"] == "escalated"
    assert result["per_call"]["call-06"]["repairs"] == 2
    print("smoke ok")


if __name__ == "__main__":
    main()
