---
name: web-inspector
description: Given a URL (and optional login credentials), extract all interactive elements from a webpage — buttons, links, forms, and inputs — and return them as structured JSON. Use this skill whenever the user wants to understand what's on a page, inspect a UI, map out a website's elements, or extract page structure. Trigger even for casual requests like "what's on this page", "inspect this URL", "what buttons/forms does this site have", or "analyse this webpage".
---

# Web Inspector Skill

Navigates to a URL, optionally logs in, and extracts all interactive elements as structured JSON.

## Inputs

| Field      | Required | Description                              |
|------------|----------|------------------------------------------|
| `url`      | ✅       | Full URL to inspect                      |
| `username` | ❌       | Username/email if login is required      |
| `password` | ❌       | Password if login is required            |
| `output`   | ❌       | Output folder (default: `/tmp/inspections/<timestamp>/`) |

> ⚠️ Credentials are passed only as runtime arguments — never saved to disk.

## Instructions

1. Collect the URL from the user. Ask for credentials only if the page requires login.
2. Generate a timestamp in the format `YYYYMMDD_HHmmss` and create an output folder:
   ```
   /tmp/inspections/<timestamp>/
   ```
3. Set the output path to `<output_folder>/inspection.json`.
4. Run the inspector script:

```bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S) && mkdir -p /tmp/inspections/$TIMESTAMP && node <skill_dir>/scripts/inspect_page.js "<url>" "<username>" "<password>" "/tmp/inspections/$TIMESTAMP/inspection.json"
```

Omit username/password args if no login is needed:
```bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S) && mkdir -p /tmp/inspections/$TIMESTAMP && node <skill_dir>/scripts/inspect_page.js "<url>" "" "" "/tmp/inspections/$TIMESTAMP/inspection.json"
```

5. Parse the JSON output and present a **summary** to the user in chat:
   - Page title and URL
   - Output folder path
   - Count of buttons, links, forms, inputs
   - Notable elements (e.g. primary CTAs, form fields, key nav links)
6. Present the full JSON file path for download.
7. Offer to dig deeper into any specific element type if the user wants.

## Output Structure

```json
{
  "url": "https://...",
  "title": "Page Title",
  "capturedAt": "2025-01-01T00:00:00Z",
  "summary": {
    "totalButtons": 4,
    "totalLinks": 12,
    "totalForms": 1,
    "totalStandaloneInputs": 0
  },
  "buttons": [ { "text": "Sign Up", "type": "submit", "disabled": false, ... } ],
  "links":   [ { "text": "Home", "href": "https://...", ... } ],
  "forms":   [ { "action": "/login", "method": "post", "fields": [ ... ] } ],
  "standaloneInputs": [ ... ]
}
```

## Troubleshooting

| Problem | Fix |
|---|---|
| Empty results | Page may be JS-heavy; the script uses `networkidle` wait — increase timeout if needed |
| Login fields not found | Non-standard selectors; ask user for field `name`/`id` |
| CAPTCHA blocking login | Cannot be bypassed; inspect the pre-login page instead |