# Day 1 lab · Diagnostic: Software engineering

**Date:** 2026-10-29 · **Track:** Software engineering · **Status:** partial

`average_yield` in `yields.py` averages the measured runs: `None` is skipped, `0.0` counts, and no measured runs raises `ValueError`. `test_yields.py` has a test for each rule.

```bash
python -m pytest labs/2026-10/29-diagnostic-software-engineering -q
```

Struggled with: truthiness vs `is not None`, test design, mutable default arguments. See Day 1 in `progress.md`. Flashcards: `cards.json`.
