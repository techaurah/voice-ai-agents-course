"""Lesson 30 artifact: the capstone voice agent, assembled.

The BrightSmile Dental booking line as a single callable system:
the shared dialogue manager under the hardened configuration
(adaptive endpointing, read-back confirmation with digit-level
correction, name spelling with letter-level correction, the consent
gate on, card storage off). book_call() is the whole product; the
evaluation harness around it is Lesson 31's job.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from vox import dialogue, latency, metrics  # noqa: E402

SCHEDULE = dialogue.load("schedule.json")
POLICY = dialogue.load("policy.json")
RATES = dialogue.load("rates.json")


def book_call(call):
    """Run one simulated call through the capstone system."""
    return dialogue.run_call(call, SCHEDULE, POLICY,
                             dialogue.HARDENED_CONFIG, RATES)


def evaluate():
    calls = dialogue.load("calls.json")["calls"]
    per_call = {}
    pooled, repairs, success_costs = [], [], []
    success = escapes = 0
    for call in calls:
        result = book_call(call)
        grade = dialogue.grade(call, result, POLICY)
        success += grade["success"]
        escapes += grade["escapes"]
        pooled.extend(result["first_audio_ms"])
        repairs.append(result["repairs"])
        if grade["success"] and result["outcome"] == "booked":
            success_costs.append(result["cost_usd"])
        per_call[call["id"]] = {
            "outcome": result["outcome"],
            "success": grade["success"],
            "repairs": result["repairs"],
            "cutoffs": result["cutoffs"],
        }
    return {
        "per_call": per_call,
        "summary": {
            "success": success,
            "of": len(calls),
            "success_rate": round(success / len(calls), 4),
            "escapes": escapes,
            "p50_first_audio_ms": latency.percentile(pooled, 50),
            "p95_first_audio_ms": latency.percentile(pooled, 95),
            "mean_repairs": round(metrics.mean(repairs), 2),
            "cost_per_successful_booking": round(
                metrics.mean(success_costs), 4),
        },
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2, sort_keys=True))
