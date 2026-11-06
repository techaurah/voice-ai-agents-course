"""Lesson 22 artifact: what lands in the stored transcript.

Builds the corpus a naive deployment would store: every caller
answer from the bundled calls, plus the card utterance from the
trap call, exactly as heard. Counts the card digits and phone
digits sitting in that text. Then applies a redactor that replaces
runs of digit words and raw digit strings with a marker, and counts
again. Redaction is measured, not asserted.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from vox import stt  # noqa: E402
from vox.dialogue import CARD_UTTERANCE  # noqa: E402

DIGIT_WORDS = set(stt.DIGIT_WORDS) | {"double"}


def digit_runs(text):
    """Digit strings recoverable from a text, spoken or typed."""
    found = []
    tokens = text.lower().split()
    current = []
    for tok in tokens + [""]:
        if tok in DIGIT_WORDS:
            current.append(tok)
        else:
            if len(current) >= 4:
                parsed = stt.words_to_digits(" ".join(current))
                if parsed:
                    found.append(parsed)
            current = []
    found.extend(re.findall(r"\d{4,}", text))
    return found


def redact(text):
    tokens = text.split()
    out = []
    i = 0
    while i < len(tokens):
        if tokens[i].lower().strip(".,") in DIGIT_WORDS:
            j = i
            while j < len(tokens) and \
                    tokens[j].lower().strip(".,") in DIGIT_WORDS:
                j += 1
            if j - i >= 4:
                out.append("[redacted]")
                i = j
                continue
        out.append(tokens[i])
        i += 1
    return re.sub(r"\d{4,}", "[redacted]", " ".join(out))


def evaluate():
    calls = json.loads((ROOT / "fixtures" / "calls.json").read_text())
    corpus = [CARD_UTTERANCE]
    for call in calls["calls"]:
        corpus.extend(v for v in call["answers"].values()
                      if isinstance(v, str))
    corpus = [text for text in corpus if text]
    before = [d for text in corpus for d in digit_runs(text)]
    after = [d for text in (redact(t) for t in corpus)
             for d in digit_runs(text)]
    card_before = digit_runs(CARD_UTTERANCE)
    return {
        "texts_stored": len(corpus),
        "digit_strings_before": len(before),
        "digits_before": sum(len(d) for d in before),
        "card_digits_before": len(card_before[0]) if card_before else 0,
        "digit_strings_after_redaction": len(after),
        "digits_after_redaction": sum(len(d) for d in after),
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2, sort_keys=True))
