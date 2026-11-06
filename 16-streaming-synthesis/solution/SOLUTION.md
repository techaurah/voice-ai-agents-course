# Solution, Lesson 16

Six of the agent's 13 lines contain more than one sentence. On those lines the mean full render is 256.5 ms and the mean first chunk is 129.0 ms, a saving of 127.5 ms, more than double the all-lines figure.

The all-lines average misleads in both directions because it dilutes the multi-sentence saving with seven lines that save exactly zero, while simultaneously hiding the greeting, whose turn-level saving (334 ms) is the one that decides whether callers say "hello?" into a silence. A design review shown 58.8 ms would underfund streaming for the lines that need it and overcredit it for the lines that cannot use it.
