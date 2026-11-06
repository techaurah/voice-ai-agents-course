# Solution, Lesson 31

The middle system measures: success rate 0.5, escapes 0, p50 742 ms, p95 891 ms, mean repairs 0.0. It passes four of the five gates, failing only task success.

That pattern is the most useful diagnostic in the course. A system that is fast enough and safe but still failing is not failing on experience or on compliance; it is failing on the transaction itself, in this case on values it hears wrong and never checks. The next unit of work belongs to the confirmation layer and nothing else: not a faster model (latency already passes), not more safety machinery (escapes already zero), and not more endpointing (the slow callers already complete their turns). Gate tables earn their keep by making that allocation argument unavoidable.
