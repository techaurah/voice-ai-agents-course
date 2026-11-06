#!/usr/bin/env python3
"""Validate the structure and internal consistency of this course.

Checks, from the repo root:
- all 32 lesson folders exist, each with README.md, exercise.md,
  smoke_test.py, solution/SOLUTION.md, and at least one runnable
  Python artifact besides the smoke test
- every lesson README carries the five required sections and is
  more than 800 characters
- no em dashes anywhere in the repo's text files
- the fixtures parse and agree with each other: call truth records
  match what the caller-intent parse of the answers produces, and
  every expected booking corresponds to a free schedule slot
- the capstone gates file exists with all five gate keys

Run from the repo root: python3 tools/validate_course.py
Exit code 0 means the course is structurally sound. Behavioural
correctness is the smoke tests' job; this checks the frame.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

LESSON_DIRS = [
    "00-course-setup", "01-what-makes-it-voice", "02-the-latency-ledger",
    "03-capturing-audio", "04-the-telephone-channel",
    "05-voice-activity-detection", "06-endpointing",
    "07-the-stt-standin", "08-noise-as-a-data-problem",
    "09-numbers-and-names", "10-streaming-partials",
    "11-the-dialogue-manager", "12-confirmation-and-repair",
    "13-tool-calls-mid-call", "14-speaking-output",
    "15-the-tts-standin", "16-streaming-synthesis", "17-barge-in",
    "18-the-latency-budget", "19-turn-taking", "20-voice-failure-modes",
    "21-consent-and-disclosure", "22-sensitive-data",
    "23-escalation-and-handoff", "24-cost-per-minute",
    "25-concurrency-and-capacity", "26-evaluating-transcripts",
    "27-evaluating-conversations", "28-failure-taxonomy",
    "29-capstone-spec", "30-build-the-capstone",
    "31-evaluate-and-harden",
]

REQUIRED_LESSON_FILES = ["README.md", "exercise.md", "smoke_test.py",
                         "solution/SOLUTION.md"]
REQUIRED_SECTIONS = ["## Run it", "## What the code measures",
                     "## Common failures", "## Recap checklist",
                     "## Resources"]
ROOT_FILES = ["README.md", "AGENTS.md", "CHANGELOG.md",
              "CODE_OF_CONDUCT.md", "CONTRIBUTING.md", "DESIGN.md",
              "LICENSE", "PROGRESS.md", "RESEARCH.md", "SECURITY.md",
              "llms.txt", "requirements.txt", ".gitignore",
              ".github/workflows/ci.yml", "tools/README.md",
              "assets/README.md", "resources/README.md",
              "showcase/README.md", "translations/README.md"]

problems = []


def check(cond, message):
    if not cond:
        problems.append(message)


for name in ROOT_FILES:
    check((ROOT / name).is_file(), f"missing root file: {name}")

for lesson in LESSON_DIRS:
    folder = ROOT / lesson
    check(folder.is_dir(), f"missing lesson folder: {lesson}")
    if not folder.is_dir():
        continue
    for required in REQUIRED_LESSON_FILES:
        check((folder / required).is_file(),
              f"{lesson}: missing {required}")
    artifacts = [p for p in folder.glob("*.py")
                 if p.name != "smoke_test.py"]
    check(len(artifacts) >= 1,
          f"{lesson}: no runnable artifact besides smoke_test.py")
    readme = folder / "README.md"
    if readme.is_file():
        text = readme.read_text(encoding="utf-8")
        check(len(text) > 800, f"{lesson}: README too short")
        for section in REQUIRED_SECTIONS:
            check(section in text,
                  f"{lesson}: README missing section {section}")

for path in ROOT.rglob("*"):
    if ".git" in path.parts or "__pycache__" in path.parts:
        continue
    if path.is_file() and path.suffix in (".md", ".py", ".txt",
                                          ".json", ".yml"):
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        check("\u2014" not in content,
              f"em dash found in {path.relative_to(ROOT)}")

# Fixture consistency
from vox import stt  # noqa: E402
from vox.dialogue import caller_intent  # noqa: E402

transcripts = json.loads((ROOT / "fixtures" / "transcripts.json")
                         .read_text())
utterances = transcripts["utterances"]
check(len(utterances) == 24, "transcripts.json must hold 24 utterances")
check(len({u["id"] for u in utterances}) == 24,
      "transcript ids must be unique")

schedule = json.loads((ROOT / "fixtures" / "schedule.json").read_text())
free_slots = {(s["service"], s["day"], s["time"])
              for s in schedule["slots"] if s["status"] == "free"}

calls = json.loads((ROOT / "fixtures" / "calls.json").read_text())["calls"]
check(len(calls) == 12, "calls.json must hold 12 calls")
for call in calls:
    answers, truth = call["answers"], call["truth"]
    parsed_phone = stt.words_to_digits(answers["phone_text"])
    check(parsed_phone == truth["phone"],
          f"{call['id']}: truth phone {truth['phone']} != parsed "
          f"answer {parsed_phone}")
    check(len(truth["phone"]) == 11,
          f"{call['id']}: truth phone is not 11 digits")
    service = caller_intent(call, "service_text")
    if truth["service"] is not None and service is not None:
        check(service == truth["service"],
              f"{call['id']}: intent service {service} != truth "
              f"{truth['service']}")
    if truth["day"] is not None:
        day_time = caller_intent(call, "when_text")
        check(day_time == (truth["day"], truth["time"]),
              f"{call['id']}: intent when {day_time} != truth "
              f"({truth['day']}, {truth['time']})")
    if call["expected_outcome"] == "booked":
        slot = (truth["service"], truth["day"], truth["time"])
        check(slot in free_slots,
              f"{call['id']}: expected booking {slot} is not a free slot")

gates_path = ROOT / "29-capstone-spec" / "capstone" / "gates.json"
check(gates_path.is_file(), "capstone gates file missing")
if gates_path.is_file():
    spec = json.loads(gates_path.read_text())
    check(spec.get("fixed_on") == "2026-11-06",
          "gates file must record fixed_on 2026-11-06")
    gates = spec["capstone_system"]["gates"]
    for key in ("task_success_rate_min", "policy_escapes_max",
                "p50_first_audio_ms_max", "p95_first_audio_ms_max",
                "mean_repairs_per_call_max"):
        check(key in gates, f"gates file missing key {key}")

if problems:
    print("COURSE PROBLEMS")
    for problem in problems:
        print(" -", problem)
    sys.exit(1)
print(f"course structure OK: {len(LESSON_DIRS)} lessons, fixtures "
      f"consistent, gates present")
