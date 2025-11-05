---
name: webapp-testing
description: Toolkit for interacting with and testing React Native web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browser logs.
license: Complete terms in LICENSE.txt
---

# Web Application Testing

To test local web applications, write native Python Playwright scripts.

## Project Context: React Native + Expo

This project uses **React Native 0.81 + Expo 54** with web support via `@expo/metro-runtime`.

**Development Environment**:
- Backend: `http://localhost:8000` (FastAPI)
- Frontend: `http://localhost:8081` (Expo web)
- Start command: `make webapp` (starts both services)

**Important**: Always test against `http://localhost:8081` unless specified otherwise.

**Python Environment**:
This skill uses a shared uv-based virtual environment at `.claude/skills/.venv`. All scripts should be run from the project root using `uv run`:

```bash
# Run scripts with uv
uv run python .claude/skills/webapp-testing/scripts/with_server.py --help
uv run python .claude/skills/webapp-testing/examples/element_discovery.py
```

**Helper Scripts Available**:
- `scripts/with_server.py` - Manages server lifecycle (supports multiple servers)

**Always run scripts with `--help` first** to see usage. DO NOT read the source until you try running the script first and find that a customized solution is abslutely necessary. These scripts can be very large and thus pollute your context window. They exist to be called directly as black-box scripts rather than ingested into your context window.

## Decision Tree: Choosing Your Approach

```
User task → Is it static HTML?
    ├─ Yes → Read HTML file directly to identify selectors
    │         ├─ Success → Write Playwright script using selectors
    │         └─ Fails/Incomplete → Treat as dynamic (below)
    │
    └─ No (dynamic webapp) → Is the server already running?
        ├─ No → Run: python scripts/with_server.py --help
        │        Then use the helper + write simplified Playwright script
        │
        └─ Yes → Reconnaissance-then-action:
            1. Navigate and wait for networkidle
            2. Take screenshot or inspect DOM
            3. Identify selectors from rendered state
            4. Execute actions with discovered selectors
```

## Example: Using with_server.py

To start a server, run `--help` first, then use the helper:

**For this project (React Native + FastAPI):**
```bash
# Use project's make command to start services, then run tests
make webapp  # Starts backend:8000 + frontend:8081
# Wait ~30s for services to be ready, then run:
uv run python your_automation.py
```

**Alternative: Using with_server.py directly:**
```bash
uv run python .claude/skills/webapp-testing/scripts/with_server.py \
  --server "make dev-backend" --port 8000 \
  --server "make dev-frontend" --port 8081 \
  -- uv run python your_automation.py
```

To create an automation script, include only Playwright logic:
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True) # Always launch chromium in headless mode
    page = browser.new_page()
    page.goto('http://localhost:8081') # React Native web on port 8081
    page.wait_for_load_state('networkidle') # CRITICAL: Wait for JS/React to execute
    # ... your automation logic
    browser.close()
```

## Reconnaissance-Then-Action Pattern

1. **Inspect rendered DOM**:
   ```python
   page.screenshot(path='/tmp/inspect.png', full_page=True)
   content = page.content()
   page.locator('button').all()
   ```

2. **Identify selectors** from inspection results

3. **Execute actions** using discovered selectors

## Common Pitfall

❌ **Don't** inspect the DOM before waiting for `networkidle` on dynamic apps
✅ **Do** wait for `page.wait_for_load_state('networkidle')` before inspection

## Best Practices

- **Use bundled scripts as black boxes** - To accomplish a task, consider whether one of the scripts available in `scripts/` can help. These scripts handle common, complex workflows reliably without cluttering the context window. Use `--help` to see usage, then invoke directly. 
- Use `sync_playwright()` for synchronous scripts
- Always close the browser when done
- Use descriptive selectors: `text=`, `role=`, CSS selectors, or IDs
- Add appropriate waits: `page.wait_for_selector()` or `page.wait_for_timeout()`

## Reference Files

- **examples/** - Examples showing common patterns:
  - `element_discovery.py` - Discovering buttons, links, and inputs on a page
  - `static_html_automation.py` - Using file:// URLs for local HTML
  - `console_logging.py` - Capturing console logs during automation