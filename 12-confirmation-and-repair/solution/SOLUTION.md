# Solution, Lesson 12

With spelling off, success falls to 11 of 12. The missing call is call-06, whose caller is Niamh Byrne: the recogniser garbles "niamh" to "neve" as a whole word, read-back of the recognised name cannot recover it, and only the spelled channel (with letter-level correction) reconstructs the name.

Spelling protects exactly the payloads that fail as whole units: names outside the recogniser's vocabulary, where re-hearing reproduces the same garble deterministically. Phone numbers do not need it because their failure mode is per-symbol substitution, which digit-level read-back correction already redraws symbol by symbol. Match the defence to the failure geometry: substitution errors want correction, vocabulary errors want a different channel.
