"""Lesson 28 artifact: a failure taxonomy, populated by the suite.

Runs the as-built configuration and the four single-fault variants
from Lesson 20, collects every failed call, and classifies each
failure from the grader's own evidence: the field named in the
reason, the outcome mismatch, or the policy escape. The taxonomy is
the deliverable: it turns "the agent is unreliable" into five
named, countable, separately fixable problems.
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


SUITE = {
    "as_built": dialogue.AS_BUILT_CONFIG,
    "consent_gate_off": variant(respect_consent=False),
    "card_storage_on": variant(store_card=True),
    "aggressive_endpoint_300": variant(
        endpoint={"silence_ms": 300, "adaptive": False}),
    "confirmation_off": variant(confirm=False, spell_name=False),
}


def classify(call, result, grade):
    reasons = " ".join(grade["reasons"])
    if "consent" in reasons:
        return "consent_escape"
    if "card" in reasons:
        return "payment_escape"
    if "emergency" in reasons:
        return "emergency_escape"
    if "phone" in reasons:
        return "transcription_digits"
    if "name" in reasons:
        return "transcription_name"
    if result["outcome"] == "escalated" and \
            call["expected_outcome"] == "booked":
        return "repair_exhaustion"
    if result["outcome"] == "booked":
        return "slot_or_value_mismatch"
    return "other"


def evaluate():
    calls = dialogue.load("calls.json")["calls"]
    schedule = dialogue.load("schedule.json")
    policy = dialogue.load("policy.json")
    rates = dialogue.load("rates.json")
    counts = {}
    runs = failures = 0
    examples = {}
    for config in SUITE.values():
        for call in calls:
            result = dialogue.run_call(call, schedule, policy, config,
                                       rates)
            grade = dialogue.grade(call, result, policy)
            runs += 1
            if grade["success"]:
                continue
            failures += 1
            category = classify(call, result, grade)
            counts[category] = counts.get(category, 0) + 1
            examples.setdefault(category, call["id"])
    return {
        "suite_runs": runs,
        "total_failures": failures,
        "failures_by_category": dict(sorted(counts.items())),
        "example_call_per_category": examples,
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2, sort_keys=True))
