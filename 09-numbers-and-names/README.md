# Lesson 09: Numbers and names

50 min · Intermediate · Prerequisites: Lessons 07 and 08

Two payloads carry the whole value of a booking call: the phone number the confirmation goes to, and the name the booking is under. Both are worst-case payloads for speech. A phone number is eleven digits with no redundancy, where one wrong digit is a wrong number, not a slightly wrong number. A name is an open-vocabulary item the recogniser may never have seen, spoken once, by someone who assumes it is obvious. This lesson measures both at the level that matters, exact string match, and then measures the corrections that rescue them.

Three measurements. Digit utterances from the transcript fixtures: every one in the set is on telephony, and all 7 parse to exactly the right digit string, which sounds reassuring until the second measurement. The twelve capstone phone numbers, transcribed as the dialogue manager hears them: only 5 of 12 arrive exactly right on the first attempt. Spelled names from the call fixtures: 1 of 2 arrives letter-perfect.

## Run it

```bash
python3 numbers_names.py
```

Then the corrections. Digit-by-digit read-back correction, where the caller hears the read-back, identifies the wrong digits, and repeats just those (the model `vox.dialogue` uses): 12 of 12 phone numbers end exactly right. Letter-by-letter correction for spelled names: 2 of 2.

## What the code measures

The gap between the first and second measurement is the lesson. Word-level scores flattered digits (0.0278 WER in Lesson 08) because most digit words survive; string-level success is what a booking needs, and at string level a per-digit error rate compounds over eleven digits until most numbers are wrong somewhere. Telephony digit substitutions run at 8 percent per digit in the stand-in, wideband at 3 percent, and the fifteen/fifty chunk swap can take two digits at once. No plausible recogniser improvement makes an unconfirmed eleven-digit string safe; the arithmetic forbids it.

Correction works because it changes the error structure, not because callers speak more clearly. Repeating one digit is a fresh draw on a one-symbol alphabet, and only the wrong positions are redrawn. Two correction rounds are available in the manager; on this fixture set, one round already repairs all 12 numbers, and the second round is insurance rather than load-bearing, a distinction worth knowing before you budget call time for it.

Names follow the same shape with a different mechanism: the stand-in garbles unknown names whole (Niamh becomes "neve"), which no amount of re-listening fixes, because the recogniser will garble it the same way. Spelling changes the alphabet to 26 letters with known confusions (m/n, f/s on telephony), and correction redraws only the wrong letters.

## Common failures

- Validating a phone number by length alone. Seven of the twelve first-attempt numbers were the right length and the wrong number.
- Asking "was that right?" after reading back a whole number. Callers cannot localise an error in an eleven-digit string they heard once; read-back has to be correctable in pieces.
- Treating a name as a string to recognise rather than a string to construct. For names outside the recogniser's vocabulary, spelling is not a fallback, it is the primary channel.

## Recap checklist

- [ ] You know the raw exact-match rates for phone numbers and spelled names
- [ ] You can explain why string-level success collapses over eleven digits
- [ ] You can describe digit-level correction and why one round usually suffices

## Resources

- Correction inside the full dialogue: [Lesson 12](../12-confirmation-and-repair/README.md)
- What unconfirmed numbers do to stored data: [Lesson 22](../22-sensitive-data/README.md)
