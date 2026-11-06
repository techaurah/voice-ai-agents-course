# Solution, Lesson 29

Both hypothetical gates are stricter than the baseline: 0.95 exceeds the baseline success rate of 0.5, and 1,200 ms is below the baseline p95 of 1,391 ms.

The configuration a 1,200 ms p95 gate additionally threatens is the sequential-with-fixed-endpointing design from Lesson 18 only in passing; the live threat is to the streamed fixed-endpointing design (p95 1,391 ms, already equal to the baseline) and, more importantly, it would leave the passing designs almost no headroom: the hardened system's p95 is 891 ms, so it still passes, but any future fixture or stand-in change that added tail latency would fail a gate that was tightened for elegance rather than need. The argument for leaving the gates at their sourced values is that 800 and 1,500 ms come from the published budget in RESEARCH.md, not from what this implementation happens to achieve. A gate should encode what callers need, not what the current build can clear, in either direction.
