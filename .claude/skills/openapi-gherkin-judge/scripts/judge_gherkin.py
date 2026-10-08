#!/usr/bin/env python3
"""
judge_gherkin.py
================
Uses the Anthropic API (LLM-as-a-Judge) to evaluate a generated Gherkin
.feature file against its source OpenAPI spec.

Usage:
    python judge_gherkin.py <spec_file> <feature_file> [output_report]

    spec_file     : OpenAPI JSON or YAML file
    feature_file  : Generated .feature file to evaluate
    output_report : Path for JSON report output (default: /tmp/judge_report.json)

Outputs:
    - A structured JSON report with per-criterion scores and reasoning
    - A human-readable markdown summary printed to stdout
"""

import sys
import json
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


# ── Rubric definition ─────────────────────────────────────────────────────────

RUBRIC = [
    {
        "id": "endpoint_coverage",
        "name": "Endpoint Coverage",
        "description": "Every endpoint and HTTP method in the spec has at least one [HAPPY] scenario."
    },
    {
        "id": "error_coverage",
        "name": "Error Code Coverage",
        "description": "Every documented response status code (4xx, 5xx) has a corresponding scenario."
    },
    {
        "id": "auth_coverage",
        "name": "Auth Coverage",
        "description": "All secured endpoints have 401 (unauthenticated) and 403 (forbidden) scenarios."
    },
    {
        "id": "validation_depth",
        "name": "Validation Depth",
        "description": "Each required request body field is tested individually with a missing-field scenario."
    },
    {
        "id": "step_clarity",
        "name": "Step Clarity",
        "description": "Given/When/Then steps are unambiguous, consistent, and implementable by a developer without guesswork."
    },
    {
        "id": "bdd_correctness",
        "name": "BDD Correctness",
        "description": "Each scenario tests exactly one behaviour. Given=precondition, When=action, Then=assertion — not mixed."
    },
    {
        "id": "spec_fidelity",
        "name": "Spec Fidelity",
        "description": "No hallucinated paths, methods, parameters, or status codes. All details traceable to the spec."
    },
    {
        "id": "completeness",
        "name": "Completeness",
        "description": "No obvious test cases are missing that a thorough QA engineer would include (e.g. edge cases, boundary values, rate limits)."
    },
]


# ── Helpers ───────────────────────────────────────────────────────────────────

def load_file(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def load_spec_summary(path: str) -> str:
    """Return a compact spec summary to keep the judge prompt concise."""
    text = load_file(path)
    try:
        if path.endswith((".yaml", ".yml")):
            if not HAS_YAML:
                return text[:6000]
            spec = yaml.safe_load(text)
        else:
            spec = json.loads(text)
    except Exception:
        return text[:6000]

    info = spec.get("info", {})
    paths = spec.get("paths", {})
    summary_lines = [
        f"API: {info.get('title', 'Unknown')} v{info.get('version', '?')}",
        f"Endpoints: {len(paths)}",
        "",
        "Endpoint summary:"
    ]
    for path, item in paths.items():
        for method in ("get", "post", "put", "patch", "delete"):
            op = item.get(method)
            if not op:
                continue
            codes = list(op.get("responses", {}).keys())
            security = "🔒" if op.get("security") or spec.get("security") else "🔓"
            req_fields = []
            rb = op.get("requestBody", {})
            if rb:
                for mime, content in rb.get("content", {}).items():
                    schema = content.get("schema", {})
                    if "$ref" in schema:
                        ref = schema["$ref"].lstrip("#/").split("/")
                        node = spec
                        for p in ref:
                            node = node.get(p, {})
                        schema = node
                    req_fields = schema.get("required", [])
                    break
            summary_lines.append(
                f"  {security} {method.upper()} {path} → [{', '.join(codes)}]"
                + (f" required: {req_fields}" if req_fields else "")
            )

    return "\n".join(summary_lines)


def call_claude(prompt: str) -> str:
    """Call the Anthropic API and return the text response."""
    payload = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 4096,
        "system": (
            "You are a senior QA engineer and BDD expert evaluating Gherkin test scenarios. "
            "You are precise, thorough, and critical. You always respond with valid JSON only — "
            "no preamble, no markdown fences, no commentary outside the JSON structure."
        ),
        "messages": [{"role": "user", "content": prompt}]
    }

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01",
        },
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    return data["content"][0]["text"]


