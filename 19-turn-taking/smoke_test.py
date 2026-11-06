"""Smoke test for Lesson 19: turn-taking numbers match the README."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "artifact", Path(__file__).parent / "turn_taking.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def main():
    result = mod.evaluate()
    pauses = result["internal_pauses_by_style"]
    assert pauses["slow"]["mean_ms"] == 569.3
    assert pauses["slow"]["p95_ms"] == 925
    assert pauses["normal"]["mean_ms"] == 187.8
    assert result["patience_ms"] == 1200
    assert result["collision_risk"]["as_built"]["pct_over"] == 89.7
    assert result["collision_risk"]["hardened"]["turns_over_patience"] == 0
    print("smoke ok")


if __name__ == "__main__":
    main()
