# Screenshot Tool

CLI tool for capturing web page screenshots using Playwright.

## Development

```bash
uv run screenshot <url>           # capture a screenshot
uv run screenshot presets          # list viewport presets
uv run screenshot sessions         # list saved sessions
uv run pytest                      # run tests
```

## Project Structure

- `src/screenshot/cli.py` — CLI entry point and argument parsing
- `src/screenshot/capture.py` — core screenshot capture logic
- `src/screenshot/browser.py` — Playwright browser lifecycle management
- `src/screenshot/sessions.py` — authenticated session save/load
- `src/screenshot/viewports.py` — viewport preset definitions
- `src/screenshot/output.py` — output path and filename generation

## Key Decisions

- Uses argparse (no external CLI framework)
- Sync Playwright API
- Sessions stored at `~/.screenshot_sessions/<name>/state.json`
- Screenshots output to `.screenshots/` by default

## Versioning

- Always bump the version in `.claude-plugin/plugin.json` after any changes, following semver:
  - `patch` for bug fixes
  - `minor` for new features or non-breaking changes
  - `major` for breaking changes
