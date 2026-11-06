# Solution, Lesson 07

Split by channel, telephony averages 0.0846 WER and wideband 0.0558 across the fixture set.

The gap can only come from the weakness classes that are channel-gated in `vox/stt.py`: the number-word swaps (fifteen/fifty, sixteen/sixty, and five/nine inside digit contexts) and the spelled-letter swaps, both of which fire only when the channel is telephony, because both exploit distinctions the telephone band removes. Homophones fire on both channels, the unknown-name garbles fire on both, and the noise-driven drops and garbles follow the SNR, not the channel, so none of those three can explain a channel gap on their own.
