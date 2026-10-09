---
name: openapi-gherkin
description: Given an OpenAPI or Swagger spec file (JSON or YAML), parse every endpoint, method, response code, and error path, then generate a comprehensive Gherkin .feature file with full test coverage. Use this skill whenever the user mentions OpenAPI, Swagger, API spec, API testing, Gherkin, BDD, feature files, or says things like "generate tests from my spec", "create BDD scenarios for my API", "write Gherkin for this endpoint", "test coverage for my OpenAPI file", or uploads a .json/.yaml file that looks like an API spec. Trigger even if the user just says "here is my API spec, generate tests".
---

# OpenAPI → Gherkin Skill

Parses an OpenAPI 3.x or Swagger 2.x spec and generates a `.feature` file with full Gherkin test coverage — happy paths, every documented error code, validation scenarios, and auth paths.

## Inputs

| Field | Required | Description |
|---|---|---|
| `spec_file` | ✅ | Path to OpenAPI JSON or YAML file |
| `output_file` | ❌ | Output path for `.feature` file (default: `/mnt/user-data/outputs/<api-name>.feature`) |

## What gets generated

For every endpoint + HTTP method the script produces:

| Scenario type | Trigger |
|---|---|
| `[HAPPY]` | One per endpoint — covers the primary success code (200/201/204) |
| `[ERROR]` | One per documented 4xx code (400, 404, 409, 410…) |
| `[AUTH]` | 401 and 403 — generated from documented codes OR inferred from security schemes |
| `[VALIDATION]` | One per required request body field — missing field → 400/422 |
| `[REDIRECT]` | One per documented 3xx code |
| `[RATE LIMIT]` | 429 if documented |
| `[SERVER ERROR]` | One per documented 5xx code |

## Instructions

### Step 1 — Get the spec file

Accept the spec as:
- An uploaded file → available at `/mnt/user-data/uploads/<filename>`
- A path the user provides
- Ask if unclear

### Step 2 — Install dependencies if needed

```bash
pip install pyyaml --break-system-packages 2>/dev/null || true
```

### Step 3 — Run the generator

```bash
python <skill_dir>/scripts/generate_gherkin.py \
  "<spec_file_path>" \
  "/mnt/user-data/outputs/<api_name>.feature"
```

Replace `<skill_dir>` with the actual path to this skill's directory.

### Step 4 — Summarise results in chat

After running, tell the user:
- API name and version detected
- Number of endpoints parsed
- Total scenarios generated, broken down by type:
  - Happy path, Validation, Auth, Error, Server Error
- Path to the output `.feature` file

Format the summary like:
```
✅ Generated: my-api.feature
   API: Petstore v1.0.0
   Endpoints: 12 | Scenarios: 47
   ├── Happy path:   12
   ├── Validation:   8
   ├── Auth:         18
   ├── Error (4xx):  7
   └── Server error: 2
```

### Step 5 — Present the file

Use `present_files` to give the user the `.feature` file for download.

### Step 6 — Offer follow-up

After presenting, offer:
1. "Want me to add a Background block for shared auth setup?"
2. "Should I add Scenario Outline examples for parameterised inputs?"
3. "Want tags added (e.g. @smoke, @regression, @auth) for selective test runs?"

Apply any requested refinements and re-present.

## Quality rules to apply manually (if refining output)

- Scenario titles must be unique and self-describing
- Each scenario tests exactly one behaviour
- `Given` = precondition, `When` = action, `Then` = assertion — never mix
- No implementation details (SQL, code) in steps
- Read `references/gherkin-best-practices.md` for full style guide

## Troubleshooting

| Problem | Fix |
|---|---|
| YAML parse error | Ensure `pyyaml` is installed (Step 2) |
| Empty output | Spec may use Swagger 2.x `definitions` — script handles both, check spec is valid JSON/YAML |
| `$ref` not resolved | Deeply nested `$ref` chains may need manual review — script resolves one level |
| Missing auth scenarios | Check if `security` is defined at operation or root level in the spec |