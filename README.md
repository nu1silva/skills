# Skills

A collection of reusable GitHub Copilot skills for automating common tasks.

## Available Skills

### [`email-drafter`](skills/email-drafter/SKILL.md)

Drafts a personalized welcome/onboarding email for a new user using a standard template.

**Trigger:** Ask Copilot to draft a welcome or onboarding email and provide the recipient's details.

**Inputs required:**

| Field     | Description                        | Example              |
|-----------|------------------------------------|----------------------|
| `name`    | The recipient's full or first name | "Maria Santos"       |
| `email`   | The recipient's email address      | "maria@example.com"  |
| `country` | The recipient's country            | "Netherlands"        |

**Example prompt:**
> Draft a welcome email for Dan Silva, dan@example.com, Netherlands

---

### [`web-inspector`](skills/web-inspector/SKILL.md)

Navigates to a URL, optionally logs in, and extracts all interactive elements (buttons, links, forms, inputs) as structured JSON. Results are saved to a timestamped folder for easy reference.

**Trigger:** Ask Copilot to inspect a page, capture elements, or analyse a URL.

**Inputs required:**

| Field      | Required | Description                                              |
|------------|----------|----------------------------------------------------------|
| `url`      | ✅       | Full URL to inspect                                      |
| `username` | ❌       | Username/email if login is required                      |
| `password` | ❌       | Password if login is required                            |
| `output`   | ❌       | Output folder (default: `/tmp/inspections/<timestamp>/`) |

**Example prompt:**
> Inspect page https://example.com and capture all elements using skill web-inspector

**Output:** JSON report saved to `/tmp/inspections/<timestamp>/inspection.json`

---

## Structure

```
skills/
├── email-drafter/
│   ├── SKILL.md                  # Skill definition and instructions
│   └── assets/
│       └── welcome-template.md   # Email template with placeholders
└── web-inspector/
    ├── SKILL.md                  # Skill definition and instructions
    └── scripts/
        └── inspect_page.js       # Playwright-based page inspector
```

## License

See [LICENSE](LICENSE).
