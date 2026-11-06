# Solution, Lesson 09

With only one correction round, the count is still 12 of 12. On this fixture set the second round is never the round that saves a number: every number that correction can fix at all is fixed in round one, because each wrong digit is redrawn independently and the per-digit success rate on a single repeated digit is high.

A production system keeps the second round because the fixture set is twelve numbers, not twelve thousand. The round costs a few seconds only on calls where the first round already failed, which are precisely the calls (worst channels, worst noise) where a second independent draw is most valuable. Insurance is priced by the tail, not by the median, and Lesson 24 shows the per-call cost of repairs is small next to the cost of a wrong booking.
