# Day 2 lab · Diagnostic: App development

**Goal:** finish two handlers of a tiny notes API (read one note, create one note) and read an inherited handler to find its bugs, so the diagnostic sees how you reason about status codes, auth checks, input validation and safe SQL in code.
**Time:** 20 min · **Track:** App development

## Setup
Nothing to install beyond pytest: it uses Python's built-in `sqlite3`, and there's no web server. Each handler returns `(status_code, body)`, which is what a framework like FastAPI would turn into an HTTP response.

```bash
python -m pytest labs/2026-11/04-diagnostic-app-development -q
```

All 13 tests fail at the start, because the two handlers raise `NotImplementedError`.

## Steps
1. Read `notes_api.py` top to bottom, including `naive_get_note`. Don't change `naive_get_note`.
2. Implement `create_note(conn, user, payload)`: 401 with no user, 422 for a missing, non-string or blank title, otherwise insert the note and return 201 with the stored row (including its new `id`).
3. Implement `get_note(conn, user, note_id)`: 401 with no user, 404 if the note doesn't exist or isn't yours, otherwise 200 with the note.
4. In `ANSWERS.md` (create it), list every bug you can find in `naive_get_note` (at least three), one line each: what goes wrong and with what input.

## Done when
- [ ] `python -m pytest labs/2026-11/04-diagnostic-app-development -q` passes (13 tests)
- [ ] Neither handler builds SQL with an f-string or `+`: values go in as `?` parameters
- [ ] `ANSWERS.md` names at least three bugs in `naive_get_note`, each with an input that triggers it

## Stretch
Add `update_note(conn, user, note_id, payload)` for `PATCH /notes/<id>`: same 401/404/422 rules, only the fields present in the payload change, return 200 with the updated note. Write its tests first.
