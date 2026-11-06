# Solution, Lesson 08

Pooled, the clean group is 14 utterances at 0.0585 mean WER and the noisy group is 10 utterances at 0.0867.

The pooled comparison is more trustworthy because each mean now rests on ten or more utterances, so a single confusable word can no longer swing a cell from best to worst the way it does in the n=1 and n=2 cells. What pooling throws away is the channel axis: telephony and wideband are averaged together, hiding the fact that the channels fail by different mechanisms (confusions versus drops). The by-tag cut keeps the mechanism visible, which is why the course evaluates on tags and families rather than on one pooled number.
