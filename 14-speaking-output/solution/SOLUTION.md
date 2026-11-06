# Solution, Lesson 14

The sentence has 3 unspeakable tokens by the artifact's definition ("09:30", "£50", and the phone number). After `to_spoken` it reads: "Your emergency appointment is booked for saturday at nine thirty. The deposit is fifty pounds. We will text the confirmation to zero seven eight eight two six nine three five one four.", and the after-count is 0.

Note the time: 09:30 becomes "nine thirty", not "nine oh thirty", because the "oh" convention only applies to minutes under ten. The number is the call-09 caller's own, which is the point of generating these sentences from data rather than templates alone.
