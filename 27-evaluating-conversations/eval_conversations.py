"""Lesson 27 artifact: conversation evaluation by call family.

A single success rate hides where a system is weak. This harness
groups the twelve bundled calls into the families the course built
them to probe, and scores the as-built and hardened configurations
per family. Families overlap on purpose: the hard call (call-11) is
both a slow-speaker call and a noisy-line call, because real calls
do not fail one variable at a time.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from vox import dialogue  # noqa: E402

FAMILIES = {
    "clean_bookings": ["call-01", "call-12"],
    "slow_speakers": ["call-02", "call-11"],
    "noisy_lines": ["call-03", "call-11"],
    "names_and_spelling": ["call-06", "call-10"],
    "spoken_number_chunks": ["call-04"],
    "safety_paths": ["call-05", "call-07", "call-09"],
    "reschedule": ["call-08"],
}


def score(config, calls, schedule, policy, rates):
    results = {}
    for call in calls:
        result = dialogue.run_call(call, schedule, policy, config, rates)
        results[call["id"]] = dialogue.grade(call, result,
                                             policy)["success"]
    return results


def evaluate():
    calls = dialogue.load("calls.json")["calls"]
    schedule = dialogue.load("schedule.json")
    policy = dialogue.load("policy.json")
    rates = dialogue.load("rates.json")
    by_id = {c["id"]: c for c in calls}
    out = {}
    for name, config in (("as_built", dialogue.AS_BUILT_CONFIG),
                         ("hardened", dialogue.HARDENED_CONFIG)):
        grades = score(config, calls, schedule, policy, rates)
        families = {}
        for family, ids in FAMILIES.items():
            families[family] = {
                "success": sum(1 for i in ids if grades[i]),
                "of": len(ids),
            }
        out[name] = {
            "overall": {"success": sum(grades.values()), "of": len(calls)},
            "families": families,
        }
    return out


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2, sort_keys=True))
