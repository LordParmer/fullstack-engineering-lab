from orders_pipeline import connect, dedupe_latest, load, upsert_orders


def ev(order_id, status, amount, updated_at):
    return {
        "order_id": order_id,
        "status": status,
        "amount": amount,
        "updated_at": updated_at,
    }


def rows(conn):
    return conn.execute("SELECT * FROM orders ORDER BY order_id").fetchall()


def test_dedupe_keeps_latest_version_regardless_of_arrival_order():
    events = [
        ev("o1", "shipped", 20.0, "2026-11-01T10:00"),
        ev("o1", "placed", 20.0, "2026-11-01T09:00"),
        ev("o2", "placed", 5.0, "2026-11-01T09:30"),
    ]
    result = {e["order_id"]: e for e in dedupe_latest(events)}
    assert len(result) == 2
    assert result["o1"]["status"] == "shipped"


def test_dedupe_keeps_zero_and_missing_amounts():
    events = [
        ev("promo", "placed", 0.0, "2026-11-01T09:00"),
        ev("draft", "placed", None, "2026-11-01T09:00"),
    ]
    assert {e["order_id"] for e in dedupe_latest(events)} == {"promo", "draft"}


def test_upsert_twice_is_idempotent():
    conn = connect()
    batch = [ev("o1", "placed", 20.0, "2026-11-01T09:00")]
    upsert_orders(conn, batch)
    first = rows(conn)
    upsert_orders(conn, batch)
    assert rows(conn) == first


def test_upsert_updates_with_newer_event():
    conn = connect()
    upsert_orders(conn, [ev("o1", "placed", 20.0, "2026-11-01T09:00")])
    upsert_orders(conn, [ev("o1", "shipped", 20.0, "2026-11-01T10:00")])
    assert rows(conn) == [("o1", "shipped", 20.0, "2026-11-01T10:00")]


def test_late_older_event_does_not_overwrite_newer():
    conn = connect()
    upsert_orders(conn, [ev("o1", "cancelled", 20.0, "2026-11-01T11:00")])
    upsert_orders(conn, [ev("o1", "placed", 20.0, "2026-11-01T09:00")])
    assert rows(conn) == [("o1", "cancelled", 20.0, "2026-11-01T11:00")]


def test_full_load_across_two_batches():
    conn = connect()
    load(
        conn,
        [
            ev("o1", "placed", 20.0, "2026-11-01T09:00"),
            ev("o1", "placed", 20.0, "2026-11-01T09:00"),  # duplicate delivery
            ev("promo", "placed", 0.0, "2026-11-01T09:05"),
        ],
    )
    load(conn, [ev("o1", "shipped", 20.0, "2026-11-01T10:00")])
    assert rows(conn) == [
        ("o1", "shipped", 20.0, "2026-11-01T10:00"),
        ("promo", "placed", 0.0, "2026-11-01T09:05"),
    ]
