# screenshot

A Claude Code plugin that captures web page screenshots using Playwright. Designed for AI agent workflows where an agent needs to visually inspect rendered UI — take a screenshot, read the PNG, reason about layout and styling.

Supports viewport presets, authenticated sessions, dark mode, full-page capture, and HTML dumping.

## Install

As a Claude Code plugin:

```
/plugin install screenshot@dig-experimental
```

Or clone and run directly:

```bash
git clone https://github.com/falense/claude-plugin-screenshot.git
cd claude-plugin-screenshot
uv run screenshot https://example.com
```

Chromium is installed automatically on first run.

## Usage

### Basic screenshot

```bash
uv run screenshot https://example.com
```

Saves a PNG to `.screenshots/` and prints the absolute path to stdout.

### Viewport presets

```bash
uv run screenshot https://example.com --preset mobile
uv run screenshot https://example.com --preset tablet
uv run screenshot https://example.com --width 1920 --height 1080
```

Available presets:

| Preset | Size |
|---|---|
| desktop (default) | 1280×720 |
| laptop | 1440×900 |
| tablet | 768×1024 |
| tablet-landscape | 1024×768 |
| mobile | 375×667 |
| mobile-large | 414×896 |

### Authenticated pages

Save a browser session by logging in interactively (opens a visible browser):

```bash
uv run screenshot login myapp https://myapp.com/login
```

Then reuse the session for headless captures:

```bash
uv run screenshot https://myapp.com/dashboard --session myapp
```

Sessions are stored in `~/.screenshot_sessions/` and persist across runs.

### Additional options

```bash
uv run screenshot https://example.com --full-page          # capture entire scrollable page
uv run screenshot https://example.com --dark               # dark color scheme
uv run screenshot https://example.com --dump-html          # save rendered HTML alongside PNG
uv run screenshot https://example.com --click "#open-menu" # click element before capture
uv run screenshot https://example.com -o report.png        # explicit output path
```

### Listing resources

```bash
uv run screenshot presets     # list viewport presets
uv run screenshot sessions    # list saved sessions
```

## CLI reference

```
screenshot <url> [options]
screenshot login <name> <url>
screenshot sessions
screenshot presets

Options:
  -o, --output PATH         Output file path (default: .screenshots/<auto>.png)
  --width N                 Viewport width
  --height N                Viewport height
  --preset NAME             Named viewport preset
  --mobile                  Shortcut for --preset mobile
  --full-page               Capture full scrollable page
  --timeout MS              Navigation timeout (default: 30000)
  --session NAME            Use a saved session for authentication
  --dump-html               Save rendered HTML alongside the PNG
  --dark                    Capture in dark color scheme
  --click SELECTOR          Click an element before capture
  --click-delay SEC         Delay after click in seconds (default: 0.5)
```

## Agent usage pattern

The tool is built for the agent loop: run the tool, read the image, reason about it.

```bash
# capture
uv run screenshot https://myapp.com/dashboard --session myapp

# the agent then reads the PNG to analyze layout, check for visual regressions, etc.
```

Output is deliberately minimal — just the file path on stdout, errors on stderr, non-zero exit on failure.

## Development

```bash
uv run pytest              # run tests
uv run screenshot <url>    # test capture
```

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
