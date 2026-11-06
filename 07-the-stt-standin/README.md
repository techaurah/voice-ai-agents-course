# Lesson 07: The STT stand-in

40 min · Intermediate · Prerequisites: Lessons 04 and 06

The course's recogniser is a stand-in and says so on the label. `vox.stt.transcribe` is a confusion model: given the words a caller actually said (a fixture), it produces the hypothesis a recogniser with known weaknesses would plausibly emit on that channel and noise level. Its weaknesses are written in its source and they are the curriculum: homophones on any channel, number-word swaps that only fire on telephony where the distinguishing fricatives never arrive, spelled-letter swaps (f/s, m/n), a small set of names it garbles whole, and word drops and neighbour garbles that grow as the signal-to-noise ratio falls. Every draw is seeded by utterance id and attempt number, so results reproduce exactly and a second attempt is a genuinely different draw, which is what makes repair strategies measurable later.

This lesson scores the stand-in on the full fixture set: word error rate (WER) overall, split clean versus noisy, and as raw edit counts.

## Run it

```bash
python3 stt_lab.py
```

Mean WER across the 24 utterances is 0.0702. Clean utterances score 0.0585, noisy ones 0.0867. The edit counts tell the mechanism: 11 substitutions, 5 deletions, 0 insertions. The worst utterance is utt-13 at 0.3333, with utt-18 and utt-14 at 0.2222.

## What the code measures

Two calibration facts before the number is used anywhere. First, this WER is a property of the stand-in's stated rules, measured so the rest of the course has errors to engineer against; it is not a claim about any real recogniser. Real systems publish their own numbers, and RESEARCH.md keeps those separate. Second, the composition matters more than the rate: a system whose errors are substitutions of confusable words (fifteen for fifty, thursday for tuesday) fails differently from one whose errors are deletions, and the defences differ too. Confirmation (Lesson 12) exists because substitutions survive every plausibility check the parser can run; the wrong word is a perfectly good word.

The clean-versus-noisy split also refuses to tell a simple story. Noise roughly doubles the deletion pressure in the stand-in's rules, yet clean WER is already 0.0585 with no noise at all, because the confusion rules (homophones, telephony number swaps, unknown names) do not need noise to fire. Channel, not weather, is the bigger enemy on this fixture set: telephony utterances average 0.0846 WER against wideband's 0.0558, a split the exercise asks you to compute.

## Common failures

- Reporting one WER for a recogniser that serves two channels and four noise conditions. The aggregate hides exactly the cells that hurt.
- Tuning against a stand-in and believing the result transfers. What transfers is the architecture of the defence (confirm the payload, spell the name), not the tuned constants.
- Counting insertions as impossible. They are zero here because this confusion model never inserts; real recognisers insert hallucinated words in noise, and a parser that assumes they cannot will mishandle them.

## Recap checklist

- [ ] You can list the stand-in's five weakness classes and where each is defined
- [ ] You know the overall, clean, and noisy mean WER on the fixtures
- [ ] You can explain why error composition matters more than the headline rate

## Resources

- WER by condition and tag: [Lesson 08](../08-noise-as-a-data-problem/README.md)
- The payloads errors hurt most: [Lesson 09](../09-numbers-and-names/README.md)
- Evaluating a proposed recogniser fix: [Lesson 26](../26-evaluating-transcripts/README.md)
