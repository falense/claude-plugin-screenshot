---
name: screenshot
description: Capture a screenshot of a web page
arguments:
  - name: url
    description: URL to capture
    required: true
---

Capture a screenshot of the given URL using the screenshot tool.

Run the following command:

```bash
uv run --project ${CLAUDE_PLUGIN_ROOT} screenshot $ARGUMENTS
```

After the screenshot is captured, read the PNG file to analyze the page visually.
