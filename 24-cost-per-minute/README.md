# Lesson 24: Cost per minute

40 min · Intermediate · Prerequisites: Lessons 11 and 15

Voice agents are billed by the minute, so their economics are arithmetic any builder can do and many skip. The rates here are teaching parameters in `fixtures/rates.json`, stated as such: platform 0.05, transcription 0.008, model 0.024, synthesis 0.02, and telephony 0.009 USD per minute, summing to 0.111 per minute, plus small per-call fixed costs. They are shaped like the real stacks described in RESEARCH.md (where a headline per-minute platform price turned out to be hosting only, and all-in minutes price higher), but they are not quotes, and the lesson's method matters more than its prices: run both reference configurations over the call set and account for every dollar, including the wasted ones.

## Run it

```bash
python3 cost.py
```

As-built: total spend on the twelve calls is 0.761 USD. Six succeed, four of them bookings, at 0.0548 USD per successful booking. The uncomfortable line: 0.4774 USD, 63 percent of all spend, went to calls that failed. Mean call length 0.52 minutes, inflated by repair-exhaustion marathons.

Hardened: total spend falls to 0.6453 USD despite the extra confirmation exchanges, because no call burns minutes failing slowly. All twelve succeed, ten of them bookings. Cost per successful booking rises slightly, to 0.0581, because the successful set now includes the hard calls that are expensive to serve. Waste: zero.

## What the code measures

Two cost truths that survive any rate card. First, failed calls are not free calls: in the as-built run they are the majority of the bill, because failure in voice is slow (repairs, re-asks, escalations at minute prices) while success is quick. Reliability work is therefore a cost programme, not just a quality programme; the hardened system is cheaper overall while doing strictly more work per call. Second, cost per successful booking can rise while the system improves, because the denominator fills with harder successes. A team watching only that ratio would conclude the hardened system is worse value. The honest dashboard shows all four numbers together: total spend, success count, cost per success, and wasted spend. Any one of them alone can be made to lie.

Per-minute thinking also disciplines design: at 0.111 USD a minute, the greeting's 7.6 seconds cost about a cent and a half per call in raw time, before the hangup risk Lesson 17 priced in attention. Small numbers, multiplied by Lesson 25's volumes, become the budget.

## Common failures

- Quoting the platform's headline per-minute price as the cost of a call. The stack has five meters running, and RESEARCH.md shows how the advertised one is often only hosting.
- Averaging cost over all calls instead of over successful outcomes, which hides waste inside a healthy-looking mean.
- Cutting confirmation to save seconds, then paying for wrong bookings in reschedules, no-shows, and support time that never appears in the voice budget.

## Recap checklist

- [ ] You can quote both configurations' total spend and wasted spend
- [ ] You can explain why cost per successful booking rises as the system improves
- [ ] You know the five per-minute components and their sum

## Resources

- The rates as data: [fixtures/rates.json](../fixtures/rates.json)
- Volume, where small costs compound: [Lesson 25](../25-concurrency-and-capacity/README.md)
- Sourced pricing context: [RESEARCH.md](../RESEARCH.md)
