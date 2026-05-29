from pathlib import Path

from screenshot.output import generate_filename, resolve_output_path, sanitize_domain


def test_sanitize_domain_simple():
    assert sanitize_domain("https://example.com/page") == "example_com"


def test_sanitize_domain_strips_www():
    assert sanitize_domain("https://www.example.com") == "example_com"


def test_sanitize_domain_with_port():
    assert sanitize_domain("http://localhost:3000/path") == "localhost"


def test_generate_filename_basic():
    name = generate_filename("https://example.com")
    assert name.startswith("screenshot_example_com_")
    assert name.endswith(".png")


def test_generate_filename_with_session():
    name = generate_filename("https://example.com", session="mysite")
    assert "mysite" in name
    assert name.startswith("screenshot_example_com_mysite_")


def test_resolve_output_path_explicit(tmp_path):
    path = resolve_output_path(str(tmp_path / "out.png"), "https://example.com")
    assert path == tmp_path / "out.png"


def test_resolve_output_path_auto(tmp_screenshots):
    path = resolve_output_path(None, "https://example.com")
    assert path.parent.name == ".screenshots"
    assert path.suffix == ".png"
    assert path.parent.exists()


def test_resolve_output_path_creates_parents(tmp_path):
    nested = tmp_path / "a" / "b" / "c" / "shot.png"
    path = resolve_output_path(str(nested), "https://example.com")
    assert path == nested
    assert nested.parent.exists()
