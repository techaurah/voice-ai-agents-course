"""Lesson 11 artifact: the slot-filling dialogue manager at work.

Runs three bundled calls through the as-built configuration (the
naive composition: fixed 800 ms endpointing, no confirmation, no
spelling) and reports what the manager did on each: outcome, agent
turns, repairs, cut-offs, duration, and what the grader said. The
manager only ever hears stand-in hypotheses; grading happens
afterwards, against truth it never saw.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from vox import dialogue  # noqa: E402

CALL_IDS = ("call-01", "call-07", "call-12")


def evaluate():
    calls = {c["id"]: c
             for c in dialogue.load("calls.json")["calls"]}
    schedule = dialogue.load("schedule.json")
    policy = dialogue.load("policy.json")
    rates = dialogue.load("rates.json")
    out = {}
    for call_id in CALL_IDS:
        call = calls[call_id]
        result = dialogue.run_call(call, schedule, policy,
                                   dialogue.AS_BUILT_CONFIG, rates)
        grade = dialogue.grade(call, result, policy)
        out[call_id] = {
            "label": call["label"],
            "outcome": result["outcome"],
            "success": grade["success"],
            "reasons": grade["reasons"],
            "agent_turns": result["agent_turns"],
            "repairs": result["repairs"],
            "cutoffs": result["cutoffs"],
            "duration_s": result["duration_s"],
            "booked": result["booked"],
        }
    return out


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2, sort_keys=True))
