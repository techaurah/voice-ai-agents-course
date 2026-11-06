"""vox: the shared machinery of the Voice AI Agents course.

Synthetic audio, an energy VAD and endpointing policies, deterministic
STT and TTS stand-ins, a simulated latency ledger, the BrightSmile
dialogue manager, and metrics. Standard library only. Every component
is a labelled stand-in: see each module's docstring for what it models
and what it deliberately does not.
"""

from . import audio, latency, metrics, stt, tts, vad  # noqa: F401
