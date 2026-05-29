---
name: screenshot
description: >
  Capture screenshots of web pages. Use when the user asks to take a screenshot,
  capture a web page, see what a page looks like, or verify visual output of a
  web application. Also use when the user says "screenshot this", "show me the page",
  "capture the site", or "take a picture of".
---

# screenshot

Capture screenshots of web pages using headless Chromium.

## Usage

All commands must be run from the plugin root directory. Use `${CLAUDE_PLUGIN_ROOT}` to reference it:

```bash
cd ${CLAUDE_PLUGIN_ROOT} && uv run screenshot <url>
```

### Basic screenshot

```bash
cd ${CLAUDE_PLUGIN_ROOT} && uv run screenshot https://example.com
```

### With options

```bash
cd ${CLAUDE_PLUGIN_ROOT} && uv run screenshot https://example.com --preset mobile --full-page --dark
```

### Authenticated pages

```bash
# First: save a session (opens browser for manual login)
cd ${CLAUDE_PLUGIN_ROOT} && uv run screenshot login mysite https://example.com/login

# Then: use the session
cd ${CLAUDE_PLUGIN_ROOT} && uv run screenshot https://example.com/dashboard --session mysite
```

## Available viewports

desktop (1280x720), laptop (1440x900), tablet (768x1024),
tablet-landscape (1024x768), mobile (375x667), mobile-large (414x896).

```bash
cd ${CLAUDE_PLUGIN_ROOT} && uv run screenshot presets
```

## Output

Screenshots are saved to `.screenshots/` in the current working directory with auto-generated filenames.
Use `-o path.png` for an explicit output path.
The tool prints the absolute path of the saved file to stdout.

## Other features

- `--dump-html` — save rendered HTML alongside the PNG
- `--dark` — capture in dark color scheme
- `--click SELECTOR` — click an element before capture
- `--full-page` — capture the entire scrollable page

## Notes

- Chromium is auto-installed on first run.
- `${CLAUDE_PLUGIN_ROOT}` is set by Claude Code and points to the plugin's install directory.
