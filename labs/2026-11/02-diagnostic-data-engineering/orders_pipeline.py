"""Incremental orders load into SQLite.

Each event is one version of an order. The source sends the full row every
time an order changes, can send the same event twice (at-least-once
delivery), and can deliver events late and out of order.
"""

import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS orders (
    order_id   TEXT PRIMARY KEY,
    status     TEXT NOT NULL,
    amount     REAL,
    updated_at TEXT NOT NULL  -- ISO-8601, so string order is time order
)
"""


def connect(path: str = ":memory:") -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.execute(SCHEMA)
    return conn


def naive_load(conn: sqlite3.Connection, events: list[dict]) -> None:
    """The loader we inherited. Read it and list its bugs in ANSWERS.md.

    Do not change this function.
    """
    for e in events:
        if not e["amount"]:
            continue
        conn.execute(
            "INSERT INTO orders VALUES (?, ?, ?, ?)",
            (e["order_id"], e["status"], e["amount"], e["updated_at"]),
        )
    conn.commit()


def dedupe_latest(events: list[dict]) -> list[dict]:
    """Return one event per order_id: the one with the greatest updated_at.

    Keep every order, including ones whose amount is 0.0 or None.
    """
    # TODO: build the result in one pass over events
    raise NotImplementedError


def upsert_orders(conn: sqlite3.Connection, rows: list[dict]) -> None:
    """Insert new orders and update existing ones.

    An incoming row only replaces the stored one if it is newer
    (greater updated_at). Running this twice with the same rows must leave
    the table exactly as after the first run.
    """
    # TODO: one INSERT ... ON CONFLICT(order_id) DO UPDATE statement,
    # executed for every row, then commit
    raise NotImplementedError


def load(conn: sqlite3.Connection, events: list[dict]) -> None:
    upsert_orders(conn, dedupe_latest(events))
