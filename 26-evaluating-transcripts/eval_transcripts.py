"""Lesson 26 artifact: a transcript evaluation with a proposed fix.

Evaluation is only useful when it can kill a change. The proposed
change here is a domain-vocabulary post-processor: map known garbles
back to the clinic vocabulary the stand-in confused them with
(clearing back to cleaning, checkups back to checkup). The harness
scores every fixture utterance before and after, overall and by
tag, and counts the utterances the fix made worse, because a
post-processor that rewrites a caller's real words is a bug with
good intentions.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from vox import metrics, stt  # noqa: E402

FIX_MAP = {garble: word for word, garble in stt.NEIGHBOURS.items()}


def post_process(hyp):
    return " ".join(FIX_MAP.get(tok, tok) for tok in hyp.split())


def evaluate():
    data = json.loads((ROOT / "fixtures" / "transcripts.json").read_text())
    before, after = [], []
    by_tag_before, by_tag_after = {}, {}
    helped = hurt = same = 0
    for utt in data["utterances"]:
        hyp = stt.transcribe(utt["text"], utt["channel"], utt["snr_db"],
                             seed_key=utt["id"])
        fixed = post_process(hyp)
        w_before = metrics.wer(utt["text"], hyp)
        w_after = metrics.wer(utt["text"], fixed)
        before.append(w_before)
        after.append(w_after)
        helped += 1 if w_after < w_before else 0
        hurt += 1 if w_after > w_before else 0
        same += 1 if w_after == w_before else 0
        for tag in utt["tags"]:
            by_tag_before.setdefault(tag, []).append(w_before)
            by_tag_after.setdefault(tag, []).append(w_after)
    return {
        "mean_wer_before": round(metrics.mean(before), 4),
        "mean_wer_after": round(metrics.mean(after), 4),
        "utterances_helped": helped,
        "utterances_hurt": hurt,
        "utterances_unchanged": same,
        "by_tag": {tag: {
            "before": round(metrics.mean(by_tag_before[tag]), 4),
            "after": round(metrics.mean(by_tag_after[tag]), 4)}
            for tag in sorted(by_tag_before)},
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2, sort_keys=True))
