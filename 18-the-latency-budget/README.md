# Lesson 18: The latency budget

50 min · Intermediate · Prerequisites: Lessons 02, 06, 12, and 16

This lesson cashes the course's latency work into a single budget and grades four designs against it. The budget comes from the sourced reporting in RESEARCH.md: first audio at p50 under 800 ms reads as responsive, and p95 under 1,500 ms keeps the tail out of the range callers experience as broken. The four designs are the levers built so far, composed: sequential staging with fixed endpointing; streamed with fixed endpointing (the as-built system); streamed with adaptive endpointing; and streamed with adaptive endpointing plus the confirmation layer (the hardened system). Every design runs all twelve bundled calls, and every completed turn's simulated latency to first audio is pooled.

## Run it

```bash
python3 budget.py
```

Sequential with fixed 800 ms endpointing: p50 1,493 ms, p95 1,752 ms, outside the budget on both measures. Streamed with fixed endpointing: p50 1,251 ms, p95 1,391 ms, inside on p95 only. Streamed with adaptive endpointing: p50 742 ms, p95 891 ms, inside on both. Adding confirmation changes neither number (p50 742, p95 891), because confirmation adds exchanges, not waiting; its cost shows up in call duration and repairs, and its benefit shows up in task success, neither of which is a latency measure.

## What the code measures

Read the deltas as a priority list. Streaming the stages bought about 240 ms of p50. Replacing the fixed endpoint with the adaptive policy bought about 510 ms more, the single largest improvement in the course, and it is a policy change, not a faster component. Sequential staging is disqualified on its own: even before endpointing is considered, waiting for full replies and batch transcripts puts the median turn near a second and a half.

The percentiles matter more than any single turn. A design can demo beautifully (the greeting turn streams to 707 ms, Lesson 16) while its pooled p95 sits at 1,752 ms, because the pooled distribution includes slow callers on telephony with long prompts late in calls. Budgets exist to force the pooled view: quote p50 and p95 over a representative call set, or you are quoting the demo.

This table is also the capstone's spine. Lesson 29 turns these two thresholds into fixed gates, with the as-built row as the baseline they must beat, and Lesson 31 grades the final system against them.

## Common failures

- Budgeting to the mean. Means hide the tail that hangs up.
- Spending on model latency while endpointing is unexamined; here the model was never the bottleneck.
- Believing a design is within budget because its best turn is. The pooled p95 is the budget's unit of account.

## Recap checklist

- [ ] You can quote all four designs' p50 and p95
- [ ] You know which single change bought the most latency
- [ ] You can explain why confirmation is latency-neutral here

## Resources

- The gates these thresholds become: [Lesson 29](../29-capstone-spec/README.md)
- What the tail does to callers: [Lesson 19](../19-turn-taking/README.md)
- Sourced budget ranges: [RESEARCH.md](../RESEARCH.md)
