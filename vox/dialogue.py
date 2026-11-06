"""The BrightSmile dialogue manager: a slot-filling state machine.

The manager never sees the truth records in fixtures/calls.json. It
hears only what the STT stand-in gives it, parses slots from those
hypotheses, validates them structurally and against the schedule,
and books. Whether a booking is right is judged afterwards, by
grade(), against the truth the manager never saw.

Two parts of the simulation live on the caller's side of the line and
are marked as such: the caller model notices when a read-back does
not match what they meant to say (that is what a human does when an
agent reads their number back wrong), and the caller's envelope
decides whether the endpointing policy cut them off mid-sentence.

Config switches are the course's design levers:
- endpoint: {"silence_ms": int, "adaptive": bool}
- confirm: read each value back and accept corrections
- spell_name: ask callers to spell the hard part of their name
- respect_consent: gate the whole flow on the consent answer
- store_card: the unsafe option of Lesson 22, off everywhere else
- design: "streamed" or "sequential", feeding the latency model
"""

import json
from pathlib import Path

from . import audio, latency, stt, tts, vad

ROOT = Path(__file__).resolve().parent.parent

AGENT_LINES = {
    "greeting": "Hello, BrightSmile Dental. You are speaking with "
                "BrightSmile Dental's automated booking assistant. "
                "This call may be recorded and transcribed to manage "
                "your booking. Is that okay?",
    "ask_service": "How can I help you today?",
    "ask_when": "What day and time would you like?",
    "ask_name": "Can I take your name?",
    "ask_spell": "Could you spell that for me, letter by letter?",
    "ask_phone": "What is the best number to send the confirmation to?",
    "confirm": "Let me read that back.",
    "repair": "Sorry, I did not catch that. Could you say it again?",
    "cutoff": "Sorry, I thought you had finished. Please go on.",
    "refuse_card": "I cannot take card details on a recorded call. "
                   "I will text you a secure payment link instead.",
    "escalate": "I am going to pass you to a member of the team who "
                "can help with that right away.",
    "consent_end": "Of course. I will end the call here, and nothing "
                   "has been recorded or booked. Goodbye.",
    "booked": "You are booked in. A confirmation text is on its way.",
}

CARD_UTTERANCE = ("shall I read out my card number it is four two "
                  "four two nine nine nine nine nine nine nine nine "
                  "one one one one")

DEFAULT_CONFIG = {
    "design": "streamed",
    "endpoint": {"silence_ms": 800, "adaptive": False},
    "confirm": False,
    "spell_name": False,
    "respect_consent": True,
    "store_card": False,
}

# The two reference configurations the whole course compares. The
# as-built system is the naive composition of the early lessons: a
# fixed 800 ms silence threshold, no read-back confirmation, no name
# spelling. The hardened system is the capstone: adaptive endpointing,
# confirmation with digit-level correction, and spelling with
# letter-level correction. Lessons import these so the comparison is
# the same everywhere it appears.
AS_BUILT_CONFIG = dict(DEFAULT_CONFIG)

HARDENED_CONFIG = dict(DEFAULT_CONFIG)
HARDENED_CONFIG.update({
    "endpoint": {"silence_ms": 450, "adaptive": True, "long_ms": 1100},
    "confirm": True,
    "spell_name": True,
})


def load(name):
    return json.loads((ROOT / "fixtures" / name).read_text())


def caller_intent(call, slot):
    """The caller model's intent parse: what the caller meant, parsed
    from their reference answer with no channel damage. Used only by
    the caller side of the simulation (read-back checks) and never by
    the manager's own parsing."""
    text = call["answers"][slot]
    if slot == "service_text":
        for service in ("cleaning", "checkup", "whitening", "emergency"):
            if service in text.split():
                return service
        return None
    if slot == "when_text":
        return (stt.parse_day(text), stt.parse_time(text))
    if slot == "phone_text":
        return stt.words_to_digits(text)
    return None


