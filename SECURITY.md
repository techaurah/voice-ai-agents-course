# Security policy

This repository is a teaching codebase: Python standard library only, no network calls, no credentials, no live services. It processes only the synthetic fixtures bundled in `fixtures/`; the callers, the clinic, and the card number in the trap call are all invented.

If you find a problem that matters beyond the teaching context (for example, a lesson whose guidance would be unsafe if followed literally on a real telephony deployment), please open an issue describing it, or contact the maintainers through the TechAura GitHub organisation page at https://github.com/techaurah.

Two standing notes for readers adapting the patterns:

- The consent, disclosure, and card-handling patterns in Module 6 are engineering shapes, not legal advice. Recording and consent law varies by jurisdiction; check yours before deploying anything similar.
- The fixtures contain no real personal data and must stay that way. Do not contribute real call recordings or transcripts.
