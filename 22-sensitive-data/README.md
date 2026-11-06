# Lesson 22: Sensitive data

45 min · Intermediate · Prerequisites: Lessons 09 and 21

A voice agent's memory is its transcript, and transcripts accumulate things nobody decided to store: phone numbers spoken aloud, and in call-07, a full card number a caller insisted on reading out on a recorded call. Lesson 20 showed the manager refusing the card; this lesson asks the quieter question: what lands in the stored text of all the calls that went fine, and can it be cleaned measurably?

The artifact builds the corpus a naive deployment would keep: every caller answer from the twelve bundled calls, plus the card utterance exactly as heard, 49 texts in all. It then counts digit strings recoverable from that text, where "recoverable" is strict: a run of at least four digit words that parses to digits, or a raw digit string of at least four digits.

## Run it

```bash
python3 redaction.py
```

Before redaction: 13 digit strings, totalling 148 digits, sit in the stored corpus. Sixteen of those digits are the card number. After a redactor replaces digit-word runs and raw digit strings with a marker: 0 strings, 0 digits.

## What the code measures

The count reframes data minimisation as an auditable property instead of a policy sentence. "We do not store card numbers" is a claim; "the stored corpus contains zero recoverable digit strings, and here is the script that counts them" is a control. The redactor here is deliberately simple, a run-length rule over digit words plus a regex for typed digits, and the lesson does not oversell it: it would miss a number spelled with interruptions ("zero seven, um, nine five"), which is why redaction is the second line of defence. The first line is the dialogue itself: the manager never asks for card details, actively refuses them (call-07), and takes payment by a secure link sent by text, per the clinic policy in the fixtures. Data you never collect cannot leak from a transcript.

Phone numbers are the genuinely hard case, and the lesson leaves the tension visible: the redactor removes them too (they are most of the 148 digits), yet the business legitimately needs the number it sends the confirmation to. The resolution is architectural, not textual: the number belongs in the booking record, access-controlled and retained on a schedule, not in the free-text transcript that gets copied into logs, evaluations, and training sets. Same data, different stores, different rules.

## Common failures

- Storing raw transcripts forever because storage is cheap, then discovering them in a debug log, an eval export, and a support ticket.
- Redacting with a pattern that only catches typed digits, while callers speak their numbers as words.
- Letting the agent ask for data it should never hold. If the flow can be completed with a payment link, the card number's presence on the call is a design bug before it is a storage bug.

## Recap checklist

- [ ] You know the before and after digit counts for the stored corpus
- [ ] You can explain redaction's limits and the first line of defence
- [ ] You can state where a phone number legitimately belongs, if not the transcript

## Resources

- The refusal behaviour: [Lesson 11](../11-the-dialogue-manager/README.md)
- The clinic's card rule as data: [fixtures/policy.json](../fixtures/policy.json)
