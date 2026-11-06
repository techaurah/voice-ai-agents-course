# Solution, Lesson 15

The greeting at 4.0 ms per character costs 70 + 4.0 × 178 = 782 ms to synthesise in one pass, up from 461 ms.

It does not change which lines you would rewrite first. The rewrite priority is set by spoken duration and position in the call (the greeting's 7,618 ms in front of a caller who has not yet spoken), not by synthesis time, which even at the higher rate stays well under the audio's own duration. Synthesis price decides providers; duration decides scripts. The lesson's two curves point at different decisions, and conflating them produces a cheaper voice saying lines that are still too long.
