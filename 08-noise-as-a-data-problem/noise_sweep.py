"""Lesson 08 artifact: WER as a function of channel and noise.

Groups the 24 fixture utterances by channel and SNR band and by
their curriculum tags, and scores each group with the STT stand-in.
The groups are small, and the table says so: a two-utterance group
is an anecdote with a mean, not a finding. The point of the lesson
is the shape of the table and what data you would collect to fill
it properly, not any single cell.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from vox import metrics, stt  # noqa: E402


def evaluate():
    data = json.loads((ROOT / "fixtures" / "transcripts.json").read_text())
    by_condition = {}
    by_tag = {}
    for utt in data["utterances"]:
        hyp = stt.transcribe(utt["text"], utt["channel"], utt["snr_db"],
                             seed_key=utt["id"])
        w = metrics.wer(utt["text"], hyp)
        band = "clean" if utt["snr_db"] is None else f"snr{utt['snr_db']}"
        by_condition.setdefault(f"{utt['channel']}_{band}", []).append(w)
        for tag in utt["tags"]:
            by_tag.setdefault(tag, []).append(w)
    return {
        "by_condition": {
            key: {"n": len(vals), "mean_wer": round(metrics.mean(vals), 4)}
            for key, vals in sorted(by_condition.items())},
        "by_tag": {
            key: {"n": len(vals), "mean_wer": round(metrics.mean(vals), 4)}
            for key, vals in sorted(by_tag.items())},
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2, sort_keys=True))
