---
name: email-drafter
description: Draft and send a personalized welcome/onboarding email for a new user given their name, email address, and country. Use this skill whenever the user provides a name, email, and country and wants to generate or send a welcome email, onboarding email, or any personalized email from a template. Trigger even if the user says something casual like "draft a welcome email for John", "send onboarding email to this user", or "email this person a welcome".
---

# Email Drafter Skill (with Gmail Send)

This skill drafts a personalized welcome/onboarding email and — with the user's confirmation — sends it directly via Gmail MCP.

**MCP required:** Gmail (`https://gmailmcp.googleapis.com/mcp/v1`) — for sending. Falls back to draft-only if unavailable.

## Inputs Required

Collect these fields (ask if any are missing):

| Field     | Description                        | Example              |
|-----------|------------------------------------|----------------------|
| `name`    | The recipient's full or first name | "Maria Santos"       |
| `email`   | The recipient's email address      | "maria@example.com"  |
| `country` | The recipient's country            | "Netherlands"        |

## Instructions

### Step 1 — Draft the email

1. Read the template from `assets/welcome-template.md`.
2. Replace all placeholders:
   - `{{name}}` → recipient's name
   - `{{email}}` → recipient's email address
   - `{{country}}` → recipient's country
3. Present the drafted email clearly in chat:

---
**Subject:** <subject line>

<full email body>

---

### Step 2 — Confirm before sending

Always ask the user explicitly before sending:

> "Shall I send this to **{email}** via Gmail, or would you like to make any changes first?"

Never send without explicit confirmation. If the user wants edits, apply them and show the updated draft before asking again.

### Step 3 — Send via Gmail MCP

Once confirmed, use the Gmail MCP to send the email:

- **To:** recipient's email address
- **Subject:** the drafted subject line
- **Body:** the full drafted email body (plain text)

Use the Gmail MCP `send_email` (or equivalent) tool. Pass the subject and body exactly as drafted — do not truncate or summarize.

### Step 4 — Confirm delivery

After the Gmail MCP responds, tell the user:
- ✅ "Email sent successfully to {email}" — if successful
- ❌ "Sending failed: {reason}" — if there was an error, and offer to retry or copy the draft for manual sending

## Tone & Style

- Warm, friendly, and professional
- Do not invent personalization beyond what the template provides
- If the user wants to customize the company name or add details, apply edits before sending

## Fallback (if Gmail MCP unavailable)

If the Gmail MCP is not connected or returns an auth error:
1. Inform the user: "Gmail isn't connected — I can't send directly."
2. Still present the fully drafted email so they can copy and send it manually.
3. Suggest they connect Gmail in their Claude settings.