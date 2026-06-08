---
name: gherkin-judge
description: Use LLM-as-a-Judge to evaluate the quality of a Gherkin .feature file against its source OpenAPI spec. Scores the output across 8 criteria (endpoint coverage, error coverage, auth coverage, validation depth, step clarity, BDD correctness, spec fidelity, completeness) and produces a structured JSON report plus a markdown summary. Use this skill whenever the user wants to validate, score, review, or quality-check a Gherkin file, says things like "judge this feature file", "evaluate my Gherkin", "how good is this test coverage", "check my BDD scenarios against the spec", or has just run the openapi-gherkin skill and wants to verify the output. Always trigger after openapi-gherkin if the user asks for validation or a quality check.
---

# Gherkin Judge Skill

Evaluates a Gherkin `.feature` file against its source OpenAPI spec using LLM-as-a-Judge. Returns per-criterion scores, reasoning, critical issues, missing scenarios, and improvement suggestions.

## Inputs

| Field           | Required | Description                                                                |
| --------------- | -------- | -------------------------------------------------------------------------- |
| `spec_file`     | ✅       | Path to the OpenAPI JSON or YAML spec                                      |
| `feature_file`  | ✅       | Path to the `.feature` file to evaluate                                    |
| `output_report` | ❌       | Path for JSON report (default: `/mnt/user-data/outputs/judge_report.json`) |

## Scoring rubric (8 criteria, each 1–5)

| Criterion           | What is evaluated                              |
| ------------------- | ---------------------------------------------- |
| `endpoint_coverage` | Every endpoint+method has a [HAPPY] scenario   |
| `error_coverage`    | Every documented 4xx/5xx has a scenario        |
| `auth_coverage`     | Secured endpoints have 401 + 403 scenarios     |
| `validation_depth`  | Each required field individually tested        |
| `step_clarity`      | Steps are unambiguous and implementable        |
| `bdd_correctness`   | One behaviour per scenario, correct step types |
| `spec_fidelity`     | No hallucinated paths, methods, or codes       |
| `completeness`      | No obvious missing cases                       |

**Verdict:** PASS if overall average ≥ 3.5 / 5.0

> For full rubric detail, see `assets/rubric.md`

## Instructions

### Step 1 — Collect inputs

Accept:

- Files uploaded by the user → `/mnt/user-data/uploads/<filename>`
- Paths from a previous `openapi-gherkin` skill run
- Ask if either file is missing

### Step 2 — Install dependencies if needed

```bash
pip install pyyaml --break-system-packages 2>/dev/null || true
```

### Step 3 — Run the judge

```bash
python <skill_dir>/scripts/judge_gherkin.py \
  "<spec_file>" \
  "<feature_file>" \
  "/mnt/user-data/outputs/judge_report.json" 2>&1
```

The script calls the Anthropic API internally — no API key argument needed.

### Step 4 — Present results in chat

After the script runs, show the user:

1. **Verdict banner** — PASS ✅ or FAIL ❌ with overall score
2. **Score table** — all 8 criteria with scores and ratings
3. **Critical issues** — blocking problems (if any)
4. **Missing scenarios** — specific gaps identified
5. **Top suggestions** — up to 3 actionable improvements

Format example:

```
✅ PASS — Overall: 4.2 / 5.0

Endpoint Coverage    ████████░░  4/5
Error Coverage       ██████████  5/5
Auth Coverage        ████████░░  4/5
Validation Depth     ██████░░░░  3/5
Step Clarity         ████████░░  4/5
BDD Correctness      ██████████  5/5
Spec Fidelity        ██████████  5/5
Completeness         ██████░░░░  3/5

💡 Top suggestion: Add individual missing-field scenarios for
   "customerId" and "quantity" in POST /orders
```

### Step 5 — Present files

Use `present_files` to give the user:

- `judge_report.json` — full structured report for CI/CD integration
- The markdown summary (printed to stdout by the script)

### Step 6 — Offer next steps

After presenting results, offer:

- "Want me to regenerate the Gherkin with these issues fixed?" → triggers `openapi-gherkin` skill with judge feedback appended
- "Want me to export the report as a markdown file?"
- "Should I add the missing scenarios manually?"

## Chaining with openapi-gherkin

This skill is designed to chain after `openapi-gherkin`:

```
openapi-gherkin  →  gherkin-judge  →  (optional) regenerate with fixes
     spec               spec
       ↓              + feature
   feature               ↓
                      report + scores
```

If the verdict is FAIL, offer to re-run `openapi-gherkin` with the judge's
critical issues and missing scenarios appended as additional instructions.

## Troubleshooting

| Problem                     | Fix                                                                           |
| --------------------------- | ----------------------------------------------------------------------------- |
| API call fails              | Check network access to api.anthropic.com                                     |
| JSON parse error from judge | Script strips markdown fences — if still failing, check raw output            |
| Score seems wrong           | Judge is non-deterministic — re-run for a second opinion on borderline scores |
| Feature file too large      | Script truncates to 8000 chars — consider splitting large specs               |
