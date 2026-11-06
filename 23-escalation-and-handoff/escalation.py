"""Lesson 23 artifact: escalation paths, and the keyword list.

Three measurements. First, the designed path: the emergency call
under the hardened configuration escalates on its first answer.
Second, the exhausted path: the slow, noisy hard call under the
as-built configuration escalates only after repairs run out, and
the repair cap in the policy decides how long that takes; the cap
is swept at 2, 4, and 8. Third, the ablation: a caller who asks for
a checkup while describing emergency symptoms, graded as an
emergency, under the full keyword list from the policy and under a
reduced list containing only the word emergency.
"""
import copy
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
    designed = dialogue.run_call(calls["call-09"], schedule, policy,
                                 dialogue.HARDENED_CONFIG, rates)
    sweep = {}
    for cap in (2, 4, 8):
        capped = dict(policy)
        capped["max_total_repairs"] = cap
        capped["max_repairs_per_slot"] = cap
        result = dialogue.run_call(calls["call-11"], schedule, capped,
                                   dialogue.AS_BUILT_CONFIG, rates)
        sweep[f"repair_cap_{cap}"] = {
            "outcome": result["outcome"],
            "repairs": result["repairs"],
            "agent_turns": result["agent_turns"],
        }
    variant = copy.deepcopy(calls["call-09"])
    variant["id"] = "call-09-variant"
    variant["answers"]["service_text"] = (
        "I would like a checkup but my face is swollen")
    variant["answers"]["when_text"] = "tuesday at nine please"
    full = dialogue.run_call(variant, schedule, policy,
                             dialogue.HARDENED_CONFIG, rates)
    reduced_policy = dict(policy)
    reduced_policy["emergency_keywords"] = ["emergency"]
    reduced = dialogue.run_call(variant, schedule, reduced_policy,
                                dialogue.HARDENED_CONFIG, rates)
    return {
        "designed_path_call_09": {
            "outcome": designed["outcome"],
            "agent_turns": designed["agent_turns"],
            "repairs": designed["repairs"],
        },
        "repair_cap_sweep_call_11": sweep,
        "keyword_ablation": {
            "full_list": {
                "outcome": full["outcome"],
                "grade": dialogue.grade(variant, full, policy),
            },
            "reduced_list": {
                "outcome": reduced["outcome"],
                "grade": dialogue.grade(variant, reduced, policy),
            },
        },
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2, sort_keys=True))
