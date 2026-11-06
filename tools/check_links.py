#!/usr/bin/env python3
"""Check that every relative link in the course markdown resolves.

Scans all .md files under the repo root (skipping .git), extracts
Markdown links, and verifies that relative targets exist on disk.
External (http/https/mailto) links and in-page anchors are skipped.

Run from the repo root: python3 tools/check_links.py
Exit code 0 means no broken relative links.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")

broken = []
checked = 0

for md in sorted(ROOT.rglob("*.md")):
    if ".git" in md.parts:
        continue
    text = md.read_text(encoding="utf-8")
    for target in LINK_RE.findall(text):
        target = target.strip()
        if not target or target.startswith(("#", "http://", "https://",
                                            "mailto:")):
            continue
        path_part = target.split("#")[0]
        if not path_part:
            continue
        checked += 1
        resolved = (md.parent / path_part).resolve()
        if not resolved.exists():
            broken.append(f"{md.relative_to(ROOT)} -> {target}")

if broken:
    print("BROKEN LINKS")
    for item in broken:
        print(" -", item)
    sys.exit(1)
print(f"links OK: {checked} relative links checked, 0 broken")
