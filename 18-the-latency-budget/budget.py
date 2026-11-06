"""Lesson 18 artifact: four designs against the latency budget.

Runs all twelve bundled calls under four configurations that differ
in exactly the levers the course has built so far: sequential versus
streamed staging, fixed versus adaptive endpointing, and the
confirmation layer. Pools every completed turn's simulated latency
to first audio and reports p50 and p95 against the budget from
RESEARCH.md: p50 under 800 ms, p95 under 1500 ms.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from vox import dialogue, latency  # noqa: E402

SEQUENTIAL = dict(dialogue.AS_BUILT_CONFIG)
SEQUENTIAL["design"] = "sequential"
ADAPTIVE_NO_CONFIRM = dict(dialogue.AS_BUILT_CONFIG)
ADAPTIVE_NO_CONFIRM["endpoint"] = {"silence_ms": 450, "adaptive": True,
                                   "long_ms": 1100}

DESIGNS = {
    "sequential_fixed800": SEQUENTIAL,
    "streamed_fixed800": dialogue.AS_BUILT_CONFIG,
    "streamed_adaptive": ADAPTIVE_NO_CONFIRM,
    "streamed_adaptive_confirm": dialogue.HARDENED_CONFIG,
}


def evaluate():
    calls = dialogue.load("calls.json")["calls"]
    schedule = dialogue.load("schedule.json")
    policy = dialogue.load("policy.json")
    rates = dialogue.load("rates.json")
    out = {}
    for name, config in DESIGNS.items():
        pooled = []
        for call in calls:
            result = dialogue.run_call(call, schedule, policy, config,
                                       rates)
            pooled.extend(result["first_audio_ms"])
        out[name] = {
            "turns": len(pooled),
            "p50_ms": latency.percentile(pooled, 50),
            "p95_ms": latency.percentile(pooled, 95),
            "within_budget": latency.percentile(pooled, 50) <= 800
            and latency.percentile(pooled, 95) <= 1500,
        }
    return out


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2, sort_keys=True))
