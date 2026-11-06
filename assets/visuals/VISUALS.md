# Visuals

Branded SVG diagrams for the course README and lessons. Regenerate them with:

```bash
python3 generate_visuals.py
```

| File | What it shows | Source of its numbers |
|---|---|---|
| `course-map.svg` | The 10 modules and 32 lessons | Course structure |
| `latency-ledger.svg` | Simulated latency stage totals and shares over 24 turns | Lesson 02 |
| `wer-by-condition.svg` | Word error rate by channel and SNR band, with cell counts | Lesson 08 |
| `endpointing.svg` | Cut-offs and completed-turn waits for three endpointing policies | Lesson 06 |
| `failure-taxonomy.svg` | Failure categories across the 60-run fault suite | Lesson 28 |
| `capstone-gates.svg` | The gate table: as-built versus capstone against the fixed gates | Lessons 29 to 31 |

Style: white canvas, navy `#0B1F4A`, light blue `#E0F2FE`, cyan `#0891B2`, amber `#F59E0B`. Every number in a visual is produced by the course's own code on the bundled fixtures, and each subtitle names the lesson it comes from.
