# Lesson 12: Confirmation and repair

50 min · Intermediate · Prerequisites: Lesson 11

Lesson 11 ended with a booking that every structural check passed and that was wrong. The defence is the oldest one in telephony: read the value back and let the caller correct it. This lesson isolates that layer. Both configurations use adaptive endpointing, so slow speakers are no longer cut off; the only difference is confirmation: off (values booked as first heard, names taken as recognised) versus on (read-back with digit-level correction for phone numbers, spelling with letter-level correction for names, as designed in Lesson 09).

## Run it

```bash
python3 repair.py
```

Without confirmation: 6 of 12 calls succeed. The failures are call-01, call-02, call-04, call-06, call-08, and call-11, every one of them a booked call with a wrong value, a phone digit or a name, written into the diary. Mean repairs are 0.0, because the system never notices anything to repair.

With confirmation: 12 of 12 succeed. Mean repairs rise to 0.58 per call. Mean agent turns are 5.5 in both configurations, and mean call duration is 25.83 seconds in both, because in this model corrections re-hear single digits and letters rather than whole answers, and the read-back rides on turns the call already has.

## What the code measures

Read the failed list carefully, because it refutes the obvious theory. Call-02 and call-11 are in it: the slow and hard calls that endpointing rescued from escalation now fail as wrong bookings instead. Fixing the loud failure converted it into the silent one. That is a general law of this stack: each layer's fix promotes the surviving errors to the next layer, and a system is only as good as its last unchecked layer. Endpointing without confirmation produces confident wrong bookings at scale.

The cost side is the pleasant surprise. Confirmation is usually sold as a latency and duration tax, and at the turn level Lesson 18 will show it costs no first-audio latency at all, because it adds exchanges, not waiting. Here it does not even move mean duration, though that is partly the model's kindness (digit redraws are cheap in the stand-in). What it costs is repairs: 0.58 extra exchanges per call, spent exactly on the calls that were wrong. A repair is the cheapest possible price for a corrected booking, and Lesson 24 prices the alternative: the as-built system spends 63 percent of its money on calls that fail.

## Common failures

- Confirming everything. Reading back the service and the day and the name and the number makes calls interminable; confirm the payloads whose errors are silent and expensive (numbers, names, times), not the ones the schedule validates for free.
- Confirming with a yes/no question. "I have 07960155240, is that right?" earns a reflexive yes. The correction model here works because the caller hears the value and can localise the wrong digit; design read-backs that expose the value, chunked the way Lesson 09 prescribes.
- Treating a correction as a restart. Re-asking the whole question redraws every digit, including the ten that were right.

## Recap checklist

- [ ] You know the success counts with and without confirmation, endpointing held equal
- [ ] You can explain why fixing endpointing alone changed escalation failures into wrong bookings
- [ ] You know what confirmation costs in this model, and what it does not cost

## Resources

- The correction mechanics: [Lesson 09](../09-numbers-and-names/README.md)
- Confirmation in the full design comparison: [Lesson 18](../18-the-latency-budget/README.md)
- Confirmation removed as a fault injection: [Lesson 20](../20-voice-failure-modes/README.md)
