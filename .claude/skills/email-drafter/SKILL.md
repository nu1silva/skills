---
name: email-drafter
description: Draft a personalized welcome/onboarding email for a new user given their name, email address, and country. Use this skill whenever the user provides a name, email, and country and wants to generate a welcome email, onboarding email, or any personalized email from a template. Trigger even if the user says something casual like "draft a welcome email for John" or "send onboarding email to this user".
---

# Email Drafter Skill

This skill drafts a personalized welcome/onboarding email by filling in a standard template with the user's details.

## Inputs Required

Collect these three fields (ask if any are missing):

| Field     | Description                        | Example              |
|-----------|------------------------------------|----------------------|
| `name`    | The recipient's full or first name | "Maria Santos"       |
| `email`   | The recipient's email address      | "maria@example.com"  |
| `country` | The recipient's country            | "Netherlands"        |

## Instructions

1. **Read the template** from `assets/welcome-template.md`.
2. **Replace all placeholders** in the template:
   - `{{name}}` → recipient's name
   - `{{email}}` → recipient's email address
   - `{{country}}` → recipient's country
3. **Output the final email** clearly formatted, including:
   - The subject line (clearly labeled)
   - The full email body
4. Keep the tone warm, friendly, and professional.
5. Do not invent additional personalization beyond what the template provides — keep it clean and consistent.

## Output Format

Present the drafted email like this:

---
**Subject:** <subject line here>

<full email body here>

---

Then offer to make any adjustments the user wants (e.g., tone, company name, extra details).