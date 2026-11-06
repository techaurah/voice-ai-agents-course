# Tools

Two validators keep this course honest. Both run from the repo root
and need nothing beyond Python 3.10+.

- `validate_course.py` checks the structure: all 32 lesson folders
  with their required files and README sections, no em dashes
  anywhere, fixture self-consistency (call truth records against the
  answers, expected bookings against free schedule slots), and the
  presence of the capstone gates file. Run it after any edit.
- `check_links.py` verifies that every relative Markdown link in the
  repo resolves to a real file. External links are skipped.

Continuous integration runs both, compiles every Python file, and
then runs all 32 lesson smoke tests.
