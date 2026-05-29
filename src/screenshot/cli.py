import argparse
import sys

from screenshot.capture import capture
from screenshot.output import resolve_output_path
from screenshot.sessions import list_sessions, login
from screenshot.viewports import PRESETS, resolve_viewport


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="screenshot",
        description="Capture screenshots of web pages using Playwright.",
    )
    subparsers = parser.add_subparsers(dest="command")

    cap = subparsers.add_parser("capture", help="Take a screenshot (default)")
    _add_capture_args(cap)

    log = subparsers.add_parser("login", help="Interactive login to save a session")
    log.add_argument("name", help="Session name")
    log.add_argument("url", help="URL to navigate to for login")

    subparsers.add_parser("sessions", help="List saved sessions")
    subparsers.add_parser("presets", help="List viewport presets")

    return parser


def _add_capture_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("url", help="URL to capture")
    parser.add_argument("-o", "--output", help="Output file path")
    parser.add_argument("--width", type=int, help="Viewport width")
    parser.add_argument("--height", type=int, help="Viewport height")
    parser.add_argument("--preset", help="Named viewport preset")
    parser.add_argument(
        "--mobile", action="store_true", help="Shortcut for --preset mobile"
    )
    parser.add_argument(
        "--full-page", action="store_true", help="Capture full scrollable page"
    )
    parser.add_argument(
        "--timeout", type=int, default=30000, help="Navigation timeout in ms"
    )
    parser.add_argument("--session", help="Use a saved session for authentication")
    parser.add_argument(
        "--dump-html", action="store_true", help="Save rendered HTML alongside PNG"
    )
    parser.add_argument(
        "--dark", action="store_true", help="Capture in dark color scheme"
    )
    parser.add_argument("--click", metavar="SELECTOR", help="Click element before capture")
    parser.add_argument(
        "--click-delay", type=float, default=0.5, help="Delay after click in seconds"
    )


def _handle_capture(args: argparse.Namespace) -> None:
    viewport = resolve_viewport(
        preset=args.preset,
        width=args.width,
        height=args.height,
        mobile=args.mobile,
    )
    output = resolve_output_path(args.output, args.url, args.session)

    result = capture(
        args.url,
        output=output,
        viewport=viewport,
        full_page=args.full_page,
        dark=args.dark,
        session=args.session,
        click_selector=args.click,
        click_delay=args.click_delay,
        dump_html=args.dump_html,
        timeout=args.timeout,
    )

    print(result.screenshot_path.resolve())
    if result.html_path:
        print(result.html_path.resolve())


def _handle_login(args: argparse.Namespace) -> None:
    login(args.name, args.url)


def _handle_sessions() -> None:
    sessions = list_sessions()
    if not sessions:
        print("No saved sessions.")
        return
    for s in sessions:
        print(f"  {s['name']:20s}  last used: {s['last_used']}")


def _handle_presets() -> None:
    for name, vp in PRESETS.items():
        print(f"  {name:20s}  {vp['width']}x{vp['height']}")


SUBCOMMANDS = {"capture", "login", "sessions", "presets"}


def main() -> None:
    parser = _build_parser()

    argv = sys.argv[1:]
    if not argv:
        parser.print_help()
        sys.exit(1)

    if argv[0] not in SUBCOMMANDS:
        argv = ["capture"] + argv

    args = parser.parse_args(argv)

    try:
        match args.command:
            case "capture":
                _handle_capture(args)
            case "login":
                _handle_login(args)
            case "sessions":
                _handle_sessions()
            case "presets":
                _handle_presets()
    except KeyboardInterrupt:
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
