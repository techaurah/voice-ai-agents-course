# Lesson 14: Speaking output

35 min · Beginner · Prerequisites: Lesson 11

Text written for screens fails out loud. A confirmation line that reads perfectly well, "Your cleaning is booked for monday at 09:00. The deposit is £50. We will text the confirmation to 07950155240.", hands a synthesiser three things it will mangle: a colon-time it may read as "nine colon zero zero" or pause in the wrong place, a currency symbol it may skip or verbalise wrongly, and an eleven-digit string it may group arbitrarily. Speech output needs its own normalisation layer, the mirror of the parsing work on the input side: convert everything speakable into the words a human would say.

This lesson builds the confirmation sentences the booking line actually speaks, one per free slot in the fixture schedule (15 of them), counts the tokens no synthesiser should receive raw, rewrites them into spoken forms (times as words, "£50" as "fifty pounds", phone numbers as digit words), and counts again.

## Run it

```bash
python3 spoken_forms.py
```

Before rewriting, the 15 sentences contain 45 unspeakable tokens, three per sentence. After rewriting, zero. The example sentence becomes: "Your cleaning is booked for monday at nine o'clock. The deposit is fifty pounds. We will text the confirmation to zero seven nine five zero one five five two four zero."

## What the code measures

Normalisation looks trivial until you enumerate what it must handle: times (with the "oh" convention for minutes under ten, "nine oh five"), money, phone numbers as digit sequences rather than quantities (nobody says "seventy-nine billion" for a phone number), dates, and the clinic's own vocabulary. Each is a small rule; missing any one is a daily, audible, credibility-costing error on real calls. The count is the lesson's discipline: do not assert the layer works, count the raw tokens reaching the synthesiser and drive the count to zero on everything the agent can say, including the sentences generated from data (slots, prices, names) rather than written by hand.

The digit-words choice for phone numbers deserves its note: it matches how the input side expects numbers to arrive (Lesson 09's digit words), so a caller who repeats the number back is speaking the same representation the recogniser parses best. Output design and input design are one design.

## Common failures

- Normalising only the templates and forgetting the data interpolated into them, which is where times and prices actually come from.
- Reading numbers as quantities everywhere. A deposit of £50 is "fifty pounds"; a phone number is eleven separate digits; confusing the two is instantly audible.
- Letting the language model freestyle its spoken output. The model's text is written text; the normalisation layer is not optional polish, it is the contract between the model and the synthesiser.

## Recap checklist

- [ ] You can name the token classes that need spoken forms
- [ ] You know the before and after counts on the generated confirmations
- [ ] You can explain why phone numbers are spoken as digit words

## Resources

- The synthesiser that receives this text: [Lesson 15](../15-the-tts-standin/README.md)
- Numbers arriving in the other direction: [Lesson 09](../09-numbers-and-names/README.md)
