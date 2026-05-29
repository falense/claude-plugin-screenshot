import subprocess
import sys
from contextlib import contextmanager

from playwright.sync_api import Browser, BrowserContext, sync_playwright


def ensure_installed() -> None:
    try:
        subprocess.run(
            [sys.executable, "-m", "playwright", "install", "--dry-run", "chromium"],
            capture_output=True,
            check=True,
        )
    except subprocess.CalledProcessError:
        print("Installing Chromium browser...", file=sys.stderr)
        subprocess.run(
            [sys.executable, "-m", "playwright", "install", "chromium"],
            check=True,
        )


@contextmanager
def managed_browser(*, headless: bool = True):
    pw = sync_playwright().start()
    try:
        browser = pw.chromium.launch(headless=headless)
        try:
            yield browser
        finally:
            browser.close()
    finally:
        pw.stop()


@contextmanager
def managed_context(
    browser: Browser,
    viewport: dict[str, int],
    *,
    session_path: str | None = None,
    dark: bool = False,
    locale: str = "en-US",
    timezone_id: str = "America/New_York",
) -> BrowserContext:
    kwargs: dict = {
        "viewport": viewport,
        "locale": locale,
        "timezone_id": timezone_id,
        "user_agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        ),
    }
    if session_path:
        kwargs["storage_state"] = session_path
    if dark:
        kwargs["color_scheme"] = "dark"

    context = browser.new_context(**kwargs)
    try:
        yield context
    finally:
        context.close()
