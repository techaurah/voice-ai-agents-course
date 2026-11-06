"""Lesson 29 artifact: the capstone gates, and where they came from.

Loads the gates file that was fixed on 2026-11-06, before the
capstone code was written, and recomputes the as-built baseline the
gates were set against. The check that matters: on the two binding
dimensions (task success and p50 latency) the gates are stricter
than the as-built system actually is, so passing them means the
hardening work did something, not that the bar was set under it.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from vox import dialogue, latency, metrics  # noqa: E402

GATES_PATH = Path(__file__).resolve().parent / "capstone" / "gates.json"


def baseline():
    calls = dialogue.load("calls.json")["calls"]
    schedule = dialogue.load("schedule.json")
    policy = dialogue.load("policy.json")
    rates = dialogue.load("rates.json")
    success = escapes = 0
    pooled, repairs = [], []
    for call in calls:
        result = dialogue.run_call(call, schedule, policy,
                                   dialogue.AS_BUILT_CONFIG, rates)
        grade = dialogue.grade(call, result, policy)
        success += grade["success"]
        escapes += grade["escapes"]
        pooled.extend(result["first_audio_ms"])
        repairs.append(result["repairs"])
    return {
        "success_rate": round(success / len(calls), 4),
        "escapes": escapes,
        "p50_first_audio_ms": latency.percentile(pooled, 50),
        "p95_first_audio_ms": latency.percentile(pooled, 95),
        "mean_repairs": round(metrics.mean(repairs), 2),
    }


def evaluate():
    spec = json.loads(GATES_PATH.read_text())
    gates = spec["capstone_system"]["gates"]
    base = baseline()
    return {
        "fixed_on": spec["fixed_on"],
        "gates": gates,
        "as_built_baseline": base,
        "success_gate_stricter_than_baseline":
            gates["task_success_rate_min"] > base["success_rate"],
        "p50_gate_stricter_than_baseline":
            gates["p50_first_audio_ms_max"] < base["p50_first_audio_ms"],
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2, sort_keys=True))