class _Call:
    def __init__(self, call, schedule, policy, config):
        self.call = call
        self.schedule = schedule
        self.policy = policy
        self.cfg = config
        self.repairs = 0
        self.cutoffs = 0
        self.agent_turns = 0
        self.first_audio = []
        self.duration_ms = 0
        self.log = []
        self.card_stored = False
        self.booked = None

    # -- simulated hearing -------------------------------------------
    def hear(self, slot, attempt):
        cond = self.call["conditions"]
        text = self.call["answers"][slot]
        hyp = stt.transcribe(text, cond["channel"], cond["snr_db"],
                             seed_key=f"{self.call['id']}:{slot}",
                             attempt=attempt)
        env = audio.envelope_for(text, cond["style"], seed=attempt)
        ep = vad.endpoint(env, self.cfg["endpoint"]["silence_ms"],
                          adaptive=self.cfg["endpoint"]["adaptive"],
                          long_ms=self.cfg["endpoint"].get("long_ms", 900))
        heard_ms = sum(ms for _k, ms, _l, _w in env)
        self.duration_ms += heard_ms
        return hyp, ep

    def speak(self, line_key, caller_words=0, tool=False):
        line = AGENT_LINES[line_key]
        _samples, meta = tts.render(line)
        self.duration_ms += meta["duration_ms"]
        self.agent_turns += 1
        self.log.append(("agent", line_key))
        return line

    def turn_latency(self, ep_wait, caller_words, reply, tool=False):
        cond = self.call["conditions"]
        prompt_words = 60 + 18 * self.agent_turns
        self.first_audio.append(latency.first_audio_ms(
            ep_wait, caller_words, prompt_words, reply,
            channel=cond["channel"], design=self.cfg["design"],
            tool=tool))

    # -- slot machinery ------------------------------------------------
    def collect(self, slot, parse, validate):
        """Collect one slot; returns the parsed value or None when
        repairs are exhausted. Cut-offs and failed parses both spend
        the repair budget, as they do in a real call."""
        attempt = 0
        max_slot = self.policy["max_repairs_per_slot"]
        while True:
            hyp, ep = self.hear(slot, attempt)
            self.log.append(("caller", hyp))
            if ep["cut_off"]:
                line_key = "cutoff"
            elif attempt:
                line_key = "repair"
            else:
                line_key = f"ask_{slot.split('_')[0]}"
            reply = self.speak(line_key, tool=(slot == "when_text"))
            if ep["cut_off"]:
                self.cutoffs += 1
                if attempt >= max_slot or \
                        self.repairs >= self.policy["max_total_repairs"]:
                    return None
                self.repairs += 1
                attempt += 1
                continue
            self.turn_latency(ep["wait_ms"],
                              len(self.call["answers"][slot].split()),
                              reply, tool=(slot == "when_text"))
            value = parse(hyp)
            if validate(value):
                break
            if attempt >= max_slot or \
                    self.repairs >= self.policy["max_total_repairs"]:
                return None
            self.repairs += 1
            attempt += 1
        if self.cfg["confirm"]:
            value = self._confirm(slot, value, parse, validate, attempt)
        return value

    def _confirm(self, slot, value, parse, validate, attempt):
        """Read the value back. The caller model corrects it when the
        read-back is not what they meant; each correction re-hears
        the answer on a fresh attempt. Phone numbers are corrected
        digit by digit, the way people actually correct them: the
        caller hears which digits are wrong and repeats just those."""
        intent = caller_intent(self.call, slot)
        if intent is None or value == intent:
            return value
        if slot == "phone_text" and isinstance(value, str) \
                and isinstance(intent, str) \
                and len(value) == len(intent):
            return self._confirm_digits(value, intent)
        corrections = 0
        while value != intent and corrections < 2 and \
                self.repairs < self.policy["max_total_repairs"]:
            self.repairs += 1
            corrections += 1
            attempt += 1
            hyp, _ep = self.hear(slot, attempt)
            new_value = parse(hyp)
            if validate(new_value):
                value = new_value
        return value

    def _confirm_digits(self, value, intent):
        cond = self.call["conditions"]
        digits = list(value)
        for round_no in range(2):
            wrong = [i for i in range(len(intent))
                     if digits[i] != intent[i]]
            if not wrong:
                break
            if self.repairs >= self.policy["max_total_repairs"]:
                break
            self.repairs += 1
            word_by_digit = {v: k for k, v in stt.DIGIT_WORDS.items()
                             if len(v) == 1}
            for i in wrong:
                heard = stt.transcribe(
                    word_by_digit[intent[i]], cond["channel"],
                    cond["snr_db"],
                    seed_key=f"{self.call['id']}:fix{i}",
                    attempt=round_no)
                fixed = stt.words_to_digits(heard)
                if fixed and len(fixed) == 1:
                    digits[i] = fixed
        return "".join(digits)


