---
name: openapi-quality-check
description: >
  Analyze an OpenAPI specification file for quality issues across four dimensions:
  schema validity, completeness, REST design best practices, and security. Use this
  skill whenever a user uploads or provides an OpenAPI spec (JSON format) and asks
  for a review, audit, quality check, lint, or feedback — or whenever they ask things
  like "check my API spec", "what's wrong with this OpenAPI file", "review my swagger",
  or "is this spec production-ready?". Always use this skill for OpenAPI/Swagger quality
  tasks — do not attempt to review specs manually without it.
---

# OpenAPI Quality Check Skill

Performs a structured quality audit of a JSON OpenAPI 3.x specification and produces
a severity-ranked report covering four dimensions: schema validity, completeness,
REST design best practices, and security.

## Step 1 — Locate the spec file

The user will either:

- Upload a `.json` file → find it at `/mnt/user-data/uploads/<filename>`
- Paste a path or URL → use that directly
- Paste raw JSON inline → save it to `/tmp/openapi_spec.json` first

If no file is present and the user hasn't pasted content, ask them to provide the spec.

## Step 2 — Run the analyzer script

Install dependencies and run the bundled script:

```bash
python3 /mnt/skills/user/openapi-quality-check/scripts/analyze_spec.py <path_to_spec.json>
```

The script self-installs `openapi-spec-validator` if needed. It outputs a full
Markdown quality report directly to stdout — capture and present it to the user.

If the script path above fails (e.g. skill is installed elsewhere), find it with:

```bash
find /mnt/skills -name "analyze_spec.py" 2>/dev/null
```

## Step 3 — Present the report

Print the Markdown report output in full. Then add a brief **2–3 sentence summary**
in your own words highlighting the most important findings — especially any CRITICAL
or HIGH severity issues — and what the user should fix first.

## What the report covers

The script checks across four categories, each tagged by severity:

| Severity    | Meaning                                                                     |
| ----------- | --------------------------------------------------------------------------- |
| 🔴 CRITICAL | Spec is invalid or unparseable — must fix before use                        |
| 🟠 HIGH     | Significant risk: security gaps, missing success responses, exposed secrets |
| 🟡 MEDIUM   | Quality issues: missing operationIds, undocumented errors, bad versioning   |
| 🔵 LOW      | Polish items: missing descriptions, examples, tags, naming conventions      |

**Schema Validity** — Is the spec well-formed OpenAPI 3.x? Catches structural errors
that would break code generators and validators.

**Completeness** — Are all operations described well? Checks for missing summaries,
descriptions, operationIds, error responses, request body schemas, parameter
descriptions, and examples.

**Design Best Practices** — Does the API follow REST conventions? Checks for:

- Semantic versioning in `info.version`
- API version prefix in paths (e.g. `/v1/...`)
- Noun-based paths (no `/getUsers`, `/createOrder`)
- Plural resource names for collections
- Correct HTTP method usage (no GET with body)
- kebab-case path segments
- Tags on all operations

**Security** — Are endpoints protected? Checks for:

- Presence of `securitySchemes`
- Unsafe auth methods (HTTP Basic, API key in query string)
- Operations missing security requirements
- Sensitive field names exposed in responses (`password`, `token`, `secret`, etc.)

## Notes

- Supports OpenAPI 3.x specs in JSON format only
- For YAML specs, ask the user to convert first: `python3 -c "import sys,json,yaml; json.dump(yaml.safe_load(sys.stdin), sys.stdout, indent=2)" < spec.yaml > spec.json`
- The quality score (0–100) deducts: 20 per CRITICAL, 10 per HIGH, 5 per MEDIUM, 1 per LOW
- Encourage the user to fix CRITICAL and HIGH issues first, then iterate
