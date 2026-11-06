"""Lesson 31 artifact: the capstone, graded against its gates.

Runs the as-built configuration and the capstone system over the
twelve bundled calls and scores both against the gates fixed in
Lesson 29, before the capstone was built. The ship verdict is the
capstone's row, but the as-built row stays in the report: a gate
table that only shows the passing system teaches nothing.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from vox import dialogue, latency, metrics  # noqa: E402

GATES_PATH = ROOT / "29-capstone-spec" / "capstone" / "gates.json"


def measure(config):
    calls = dialogue.load("calls.json")["calls"]
    schedule = dialogue.load("schedule.json")
    policy = dialogue.load("policy.json")
    rates = dialogue.load("rates.json")
    success = escapes = 0
    pooled, repairs = [], []
    for call in calls:
        result = dialogue.run_call(call, schedule, policy, config, rates)
        grade = dialogue.grade(call, result, policy)
        success += grade["success"]
        escapes += grade["escapes"]
        pooled.extend(result["first_audio_ms"])
        repairs.append(result["repairs"])
    return {
        "task_success_rate": round(success / len(calls), 4),
        "policy_escapes": escapes,
        "p50_first_audio_ms": latency.percentile(pooled, 50),
        "p95_first_audio_ms": latency.percentile(pooled, 95),
        "mean_repairs_per_call": round(metrics.mean(repairs), 2),
    }


def verdict(measured, gates):
    checks = {
        "task_success_rate_min":
            measured["task_success_rate"] >=
            gates["task_success_rate_min"],
        "policy_escapes_max":
            measured["policy_escapes"] <= gates["policy_escapes_max"],
        "p50_first_audio_ms_max":
            measured["p50_first_audio_ms"] <=
            gates["p50_first_audio_ms_max"],
        "p95_first_audio_ms_max":
            measured["p95_first_audio_ms"] <=
            gates["p95_first_audio_ms_max"],
        "mean_repairs_per_call_max":
            measured["mean_repairs_per_call"] <=
            gates["mean_repairs_per_call_max"],
    }
    return {"gates_passed": sum(checks.values()), "of": len(checks),
            "checks": checks, "all_passed": all(checks.values())}


def evaluate():
    spec = json.loads(GATES_PATH.read_text())
    gates = spec["capstone_system"]["gates"]
    as_built = measure(dialogue.AS_BUILT_CONFIG)
    capstone = measure(dialogue.HARDENED_CONFIG)
    return {
        "gates": gates,
        "as_built": {"measured": as_built,
                     "verdict": verdict(as_built, gates)},
        "capstone": {"measured": capstone,
                     "verdict": verdict(capstone, gates)},
        "ship": verdict(capstone, gates)["all_passed"],
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2, sort_keys=True))
