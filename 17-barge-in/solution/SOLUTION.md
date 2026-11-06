# Solution, Lesson 17

At a 10 percent interrupt, with the 120 ms stop latency, the caller hears exactly 1 word ("your"). Sixteen words are phantom, and all three fact words (cleaning, tuesday, ten) were never heard, so the line delivered nothing of substance at all.

A front-loaded rewrite that opens with the facts, for example "ten o'clock on tuesday, your cleaning is booked, and a confirmation text is on its way", would by the same interrupt point have delivered at most the first word or two, so even front-loading cannot save a 10 percent interrupt; what it changes is the 25 percent case, where the facts would already have landed. The honest conclusion is two-layered: front-load for the plausible interrupts, and keep the confirmation text message as the channel that does not depend on being heard at all.
