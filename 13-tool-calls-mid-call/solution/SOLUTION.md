# Solution, Lesson 13

In the series-streamed design the tool sits additively inside the turn, so doubling it adds the full extra 140 ms: the mean when-turn latency rises from 834.8 ms to 974.8 ms.

The prefetched design's ranking does not change: it still adds nothing, because the lookup, fast or slow, finishes during the caller's speech as long as it completes within the utterance, so its lead over the series designs grows by exactly the degradation. The two series designs keep their relative order too (sequential stays worst), but both cross further into the range where callers start talking over the agent, which is the practical meaning of the extra 140 ms.
