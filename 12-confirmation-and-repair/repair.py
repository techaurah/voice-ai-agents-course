"""Lesson 12 artifact: what read-back confirmation buys, isolated.

Both configurations use adaptive endpointing, so the only difference
is the confirmation layer: off (values are booked as first heard)
versus on (read-back with digit-level correction for phone numbers,
plus spelling with letter-level correction for names). Reports task
success, repairs, agent turns, and call duration across all twelve
bundled calls.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from vox import dialogue, metrics  # noqa: E402

NO_CONFIRM = dict(dialogue.AS_BUILT_CONFIG)
NO_CONFIRM["endpoint"] = {"silence_ms": 450, "adaptive": True,
                          "long_ms": 1100}


def summarise(config):
    calls = dialogue.load("calls.json")["calls"]
    schedule = dialogue.load("schedule.json")
    policy = dialogue.load("policy.json")
    rates = dialogue.load("rates.json")
    success = 0
    repairs, turns, durations = [], [], []
    failed = []
    for call in calls:
        result = dialogue.run_call(call, schedule, policy, config, rates)
        grade = dialogue.grade(call, result, policy)
        success += grade["success"]
        repairs.append(result["repairs"])
        turns.append(result["agent_turns"])
        durations.append(result["duration_s"])
        if not grade["success"]:
            failed.append(call["id"])
    return {
        "success": success,
        "of": len(calls),
        "failed_ids": failed,
        "mean_repairs": round(metrics.mean(repairs), 2),
        "mean_agent_turns": round(metrics.mean(turns), 2),
        "mean_duration_s": round(metrics.mean(durations), 2),
    }


def evaluate():
    return {
        "adaptive_no_confirm": summarise(NO_CONFIRM),
        "adaptive_with_confirm": summarise(dialogue.HARDENED_CONFIG),
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2, sort_keys=True))
