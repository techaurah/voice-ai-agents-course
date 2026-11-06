# Solution, Lesson 05

At -20 dB the clean frame accuracy is 0.7766, barely different from the -32 dB default's 0.7663. The frame errors at both thresholds are dominated by the hangover bridging pause frames, not by the threshold itself, so moving the threshold barely moves the score.

What the stricter threshold buys on clean audio is therefore almost nothing. What it risks, per the noise experiment in reverse, is the quiet caller: in noise the problem was false speech from a floor that rose, but a caller speaking softly sits near any threshold you set, and every decibel you raise it is a decibel of their speech reclassified as silence. Threshold choice is a decision about which caller you would rather fail, and the fixture numbers give no free lunch in either direction.
