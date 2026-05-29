from screenshot.cli import _build_parser


def test_capture_subcommand():
    parser = _build_parser()
    args = parser.parse_args(["capture", "https://example.com"])
    assert args.command == "capture"
    assert args.url == "https://example.com"
    assert args.output is None
    assert args.full_page is False
    assert args.dark is False


def test_capture_with_options():
    parser = _build_parser()
    args = parser.parse_args([
        "capture", "https://example.com",
        "-o", "out.png",
        "--preset", "mobile",
        "--full-page",
        "--dark",
        "--dump-html",
        "--click", "#menu-button",
        "--click-delay", "1.0",
        "--timeout", "5000",
    ])
    assert args.output == "out.png"
    assert args.preset == "mobile"
    assert args.full_page is True
    assert args.dark is True
    assert args.dump_html is True
    assert args.click == "#menu-button"
    assert args.click_delay == 1.0
    assert args.timeout == 5000


def test_capture_with_session():
    parser = _build_parser()
    args = parser.parse_args(["capture", "https://example.com", "--session", "mysite"])
    assert args.session == "mysite"


def test_capture_mobile_flag():
    parser = _build_parser()
    args = parser.parse_args(["capture", "https://example.com", "--mobile"])
    assert args.mobile is True


def test_login_subcommand():
    parser = _build_parser()
    args = parser.parse_args(["login", "mysite", "https://example.com/login"])
    assert args.command == "login"
    assert args.name == "mysite"
    assert args.url == "https://example.com/login"


def test_sessions_subcommand():
    parser = _build_parser()
    args = parser.parse_args(["sessions"])
    assert args.command == "sessions"


def test_presets_subcommand():
    parser = _build_parser()
    args = parser.parse_args(["presets"])
    assert args.command == "presets"
