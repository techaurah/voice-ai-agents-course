"""Lesson 25 artifact: how many lines does the diary need?

A deterministic discrete-event simulation. The arrival profile is a
stated teaching day for a platform serving ten BrightSmile-sized
clinics at once, which is how voice agents are actually sold: 490
calls across eight hours, peaking mid-morning. Service times cycle through the twelve real
call durations the hardened system produced on the bundled set.
Callers abandon if they would wait more than 300 seconds. The
simulation is run for one, two, and four concurrent agents (lines),
and reports mean and p95 wait plus abandonments.
"""
import heapq
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from vox import dialogue, latency, metrics  # noqa: E402

CALLS_PER_HOUR = [30, 50, 80, 120, 90, 60, 40, 20]
PATIENCE_S = 300


def arrivals():
    """Arrival times within each hour cluster towards the hour
    boundary: callers ring when the clock reminds them, not evenly.
    The cubic bias is the stated teaching assumption; Lesson 25's
    exercise replaces it with an even spread and watches the queues
    vanish."""
    rng = random.Random("capacity-day")
    times = []
    for hour, count in enumerate(CALLS_PER_HOUR):
        for _ in range(count):
            times.append(hour * 3600 + int(rng.random() ** 3 * 1800))
    return sorted(times)


def simulate(n_agents, service_times, arrival_times):
    free = [0] * n_agents
    heapq.heapify(free)
    waits = []
    abandoned = 0
    for i, at in enumerate(arrival_times):
        earliest = heapq.heappop(free)
        wait = max(0, earliest - at)
        if wait > PATIENCE_S:
            abandoned += 1
            heapq.heappush(free, earliest)
            continue
        waits.append(wait)
        heapq.heappush(free, max(earliest, at) +
                       service_times[i % len(service_times)])
    return {
        "agents": n_agents,
        "served": len(waits),
        "abandoned": abandoned,
        "mean_wait_s": round(metrics.mean(waits), 1) if waits else 0,
        "p95_wait_s": round(latency.percentile(waits, 95), 1) if waits else 0,
    }


def evaluate():
    calls = dialogue.load("calls.json")["calls"]
    schedule = dialogue.load("schedule.json")
    policy = dialogue.load("policy.json")
    rates = dialogue.load("rates.json")
    durations = []
    for call in calls:
        result = dialogue.run_call(call, schedule, policy,
                                   dialogue.HARDENED_CONFIG, rates)
        durations.append(result["duration_s"])
    times = arrivals()
    return {
        "calls_in_day": len(times),
        "patience_s": PATIENCE_S,
        "results": [simulate(n, durations, times) for n in (1, 2, 4)],
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2, sort_keys=True))
