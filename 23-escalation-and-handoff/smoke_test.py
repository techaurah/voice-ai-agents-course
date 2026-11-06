"""Smoke test for Lesson 23: escalation results match the README."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "artifact", Path(__file__).parent / "escalation.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def main():
    result = mod.evaluate()
    assert result["designed_path_call_09"] == {
        "outcome": "escalated", "agent_turns": 3, "repairs": 0}
    sweep = result["repair_cap_sweep_call_11"]
    assert sweep["repair_cap_2"]["outcome"] == "escalated"
    assert sweep["repair_cap_4"]["outcome"] == "booked"
    assert sweep["repair_cap_8"]["repairs"] == 4
    ablation = result["keyword_ablation"]
    assert ablation["full_list"]["outcome"] == "escalated"
    assert ablation["reduced_list"]["outcome"] == "booked"
    assert ablation["reduced_list"]["grade"]["escapes"] == 1
    print("smoke ok")


if __name__ == "__main__":
    main()
