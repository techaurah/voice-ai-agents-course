# Solution, Lesson 01

The longest fixture utterance is utt-07, the spelled-name call on the telephone channel, at 13 words. Priced the same way as the README's turn, it comes to 1,592 ms sequential and 1,237 ms streamed, a saving of 355 ms.

The gap grows because the stage streaming attacks hardest, batch transcription finalisation, is priced per word in the ledger (120 ms plus 18 ms per word in batch mode, against 30 ms plus 3 ms per word streamed). More words means more batch penalty to remove. The endpointing wait, still 800 ms in both, does not care how long the utterance was, which is why it stays the largest single term in both designs even as the saving grows.
