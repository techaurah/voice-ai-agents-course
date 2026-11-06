"""Voice activity detection and endpointing: deterministic stand-ins.

The VAD here is an energy gate over frame levels, the oldest and still
most common design, which is exactly why its failure modes are worth
measuring: it knows nothing about language, so a thinking pause and a
finished turn look identical to it.

A segment script (from vox.audio.envelope_for) is the ground truth:
speech segments carry words, pauses carry None. Grading compares what
a policy does against that truth.
"""

from . import audio

FRAME_MS = 20


def frame_levels(segments, rate=16000, seed=0):
    """Render segments and return (levels_db, truth) per 20 ms frame.

    truth[i] is True when the midpoint of frame i falls inside a
    true speech segment.
    """
    samples = audio.render(segments, rate=rate, seed=seed)
    levels = [audio.to_db(r) for r in audio.frames(samples, rate, FRAME_MS)]
    bounds = []
    elapsed = 0
    for kind, ms, _level, _word in segments:
        bounds.append((elapsed, elapsed + ms, kind == "speech"))
        elapsed += ms
    truth = []
    for i in range(len(levels)):
        mid = i * FRAME_MS + FRAME_MS / 2
        truth.append(any(start <= mid < end and is_speech
                         for start, end, is_speech in bounds))
    return levels, truth


def detect(levels, threshold_db=-32.0, hangover_ms=200, min_speech_ms=120):
    """Energy VAD: frames above threshold are speech; short gaps are
    bridged by the hangover; short bursts are discarded as noise."""
    hang = hangover_ms // FRAME_MS
    min_len = max(1, min_speech_ms // FRAME_MS)
    raw = [level > threshold_db for level in levels]
    bridged = list(raw)
    gap = 0
    for i, is_speech in enumerate(raw):
        if is_speech:
            if 0 < gap <= hang:
                for j in range(i - gap, i):
                    bridged[j] = True
            gap = 0
        else:
            gap += 1
    segments = []
    start = None
    for i, is_speech in enumerate(bridged):
        if is_speech and start is None:
            start = i
        elif not is_speech and start is not None:
            if (i - start) >= min_len:
                segments.append((start * FRAME_MS, i * FRAME_MS))
            start = None
    if start is not None and (len(bridged) - start) >= min_len:
        segments.append((start * FRAME_MS, len(bridged) * FRAME_MS))
    return segments


INCOMPLETE_CUES = {"and", "but", "because", "so", "the", "a", "my",
                   "to", "at", "on", "um", "uh", "er", "if", "when"}

DIGIT_WORDS = {"zero", "oh", "one", "two", "three", "four", "five",
               "six", "seven", "eight", "nine", "fifteen", "sixteen",
               "fifty", "sixty", "double"}


def _adaptive_threshold(segments, upto, silence_ms, long_ms):
    """The adaptive policy's wait for the pause at segment index upto.

    A completeness model, in miniature, plus one speaker-adaptation
    rule. It waits long when the words so far cannot be a finished
    request: fewer than three words heard, the last word an incomplete
    cue, or the speaker in the middle of a digit run (people pause
    inside phone numbers to remember them). It also learns the
    speaker's own pause ceiling as the utterance goes on: a pause no
    longer than the longest pause this speaker has already taken
    mid-utterance, plus 150 ms of slack, is treated as their rhythm,
    not their ending.
    """
    heard = [w.lower() for kind, _m, _l, w in segments[:upto]
             if kind == "speech"]
    if len(heard) < 3:
        return long_ms
    last = heard[-1].strip(".,")
    if last in INCOMPLETE_CUES:
        return long_ms
    if last in DIGIT_WORDS and upto + 1 < len(segments) \
            and (segments[upto + 1][3] or "").lower() in DIGIT_WORDS:
        return long_ms
    prev_pauses = [ms for kind, ms, _l, _w in segments[:upto]
                   if kind == "pause"]
    if prev_pauses:
        ceiling = min(max(prev_pauses) + 150, long_ms)
        return max(silence_ms, ceiling)
    return silence_ms


def endpoint(segments, silence_ms, adaptive=False, long_ms=900):
    """Decide when an utterance ends, walking its true segment script.

    Returns a dict with:
    - cut_off: True when the policy fired during an internal pause,
      splitting the utterance before its true end
    - wait_ms: the silence the policy waited at the true end (or the
      internal pause it fired on, when cut off)
    - turns_heard: how many "utterances" the policy would report

    With adaptive=True, a pause after an incomplete cue word (a
    conjunction, article, or filler) waits long_ms instead, the
    cheapest possible stand-in for a semantic turn detector.
    """
    speech_seen = False
    last_word = None
    for idx, (kind, ms, _level, word) in enumerate(segments):
        if kind == "speech":
            speech_seen = True
            last_word = word
            continue
        if not speech_seen:
            continue
        if adaptive:
            threshold = _adaptive_threshold(segments, idx, silence_ms,
                                            long_ms)
        else:
            threshold = silence_ms
        if ms >= threshold:
            return {"cut_off": True, "wait_ms": threshold, "turns_heard": 2}
    if adaptive:
        # A completeness model decides from the audio of the turn and
        # commits in roughly a fixed decision time (LiveKit's audio
        # turn detector runs with a 0.3 s minimum endpointing delay,
        # RESEARCH.md); the long waits happen mid-utterance, where
        # they prevent cut-offs, not at the true end.
        end_wait = 300
    else:
        end_wait = silence_ms
    return {"cut_off": False, "wait_ms": end_wait, "turns_heard": 1}
