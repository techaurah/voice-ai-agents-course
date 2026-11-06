"""Lesson 19 artifact: turn-taking, measured from both chairs.

Three views. The caller's side: the distribution of pauses inside
fixture utterances, by speaking style, because the gap an agent must
tolerate is set by the slowest speaker it serves. The agent's side:
the response gap the two endpointing policies produce. And the
collision: turns whose simulated latency to first audio exceeds a
stated caller patience of 1200 ms, after which real callers start
talking again and both parties speak at once.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from vox import audio, dialogue, latency  # noqa: E402

PATIENCE_MS = 1200


def evaluate():
    data = json.loads((ROOT / "fixtures" / "transcripts.json").read_text())
    pauses = {}
    for utt in data["utterances"]:
        env = audio.envelope_for(utt["text"], utt["style"], seed=0)
        pauses.setdefault(utt["style"], []).extend(
            ms for kind, ms, _l, _w in env if kind == "pause")
    pause_stats = {
        style: {"n": len(vals),
                "mean_ms": round(sum(vals) / len(vals), 1),
                "p95_ms": latency.percentile(vals, 95)}
        for style, vals in pauses.items()}
    calls = dialogue.load("calls.json")["calls"]
    schedule = dialogue.load("schedule.json")
    policy = dialogue.load("policy.json")
    rates = dialogue.load("rates.json")
    collisions = {}
    for name, config in (("as_built", dialogue.AS_BUILT_CONFIG),
                         ("hardened", dialogue.HARDENED_CONFIG)):
        pooled = []
        for call in calls:
            result = dialogue.run_call(call, schedule, policy, config,
                                       rates)
            pooled.extend(result["first_audio_ms"])
        over = sum(1 for v in pooled if v > PATIENCE_MS)
        collisions[name] = {
            "turns": len(pooled),
            "turns_over_patience": over,
            "pct_over": round(100.0 * over / len(pooled), 1),
        }
    return {"internal_pauses_by_style": pause_stats,
            "patience_ms": PATIENCE_MS,
            "collision_risk": collisions}


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2, sort_keys=True))
