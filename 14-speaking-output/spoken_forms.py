"""Lesson 14 artifact: text that was written to be read, not heard.

A synthesiser reads literally: "10:30" is not a time to it, and a
bare digit string is not a phone number. This lesson builds the
confirmation sentences the booking line actually speaks, from the
bundled schedule and policy, counts the tokens no synthesiser
should be handed raw, then rewrites them into spoken forms (times
as words, money as words, phone numbers as digit words) and counts
again.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven",
        "eight", "nine", "ten", "eleven", "twelve", "thirteen",
        "fourteen", "fifteen", "sixteen", "seventeen", "eighteen",
        "nineteen"]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty",
        "seventy", "eighty", "ninety"]
DIGIT_WORD = {str(i): ONES[i] for i in range(10)}


def number_words(n):
    if n < 20:
        return ONES[n]
    if n < 100:
        return TENS[n // 10] + (" " + ONES[n % 10] if n % 10 else "")
    if n < 1000:
        rest = n % 100
        return ONES[n // 100] + " hundred" + \
            (" " + number_words(rest) if rest else "")
    rest = n % 1000
    return ONES[n // 1000] + " thousand" + \
        (" " + number_words(rest) if rest else "")


def spoken_time(hhmm):
    hour, minute = (int(p) for p in hhmm.split(":"))
    hour_word = number_words(hour % 12 or 12)
    if minute == 0:
        return f"{hour_word} o'clock"
    if minute < 10:
        return f"{hour_word} oh {number_words(minute)}"
    return f"{hour_word} {number_words(minute)}"


def to_spoken(text):
    text = re.sub(r"£(\d+)", lambda m: number_words(int(m.group(1))) +
                  " pounds", text)
    text = re.sub(r"\b(\d{1,2}):(\d{2})\b",
                  lambda m: spoken_time(m.group(0)), text)
    text = re.sub(r"\b\d{7,}\b", lambda m: " ".join(
        DIGIT_WORD[d] for d in m.group(0)), text)
    text = re.sub(r"\b\d+\b", lambda m: number_words(int(m.group(0))),
                  text)
    return text


def unspeakable_tokens(text):
    return [tok for tok in text.split()
            if any(ch.isdigit() for ch in tok) or "£" in tok]


def evaluate():
    schedule = json.loads((ROOT / "fixtures" / "schedule.json").read_text())
    policy = json.loads((ROOT / "fixtures" / "policy.json").read_text())
    sentences = []
    for slot in schedule["slots"]:
        if slot["status"] != "free":
            continue
        sentences.append(
            f"Your {slot['service']} is booked for {slot['day']} at "
            f"{slot['time']}. The deposit is £{policy['deposit_gbp']}. "
            f"We will text the confirmation to 07950155240.")
    before = sum(len(unspeakable_tokens(s)) for s in sentences)
    after = sum(len(unspeakable_tokens(to_spoken(s))) for s in sentences)
    return {
        "sentences": len(sentences),
        "unspeakable_tokens_before": before,
        "unspeakable_tokens_after": after,
        "example_before": sentences[0],
        "example_after": to_spoken(sentences[0]),
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2, sort_keys=True))
