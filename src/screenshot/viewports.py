PRESETS: dict[str, dict[str, int]] = {
    "desktop": {"width": 1280, "height": 720},
    "laptop": {"width": 1440, "height": 900},
    "tablet": {"width": 768, "height": 1024},
    "tablet-landscape": {"width": 1024, "height": 768},
    "mobile": {"width": 375, "height": 667},
    "mobile-large": {"width": 414, "height": 896},
}

DEFAULT_PRESET = "desktop"


def resolve_viewport(
    preset: str | None = None,
    width: int | None = None,
    height: int | None = None,
    mobile: bool = False,
) -> dict[str, int]:
    if mobile:
        preset = "mobile"

    if preset:
        if preset not in PRESETS:
            available = ", ".join(sorted(PRESETS))
            raise ValueError(f"Unknown preset {preset!r}. Available: {available}")
        base = PRESETS[preset].copy()
    else:
        base = PRESETS[DEFAULT_PRESET].copy()

    if width is not None:
        base["width"] = width
    if height is not None:
        base["height"] = height

    return base
