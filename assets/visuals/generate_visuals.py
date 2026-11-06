#!/usr/bin/env python3
"""Generate the course's SVG visuals.

White canvas, navy headings, cyan accents, measured numbers only.
Every figure quoted in a visual is produced by the course's own code
on the bundled fixtures (see the lesson cited in each subtitle).
Run: python3 generate_visuals.py
"""

import os

HERE = os.path.dirname(os.path.abspath(__file__))
NAVY = "#0B1F4A"
CYAN = "#0891B2"
LIGHT = "#E0F2FE"
AMBER = "#F59E0B"
GREY = "#475569"
RED = "#DC2626"
GREEN = "#059669"


def save(name, svg):
    path = os.path.join(HERE, name)
    with open(path, "w") as f:
        f.write(svg)
    print("wrote", name)


def head(w, h, title, subtitle):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<rect width="{w}" height="{h}" fill="white"/>
<text x="48" y="64" font-family="Georgia, serif" font-size="30" fill="{NAVY}" font-weight="bold">{title}</text>
<text x="48" y="94" font-family="Georgia, serif" font-size="16" fill="{GREY}">{subtitle}</text>
'''


def foot(w, h, text):
    return f'''<text x="48" y="{h - 24}" font-family="Georgia, serif" font-size="13" fill="{GREY}">{text}</text>
