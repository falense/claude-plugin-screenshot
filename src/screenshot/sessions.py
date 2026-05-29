import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from screenshot.browser import ensure_installed, managed_browser

SESSIONS_DIR = Path.home() / ".screenshot_sessions"


def get_session_path(name: str) -> Path:
    return SESSIONS_DIR / name / "state.json"


def session_exists(name: str) -> bool:
    return get_session_path(name).is_file()


def load_session(name: str) -> str:
    path = get_session_path(name)
    if not path.is_file():
        available = list_sessions()
        if available:
            names = ", ".join(s["name"] for s in available)
            raise FileNotFoundError(
                f"Session {name!r} not found. Available sessions: {names}"
            )
        raise FileNotFoundError(
            f"Session {name!r} not found. No sessions saved yet. "
            "Use 'screenshot login <name> <url>' to create one."
        )
    return str(path)


def save_session(name: str, storage_state: dict) -> Path:
    path = get_session_path(name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(storage_state, indent=2))
    return path


def list_sessions() -> list[dict]:
    if not SESSIONS_DIR.is_dir():
        return []
    sessions = []
    for entry in sorted(SESSIONS_DIR.iterdir()):
        state_file = entry / "state.json"
        if state_file.is_file():
            modified = datetime.fromtimestamp(
                state_file.stat().st_mtime, tz=timezone.utc
            )
            sessions.append({
                "name": entry.name,
                "last_used": modified.isoformat(),
            })
    return sessions


def login(name: str, url: str) -> Path:
    ensure_installed()
    print(
        f"Opening browser for login. Navigate to {url} and log in.\n"
        "Close the browser when done to save the session.",
        file=sys.stderr,
    )
    with managed_browser(headless=False) as browser:
        context = browser.new_context()
        page = context.new_page()
        page.goto(url, wait_until="domcontentloaded")
        page.wait_for_event("close", timeout=0)
        state = context.storage_state()
        context.close()

    path = save_session(name, state)
    print(f"Session {name!r} saved.", file=sys.stderr)
    return path
