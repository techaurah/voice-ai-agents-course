# Solution, Lesson 18

Sequential staging with adaptive endpointing and confirmation pools 41 turns at p50 993 ms and p95 1,252 ms. It passes the p95 gate and fails the p50 gate.

Good endpointing cannot rescue a sequential pipeline. The adaptive policy removes the endpointing excess (the same policy takes the streamed design to 742 ms), but the sequential design still pays batch transcription and full-reply generation inside every turn, and those two terms alone keep the median turn near a second. The levers are not interchangeable: staging decides the floor, endpointing decides how close to the floor you run, and both have to be right before the budget is met.
