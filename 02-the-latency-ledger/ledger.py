"""Lesson 02 artifact: the latency ledger over every fixture turn.

Runs all 24 bundled utterances through the streamed pipeline model
and accumulates where the milliseconds go, stage by stage. The
endpointing stage uses each utterance's own simulated end-of-turn
wait from the stand-in VAD, so slow speakers cost more here, exactly
as they do on a real line. Prompt size grows across each simulated
call the way a real prompt accumulates slot state.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from vox import audio, latency, tts, vad  # noqa: E402
from vox.dialogue import AGENT_LINES  # noqa: E402

REPLIES = [AGENT_LINES["greeting"], AGENT_LINES["ask_service"],
           AGENT_LINES["ask_when"], AGENT_LINES["ask_name"],
           AGENT_LINES["ask_phone"], AGENT_LINES["confirm"],
           AGENT_LINES["booked"]]


def evaluate():
    data = json.loads((ROOT / "fixtures" / "transcripts.json").read_text())
    ledger = latency.Ledger()
    for i, utt in enumerate(data["utterances"]):
        env = audio.envelope_for(utt["text"], utt["style"], seed=0)
        wait = vad.endpoint(env, 800)["wait_ms"]
        reply = REPLIES[i % len(REPLIES)]
        prompt_words = 60 + 18 * (i % len(REPLIES))
        ledger.add("endpoint", wait)
        ledger.add("stt_final",
                   latency.stt_final_ms(len(utt["text"].split())))
        ledger.add("llm_first_token",
                   latency.llm_first_token_ms(prompt_words))
        ledger.add("tts_first_chunk", tts.synth_first_chunk_ms(reply))
        ledger.add("jitter", latency.JITTER_MS[utt["channel"]])
    totals = ledger.totals()
    grand = sum(totals.values())
    shares = {stage: round(100.0 * ms / grand, 1)
              for stage, ms in totals.items()}
    return {
        "turns": len(data["utterances"]),
        "stage_totals_ms": totals,
        "stage_shares_pct": shares,
        "grand_total_ms": grand,
        "mean_per_turn_ms": round(grand / len(data["utterances"]), 1),
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2, sort_keys=True))
