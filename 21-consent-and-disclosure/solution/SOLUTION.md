# Solution, Lesson 21

Under the as-built configuration call-05 also ends as consent_refused, in the same 11.68 seconds. The gate produces identical behaviour in a configuration that differs in endpointing, confirmation, and spelling.

That is because consent lives in the flow's control structure, not in its tunable levers: it is evaluated before any slot collection, and its branch does not depend on how well the system hears or confirms. Endpointing and confirmation are quality levers that trade against each other and against latency; consent is a precondition, and preconditions do not get tuned. The practical consequence is that consent behaviour can be verified once, cheaply, and should be identical in every configuration you ship, which makes any difference a bug by definition.
