import json

import pytest

from screenshot.sessions import (
    get_session_path,
    list_sessions,
    load_session,
    save_session,
    session_exists,
)


@pytest.fixture
def sessions_dir(tmp_path, monkeypatch):
    monkeypatch.setattr("screenshot.sessions.SESSIONS_DIR", tmp_path)
    return tmp_path


def test_get_session_path(sessions_dir):
    path = get_session_path("mysite")
    assert path == sessions_dir / "mysite" / "state.json"


def test_session_exists_false(sessions_dir):
    assert not session_exists("nonexistent")


def test_session_exists_true(sessions_dir):
    state_path = sessions_dir / "mysite" / "state.json"
    state_path.parent.mkdir(parents=True)
    state_path.write_text("{}")
    assert session_exists("mysite")


def test_save_and_load_session(sessions_dir):
    state = {"cookies": [{"name": "auth", "value": "token123"}]}
    save_session("mysite", state)

    path = load_session("mysite")
    loaded = json.loads(open(path).read())
    assert loaded == state


def test_load_nonexistent_session_raises(sessions_dir):
    with pytest.raises(FileNotFoundError, match="No sessions saved"):
        load_session("nonexistent")


def test_load_nonexistent_lists_available(sessions_dir):
    save_session("existing", {"cookies": []})
    with pytest.raises(FileNotFoundError, match="existing"):
        load_session("nonexistent")


def test_list_sessions_empty(sessions_dir):
    assert list_sessions() == []


def test_list_sessions_returns_entries(sessions_dir):
    save_session("alpha", {"cookies": []})
    save_session("beta", {"cookies": []})
    sessions = list_sessions()
    names = [s["name"] for s in sessions]
    assert "alpha" in names
    assert "beta" in names
    assert all("last_used" in s for s in sessions)
