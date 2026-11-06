"""Smoke test for Lesson 31: the gate table matches the README."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "artifact", Path(__file__).parent / "evaluate_capstone.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def main():
    result = mod.evaluate()
    as_built = result["as_built"]
    capstone = result["capstone"]
    assert as_built["measured"]["task_success_rate"] == 0.5
    assert as_built["measured"]["p50_first_audio_ms"] == 1251
    assert as_built["verdict"]["gates_passed"] == 3
    assert as_built["verdict"]["all_passed"] is False
    assert capstone["measured"]["task_success_rate"] == 1.0
    assert capstone["measured"]["p95_first_audio_ms"] == 891
    assert capstone["verdict"]["gates_passed"] == 5
    assert capstone["verdict"]["all_passed"] is True
    assert result["ship"] is True
    print("smoke ok")


if __name__ == "__main__":
    main()
