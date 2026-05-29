from dataclasses import dataclass
from pathlib import Path

from screenshot.browser import ensure_installed, managed_browser, managed_context
from screenshot.sessions import load_session


@dataclass
class CaptureResult:
    screenshot_path: Path
    html_path: Path | None = None


def capture(
    url: str,
    *,
    output: Path,
    viewport: dict[str, int],
    full_page: bool = False,
    dark: bool = False,
    session: str | None = None,
    click_selector: str | None = None,
    click_delay: float = 0.5,
    dump_html: bool = False,
    timeout: int = 30000,
) -> CaptureResult:
    ensure_installed()

    session_path = load_session(session) if session else None

    with managed_browser() as browser:
        with managed_context(
            browser, viewport, session_path=session_path, dark=dark
        ) as context:
            page = context.new_page()
            page.goto(url, wait_until="load", timeout=timeout)
            page.wait_for_timeout(1000)

            if click_selector:
                page.click(click_selector)
                page.wait_for_timeout(int(click_delay * 1000))

            page.screenshot(path=str(output), full_page=full_page)

            html_path = None
            if dump_html:
                html_path = output.with_suffix(".html")
                html_path.write_text(page.content())

    return CaptureResult(screenshot_path=output, html_path=html_path)
