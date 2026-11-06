# Lesson 05: Voice activity detection

45 min · Intermediate · Prerequisites: Lessons 03 and 04

Before a pipeline can decide a turn has ended, it has to decide what counts as speech at all. The oldest and still most common answer is an energy gate: frames louder than a threshold are speech, quieter frames are not, with a hangover that bridges short gaps so words are not chopped into syllables, and a minimum length that discards clicks and bumps. `vox.vad.detect` implements exactly that design, and this lesson scores it against ground truth, because the fixture envelopes know precisely which frames are speech.

Scored raw, frame by frame, the bare threshold (-32 dB) is good: 0.9648 frame accuracy across the 24 utterances. Then the lesson adds the machinery real VADs need and watches the score fall, which is where it gets interesting.

## Run it

```bash
python3 vad_lab.py
```

With the 200 ms hangover and 120 ms minimum speech length applied, clean frame accuracy drops to 0.7663. The drop is not uniform: normal speech scores 0.7093, rushed 0.7794, and slow speech 0.9754. At segment level the picture sharpens: of the 19 normal and slow utterances, almost none survive as one segment. Normal utterances split (16 of 19 across both styles are split; only 3 normal and 2 rushed utterances come through whole), and all 3 slow utterances are split into pieces by their thinking pauses.

In noise the failure changes shape. With noise added at 8 dB SNR, the -32 dB threshold marks 40.61 percent of all frames as speech when they are not (false speech), while missing essentially no real speech. Raising the threshold to -18 dB cuts false speech to 22.31 percent, still with no missed speech on this fixture set.

## What the code measures

Three lessons in one table. First, frame accuracy is the wrong scoreboard for a component whose job is segmentation: the hangover deliberately mislabels pause frames as speech to keep segments whole, and is punished for it by the frame metric while doing its job. Judge a VAD on segment outcomes and downstream behaviour. Second, the hangover is a bet about pause lengths: at 200 ms it bridges rushed speakers' gaps completely and normal speakers' gaps partially, and no hangover bridges a slow speaker's 680 to 940 ms thinking pauses, so slow speakers are fragmented by any energy VAD. That fragmentation is what endpointing (Lesson 06) has to survive. Third, noise moves the whole level distribution: a threshold tuned in a quiet room spends the noisy call hallucinating speech, and the repair is a higher threshold or a noise estimate, each with its own cost.

## Common failures

- Tuning VAD on clean, single-speaker, read-speech recordings, which is to say on none of the conditions that break it.
- Treating a split segment as a transcription problem. The recogniser never stood a chance; the audio arrived pre-broken.
- Cranking the threshold to kill false speech in noise without checking the quiet caller at the other end, whose speech sits closest to the floor.

## Recap checklist

- [ ] You can explain hangover and minimum speech length, and what each trades away
- [ ] You know the raw versus post-hangover frame accuracy on the fixtures
- [ ] You can describe how 8 dB noise changes the failure mode

## Resources

- From detection to turn decisions: [Lesson 06](../06-endpointing/README.md)
- How the fragmentation reaches callers: [Lesson 20](../20-voice-failure-modes/README.md)
