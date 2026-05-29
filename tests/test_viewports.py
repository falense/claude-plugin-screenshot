import pytest

from screenshot.viewports import PRESETS, resolve_viewport


def test_default_viewport():
    vp = resolve_viewport()
    assert vp == {"width": 1280, "height": 720}


def test_preset_mobile():
    vp = resolve_viewport(preset="mobile")
    assert vp == {"width": 375, "height": 667}


def test_mobile_flag():
    vp = resolve_viewport(mobile=True)
    assert vp == {"width": 375, "height": 667}


def test_preset_with_width_override():
    vp = resolve_viewport(preset="tablet", width=800)
    assert vp == {"width": 800, "height": 1024}


def test_explicit_dimensions():
    vp = resolve_viewport(width=1920, height=1080)
    assert vp == {"width": 1920, "height": 1080}


def test_unknown_preset_raises():
    with pytest.raises(ValueError, match="Unknown preset"):
        resolve_viewport(preset="nonexistent")


def test_all_presets_have_width_and_height():
    for name, vp in PRESETS.items():
        assert "width" in vp, f"Preset {name} missing width"
        assert "height" in vp, f"Preset {name} missing height"
