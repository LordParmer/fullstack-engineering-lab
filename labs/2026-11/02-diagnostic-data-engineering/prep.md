# Day 3 prep · Diagnostic: Data engineering

Linear: ETH-17 · https://linear.app/ethan-parmer-test/issue/ETH-17/day-3-diagnostic-data-engineering

> **Why this topic today:** the issue due today, ETH-15 (Day 1 · Diagnostic: Software Engineering), was already done on 2026-10-29 and is marked Done. So this follows the `Next:` line in `progress.md` ("Diagnostic: Data engineering"), which is Linear's Day 3 (ETH-17, due 2026-11-04). Day 2 (ETH-16, App Development, due 2026-11-03) is still open. By `progress.md` counting, this would be the second logged entry; use whichever day number you prefer when you log it.

This is a **Test** session, so it follows the issue rather than the usual five parts: a 60-minute diagnostic covering data modeling, distributed processing internals, streaming, orchestration, data quality and testing, and governance. It's aimed **above day-job level**, to find real gaps. A low score is the point, not a problem.

| Part | Minutes | What happens |
|------|---------|--------------|
| Recall | 5 | 3 questions from Day 1 |
| Self-rating | 5 | Rate 0–3 on the six areas below |
| Concept questions | 25 | 12 questions, two per area, answered before grading |
| Lab | 20 | `README.md` in this folder: dedupe + idempotent upsert, find the bugs in `naive_load` |
| Check & gap ranking | 5 | 3 check questions, then rank the 3 weakest areas |

**Log (from the issue):** score and weakest topics.

## Recall

