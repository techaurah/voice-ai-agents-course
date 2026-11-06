"""A deterministic speech-to-text stand-in.

This is not a recogniser. It is a confusion model over reference text:
given what the caller actually said (a fixture), it produces the
hypothesis a recogniser with known weaknesses would plausibly emit,
under a stated channel and noise condition. The weaknesses are the
curriculum:

- homophones, on any channel (their/there, wright/right)
- number-word confusions on the telephone channel, where the
  fricatives that separate fifteen from fifty never arrive
  (fifteen/fifty, sixteen/sixty, five/nine)
- spelled-letter confusions on the telephone channel (f/s, m/n)
- a small vocabulary of names it simply does not know, garbled whole
- word drops and garbles that grow as the signal-to-noise ratio falls

Every decision comes from a seeded generator keyed by the utterance
id and the attempt number, so results reproduce exactly, and a second
attempt at the same utterance is a genuinely different draw, which is
what makes repair strategies measurable.
"""

import random

HOMOPHONES = {
    "their": "there", "there": "their", "to": "too", "too": "to",
    "two": "to", "for": "four", "four": "for", "right": "write",
    "write": "right", "wright": "right", "here": "hear", "hear": "here",
    "see": "sea", "sea": "see", "by": "buy", "buy": "by",
    "new": "knew", "knew": "new", "week": "weak", "weak": "week",
    "hour": "our", "our": "hour", "know": "no", "no": "know",
    "son": "sun", "sun": "son", "won": "one", "one": "won",
    "piece": "peace", "peace": "piece",
}

TELEPHONY_NUMBER_SWAPS = {
    "fifteen": "fifty", "fifty": "fifteen",
    "sixteen": "sixty", "sixty": "sixteen",
    "five": "nine", "nine": "five",
}

LETTER_SWAPS = {"f": "s", "s": "f", "m": "n", "n": "m"}

UNKNOWN_NAMES = {"niamh": "neve", "siobhan": "shannon",
                 "saoirse": "seersha"}

NEIGHBOURS = {
    "cracked": "tracked", "hurts": "hearts", "bite": "bike",
    "swollen": "swelling", "train": "strain", "side": "sighed",
    "crown": "clown", "night": "knight", "pain": "pane",
    "checkup": "checkups", "cleaning": "clearing",
    "whitening": "widening", "hygienist": "hygienists",
    "appointment": "appointments", "thursday": "tuesday",
    "book": "books", "move": "moved", "week": "weeks",
}

SHORT_WORDS = {"a", "an", "the", "to", "of", "I", "is", "it", "at",
               "on", "my", "me"}

DIGIT_WORDS = {"zero": "0", "oh": "0", "one": "1", "two": "2",
               "three": "3", "four": "4", "five": "5", "six": "6",
               "seven": "7", "eight": "8", "nine": "9",
               "fifteen": "15", "sixteen": "16", "fifty": "50",
               "sixty": "60"}

_SINGLE_DIGIT_WORDS = ["zero", "one", "two", "three", "four", "five",
                       "six", "seven", "eight", "nine"]

DAY_WORDS = ["monday", "tuesday", "wednesday", "thursday", "friday",
             "saturday", "sunday"]

HOUR_WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
              "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
              "eleven": 11, "twelve": 12}


def _noise_probs(snr_db):
    """(drop probability for short words, garble probability)."""
    if snr_db is None or snr_db >= 20:
        return 0.0, 0.0
    if snr_db >= 12:
        return 0.12, 0.03
    if snr_db >= 8:
        return 0.22, 0.07
    return 0.32, 0.12


