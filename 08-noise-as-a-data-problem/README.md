# Lesson 08: Noise as a data problem

40 min · Intermediate · Prerequisites: Lesson 07

Builders talk about noise as if it were weather: regrettable, external, somebody else's department. This lesson treats it as what it is, a property of your data distribution that you can measure cell by cell and design against. The artifact groups all 24 fixture utterances by channel and SNR band, and again by their curriculum tags, and scores every cell with the stand-in.

Read the table with its counts attached, because the counts are part of the result:

- telephony clean: 0.0848 (n=7)
- telephony snr12: 0.0 (n=2)
- telephony snr8: 0.1 (n=2)
- telephony snr5: 0.2222 (n=1)
- wideband clean: 0.0321 (n=7)
- wideband snr12: 0.037 (n=3)
- wideband snr8: 0.0 (n=1)
- wideband snr5: 0.3333 (n=1)

By tag: names 0.1385 and spelling 0.1496 are the worst payloads, noise-tagged utterances 0.0867, homophones 0.045, plain 0.0333, and digits, counterintuitively, the best at 0.0278.

## Run it

```bash
python3 noise_sweep.py
```

## What the code measures

Start with the embarrassment the table refuses to hide: telephony at snr12 scores 0.0, better than telephony clean at 0.0848. With n=2 that is not a finding, it is two utterances that happened to contain no confusable words. Clean telephony errors are confusion-driven, not noise-driven; whether a clean call errs depends on whether the caller said a number chunk or a confusable name, not on the SNR. A team that collected only average WER per SNR band would conclude noise does not matter on telephony, and would be wrong in a way the cell counts expose. Small cells are anecdotes with means, and the professional habit this lesson builds is refusing to quote a cell without its n.

The tags cut the data the useful way. Digits score best not because numbers are easy (Lesson 09 will show phone numbers failing constantly at the string level) but because WER counts words, and a digit utterance with one wrong word still parses to a mostly-right string, while the metric that matters for digits is exact string match. Names and spelling score worst because a single garbled token is the whole payload. Metric choice is a modelling decision; Lesson 26 builds an evaluation that respects it.

The genuine noise gradient is visible where the cells are honest: wideband degrades from 0.0321 clean to 0.3333 at snr5, and pooled across channels the noisy utterances average 0.0867 against clean's 0.0585. Noise is real. It is just not the only, or even the main, axis of failure, and a data programme that only collects noisy samples will miss the confusions killing clean calls.

## Common failures

- Quoting cell means without cell counts, especially to justify a launch decision.
- Collecting evaluation data that mirrors the demo (clean, cooperative, wideband) rather than the call distribution (telephony, noisy, rushed).
- Averaging word-level scores for payloads whose success is all-or-nothing at the string level.

## Recap checklist

- [ ] You can read the condition table and name its two least trustworthy cells
- [ ] You can explain why clean telephony can score worse than noisy telephony in a small sample
- [ ] You know which tags carry the worst WER, and why digits mislead at word level

## Resources

- The string-level view of numbers and names: [Lesson 09](../09-numbers-and-names/README.md)
- Building the evaluation harness properly: [Lesson 26](../26-evaluating-transcripts/README.md)