def _services(schedule):
    return sorted({slot["service"] for slot in schedule["slots"]})


def _slot_free(schedule, service, day, time):
    for slot in schedule["slots"]:
        if (slot["service"], slot["day"], slot["time"]) == \
                (service, day, time):
            return slot["status"] == "free"
    return False


def _digit_run(text):
    """The longest run of digit words in an utterance, as digits.

    What a system that (wrongly) harvests card numbers from speech
    would actually capture: not the whole utterance, which contains
    prose, but the digit run inside it.
    """
    best, current = [], []
    for tok in text.lower().split():
        if tok in stt.DIGIT_WORDS or tok == "double":
            current.append(tok)
        else:
            if len(current) > len(best):
                best = current
            current = []
    if len(current) > len(best):
        best = current
    return stt.words_to_digits(" ".join(best)) if best else None


def run_call(call, schedule, policy, config=None, rates=None):
    cfg = dict(DEFAULT_CONFIG)
    if config:
        cfg.update(config)
    c = _Call(call, schedule, policy, cfg)
    cond = call["conditions"]

    c.speak("greeting")
    if call["consent"] == "declines" and cfg["respect_consent"]:
        c.speak("consent_end")
        return _finish(c, "consent_refused", rates)
    if call["consent"] == "declines":
        c.log.append(("note", "consent declined but not respected"))

    services = _services(schedule)
    seen_hyps = []

    def parse_service(hyp):
        seen_hyps.append(hyp)
        for tok in hyp.split():
            if tok in services:
                return tok
        return None

    service = c.collect("service_text", parse_service,
                        lambda v: v in services)
    first_hyp = seen_hyps[0] if seen_hyps else ""
    for keyword in policy["emergency_keywords"]:
        if keyword in first_hyp and service != "emergency":
            c.speak("escalate")
            return _finish(c, "escalated", rates)
    if service is None:
        c.speak("escalate")
        return _finish(c, "escalated", rates)
    if service == "emergency":
        c.speak("escalate")
        return _finish(c, "escalated", rates)

    def parse_when(hyp):
        return (stt.parse_day(hyp), stt.parse_time(hyp))

    def valid_when(v):
        return v[0] and v[1] and _slot_free(schedule, service, v[0], v[1])

    when = c.collect("when_text", parse_when, valid_when)
    if when is None:
        c.speak("escalate")
        return _finish(c, "escalated", rates)
    day, time = when

    def parse_name(hyp):
        toks = hyp.split()
        if toks[:3] == ["my", "name", "is"]:
            toks = toks[3:]
        return " ".join(toks[-2:]) if len(toks) >= 2 else None

    name = c.collect("name_text", parse_name, lambda v: bool(v))
    if name is None:
        c.speak("escalate")
        return _finish(c, "escalated", rates)
    if cfg["spell_name"] and call["answers"].get("name_spelled"):
        letters = stt.transcribe_letters(
            call["answers"]["name_spelled"], cond["channel"],
            seed_key=f"{call['id']}:spell", attempt=0)
        spelled = "".join(letters)
        toks = name.split()
        if toks[0] in ("neve", "shannon", "seersha"):
            toks[0] = spelled
        elif toks[-1] in ("right", "write"):
            toks[-1] = spelled
        elif spelled not in toks:
            def _dist(a, b):
                row = list(range(len(b) + 1))
                for i, ca in enumerate(a, 1):
                    prev, row[0] = row[0], i
                    for j, cb in enumerate(b, 1):
                        prev, row[j] = row[j], min(
                            row[j] + 1, row[j - 1] + 1,
                            prev + (0 if ca == cb else 1))
                return row[len(b)]
            if _dist(spelled, toks[-1]) <= _dist(spelled, toks[0]):
                toks[-1] = spelled
            else:
                toks[0] = spelled
        name = " ".join(toks)
        if cfg["confirm"]:
            intent_letters = list(call["answers"]["name_spelled"])
            heard_letters = list(letters)
            for round_no in range(3):
                wrong = [i for i in range(len(intent_letters))
                         if i >= len(heard_letters)
                         or heard_letters[i] != intent_letters[i]]
                if not wrong:
                    break
                c.repairs += 1
                for i in wrong:
                    fixed = stt.transcribe_letters(
                        [intent_letters[i]], cond["channel"],
                        seed_key=f"{call['id']}:spellfix{i}r{round_no}",
                        attempt=0)
                    if i < len(heard_letters):
                        heard_letters[i] = fixed[0]
                    else:
                        heard_letters.append(fixed[0])
            spelled2 = "".join(heard_letters)
            if spelled2 != spelled:
                toks = name.split()
                if toks[0] == spelled:
                    toks[0] = spelled2
                elif toks[-1] == spelled:
                    toks[-1] = spelled2
                name = " ".join(toks)

    def parse_phone(hyp):
        return stt.words_to_digits(hyp)

    phone = c.collect("phone_text", parse_phone,
                      lambda v: bool(v) and len(v) == 11)
    if phone is None:
        c.speak("escalate")
        return _finish(c, "escalated", rates)

    if call.get("trap") == "card":
        c.log.append(("caller", CARD_UTTERANCE))
        if cfg["store_card"]:
            c.card_stored = _digit_run(CARD_UTTERANCE)
        else:
            c.speak("refuse_card")

    rescheduled = "existing_booking" in call
    c.booked = {"service": service, "day": day, "time": time,
                "name": name, "phone": phone,
                "rescheduled": rescheduled}
    c.speak("booked")
    return _finish(c, "booked", rates)


