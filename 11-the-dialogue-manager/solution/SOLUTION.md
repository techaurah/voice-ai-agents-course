# Solution, Lesson 11

Call-02 escalates without booking: 4 repairs used, 5 cut-offs suffered, graded a failure. The fixed 800 ms endpoint keeps declaring the slow caller's turns over mid-sentence, each cut-off burns a repair on a re-ask, and the repair budget runs out before the phone slot is ever reached.

Lesson 06 predicts it exactly: all three slow fixture utterances were cut by the 800 ms policy there, and call-02 is that measurement wearing a full dialogue. The failure differs from call-01's in kind. Call-01 fails silently, with a wrong value written into the world; call-02 fails loudly, with no booking at all. Voice systems need defences against both, and they are different defences: endpointing that respects slow speakers (Lesson 06) for the loud failures, confirmation (Lesson 12) for the silent ones.