def build_judge_prompt(spec_summary: str, feature_content: str) -> str:
    rubric_text = "\n".join(
        f'{i+1}. **{r["id"]}** — {r["name"]}: {r["description"]}'
        for i, r in enumerate(RUBRIC)
    )

    return f"""You are evaluating a Gherkin .feature file generated from an OpenAPI spec.

## OpenAPI Spec Summary
{spec_summary}

## Generated Gherkin Feature File
```gherkin
{feature_content[:8000]}
```

## Your Task
Evaluate the Gherkin file against each criterion in the rubric below.
For each criterion:
1. Reason carefully about what is present and what is missing
2. Assign a score from 1 to 5:
   - 5 = Excellent, no issues
   - 4 = Good, minor gaps
   - 3 = Adequate, some notable gaps
   - 2 = Poor, significant gaps
   - 1 = Very poor or missing entirely

## Rubric
{rubric_text}

## Required JSON Response Format
{{
  "api_name": "<name from spec>",
  "evaluated_at": "<ISO timestamp>",
  "scores": {{
    "endpoint_coverage":  {{ "score": <1-5>, "reasoning": "<specific findings>", "issues": ["<issue1>", ...] }},
    "error_coverage":     {{ "score": <1-5>, "reasoning": "<specific findings>", "issues": ["<issue1>", ...] }},
    "auth_coverage":      {{ "score": <1-5>, "reasoning": "<specific findings>", "issues": ["<issue1>", ...] }},
    "validation_depth":   {{ "score": <1-5>, "reasoning": "<specific findings>", "issues": ["<issue1>", ...] }},
    "step_clarity":       {{ "score": <1-5>, "reasoning": "<specific findings>", "issues": ["<issue1>", ...] }},
    "bdd_correctness":    {{ "score": <1-5>, "reasoning": "<specific findings>", "issues": ["<issue1>", ...] }},
    "spec_fidelity":      {{ "score": <1-5>, "reasoning": "<specific findings>", "issues": ["<issue1>", ...] }},
    "completeness":       {{ "score": <1-5>, "reasoning": "<specific findings>", "issues": ["<issue1>", ...] }}
  }},
  "overall_score": <average to 1 decimal place>,
  "verdict": "<PASS if overall >= 3.5, FAIL otherwise>",
  "critical_issues": ["<blocking issue 1>", ...],
  "suggestions": ["<actionable improvement 1>", ...],
  "missing_scenarios": ["<description of missing test case 1>", ...]
}}"""


def render_markdown_report(report: dict) -> str:
    scores = report.get("scores", {})
    overall = report.get("overall_score", 0)
    verdict = report.get("verdict", "UNKNOWN")
    verdict_icon = "✅" if verdict == "PASS" else "❌"

    lines = [
        f"# Gherkin Quality Report — {report.get('api_name', 'API')}",
        f"Evaluated: {report.get('evaluated_at', '')}",
        "",
        f"## Overall: {overall}/5.0 {verdict_icon} {verdict}",
        "",
        "## Scores by Criterion",
        "",
        "| Criterion | Score | Rating |",
        "|---|---|---|",
    ]

    rating = lambda s: "🟢 Excellent" if s == 5 else "🟡 Good" if s == 4 else "🟠 Adequate" if s == 3 else "🔴 Poor" if s == 2 else "⛔ Very Poor"

    for r in RUBRIC:
        crit = scores.get(r["id"], {})
        score = crit.get("score", 0)
        lines.append(f"| {r['name']} | {score}/5 | {rating(score)} |")

    lines += ["", "## Detailed Findings", ""]
    for r in RUBRIC:
        crit = scores.get(r["id"], {})
        lines.append(f"### {r['name']} — {crit.get('score', '?')}/5")
        lines.append(crit.get("reasoning", ""))
        issues = crit.get("issues", [])
        if issues:
            lines.append("")
            for issue in issues:
                lines.append(f"- ⚠️ {issue}")
        lines.append("")

    if report.get("critical_issues"):
        lines += ["## 🚨 Critical Issues", ""]
        for issue in report["critical_issues"]:
            lines.append(f"- {issue}")
        lines.append("")

    if report.get("missing_scenarios"):
        lines += ["## 🕳️ Missing Scenarios", ""]
        for s in report["missing_scenarios"]:
            lines.append(f"- {s}")
        lines.append("")

    if report.get("suggestions"):
        lines += ["## 💡 Suggestions", ""]
        for s in report["suggestions"]:
            lines.append(f"- {s}")
        lines.append("")

    return "\n".join(lines)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 3:
        print("Usage: python judge_gherkin.py <spec_file> <feature_file> [output_report]")
        sys.exit(1)

    spec_path    = sys.argv[1]
    feature_path = sys.argv[2]
    output_path  = sys.argv[3] if len(sys.argv) > 3 else "/tmp/judge_report.json"

    print(f"Loading spec:    {spec_path}", file=sys.stderr)
    print(f"Loading feature: {feature_path}", file=sys.stderr)

    spec_summary    = load_spec_summary(spec_path)
    feature_content = load_file(feature_path)

    print("Calling judge LLM...", file=sys.stderr)
    prompt   = build_judge_prompt(spec_summary, feature_content)
    raw      = call_claude(prompt)

    # Strip accidental markdown fences if present
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = "\n".join(cleaned.split("\n")[1:])
    if cleaned.endswith("```"):
        cleaned = "\n".join(cleaned.split("\n")[:-1])

    report = json.loads(cleaned)
    report["evaluated_at"] = datetime.utcnow().isoformat() + "Z"

    # Save JSON report
    Path(output_path).write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"JSON report saved to: {output_path}", file=sys.stderr)

    # Print markdown summary to stdout
    print(render_markdown_report(report))


if __name__ == "__main__":
    main()