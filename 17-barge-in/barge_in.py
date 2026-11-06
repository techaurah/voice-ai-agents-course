"""Lesson 17 artifact: barge-in and the phantom history problem.

The agent delivers a spoken confirmation built from a real booking.
The caller interrupts at 25, 50, and 75 percent of the line. Playback
takes 120 ms to stop after the interrupt (detection plus halt, a
stated simulation constant). Words that finish before the stop are
heard; the rest were never heard, but a naive conversation history
records the full reply as delivered. The lesson counts the phantom
words, and checks whether the appointment time was among them.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

STOP_LATENCY_MS = 120
CONFIRMATION = ("your cleaning is booked for tuesday at ten o'clock "
                "and a confirmation text is on its way")
FACT_WORDS = {"cleaning", "tuesday", "ten"}


def word_end_times(text):
    ends = []
    elapsed = 0
    for word in text.split():
        elapsed += 90 + 26 * len(word.strip(".,!?")) + 55
        ends.append(elapsed)
    return ends


def evaluate():
    words = CONFIRMATION.split()
    ends = word_end_times(CONFIRMATION)
    total_ms = ends[-1]
    out = {"total_words": len(words), "line_duration_ms": total_ms}
    for pct in (25, 50, 75):
        stop_at = int(total_ms * pct / 100) + STOP_LATENCY_MS
        heard = sum(1 for end in ends if end <= stop_at)
        unheard_facts = [w for w in words[heard:] if w in FACT_WORDS]
        out[f"interrupt_{pct}pct"] = {
            "heard_words": heard,
            "phantom_words": len(words) - heard,
            "facts_never_heard": unheard_facts,
        }
    return out


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2, sort_keys=True))