</svg>'''


def bar(x, y, w, h, color):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}"/>'


def label(x, y, text, size=15, color=NAVY, anchor="start", bold=False):
    weight = ' font-weight="bold"' if bold else ""
    return (f'<text x="{x}" y="{y}" font-family="Georgia, serif" '
            f'font-size="{size}" fill="{color}" text-anchor="{anchor}"'
            f'{weight}>{text}</text>')


MODULES = [
    ("0", "Foundations", "00-02"),
    ("1", "Audio in", "03-06"),
    ("2", "Speech to text", "07-10"),
    ("3", "Dialogue", "11-14"),
    ("4", "Speech out", "15-17"),
    ("5", "Real-time behaviour", "18-20"),
    ("6", "Safety and consent", "21-23"),
    ("7", "Cost and scale", "24-25"),
    ("8", "Evaluation", "26-28"),
    ("9", "Capstone", "29-31"),
]
svg = head(960, 620, "Voice AI Agents: course map",
           "10 modules, 32 lessons, one running scenario: the BrightSmile Dental booking line")
for i, (num, name, rng) in enumerate(MODULES):
    col = i % 2
    row = i // 2
    x = 48 + col * 440
    y = 140 + row * 88
    svg += bar(x, y, 400, 64, LIGHT)
    svg += label(x + 16, y + 28, f"Module {num}: {name}", 17, NAVY, bold=True)
    svg += label(x + 16, y + 52, f"Lessons {rng}", 14, GREY)
svg += foot(960, 620, "Every lesson is runnable offline, Python standard library only.")
save("course-map.svg", svg)

STAGES = [("Endpointing", 19200, "64.5%"), ("Model first token", 5041, "16.9%"),
          ("Synthesis first chunk", 3157, "10.6%"),
          ("Transcription final", 1407, "4.7%"), ("Jitter", 960, "3.2%")]
svg = head(960, 480, "The latency ledger",
           "Simulated stage totals over 24 fixture turns, streamed design (Lesson 02)")
maxv = STAGES[0][1]
for i, (name, ms, share) in enumerate(STAGES):
    y = 150 + i * 56
    svg += label(48, y + 22, name, 16)
    svg += bar(300, y, int(560 * ms / maxv), 28, CYAN if i == 0 else NAVY)
    svg += label(876, y + 22, f"{ms:,} ms ({share})", 15, NAVY, anchor="end")
svg += foot(960, 480, "Two thirds of the wait is a policy decision: how much silence ends a turn.")
save("latency-ledger.svg", svg)

CONDITIONS = [("telephony clean", 0.0848, 7), ("telephony snr12", 0.0, 2),
              ("telephony snr8", 0.1, 2), ("telephony snr5", 0.2222, 1),
              ("wideband clean", 0.0321, 7), ("wideband snr12", 0.037, 3),
              ("wideband snr8", 0.0, 1), ("wideband snr5", 0.3333, 1)]
svg = head(960, 640, "Word error rate by condition",
           "STT stand-in on the fixture set; small cells are anecdotes with means (Lesson 08)")
for i, (name, wer, n) in enumerate(CONDITIONS):
    y = 140 + i * 52
    svg += label(48, y + 22, name, 15)
    svg += bar(300, y, int(480 * wer / 0.3333), 26, AMBER if n < 3 else CYAN)
    svg += label(800, y + 22, f"{wer} (n={n})", 15, NAVY)
svg += foot(960, 640, "Amber cells have n under 3: read the counts before the means.")
save("wer-by-condition.svg", svg)

POLICIES = [("Fixed 400 ms", 3, "400 ms"), ("Fixed 800 ms", 3, "800 ms"),
            ("Adaptive 450 ms", 1, "300 ms")]
svg = head(960, 400, "Endpointing: cut-offs and wait",
           "Slow utterances cut off, of 3 in the fixture set; wait on completed turns (Lesson 06)")
for i, (name, cuts, wait) in enumerate(POLICIES):
    y = 150 + i * 64
    svg += label(48, y + 24, name, 16)
    svg += bar(300, y, cuts * 140, 30, RED if cuts == 3 else GREEN)
    svg += label(760, y + 24, f"{cuts} cut off, waits {wait}", 15, NAVY)
svg += foot(960, 400, "The adaptive policy waits longer mid-utterance so it can wait less at the end.")
save("endpointing.svg", svg)

CATS = [("Transcription: digits", 10), ("Repair exhaustion", 4),
        ("Consent escape", 1), ("Payment escape", 1)]
svg = head(960, 420, "Failure taxonomy",
           "16 failures across a 60-run fault-injection suite (Lesson 28)")
for i, (name, count) in enumerate(CATS):
    y = 150 + i * 56
    svg += label(48, y + 22, name, 16)
    svg += bar(340, y, count * 52, 28, RED if "escape" in name else NAVY)
    svg += label(880, y + 22, str(count), 16, NAVY, anchor="end", bold=True)
svg += foot(960, 420, "Escapes are singletons by count and first-order by importance.")
save("failure-taxonomy.svg", svg)

ROWS = [("Task success rate", "0.5", "1.0", "min 0.9"),
        ("Policy escapes", "0", "0", "max 0"),
        ("p50 first audio", "1251 ms", "742 ms", "max 800 ms"),
        ("p95 first audio", "1391 ms", "891 ms", "max 1500 ms"),
        ("Mean repairs per call", "0.5", "0.58", "max 1.5")]
svg = head(960, 520, "Capstone gate table",
           "Gates fixed 2026-11-06 before the capstone was built (Lessons 29 to 31)")
svg += label(48, 140, "Gate", 15, GREY, bold=True)
svg += label(400, 140, "As-built", 15, GREY, bold=True)
svg += label(570, 140, "Capstone", 15, GREY, bold=True)
svg += label(740, 140, "Gate", 15, GREY, bold=True)
for i, (name, asb, cap, gate) in enumerate(ROWS):
    y = 180 + i * 56
    passed = i in (1, 3, 4)
    svg += label(48, y + 22, name, 16)
    svg += label(400, y + 22, asb, 16, GREEN if passed else RED)
    svg += label(570, y + 22, cap, 16, GREEN)
    svg += label(740, y + 22, gate, 15, GREY)
svg += label(48, 492 - 24, "As-built passes 3 of 5 gates. Capstone passes 5 of 5.", 15, NAVY, bold=True)
svg += "</svg>"
save("capstone-gates.svg", svg)
