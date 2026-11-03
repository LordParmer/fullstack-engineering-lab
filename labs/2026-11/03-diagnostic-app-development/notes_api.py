"""A tiny notes API, without a web framework.

Each handler takes the database connection, the signed-in user (a username
string, or None when the request has no valid session) and the request data,
and returns (status_code, body). A framework such as FastAPI or Flask would
turn that pair into an HTTP response; here the tests call the handlers
directly.

Notes are private: a user may only see and change their own.
"""

import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS notes (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    owner TEXT NOT NULL,
    title TEXT NOT NULL,
    body  TEXT NOT NULL DEFAULT ''
)
"""


def connect(path: str = ":memory:") -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row  # rows behave like dicts: dict(row)
    conn.execute(SCHEMA)
    return conn


def naive_get_note(conn: sqlite3.Connection, user: str | None, note_id: str):
    """The handler we inherited. Read it and list its bugs in ANSWERS.md.

    Do not change this function.
    """
    row = conn.execute(f"SELECT * FROM notes WHERE id = {note_id}").fetchone()
    return 200, dict(row) if row else None


def get_note(conn: sqlite3.Connection, user: str | None, note_id: int):
    """GET /notes/<note_id>

    401 with {"error": ...} if there is no signed-in user.
    404 with {"error": ...} if the note doesn't exist OR belongs to someone
    else (so other users can't even tell that it exists).
    200 with the note as a dict otherwise.
    """
    # TODO: check the user, then one parameterized SELECT that also
    # filters on owner
    raise NotImplementedError


def create_note(conn: sqlite3.Connection, user: str | None, payload: dict):
    """POST /notes

    401 with {"error": ...} if there is no signed-in user.
    422 with {"error": ...} if "title" is missing, not a string, or blank.
    201 with the created note as a dict (including its new "id") otherwise.
    "body" is optional and defaults to "". The owner always comes from
    `user`, never from the payload.
    """
    # TODO: validate, then a parameterized INSERT, commit, and return the
    # stored row
    raise NotImplementedError
