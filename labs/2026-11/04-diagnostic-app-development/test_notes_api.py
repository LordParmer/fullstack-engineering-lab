import pytest

from notes_api import connect, create_note, get_note


@pytest.fixture
def conn():
    c = connect()
    yield c
    c.close()


def test_create_returns_201_with_id(conn):
    status, body = create_note(conn, "ana", {"title": "Groceries", "body": "milk"})
    assert status == 201
    assert body["id"] is not None
    assert body["title"] == "Groceries"
    assert body["body"] == "milk"
    assert body["owner"] == "ana"


def test_create_body_defaults_to_empty(conn):
    status, body = create_note(conn, "ana", {"title": "Just a title"})
    assert status == 201
    assert body["body"] == ""


def test_create_requires_user(conn):
    status, body = create_note(conn, None, {"title": "x"})
    assert status == 401
    assert "error" in body


@pytest.mark.parametrize("payload", [{}, {"title": ""}, {"title": "   "}, {"title": 42}])
def test_create_rejects_bad_title(conn, payload):
    status, body = create_note(conn, "ana", payload)
    assert status == 422
    assert "error" in body


def test_create_ignores_owner_in_payload(conn):
    _, body = create_note(conn, "ana", {"title": "mine", "owner": "ben"})
    assert body["owner"] == "ana"


def test_quotes_in_title_are_stored_as_text(conn):
    title = "Ana's list'); DROP TABLE notes; --"
    status, body = create_note(conn, "ana", {"title": title})
    assert status == 201
    assert get_note(conn, "ana", body["id"]) == (200, body)


def test_get_own_note(conn):
    _, created = create_note(conn, "ana", {"title": "Groceries"})
    assert get_note(conn, "ana", created["id"]) == (200, created)


def test_get_requires_user(conn):
    _, created = create_note(conn, "ana", {"title": "Groceries"})
    status, body = get_note(conn, None, created["id"])
    assert status == 401
    assert "error" in body


def test_get_missing_note_is_404(conn):
    status, body = get_note(conn, "ana", 999)
    assert status == 404
    assert "error" in body


def test_get_someone_elses_note_is_404(conn):
    _, created = create_note(conn, "ana", {"title": "Private"})
    status, body = get_note(conn, "ben", created["id"])
    assert status == 404
    assert "Private" not in str(body)
