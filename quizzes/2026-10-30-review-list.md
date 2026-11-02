# Review list · 2026-10-30

> There's no review history on the flashcard page yet (no `srs` document), so nothing is overdue and there are no lapse or ease numbers. This list is built from `progress.md` (Day 1 "Struggled with") and the Day 1 cards in `labs/2026-10/29-diagnostic/cards.json`.

## Suggested order for Friday

1. **Flashcard page, Review tab, about 10 minutes.** If the Day 1 deck (`daily-2026-10-29`) isn't on the page yet, import `labs/2026-10/29-diagnostic/cards.json` first. Go through the starter deck and the three Day 1 cards below.
2. **Quiz tab: "Week quiz · 2026-10-30"**, or work through `quizzes/2026-10-30.md` on paper before opening the answers.
3. If you have time left, reread `yields.py` and `test_yields.py`. Break `average_yield` on purpose and check that a test fails.

## Cards to review

| # | Question | Deck | Why it's on the list | Due |
|---|----------|------|----------------------|-----|
| 1 | Why is `if v:` the wrong filter for removing missing values from a list of measurements? | daily-2026-10-29 (c1) | Weak spot: truthiness vs `is not None` | New, not yet reviewed |
| 2 | A test passes. What question must you ask before trusting it, and how do you answer it? | daily-2026-10-29 (c2) | Weak spot: test design | New, not yet reviewed |
| 3 | Why is `x in my_list` slow for a million items, and what should you use instead? | daily-2026-10-29 (c3) | Weak spot: list vs set lookup cost | New, not yet reviewed |
| 4 | Predict the output of the `add_tag(tag, tags=[])` snippet | quiz-2026-10-30 (q6) | Weak spot: mutable default arguments (no daily card yet) | Friday quiz |
| 5 | HTTP status codes: 201 / 400 / 401 / 403 / 404 | quiz-2026-10-30 (q8) | Weak spot: HTTP status codes (no daily card yet) | Friday quiz |
| 6 | Return `0.0` or raise `ValueError` when nothing was measured? | quiz-2026-10-30 (q7) | Weak spot: function design | Friday quiz |
| 7 | One function that does everything vs. parse / compute / print split | quiz-2026-10-30 (q9) | Weak spot: function design | Friday quiz |

## Weak spots this week

From Day 1 (Diagnostic: Software engineering, 2026-10-29):

- Truthiness vs `is not None`
- Test design: would this test catch the bug?
- Function design
- HTTP status codes
- List vs set lookup cost
- Mutable default arguments
