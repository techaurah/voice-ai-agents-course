"""The simulated latency ledger.

Every number here is a formula, stated in the open, evaluated on
fixture data. These are simulated budgets for teaching where time
goes in a voice pipeline; they are not measurements of any real
platform. RESEARCH.md holds the real-world ranges reported by
sources, for comparison.

A turn's latency to first audio is the sum of what cannot overlap:
the endpointing wait, finalising the transcript, the model producing
its first token (or its whole reply, in a sequential design),
synthesising the first chunk, and one jitter allowance for the
channel.
"""

from . import tts

JITTER_MS = {"wideband": 25, "telephony": 55}


def stt_final_ms(n_words, streaming=True):
    if streaming:
        return int(30 + 3 * n_words)
    return int(120 + 18 * n_words)


def llm_first_token_ms(prompt_words):
    return int(90 + 1.1 * prompt_words)


def llm_full_ms(prompt_words, reply_words):
    return int(90 + 1.1 * prompt_words + 14 * reply_words)


def tool_ms():
    """One synchronous tool call (a schedule lookup), simulated."""
    return 140


def first_audio_ms(endpoint_wait, caller_words, prompt_words,
                   reply_text, channel="wideband", design="streamed",
                   tool=False):
    """Simulated milliseconds from the caller's last word to the
    agent's first audible word for one turn."""
    if design == "sequential":
        total = endpoint_wait
        total += stt_final_ms(caller_words, streaming=False)
        total += llm_full_ms(prompt_words, len(reply_text.split()))
        if tool:
            total += tool_ms()
        total += tts.synth_first_chunk_ms(reply_text)
        return int(total + JITTER_MS[channel])
    total = endpoint_wait
    total += stt_final_ms(caller_words, streaming=True)
    total += llm_first_token_ms(prompt_words)
    if tool:
        total += tool_ms()
    total += tts.synth_first_chunk_ms(reply_text)
    return int(total + JITTER_MS[channel])


def percentile(values, q):
    """Nearest-rank percentile, q in [0, 100]."""
    if not values:
        return 0
    ordered = sorted(values)
    rank = max(1, int(round(q / 100.0 * len(ordered))))
    return ordered[min(rank, len(ordered)) - 1]


class Ledger:
    """Accumulates simulated stage costs across many turns."""

    def __init__(self):
        self.stages = {}

    def add(self, stage, ms):
        self.stages.setdefault(stage, []).append(ms)

    def totals(self):
        return {stage: int(sum(vals)) for stage, vals in
                self.stages.items()}

    def shares(self):
        totals = self.totals()
        grand = sum(totals.values()) or 1
        return {stage: round(total / grand, 4)
                for stage, total in totals.items()}
