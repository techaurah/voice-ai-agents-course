"""Lesson 13 artifact: pricing a mid-call tool call three ways.

The schedule lookup happens on the when turn. Prices that turn's
simulated latency to first audio for every bundled call three ways:
the tool call in series in a streamed design, the tool call in
series in a sequential design, and the tool call prefetched (started
while the caller is still speaking, so it adds nothing). The tool
itself is the simulated 140 ms lookup from vox.latency.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from vox import latency, metrics  # noqa: E402
from vox.dialogue import AGENT_LINES  # noqa: E402

ENDPOINT_WAIT = 300  # the adaptive policy's completed-turn wait
PROMPT_WORDS = 96


def evaluate():
    calls = json.loads((ROOT / "fixtures" / "calls.json").read_text())
    series_streamed, series_sequential, prefetched = [], [], []
    for call in calls["calls"]:
        when = call["answers"]["when_text"]
        words = len(when.split())
        channel = call["conditions"]["channel"]
        reply = AGENT_LINES["ask_name"]
        series_streamed.append(latency.first_audio_ms(
            ENDPOINT_WAIT, words, PROMPT_WORDS, reply, channel,
            design="streamed", tool=True))
        series_sequential.append(latency.first_audio_ms(
            ENDPOINT_WAIT, words, PROMPT_WORDS, reply, channel,
            design="sequential", tool=True))
        prefetched.append(latency.first_audio_ms(
            ENDPOINT_WAIT, words, PROMPT_WORDS, reply, channel,
            design="streamed", tool=False))
    return {
        "calls": len(series_streamed),
        "tool_ms": latency.tool_ms(),
        "mean_first_audio_series_streamed": round(
            metrics.mean(series_streamed), 1),
        "mean_first_audio_series_sequential": round(
            metrics.mean(series_sequential), 1),
        "mean_first_audio_prefetched": round(
            metrics.mean(prefetched), 1),
        "prefetch_saving_ms": round(
            metrics.mean(series_streamed) - metrics.mean(prefetched), 1),
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2, sort_keys=True))