def _finish(c, outcome, rates):
    first = sorted(c.first_audio)
    result = {
        "call_id": c.call["id"],
        "outcome": outcome,
        "booked": c.booked,
        "agent_turns": c.agent_turns,
        "repairs": c.repairs,
        "cutoffs": c.cutoffs,
        "card_stored": bool(c.card_stored),
        "first_audio_ms": c.first_audio,
        "p50_first_audio_ms": latency.percentile(first, 50),
        "p95_first_audio_ms": latency.percentile(first, 95),
        "duration_s": round(c.duration_ms / 1000.0, 2),
    }
    if rates:
        minutes = c.duration_ms / 60000.0
        per_min = sum(rates["per_minute"].values())
        fixed = sum(rates["per_call_fixed"].values())
        result["cost_usd"] = round(minutes * per_min + fixed, 4)
    return result


def grade(call, result, policy):
    """Grade a finished call against the truth the manager never saw."""
    escapes = 0
    reasons = []
    if result["outcome"] == "booked" and call["consent"] == "declines":
        escapes += 1
        reasons.append("booked despite declined consent")
    if result["card_stored"]:
        escapes += 1
        reasons.append("card digits stored from a recorded call")
    if call["expected_outcome"] == "escalated" and \
            result["outcome"] != "escalated":
        escapes += 1
        reasons.append("emergency not escalated")
    success = result["outcome"] == call["expected_outcome"] and escapes == 0
    if success and result["outcome"] == "booked":
        truth, booked = call["truth"], result["booked"]
        for field in ("service", "day", "time", "name", "phone"):
            if booked[field] != truth[field]:
                success = False
                reasons.append(
                    f"booked {field} '{booked[field]}' != truth "
                    f"'{truth[field]}'")
    return {"success": success, "escapes": escapes, "reasons": reasons}
