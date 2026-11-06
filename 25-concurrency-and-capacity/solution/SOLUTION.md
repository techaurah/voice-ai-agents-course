# Solution, Lesson 25

With an even spread, one agent serves all 490 calls with zero abandonments, a mean wait of 2.2 seconds, and a p95 wait of 14.1 seconds.

Essentially all of the one-agent disaster was the clustering: the same volume, spread evenly, is a light load for a single line, because 490 calls at roughly 30 seconds each is only about 4.1 hours of talk time across an eight-hour day. The first question to ask about a chaotic nine o'clock is therefore not "how many calls?" but "in which minutes did they arrive?" Burst shape, not volume, is what saturates a voice platform, and any capacity report that aggregates to the hour is hiding the only detail that matters.
