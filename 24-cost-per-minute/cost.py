"""Lesson 24 artifact: cost accounting on the bundled call set.

Prices every call under the as-built and hardened configurations
with the teaching rates in fixtures/rates.json (stated there as
teaching parameters, not vendor quotes). Reports total spend, cost
per successful booking, and the money spent on calls that failed:
the uncomfortable line in every voice budget, because failed calls
are not free calls.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from vox import dialogue, metrics  # noqa: E402


def summarise(config):
    calls = dialogue.load("calls.json")["calls"]
    schedule = dialogue.load("schedule.json")
    policy = dialogue.load("policy.json")
    rates = dialogue.load("rates.json")
    total = wasted = 0.0
    success = bookings = 0
    success_costs = []
    minutes = []
    for call in calls:
        result = dialogue.run_call(call, schedule, policy, config, rates)
        grade = dialogue.grade(call, result, policy)
        total += result["cost_usd"]
        minutes.append(result["duration_s"] / 60.0)
        if grade["success"]:
            success += 1
            if result["outcome"] == "booked":
                bookings += 1
                success_costs.append(result["cost_usd"])
        else:
            wasted += result["cost_usd"]
    return {
        "total_cost_usd": round(total, 4),
        "success": success,
        "bookings": bookings,
        "cost_per_successful_booking": round(
            metrics.mean(success_costs), 4) if success_costs else None,
        "wasted_on_failed_calls_usd": round(wasted, 4),
        "mean_call_minutes": round(metrics.mean(minutes), 2),
        "per_minute_rate_usd": round(
            sum(dialogue.load("rates.json")["per_minute"].values()), 3),
    }


def evaluate():
    return {
        "as_built": summarise(dialogue.AS_BUILT_CONFIG),
        "hardened": summarise(dialogue.HARDENED_CONFIG),
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2, sort_keys=True))
