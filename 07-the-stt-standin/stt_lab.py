"""Lesson 07 artifact: score the STT stand-in on the fixture set.

Transcribes all 24 bundled utterances under their stated channel and
noise conditions and measures word error rate, overall, split by
clean versus noisy, and as raw edit counts. The stand-in's confusion
rules are the curriculum: every error here is one the course later
teaches a defence against.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from vox import metrics, stt  # noqa: E402


def evaluate():
    data = json.loads((ROOT / "fixtures" / "transcripts.json").read_text())
    wers = []
    clean, noisy = [], []
    subs = dels = ins = 0
    worst = []
    for utt in data["utterances"]:
        hyp = stt.transcribe(utt["text"], utt["channel"], utt["snr_db"],
                             seed_key=utt["id"])
        w = metrics.wer(utt["text"], hyp)
        wers.append(w)
        (clean if utt["snr_db"] is None else noisy).append(w)
        s, d, i = metrics.edit_counts(utt["text"], hyp)
        subs += s
        dels += d
        ins += i
        worst.append((w, utt["id"]))
    worst.sort(reverse=True)
    return {
        "utterances": len(wers),
        "mean_wer": round(metrics.mean(wers), 4),
        "mean_wer_clean": round(metrics.mean(clean), 4),
        "mean_wer_noisy": round(metrics.mean(noisy), 4),
        "edit_counts": {"substitutions": subs, "deletions": dels,
                        "insertions": ins},
        "worst_three": [{"id": uid, "wer": w}
                        for w, uid in worst[:3]],
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2, sort_keys=True))
