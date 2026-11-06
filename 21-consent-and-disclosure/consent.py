"""Lesson 21 artifact: the consent gate, measured both ways.

Runs the consent-declining call (call-05) with the gate on and off,
and grades both. Then runs the full call set with the gate off and
counts what the grader catches. The gate is one boolean in the
configuration; the lesson is what that boolean is worth, in escapes
and in a call that should never have happened.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from vox import dialogue  # noqa: E402


def evaluate():
    calls = {c["id"]: c for c in dialogue.load("calls.json")["calls"]}
    schedule = dialogue.load("schedule.json")
    policy = dialogue.load("policy.json")
    rates = dialogue.load("rates.json")
    gate_off = dict(dialogue.HARDENED_CONFIG)
    gate_off["respect_consent"] = False
    call = calls["call-05"]
    on = dialogue.run_call(call, schedule, policy,
                           dialogue.HARDENED_CONFIG, rates)
    off = dialogue.run_call(call, schedule, policy, gate_off, rates)
    total_escapes = 0
    booked_declined = 0
    for other in calls.values():
        result = dialogue.run_call(other, schedule, policy, gate_off,
                                   rates)
        grade = dialogue.grade(other, result, policy)
        total_escapes += grade["escapes"]
        if other["consent"] == "declines" and \
                result["outcome"] == "booked":
            booked_declined += 1
    return {
        "call_05_gate_on": {
            "outcome": on["outcome"],
            "duration_s": on["duration_s"],
            "success": dialogue.grade(call, on, policy)["success"],
        },
        "call_05_gate_off": {
            "outcome": off["outcome"],
            "duration_s": off["duration_s"],
            "booked": off["booked"],
            "grade": dialogue.grade(call, off, policy),
        },
        "gate_off_all_calls": {
            "escapes": total_escapes,
            "declined_calls_booked": booked_declined,
        },
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2, sort_keys=True))
