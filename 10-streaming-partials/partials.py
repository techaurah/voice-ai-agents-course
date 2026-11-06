"""Lesson 10 artifact: what streaming partials cost and buy.

Builds the partial hypothesis stream for every fixture utterance
and measures two things: how much the displayed text revises itself
on the way to the final (token changes between consecutive
partials), and what happens to accuracy if a downstream component
commits to the transcript early, at 60 percent of the words, instead
of waiting for the final.
"""
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from vox import metrics, stt  # noqa: E402


def evaluate():
    data = json.loads((ROOT / "fixtures" / "transcripts.json").read_text())
    final_wers, early_wers, batch_wers = [], [], []
    changes = words = 0
    for utt in data["utterances"]:
        parts = stt.partials(utt["text"], utt["channel"], utt["snr_db"],
                             seed_key=utt["id"])
        final = parts[-1]
        final_wers.append(metrics.wer(utt["text"], final))
        batch = stt.transcribe(utt["text"], utt["channel"],
                               utt["snr_db"], seed_key=utt["id"])
        batch_wers.append(metrics.wer(utt["text"], batch))
        early_idx = max(0, math.ceil(0.6 * len(parts)) - 1)
        early_wers.append(metrics.wer(utt["text"], parts[early_idx]))
        words += len(final.split())
        for prev, cur in zip(parts, parts[1:]):
            a, b = prev.split(), cur.split()
            changes += sum(1 for x, y in zip(a, b) if x != y)
            changes += abs(len(a) - len(b))
    return {
        "utterances": len(final_wers),
        "mean_final_wer": round(metrics.mean(final_wers), 4),
        "mean_batch_final_wer": round(metrics.mean(batch_wers), 4),
        "mean_early_commit_wer": round(metrics.mean(early_wers), 4),
        "token_changes_per_word": round(changes / words, 3),
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2, sort_keys=True))
