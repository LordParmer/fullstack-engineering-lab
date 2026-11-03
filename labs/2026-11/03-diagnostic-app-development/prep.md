# Day 2 prep · Diagnostic: App development

Linear: ETH-16 · https://linear.app/ethan-parmer-test/issue/ETH-16/day-2-diagnostic-app-development

> **Day number:** Linear calls this Day 2 (ETH-16, due 2026-11-03). `progress.md` already has two entries headed "Day 2" (the data engineering and software engineering diagnostics on 2026-11-02), so by its count this would be Day 3. Use whichever you prefer when you log it. The last `Next:` line said "Diagnostic: AI engineering (short check) + Python foundations start"; this follows Linear instead, since ETH-16 is due today (AI engineering is ETH-19, due 2026-11-06).

This is a **Test** session, so it follows the issue rather than the usual five parts: a 60-minute diagnostic covering front-end frameworks, REST/GraphQL APIs, authentication, relational databases for apps, containers and cloud deployment. It's aimed **above day-job level**, to find real gaps. A low score is the point, not a problem: it tells the curriculum where to spend time.

| Part | Minutes | What happens |
|------|---------|--------------|
| Recall | 5 | 3 questions from earlier sessions |
| Self-rating | 5 | Rate 0–3 on the six areas below |
| Concept questions | 25 | 12 questions, two per area, answered before grading |
| Lab | 20 | `README.md` in this folder: finish two API handlers, find the bugs in `naive_get_note` |
| Check & gap ranking | 5 | 3 check questions, then rank the 3 weakest areas |

**Log (from the issue):** score and weakest topics.

## Recall

1. *(Last session, 2026-11-02 software engineering.)* Why run `uv run pytest` instead of just `pytest`?
2. *(About a week ago, Day 1 on 2026-10-29.)* You filter a list of sensor readings with `[v for v in readings if v]`. Which real readings get lost, and what should the condition be?
3. *(Weak spot: missed in Day 2 recall.)* A MERGE source has two rows for the same `customer_id`. What happens, and how do you fix the source before merging?

## Diagnostic

### Self-rating (0 = never heard of it, 1 = know the words, 2 = have used it, 3 = could teach it)

| Area | 0–3 |
|------|-----|
| A. Front-end frameworks (components, state, rendering) | |
| B. APIs (REST semantics, status codes, GraphQL) | |
| C. Authentication and authorization (sessions, tokens, OAuth) | |
| D. Relational databases for apps (SQL safety, indexes, transactions, migrations) | |
| E. Containers (images, Dockerfiles, layers) | |
| F. Cloud deployment (config, health checks, rollouts) | |

### Concept questions

Answer all 12 before any grading. Short answers are fine; "don't know" is a valid answer and is useful data.

**A. Front-end frameworks**
- A1. In React, what's the difference between **props** and **state**? A component does `items.push(newItem)` on an array held in state, and the screen doesn't update. Why, and what's the fix?
- A2. What's the difference between **client-side rendering** (CSR) and **server-side rendering** (SSR)? Give one reason to choose each.

**B. APIs**
- B1. Which of `GET`, `POST`, `PUT`, `DELETE` are **idempotent**, and why does it matter when a mobile client retries after a timeout? What status code would you return for: a successful create, a request with a malformed body, a valid token but no permission, and a rate-limited client?
- B2. What problems do **over-fetching** and **under-fetching** describe, and how does **GraphQL** address them? Name one thing GraphQL makes harder than REST.

**C. Authentication and authorization**
- C1. What's the difference between **authentication** and **authorization**? Which one is missing when user A can read user B's invoice by changing `/invoices/1041` to `/invoices/1042`?
- C2. Compare a **server-side session cookie** with a **JWT** access token: where state lives, and how you'd revoke each one. For a browser single-page app signing in with Microsoft Entra ID, which **OAuth 2.0** flow should it use?

**D. Relational databases for apps**
- D1. What is **SQL injection**? Show what goes wrong with `f"SELECT * FROM users WHERE name = '{name}'"` and what the safe version looks like.
- D2. A page lists 50 orders and then runs one query per order to load its customer. What's this problem called, and how do you fix it? Separately, why would you add an **index** on `orders.customer_id`, and what does it cost?

