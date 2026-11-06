"""Lesson 20 artifact: fault injection across the whole call set.

Takes the hardened configuration and breaks one thing at a time:
the consent gate switched off, card storage switched on, the
endpointing policy replaced with an aggressive fixed 300 ms, and
the confirmation layer removed. Each fault runs all twelve bundled
calls and is graded the same way as the reference. The point is the
shape of the damage: each fault fails different calls, for different
reasons, and none of them shows up in a demo of the happy path.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from vox import dialogue  # noqa: E402


def variant(**changes):
    cfg = dict(dialogue.HARDENED_CONFIG)
    cfg.update(changes)
    return cfg


FAULTS = {
    "reference_hardened": dialogue.HARDENED_CONFIG,
    "consent_gate_off": variant(respect_consent=False),
    "card_storage_on": variant(store_card=True),
    "aggressive_endpoint_300": variant(
        endpoint={"silence_ms": 300, "adaptive": False}),
    "confirmation_off": variant(confirm=False, spell_name=False),
}


def evaluate():
    calls = dialogue.load("calls.json")["calls"]
    schedule = dialogue.load("schedule.json")
    policy = dialogue.load("policy.json")
    rates = dialogue.load("rates.json")
    out = {}
    for name, config in FAULTS.items():
        success = escapes = cutoffs = 0
        failed = []
        for call in calls:
            result = dialogue.run_call(call, schedule, policy, config,
                                       rates)
            grade = dialogue.grade(call, result, policy)
            success += grade["success"]
            escapes += grade["escapes"]
            cutoffs += result["cutoffs"]
            if not grade["success"]:
                failed.append(call["id"])
        out[name] = {"success": success, "of": len(calls),
                     "escapes": escapes, "cutoffs": cutoffs,
                     "failed_ids": failed}
    return out


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2, sort_keys=True))
