# Solution, Lesson 19

At 800 ms patience the as-built system puts all 39 of its turns (100.0 percent) over the line, and the hardened system puts 20 of its 41 turns (48.8 percent) over it.

So even the hardened system's median turn sits close enough to 800 ms that half its turns exceed a strict caller's patience, even though none exceed 1,200 ms. Lesson 02's ledger tells you where the remainder concentrates: the model's first-token stage grows with prompt size as calls progress, and the endpointing decision time is a floor under every turn, so late turns on long calls are the slow ones. The design conclusion is that 742 ms p50 is within the published budget but not comfortably inside human patience; the budget is a floor for competence, not a definition of good.
