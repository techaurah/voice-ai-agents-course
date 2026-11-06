# Solution, Lesson 10

Committing at 40 percent of the words scores 0.618 mean WER, against 0.4135 at 60 percent and 0.0702 for the batch final. Each step earlier costs roughly twenty points of error rate on this fixture set, because at 40 percent most of the utterance has not been heard at all and the draft pass's confusions are at their densest.

The implication is that "looks stable" is doing heavy lifting in any such design. A partial can stop changing because it is right or because the draft and final passes share the same confusion, and the stream itself cannot tell you which. Any action taken on a partial should be reversible, or priced with the measured error rate of the commit point, not with the final transcript's rate.