def transcribe(text, channel="wideband", snr_db=None, seed_key="utt",
               attempt=0):
    """Produce the stand-in's hypothesis for a reference utterance.

    A digit context (an utterance that is mostly digit words, like a
    phone number read aloud) is transcribed under different rules: a
    recogniser's digit language model suppresses the prose homophone
    swaps there, and the errors that remain are digit substitutions.
    """
    rng = random.Random(f"stt:{seed_key}:{attempt}")
    drop_p, garble_p = _noise_probs(snr_db)
    raw = [tok.strip(".,!?") for tok in text.lower().split()]
    digit_share = sum(1 for w in raw
                      if w in DIGIT_WORDS or w == "double") / max(1, len(raw))
    digit_context = digit_share >= 0.6
    digit_p = 0.08 if channel == "telephony" else 0.03
    out = []
    for word in raw:
        if word in UNKNOWN_NAMES:
            out.append(UNKNOWN_NAMES[word])
            continue
        if digit_context and word in _SINGLE_DIGIT_WORDS:
            if rng.random() < digit_p:
                out.append(rng.choice([d for d in _SINGLE_DIGIT_WORDS
                                       if d != word]))
            else:
                out.append(word)
            continue
        if channel == "telephony" and word in TELEPHONY_NUMBER_SWAPS:
            if word in ("fifteen", "fifty", "sixteen", "sixty") or \
                    digit_context:
                if rng.random() < 0.55:
                    out.append(TELEPHONY_NUMBER_SWAPS[word])
                    continue
        if channel == "telephony" and len(word) == 1 and word.isalpha():
            if word in LETTER_SWAPS and rng.random() < 0.4:
                out.append(LETTER_SWAPS[word])
                continue
        if word in HOMOPHONES and not (digit_context
                                       and word in DIGIT_WORDS):
            if rng.random() < 0.3:
                out.append(HOMOPHONES[word])
                continue
        if word in SHORT_WORDS and rng.random() < drop_p:
            continue
        if word in NEIGHBOURS and rng.random() < garble_p:
            out.append(NEIGHBOURS[word])
            continue
        out.append(word)
    return " ".join(out)


def transcribe_letters(letters, channel="telephony", seed_key="spell",
                       attempt=0):
    """Transcribe a spelled-out sequence, letter by letter."""
    rng = random.Random(f"letters:{seed_key}:{attempt}")
    out = []
    for letter in letters:
        if channel == "telephony" and letter in LETTER_SWAPS:
            if rng.random() < 0.4:
                out.append(LETTER_SWAPS[letter])
                continue
        out.append(letter)
    return out


def partials(text, channel="wideband", snr_db=None, seed_key="utt"):
    """Streaming partial hypotheses, one per word of the final.

    The draft pass is greedier with confusions than the final pass, so
    partials visibly revise themselves; the last partial is the final
    transcript from transcribe().
    """
    draft = transcribe(text, channel, snr_db,
                       seed_key + ":draft").split()
    final = transcribe(text, channel, snr_db, seed_key).split()
    out = []
    for i in range(len(final)):
        shown = []
        for j, word in enumerate(final[:i + 1]):
            if j < len(draft) and j >= i - 1:
                shown.append(draft[j])
            else:
                shown.append(word)
        out.append(" ".join(shown))
    return out


def words_to_digits(text):
    """Expand digit words (including 'double x' and chunk words like
    fifteen) into a digit string. Returns None if a token is not a
    digit word."""
    tokens = text.lower().split()
    digits = []
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if tok == "double" and i + 1 < len(tokens) \
                and tokens[i + 1] in DIGIT_WORDS \
                and len(DIGIT_WORDS[tokens[i + 1]]) == 1:
            digits.append(DIGIT_WORDS[tokens[i + 1]] * 2)
            i += 2
            continue
        if tok in DIGIT_WORDS:
            digits.append(DIGIT_WORDS[tok])
            i += 1
            continue
        return None
    return "".join(digits)


def parse_day(text):
    for day in DAY_WORDS:
        if day in text.lower().split():
            return day
    return None


def parse_time(text):
    """Parse a spoken time into 'HH:MM' (24h), or None.

    Stand-in rules, stated so they can be disagreed with: 'half X'
    means X:30 (the British reading used by the fixture callers);
    bare hours one to five are afternoon clinic hours, six to twelve
    are morning.
    """
    tokens = text.lower().split()
    for i, tok in enumerate(tokens):
        if tok == "half" and i + 1 < len(tokens) \
                and tokens[i + 1] in HOUR_WORDS:
            hour = HOUR_WORDS[tokens[i + 1]]
            if hour <= 5:
                hour += 12
            return f"{hour:02d}:30"
        if tok in HOUR_WORDS:
            hour = HOUR_WORDS[tok]
            if hour <= 5:
                hour += 12
            return f"{hour:02d}:00"
    return None
