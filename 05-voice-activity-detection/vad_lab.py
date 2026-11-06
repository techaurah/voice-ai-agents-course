"""Lesson 05 artifact: measure an energy VAD against ground truth.

The fixture envelopes are the truth. Renders every utterance, runs
the energy VAD from vox.vad, and scores it frame by frame, overall
and by speaking style. Then adds noise at 8 dB SNR and compares two
thresholds, because the threshold that is right in silence is wrong
in a noisy room.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from vox import audio, vad  # noqa: E402

FRAME_MS = 20


def detected_frames(segments, total_frames):
    flags = [False] * total_frames
    for start, end in segments:
        for i in range(start // FRAME_MS, min(end // FRAME_MS,
                                              total_frames)):
            flags[i] = True
    return flags


def score(flags, truth):
    tp = sum(1 for f, t in zip(flags, truth) if f and t)
    fp = sum(1 for f, t in zip(flags, truth) if f and not t)
    fn = sum(1 for f, t in zip(flags, truth) if not f and t)
    correct = sum(1 for f, t in zip(flags, truth) if f == t)
    return tp, fp, fn, correct


def evaluate():
    data = json.loads((ROOT / "fixtures" / "transcripts.json").read_text())
    total = correct = 0
    raw_total = raw_correct = 0
    by_style = {}
    segments_by_style = {}
    for utt in data["utterances"]:
        env = audio.envelope_for(utt["text"], utt["style"], seed=0)
        levels, truth = vad.frame_levels(env)
        found = vad.detect(levels)
        flags = detected_frames(found, len(truth))
        _tp, _fp, _fn, corr = score(flags, truth)
        total += len(truth)
        correct += corr
        bucket = by_style.setdefault(utt["style"], [0, 0])
        bucket[0] += corr
        bucket[1] += len(truth)
        raw_flags = [level > -32.0 for level in levels]
        raw_correct += sum(1 for f, t in zip(raw_flags, truth) if f == t)
        raw_total += len(truth)
        seg = segments_by_style.setdefault(
            utt["style"], {"one_segment": 0, "split": 0, "missed": 0})
        if len(found) == 1:
            seg["one_segment"] += 1
        elif len(found) > 1:
            seg["split"] += 1
        else:
            seg["missed"] += 1
    noisy = {}
    for threshold in (-32.0, -18.0):
        fp = fn = frames = 0
        for utt in data["utterances"]:
            env = audio.envelope_for(utt["text"], utt["style"], seed=0)
            _levels, truth = vad.frame_levels(env)
            samples = audio.render(env, rate=16000, seed=0)
            samples = audio.add_noise(samples, 8, seed=1)
            levels = [audio.to_db(r)
                      for r in audio.frames(samples, 16000, FRAME_MS)]
            flags = detected_frames(
                vad.detect(levels, threshold_db=threshold), len(truth))
            _tp, f_pos, f_neg, _c = score(flags, truth)
            fp += f_pos
            fn += f_neg
            frames += len(truth)
        noisy[f"threshold_{int(threshold)}db"] = {
            "false_speech_frames": fp,
            "missed_speech_frames": fn,
            "false_speech_pct": round(100.0 * fp / frames, 2),
            "missed_speech_pct": round(100.0 * fn / frames, 2),
        }
    return {
        "clean_frame_accuracy": round(correct / total, 4),
        "raw_threshold_frame_accuracy": round(raw_correct / raw_total, 4),
        "accuracy_by_style": {style: round(c / t, 4)
                              for style, (c, t) in by_style.items()},
        "segments_by_style": segments_by_style,
        "noisy_snr8": noisy,
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2, sort_keys=True))
