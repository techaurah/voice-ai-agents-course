"""Lesson 06 artifact: endpointing policies against the truth.

Walks every fixture utterance's true segment script under three
policies: an aggressive 400 ms silence threshold, the classic 800 ms
default, and the adaptive policy from vox.vad (450 ms base, waiting
longer on incomplete cues, digit runs, very short answers, and
pauses within a slow speaker's own rhythm). Counts cut-offs, meaning
the policy declared the turn over while the caller was mid-sentence,
and the wait paid on completed turns.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from vox import audio, vad  # noqa: E402

POLICIES = {
    "fixed_400": {"silence_ms": 400, "adaptive": False},
    "fixed_800": {"silence_ms": 800, "adaptive": False},
    "adaptive_450": {"silence_ms": 450, "adaptive": True, "long_ms": 1100},
}


def run_policy(utterances, policy):
    cut_off_ids = []
    waits = []
    slow_cut = slow_total = 0
    for utt in utterances:
        env = audio.envelope_for(utt["text"], utt["style"], seed=0)
        result = vad.endpoint(env, policy["silence_ms"],
                              adaptive=policy["adaptive"],
                              long_ms=policy.get("long_ms", 900))
        if result["cut_off"]:
            cut_off_ids.append(utt["id"])
        else:
            waits.append(result["wait_ms"])
        if utt["style"] == "slow":
            slow_total += 1
            slow_cut += 1 if result["cut_off"] else 0
    return {
        "cut_offs": len(cut_off_ids),
        "cut_off_ids": cut_off_ids,
        "slow_utterances": slow_total,
        "slow_cut_offs": slow_cut,
        "mean_wait_completed_ms": round(sum(waits) / max(1, len(waits)), 1),
    }


def evaluate():
    data = json.loads((ROOT / "fixtures" / "transcripts.json").read_text())
    utterances = data["utterances"]
    return {name: run_policy(utterances, policy)
            for name, policy in POLICIES.items()}


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2, sort_keys=True))
