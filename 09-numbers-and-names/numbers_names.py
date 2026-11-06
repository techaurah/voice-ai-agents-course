"""Lesson 09 artifact: numbers and names, the two hard payloads.

Three measurements on the bundled fixtures. First, digit utterances:
how often the parsed digit string survives the channel exactly.
Second, the twelve capstone phone numbers: exact-match rate raw,
then after the digit-by-digit read-back correction the hardened
dialogue manager uses. Third, spelled letters on the telephone
channel, raw and after letter-by-letter correction.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from vox import stt  # noqa: E402

WORD_BY_DIGIT = {v: k for k, v in stt.DIGIT_WORDS.items() if len(v) == 1}


def correct_digits(value, intent, call):
    """The caller-correction model from vox.dialogue, restated with
    the raw stand-in so this lesson can measure it in isolation: the
    caller hears which digits are wrong and repeats just those, up
    to two correction rounds."""
    cond = call["conditions"]
    digits = list(value)
    for round_no in range(2):
        wrong = [i for i in range(len(intent)) if digits[i] != intent[i]]
        if not wrong:
            break
        for i in wrong:
            heard = stt.transcribe(WORD_BY_DIGIT[intent[i]],
                                   cond["channel"], cond["snr_db"],
                                   seed_key=f"{call['id']}:fix{i}",
                                   attempt=round_no)
            fixed = stt.words_to_digits(heard)
            if fixed and len(fixed) == 1:
                digits[i] = fixed
    return "".join(digits)


def evaluate():
    data = json.loads((ROOT / "fixtures" / "transcripts.json").read_text())
    digit_exact = {}
    for utt in data["utterances"]:
        if "digits" not in utt["tags"]:
            continue
        hyp = stt.transcribe(utt["text"], utt["channel"], utt["snr_db"],
                             seed_key=utt["id"])
        ok = stt.words_to_digits(hyp) == stt.words_to_digits(utt["text"])
        bucket = digit_exact.setdefault(utt["channel"], [0, 0])
        bucket[1] += 1
        bucket[0] += 1 if ok else 0
    calls = json.loads((ROOT / "fixtures" / "calls.json").read_text())
    raw_ok = fixed_ok = total = 0
    for call in calls["calls"]:
        if "phone_text" not in call["answers"]:
            continue
        total += 1
        cond = call["conditions"]
        hyp = stt.transcribe(call["answers"]["phone_text"],
                             cond["channel"], cond["snr_db"],
                             seed_key=f"{call['id']}:phone_text",
                             attempt=0)
        heard = stt.words_to_digits(hyp)
        truth = call["truth"]["phone"]
        raw_ok += 1 if heard == truth else 0
        if heard and len(heard) == len(truth):
            fixed_ok += 1 if correct_digits(heard, truth, call) == truth \
                else 0
    letter_raw = letter_fixed = letter_total = 0
    for call in calls["calls"]:
        spelled = call["answers"].get("name_spelled")
        if not spelled:
            continue
        letter_total += 1
        cond = call["conditions"]
        heard = stt.transcribe_letters(
            spelled, cond["channel"],
            seed_key=f"{call['id']}:spell", attempt=0)
        if heard == spelled:
            letter_raw += 1
            letter_fixed += 1
            continue
        fixed = list(heard)
        for round_no in range(3):
            wrong = [i for i in range(len(spelled))
                     if i >= len(fixed) or fixed[i] != spelled[i]]
            if not wrong:
                break
            for i in wrong:
                one = stt.transcribe_letters(
                    [spelled[i]], cond["channel"],
                    seed_key=f"{call['id']}:spellfix{i}r{round_no}",
                    attempt=0)
                if i < len(fixed):
                    fixed[i] = one[0]
                else:
                    fixed.append(one[0])
        letter_fixed += 1 if fixed == spelled else 0
    return {
        "digit_utterances_exact": {
            ch: {"exact": ok, "of": n}
            for ch, (ok, n) in digit_exact.items()},
        "phone_numbers": {"of": total, "raw_exact": raw_ok,
                          "after_digit_correction": fixed_ok},
        "spelled_names": {"of": letter_total, "raw_exact": letter_raw,
                          "after_letter_correction": letter_fixed},
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2, sort_keys=True))
