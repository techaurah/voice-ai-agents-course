# Solution, Lesson 00

An 880 Hz tone for 500 ms at a 16,000 Hz sample rate is 0.5 × 16,000 = 8,000 samples, and that is what the round trip reports when the change is made: `wav_roundtrip_samples` becomes 8000, while the rate stays 16000 and the fixture counts are untouched.

If the count had come back different, the first suspect is the write and read path itself (the second failure class in the README: the lab machinery, not your Python version and not the fixtures), because the sample count is produced entirely by `audio.tone`, `audio.write_wav`, and the `wave` read inside the artifact. The check to run is the smallest one: render the tone in a REPL, print its length before writing, and compare it with the length after reading; the stage where the number changes is the broken one.
