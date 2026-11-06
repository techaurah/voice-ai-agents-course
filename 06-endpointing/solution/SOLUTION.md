# Solution, Lesson 06

The fixed 600 ms policy cuts off the same 3 utterances (utt-12, utt-16, utt-19) and waits 600 ms on completed turns. It is dominated by neither neighbour and dominates neither: it has the 800 ms policy's cut-off count with a wait between the two, which is to say it pays latency without buying a single saved caller.

That is the structural point. The slow speakers' thinking pauses (680 to 940 ms) overlap every threshold in the plausible fixed range, so sliding one number up and down mostly rearranges the latency bill among the callers who were never at risk. A mixed population cannot be served by one silence duration; the wait has to depend on what has been said and who is saying it, which is the adaptive design the lesson builds.
