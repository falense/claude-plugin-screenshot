import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

SCREENSHOTS_DIR = ".screenshots"


def sanitize_domain(url: str) -> str:
    parsed = urlparse(url)
    hostname = parsed.hostname or "unknown"
    hostname = hostname.removeprefix("www.")
    return re.sub(r"[^a-zA-Z0-9]", "_", hostname)


def generate_filename(url: str, session: str | None = None) -> str:
    domain = sanitize_domain(url)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    parts = ["screenshot", domain]
    if session:
        parts.append(session)
    parts.append(timestamp)
    return "_".join(parts) + ".png"


def resolve_output_path(
    explicit: str | None,
    url: str,
    session: str | None = None,
) -> Path:
    if explicit:
        path = Path(explicit)
    else:
        directory = Path(SCREENSHOTS_DIR)
        filename = generate_filename(url, session)
        path = directory / filename

    path.parent.mkdir(parents=True, exist_ok=True)
    return path
