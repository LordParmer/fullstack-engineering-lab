# Day 3 lab · Diagnostic: Data engineering

**Goal:** finish a small incremental orders load (dedupe to the latest version per key, then an idempotent upsert) and read a naive loader to find its bugs, so the diagnostic sees how you reason about grain, idempotency and late data in code.
**Time:** 20 min · **Track:** Data engineering

## Setup
Nothing to install beyond pytest: it uses Python's built-in `sqlite3`.

```bash
python -m pytest labs/2026-11/02-diagnostic-data-engineering -q
```

All tests fail at the start, because the two functions raise `NotImplementedError`.

## Steps
1. Read `orders_pipeline.py` top to bottom, including `naive_load`. Don't change `naive_load`.
2. Implement `dedupe_latest(events)`: one row per `order_id`, keeping the event with the greatest `updated_at`.
3. Implement `upsert_orders(conn, rows)`: insert new orders, update existing ones, but never let an older event overwrite a newer one. Running it twice with the same input must leave the table unchanged.
4. In `ANSWERS.md` (create it), list every bug you can find in `naive_load` (at least three), one line each: what goes wrong and with what input.

## Done when
- [ ] `python -m pytest labs/2026-11/02-diagnostic-data-engineering -q` passes
- [ ] `ANSWERS.md` names at least three bugs in `naive_load`, each with an input that triggers it
- [ ] You can say in one sentence what "idempotent" means for this load

## Stretch
Add a test proving that a run of `0.0`-amount orders (a free promo order) survives the whole pipeline, then add `daily_revenue(conn)` that sums `amount` per day for non-cancelled orders.