**E. Containers**
- E1. What's the difference between an **image** and a **container**? Why does copying `requirements.txt` and running `pip install` *before* `COPY . .` make rebuilds faster?
- E2. A Dockerfile has `ENV DATABASE_PASSWORD=hunter2`. Why is that a problem even if the repo is private, and where should the value come from instead?

**F. Cloud deployment**
- F1. Following **twelve-factor** config, how should the same container image run against dev and prod databases? What's a **health check** (readiness vs liveness) for?
- F2. Compare a **rolling** deployment with **blue-green**. On Azure, name a service that runs a container without you managing VMs, and how you'd roll back a bad release on it.

## Concept outline

For the debrief after grading. Use it to explain whichever area scored lowest; this outline covers the safe request handler, since the lab is built on it.

- **Why it matters:** most real app bugs that turn into incidents aren't clever exploits; they're a handler that forgot one check. A missing owner filter leaks other users' data (the most common API vulnerability, **broken object-level authorization**), string-built SQL lets input rewrite the query (**SQL injection**), and a wrong status code makes clients retry when they shouldn't or show "success" on failure.
- **How it works:** every handler runs the same checklist, in order. **Authenticate**: who is calling? No valid session or token → **401 Unauthorized**. **Validate** the input: wrong shape → **400** (malformed) or **422** (well-formed but invalid). **Authorize**: may *this* user touch *this* object? No → **403**, or **404** when you don't want to reveal the object exists. **Query** with **parameters** (`?` or `:name`), so the driver sends values separately from the SQL text and they can never become code. **Respond** with the precise code: **200** read, **201** created, **204** no content. Frameworks like FastAPI do parts of this for you (Pydantic validation returns 422, `Depends` for the current user), but the authorization and the owner filter are always yours.
- **Worked example:**

  ```python
  # FastAPI shape; the lab's handlers are the same logic without the framework
  @app.get("/notes/{note_id}")
  def read_note(note_id: int, user: str = Depends(current_user)):  # 401 if no session
      row = db.execute(
          "SELECT * FROM notes WHERE id = ? AND owner = ?",  # authorize in the query
          (note_id, user),                                    # parameters, never f-strings
      ).fetchone()
      if row is None:
          raise HTTPException(404, "not found")  # missing or not yours: same answer
      return dict(row)                           # 200
  ```

- **Takeaway:** authenticate, validate, authorize, parameterize, then return the exact status code, in that order, in every handler.

## Check

1. *(Recall)* What's the difference between a 401 and a 403?
2. *(Application)* `naive_get_note` receives `note_id = "0 OR owner = 'ben'"`. What query runs, what comes back, and which two fixes in your `get_note` each stop it?
3. *(Transfer)* Your lab returns 404 for someone else's note. When would 403 be the better answer?

## Answers (for the session, don't peek)

**Recall**
1. `uv run` executes inside the project's own `.venv`, with its Python and installed packages, so the tests can import your code. A bare `pytest` may not be installed or may run under a different Python.
2. `0`, `0.0` (and any empty values) are falsy, so real zero readings are dropped along with `None`. Use `if v is not None`.
3. The MERGE fails because several source rows match one target row. Deduplicate first: keep the latest row per key with `row_number() OVER (PARTITION BY customer_id ORDER BY updated_at DESC) = 1` (or use Auto CDC with `SEQUENCE BY`).

