# Lesson 25: Concurrency and capacity

50 min · Intermediate · Prerequisites: Lesson 24

A voice agent that handles one call beautifully can still fail its busiest hour. Capacity for voice is concurrency: how many simultaneous calls the platform can carry, and what happens to callers who arrive when every line is busy. They wait in a queue that, unlike a web queue, they experience as a ringing or silent phone, and they abandon it.

This lesson is a deterministic discrete-event simulation. The demand is a stated teaching day for a platform serving ten BrightSmile-sized clinics at once, which is how voice agents are actually sold: 490 calls over eight hours, hourly volumes of 30, 50, 80, 120, 90, 60, 40, 20, peaking mid-morning. Arrivals within each hour cluster towards the hour boundary, because callers ring when the clock reminds them. Service times cycle through the twelve real durations the hardened system produced on the bundled calls. Callers abandon if their wait would exceed 300 seconds.

## Run it

```bash
python3 capacity.py
```

One concurrent agent: 361 calls served, 129 abandoned (26 percent of the day's demand), mean wait 155.7 seconds for those who stayed. Two agents: 460 served, 30 abandoned, mean wait 104.9 seconds. Four agents: all 490 served, none abandoned, mean wait 38.7 seconds, p95 wait 159.0 seconds.

## What the code measures

The nonlinearity is the lesson. Going from one agent to two does not halve the problem; it removes most abandonments, because queueing pain concentrates at saturation, and mid-morning the single agent is saturated: 120 calls an hour against roughly 30-second calls is a full load before clustering, and clustering pushes it over. The second agent buys headroom, and headroom is what callers experience as being answered.

Note what the simulation is honest about: service times come from the simulated call set, the arrival profile is a stated assumption, and real telephony adds connection setup, ring time, and caller behaviour this model omits. The output is a sizing argument, not a promise. Its proper use is comparative: it tells you the fourth line is worth more than the fifth, and that the cost of Lesson 24's per-minute rates must be multiplied by peak concurrency, not average, when you price capacity, because lines are bought for the busiest quarter-hour.

There is also an interaction with quality: every abandoned call in this simulation is a caller the clinic never hears from, a cost that appears in no voice-platform bill. Capacity is a revenue decision wearing an engineering costume.

## Common failures

- Sizing for the average hour. Queues form at peaks; the average hour forgives everything.
- Assuming arrivals spread evenly. The clustering assumption alone is worth more than an agent in this model, and the exercise proves it.
- Counting only platform cost per line and not the demand lost to abandonment, which is usually the larger number.

## Recap checklist

- [ ] You know the served and abandoned counts for one, two, and four agents
- [ ] You can explain why the second agent helps disproportionately
- [ ] You know which assumption the arrival clustering represents

## Resources

- The per-minute costs that multiply by concurrency: [Lesson 24](../24-cost-per-minute/README.md)
- Call durations feeding the simulation: [Lesson 30](../30-build-the-capstone/README.md)