1. *(Last session, Day 1.)* `get_port` returns `cfg.get("port") or 8080`. A config sets `{"port": 0}`. What does it return, why, and what's the fix?
2. *(About a week ago, also Day 1, since that's the only history.)* You check 50,000 events against 1,000,000 known customer IDs. List or set for `known_ids`, and what's the rough cost of each?
3. *(Weak spot: "would this test catch the bug?")* Your test for a function passes on the first run. What's the one question you ask before trusting it, and how do you answer it in under a minute?

## Diagnostic

### Self-rating (0 = never heard of it, 1 = know the words, 2 = have used it, 3 = could teach it)

| Area | 0–3 |
|------|-----|
| A. Data modeling (grain, star schema, SCDs) | |
| B. Distributed processing internals (Spark shuffles, partitions, skew, joins) | |
| C. Streaming (event time, watermarks, delivery guarantees) | |
| D. Orchestration (DAGs, idempotency, backfills, retries) | |
| E. Data quality and testing (contracts, expectations, pipeline tests) | |
| F. Governance (Unity Catalog, access control, lineage, PII) | |

### Concept questions

Answer all 12 before any grading. Short answers are fine; "don't know" is a valid answer and is useful data.

**A. Data modeling**
- A1. What is the **grain** of a fact table? A `fact_orders` table has one row per order, and someone adds a `product_id` column. What just broke?
- A2. A customer moves from Leeds to York. Explain how an **SCD Type 1** and an **SCD Type 2** dimension handle it, and which columns Type 2 adds. Which would you need to report "revenue by the customer's city *at the time of the order*"?

**B. Distributed processing internals**
- B1. In Spark, what is a **shuffle**, which of `filter`, `groupBy`, `join`, `select` cause one, and why is it the expensive step?
- B2. A join stage has 199 tasks finishing in 10 seconds and 1 task running for 20 minutes. What's the likely cause, and name two ways to fix it.

**C. Streaming**
- C1. What's the difference between **event time** and **processing time**? Why does a 10-minute windowed count need a **watermark**, and what happens to an event that arrives after it?
- C2. A source delivers **at least once**. What does that mean for your sink, and what two things together give you **effectively exactly-once** results?

**D. Orchestration**
- D1. What does it mean for a pipeline task to be **idempotent**? Give one write pattern that is idempotent and one that isn't.
- D2. You need to **backfill** 90 days after a bug fix. The daily job appends to a table. What goes wrong if you just re-run it for each day, and how should the job be written so backfills are safe?

**E. Data quality and testing**
- E1. Give three different kinds of data quality check (not three columns with the same check) you'd put on an orders table, and say for each whether a failure should **stop** the pipeline or just **warn**.
- E2. What is a **data contract**, and how is it different from a test on your own table?

**F. Governance**
- F1. In Unity Catalog, what are the three levels of the namespace, and what privileges does a user need to `SELECT` from `main.sales.orders`?
- F2. Analysts may see all orders but only the last four digits of the customer's phone number. Name the Unity Catalog feature that does this, and how it differs from a **row filter**.

## Concept outline

For the debrief after grading. Use it to explain whichever area scored lowest; this outline covers idempotent incremental loads, since the lab is built on them.

- **Why it matters:** real pipelines get retried, re-run and backfilled, and sources send duplicates and late events. If a re-run changes the result, every failure becomes a data-correctness incident instead of a simple restart.
- **How it works:** decide the **grain** (one row per `order_id`) and a **natural key**. **Deduplicate** each batch to that grain, keeping the latest version by an ordering column (`updated_at`). Write with an **upsert / MERGE** on the key instead of an append, and only overwrite when the incoming row is **newer**, so **late, out-of-order** events can't roll state back. The result is **idempotent**: same input, same table, however many times it runs. This is exactly what Delta Lake `MERGE INTO` does at scale; Spark Structured Streaming adds checkpoints so it knows which input it has already processed.
- **Worked example:**

  ```sql
  -- SQLite (the lab); Delta Lake MERGE INTO has the same shape
  INSERT INTO orders (order_id, status, amount, updated_at)
  VALUES (:order_id, :status, :amount, :updated_at)
  ON CONFLICT (order_id) DO UPDATE SET
      status     = excluded.status,
      amount     = excluded.amount,
      updated_at = excluded.updated_at
  WHERE excluded.updated_at > orders.updated_at;  -- older/late rows are ignored
  ```

  ```sql
  -- Databricks / Delta equivalent
  MERGE INTO orders t
  USING latest_batch s ON t.order_id = s.order_id
  WHEN MATCHED AND s.updated_at > t.updated_at THEN UPDATE SET *
  WHEN NOT MATCHED THEN INSERT *;
  ```

- **Takeaway:** pick the grain, dedupe to it, and MERGE on the key with a "newer wins" rule, and re-runs stop being scary.

## Check

1. *(Recall)* What does "idempotent" mean for a data load, in one sentence?
2. *(Application)* With the lab's finished `upsert_orders`, the table holds `o1` as `cancelled` at 11:00. A late event arrives: `o1`, `placed`, 09:00. What does the table hold afterwards, and which part of the statement decides that?
3. *(Transfer)* When is a plain **append** (no dedupe, no MERGE) the right choice, and when is a full **overwrite** of a partition better than MERGE?

## Answers (for the session, don't peek)

**Recall**
1. It returns 8080: `0` is falsy, so `or` falls through to the default. Fix: `port = cfg.get("port"); return 8080 if port is None else port`.
2. Set. A list membership check is O(n), so about 50,000 × 1,000,000 comparisons worst case. A set is one O(n) build, then about O(1) per lookup.
3. "Would this test fail if the code were broken?" Break the code on purpose (for example swap `is not None` back to `if v`), run the test, confirm it fails, then undo.

**Diagnostic**
- A1. Grain is what one row represents. Adding `product_id` to a one-row-per-order table either forces one row per order line (the grain silently changes, and `SUM(order_total)` now double counts) or picks one product arbitrarily. Order lines belong in their own fact at line grain.
- A2. Type 1 overwrites the city, so history is lost. Type 2 closes the old row and inserts a new one, adding a surrogate key plus `valid_from` / `valid_to` (and often `is_current`). "City at the time of the order" needs Type 2, with the fact pointing at the surrogate key that was current when the order happened.
- B1. A shuffle redistributes rows across the cluster by key so that equal keys meet on the same partition. `groupBy` and `join` cause one (unless the join is broadcast); `filter` and `select` are narrow and don't. It's expensive because it writes to disk, sends data over the network and creates a stage boundary.
- B2. Data skew: one key (often a null or a "default" value) has far more rows than the rest, so one task gets them all. Fixes: turn on AQE skew-join handling (`spark.sql.adaptive.skewJoin.enabled`), broadcast the smaller side, salt the hot key, or filter or handle nulls separately.
- C1. Event time is when it happened at the source; processing time is when the system sees it. A windowed aggregation must keep window state open for late events; the watermark (max event time seen minus an allowed lateness) says when a window can be finalized and its state dropped. Events older than the watermark are dropped (or, in some sinks, not reflected in the finalized result).
- C2. The sink can see the same record more than once. Effectively exactly-once = a replayable source with checkpointed offsets **plus** an idempotent or transactional sink (dedupe on a key, MERGE, or an atomic commit like Delta's).
- D1. Running it again with the same input gives the same output. Idempotent: MERGE on a key, or overwrite a specific partition (`replaceWhere date = ...`). Not idempotent: a blind `INSERT` / append.
- D2. Re-running appends duplicates every day already loaded. Write the job to be parameterized by its logical date, and make each run overwrite its own partition (or MERGE on the key), never read "today" from the wall clock.
- E1. Any three distinct kinds, for example: schema/type (stop), not-null and unique on `order_id` (stop), referential integrity to customers (warn or quarantine), range/validity such as `amount >= 0` (stop or quarantine), freshness (max `updated_at` within N hours: warn/alert), volume anomaly versus yesterday (warn). Credit any sensible stop/warn reasoning: stop when downstream would be wrong, warn when it's late or unusual.
- E2. A data contract is an agreement with the **producer** about schema, semantics, and SLAs (freshness, quality) of the data they send, versioned and enforced at the boundary. A test on your own table checks your output; a contract makes the upstream team responsible for not breaking you.
- F1. `catalog.schema.table`. `USE CATALOG` on `main`, `USE SCHEMA` on `main.sales`, and `SELECT` on the table (or inherited from the schema/catalog).
- F2. A **column mask**: a SQL function attached to a column that rewrites the value based on who's asking (`is_account_group_member(...)`). A **row filter** hides whole rows; a mask keeps the row and changes one column's value.

**Lab: bugs in `naive_load`** (any three)
- `if not e["amount"]: continue` drops real `0.0` orders and `None` amounts (truthiness again, the Day 1 weak spot).
- Plain `INSERT` with a primary key: the second version of an order, or a duplicate delivery, raises `IntegrityError`, so it's not idempotent and can't take updates.
- No dedupe or ordering: if it were an `INSERT OR REPLACE`, a late older event would overwrite a newer state.
- Not a bug, but a good probe if they raise it: the single commit at the end means a mid-batch failure rolls the whole batch back, which is actually what you want. Credit it only if they reason it through correctly.

**Check**
1. Running the load again with the same input leaves the table exactly the same.
2. Still `cancelled` at 11:00. The `WHERE excluded.updated_at > orders.updated_at` clause on `DO UPDATE` skips the update because 09:00 is older.
3. Append is right for immutable event logs (clickstream, audit, raw/bronze) where every record is a fact and duplicates are handled downstream or can't happen. A partition overwrite beats MERGE when you recompute a whole slice anyway (a daily aggregate, a backfill of one date), since it's simpler, cheaper than a key-by-key MERGE, and naturally idempotent.