**Diagnostic**
- A1. Props are inputs passed in by the parent (read-only to the child); state is data the component owns and changes over time. `push` mutates the same array, so React sees the same reference and skips the re-render. Create a new array: `setItems([...items, newItem])` (or `setItems(prev => [...prev, newItem])`).
- A2. CSR sends a mostly empty HTML page plus JavaScript that builds the UI in the browser; SSR builds the HTML on the server per request. CSR suits highly interactive apps behind a login (cheap static hosting, rich client state). SSR suits public pages that need fast first paint and SEO (Next.js and similar). Credit either reasonable reason.
- B1. `GET`, `PUT`, `DELETE` are idempotent; `POST` is not. A retried `POST` after a timeout can create a duplicate order, so you use an **idempotency key** for safe retries. Codes: 201 Created, 400 Bad Request (or 422 for valid JSON with invalid fields), 403 Forbidden, 429 Too Many Requests.
- B2. Over-fetching: an endpoint returns far more fields than the screen needs. Under-fetching: the screen needs several round trips to collect what it needs. GraphQL lets the client ask for exactly the fields and nested objects in one query against a typed schema. Harder: HTTP caching (everything is one `POST /graphql`), per-field authorization, and N+1 resolver queries (needs batching such as DataLoader), plus rate-limiting by query cost.
- C1. Authentication = proving who you are; authorization = what you're allowed to do. The invoice case is missing **authorization** (an IDOR / broken object-level authorization bug): the server must check that invoice 1042 belongs to the caller.
- C2. A session cookie holds an opaque ID; the state lives on the server (or Redis), so you revoke it by deleting the session. A JWT carries its claims, signed, and the server validates it without a lookup; it can't be revoked before it expires unless you keep a deny-list, so keep access tokens short-lived and revoke the refresh token. A browser SPA should use the **authorization code flow with PKCE** (not the implicit flow), for example via MSAL.
- D1. User input is pasted into SQL text, so it can change the query. `name = "x' OR '1'='1"` returns every user; worse inputs can modify data. Safe: `conn.execute("SELECT * FROM users WHERE name = ?", (name,))` (or an ORM), where the driver sends the value separately from the SQL.
- D2. The **N+1 query problem** (1 query for the list + N for the related rows). Fix with a join, a single `WHERE id IN (...)` query, or the ORM's eager loading (`selectinload` / `joinedload` in SQLAlchemy). An index on `orders.customer_id` turns "find this customer's orders" from a full table scan into a fast lookup; the cost is disk space and slower inserts/updates, because the index has to be maintained.
- E1. An image is the read-only, layered template (like a class); a container is a running instance of it with its own writable layer (like an object). Docker caches each layer and rebuilds from the first changed one: dependencies only change when `requirements.txt` changes, so code edits reuse the cached `pip install` layer.
- E2. The value is baked into an image layer and visible to anyone who can pull the image (`docker history`, `docker inspect`), and in the Dockerfile history in git; private repos and registries leak, get shared or get forked. Inject it at runtime: an environment variable set by the platform, ideally from a secret store (Azure Key Vault reference, or a managed identity so there's no password at all).
- F1. One image, many environments: config (connection strings, feature flags) comes from environment variables set per environment, never built into the image. Readiness = "can I send it traffic yet?" (DB reachable, warmed up); liveness = "is it stuck, should it be restarted?". The platform uses them to route traffic and restart unhealthy instances.
- F2. Rolling replaces instances a few at a time, so old and new run side by side briefly; cheaper, but rollback means rolling again. Blue-green runs a full new environment next to the old one and switches traffic all at once; instant rollback by switching back, at double the resources during the switch. Azure: **Container Apps** (roll back by shifting traffic to the previous revision) or **App Service** for Containers (swap deployment slots back). Credit AKS only if they note you then manage the cluster.

**Lab: bugs in `naive_get_note`** (any three)
- SQL injection: `note_id` goes into the SQL via an f-string. `"0 OR 1=1"` returns the first note in the table, whoever owns it.
- No authentication: `user=None` still gets the note, with a 200.
- No authorization (IDOR): it never filters on `owner`, so `ben` can read `ana`'s note by guessing IDs.
- Wrong status for a missing note: it returns `(200, None)` instead of 404.
- Bonus, if raised: a non-numeric `note_id` like `"abc"` raises an `sqlite3.OperationalError`, which becomes a 500 instead of a 400/404.

**Check**
1. 401 means "I don't know who you are": no or invalid credentials; sign in and retry. 403 means "I know who you are, and you aren't allowed": retrying with the same credentials won't help.
2. The query becomes `SELECT * FROM notes WHERE id = 0 OR owner = 'ben'`, which returns one of ben's notes to anyone, with a 200. Parameterizing (`id = ?`, so the string is just a value that matches nothing) stops it, and so does filtering on `owner = ?` with the signed-in user (the attacker only ever gets their own notes). The typed `note_id: int` is a third guard.
3. When the caller is allowed to know the resource exists, so the honest answer helps them: for example a team member who can see a document but not edit it (403 on `PUT`), or an admin page a signed-in non-admin tries to open. Use 404 when existence itself is sensitive (other users' private notes, invoices).
