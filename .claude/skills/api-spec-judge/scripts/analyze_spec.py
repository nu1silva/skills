#!/usr/bin/env python3
"""
OpenAPI Quality Checker
Analyzes a JSON OpenAPI spec for validity, completeness, design best practices, and security.
Usage: python3 analyze_spec.py <path_to_spec.json>
"""

import sys
import json
import re
from pathlib import Path

# ── install deps if needed ──────────────────────────────────────────────────
import subprocess
subprocess.check_call(
    [sys.executable, "-m", "pip", "install", "openapi-spec-validator", "--break-system-packages", "-q"],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
)

from openapi_spec_validator import validate
from openapi_spec_validator.validation.exceptions import OpenAPIValidationError

# ── helpers ─────────────────────────────────────────────────────────────────

def load_spec(path: str) -> dict:
    with open(path) as f:
        return json.load(f)

def all_operations(paths: dict):
    """Yield (path, method, operation_obj) for every operation in the spec."""
    HTTP_METHODS = {"get", "post", "put", "patch", "delete", "head", "options", "trace"}
    for path, path_item in paths.items():
        for method, op in path_item.items():
            if method in HTTP_METHODS and isinstance(op, dict):
                yield path, method.upper(), op

# ── check categories ─────────────────────────────────────────────────────────

def check_schema_validity(spec: dict) -> list[dict]:
    issues = []
    try:
        validate(spec)
    except OpenAPIValidationError as e:
        issues.append({
            "severity": "CRITICAL",
            "category": "Schema Validity",
            "message": f"Spec fails OpenAPI validation: {str(e).splitlines()[0]}",
            "location": "root"
        })
    except Exception as e:
        issues.append({
            "severity": "CRITICAL",
            "category": "Schema Validity",
            "message": f"Could not parse spec: {e}",
            "location": "root"
        })
    return issues


def check_completeness(spec: dict) -> list[dict]:
    issues = []
    paths = spec.get("paths", {})
    info = spec.get("info", {})

    # Info block
    if not info.get("description"):
        issues.append({"severity": "MEDIUM", "category": "Completeness",
                        "message": "API is missing a top-level 'info.description'.", "location": "info"})
    if not info.get("contact"):
        issues.append({"severity": "LOW", "category": "Completeness",
                        "message": "No contact information provided in 'info.contact'.", "location": "info"})

    for path, method, op in all_operations(paths):
        loc = f"{method} {path}"

        # Summary / description
        if not op.get("summary"):
            issues.append({"severity": "MEDIUM", "category": "Completeness",
                            "message": "Operation is missing a 'summary'.", "location": loc})
        if not op.get("description"):
            issues.append({"severity": "LOW", "category": "Completeness",
                            "message": "Operation is missing a 'description'.", "location": loc})

        # operationId
        if not op.get("operationId"):
            issues.append({"severity": "MEDIUM", "category": "Completeness",
                            "message": "Operation is missing an 'operationId'. Needed for SDK generation and linking.", "location": loc})

        # Error responses
        responses = op.get("responses", {})
        has_error = any(str(code).startswith(("4", "5")) for code in responses)
        if not has_error and method not in ("GET", "HEAD"):
            issues.append({"severity": "MEDIUM", "category": "Completeness",
                            "message": "No 4xx/5xx error responses documented.", "location": loc})
        if "200" not in responses and "201" not in responses and "204" not in responses:
            issues.append({"severity": "HIGH", "category": "Completeness",
                            "message": "No success response (200/201/204) documented.", "location": loc})

        # Response descriptions
        for code, resp in responses.items():
            if isinstance(resp, dict) and not resp.get("description"):
                issues.append({"severity": "LOW", "category": "Completeness",
                                "message": f"Response {code} is missing a 'description'.", "location": loc})

        # Request body schema / examples
        req_body = op.get("requestBody", {})
        if req_body:
            content = req_body.get("content", {})
            for media_type, media_obj in content.items():
                if isinstance(media_obj, dict):
                    if not media_obj.get("schema"):
                        issues.append({"severity": "HIGH", "category": "Completeness",
                                        "message": f"Request body '{media_type}' has no schema defined.", "location": loc})
                    if not media_obj.get("examples") and not media_obj.get("example"):
                        issues.append({"severity": "LOW", "category": "Completeness",
                                        "message": f"Request body '{media_type}' has no examples.", "location": loc})

        # Parameter descriptions
        for param in op.get("parameters", []):
            if isinstance(param, dict) and not param.get("description"):
                pname = param.get("name", "?")
                issues.append({"severity": "LOW", "category": "Completeness",
                                "message": f"Parameter '{pname}' is missing a description.", "location": loc})

    return issues


def check_design(spec: dict) -> list[dict]:
    issues = []
    paths = spec.get("paths", {})

    # Version check
    version = spec.get("info", {}).get("version", "")
    if not re.match(r"^\d+\.\d+(\.\d+)?$", version):
        issues.append({"severity": "MEDIUM", "category": "Design",
                        "message": f"'info.version' ('{version}') should follow semantic versioning (e.g. 1.0.0).",
                        "location": "info.version"})

    # API versioning in path
    has_version_prefix = any(re.search(r"/v\d+/", path) or path.startswith("/v") for path in paths)
    if not has_version_prefix and paths:
        issues.append({"severity": "LOW", "category": "Design",
                        "message": "No API version prefix found in paths (e.g. /v1/...). Consider versioning your routes.",
                        "location": "paths"})

    for path, method, op in all_operations(paths):
        loc = f"{method} {path}"

        # Noun-based paths (no verbs) — match both /getUsers and /get-users
        verb_pattern = re.compile(r"/(?:get|create|update|delete|fetch|list|add|remove|set|make|do)(?:[A-Z_/-]|$)", re.IGNORECASE)
        if verb_pattern.search(path):
            issues.append({"severity": "MEDIUM", "category": "Design",
                            "message": f"Path '{path}' contains a verb. REST paths should be noun-based (e.g. /users not /getUsers).",
                            "location": loc})

        # Plural resource names for collections
        segments = [s for s in path.split("/") if s and not s.startswith("{")]
        for seg in segments:
            if re.match(r"^[a-z]+$", seg) and not seg.endswith("s") and len(seg) > 2:
                issues.append({"severity": "LOW", "category": "Design",
                                "message": f"Path segment '/{seg}' may not be plural. Collection endpoints typically use plural nouns.",
                                "location": loc})
                break  # one per operation is enough

        # Correct HTTP method usage
        if method == "GET":
            if op.get("requestBody"):
                issues.append({"severity": "HIGH", "category": "Design",
                                "message": "GET operation has a requestBody. GET requests must not have a body.",
                                "location": loc})
        if method == "POST" and re.search(r"/\{[^}]+\}$", path):
            issues.append({"severity": "LOW", "category": "Design",
                            "message": "POST to a path ending in an ID parameter is unusual. Consider PUT/PATCH for updates.",
                            "location": loc})

        # kebab-case path segments (prefer over camelCase/PascalCase)
        raw_segs = [s for s in path.split("/") if s and not s.startswith("{")]
        for seg in raw_segs:
            if re.search(r"[A-Z]", seg) or "_" in seg:
                issues.append({"severity": "LOW", "category": "Design",
                                "message": f"Path segment '{seg}' uses uppercase or underscores. Prefer kebab-case (e.g. user-profiles).",
                                "location": loc})
                break

        # Tags
        if not op.get("tags"):
            issues.append({"severity": "LOW", "category": "Design",
                            "message": "Operation has no 'tags'. Tags help group operations in documentation.",
                            "location": loc})

    return issues


def check_security(spec: dict) -> list[dict]:
    issues = []
    paths = spec.get("paths", {})
    global_security = spec.get("security")
    security_schemes = spec.get("components", {}).get("securitySchemes", {})

    # No security schemes defined at all
    if not security_schemes:
        issues.append({"severity": "HIGH", "category": "Security",
                        "message": "No securitySchemes defined in 'components'. All endpoints may be publicly accessible.",
                        "location": "components.securitySchemes"})

    # Insecure scheme types
    for scheme_name, scheme in security_schemes.items():
        if isinstance(scheme, dict):
            if scheme.get("type") == "http" and scheme.get("scheme") == "basic":
                issues.append({"severity": "HIGH", "category": "Security",
                                "message": f"Security scheme '{scheme_name}' uses HTTP Basic auth. Prefer Bearer tokens or OAuth2.",
                                "location": f"components.securitySchemes.{scheme_name}"})
            if scheme.get("type") == "apiKey" and scheme.get("in") == "query":
                issues.append({"severity": "MEDIUM", "category": "Security",
                                "message": f"Security scheme '{scheme_name}' passes API key in query string. Prefer header-based keys to avoid leaking in logs/URLs.",
                                "location": f"components.securitySchemes.{scheme_name}"})

    for path, method, op in all_operations(paths):
        loc = f"{method} {path}"
        op_security = op.get("security")

        # Skip auth check for read-only public-looking endpoints is a judgment call;
        # flag operations with no security at all when there ARE schemes defined
        if security_schemes:
            effective_security = op_security if op_security is not None else global_security
            if effective_security is None:
                issues.append({"severity": "HIGH", "category": "Security",
                                "message": "Operation has no security requirement applied (neither global nor operation-level).",
                                "location": loc})
            elif effective_security == []:
                if method not in ("GET", "HEAD"):
                    issues.append({"severity": "MEDIUM", "category": "Security",
                                    "message": "Operation explicitly opts out of security (security: []). Confirm this endpoint is intentionally public.",
                                    "location": loc})

        # Sensitive field names in responses (check both direct properties and nested items)
        SENSITIVE = {"password", "secret", "token", "api_key", "apikey", "ssn", "credit_card", "cvv"}
        responses = op.get("responses", {})
        for code, resp in responses.items():
            if not isinstance(resp, dict):
                continue
            content = resp.get("content", {})
            for media_type, media_obj in content.items():
                schema = media_obj.get("schema", {}) if isinstance(media_obj, dict) else {}
                # Check both top-level properties and array item properties
                schemas_to_check = [schema, schema.get("items", {})]
                for s in schemas_to_check:
                    props = s.get("properties", {}) if isinstance(s, dict) else {}
                    for field in props:
                        if field.lower() in SENSITIVE:
                            issues.append({"severity": "HIGH", "category": "Security",
                                            "message": f"Response {code} exposes field '{field}' which may contain sensitive data. Consider removing or masking it.",
                                            "location": loc})

    return issues


# ── report formatting ────────────────────────────────────────────────────────

SEVERITY_ORDER = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
SEVERITY_EMOJI = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🔵"}

def format_report(spec: dict, all_issues: list[dict], spec_path: str) -> str:
    info = spec.get("info", {})
    title = info.get("title", "Unknown API")
    version = info.get("version", "?")
    path_count = len(spec.get("paths", {}))
    op_count = sum(1 for _ in all_operations(spec.get("paths", {})))

    sorted_issues = sorted(all_issues, key=lambda i: SEVERITY_ORDER.get(i["severity"], 99))

    counts = {s: 0 for s in SEVERITY_ORDER}
    for i in sorted_issues:
        counts[i["severity"]] = counts.get(i["severity"], 0) + 1

    total = len(sorted_issues)

    # Quality score: start at 100, deduct by severity
    deductions = counts["CRITICAL"]*20 + counts["HIGH"]*10 + counts["MEDIUM"]*5 + counts["LOW"]*1
    score = max(0, 100 - deductions)
    grade = "A" if score >= 90 else "B" if score >= 75 else "C" if score >= 60 else "D" if score >= 40 else "F"

    lines = [
        f"# OpenAPI Quality Report",
        f"",
        f"**File:** `{spec_path}`",
        f"**API:** {title} v{version}",
        f"**Paths:** {path_count}  |  **Operations:** {op_count}",
        f"",
        f"## Quality Score: {score}/100 (Grade: {grade})",
        f"",
        f"| Severity | Count |",
        f"|----------|-------|",
    ]
    for sev, emoji in SEVERITY_EMOJI.items():
        lines.append(f"| {emoji} {sev} | {counts[sev]} |")
    lines.append(f"| **Total Issues** | **{total}** |")
    lines.append("")

    if not sorted_issues:
        lines.append("✅ No issues found. Spec looks great!")
        return "\n".join(lines)

    # Group by category
    from collections import defaultdict
    by_category = defaultdict(list)
    for issue in sorted_issues:
        by_category[issue["category"]].append(issue)

    CATEGORY_ORDER = ["Schema Validity", "Security", "Completeness", "Design"]
    for cat in CATEGORY_ORDER:
        if cat not in by_category:
            continue
        lines.append(f"## {cat}")
        lines.append("")
        for issue in by_category[cat]:
            emoji = SEVERITY_EMOJI.get(issue["severity"], "⚪")
            lines.append(f"- {emoji} **[{issue['severity']}]** `{issue['location']}`")
            lines.append(f"  {issue['message']}")
        lines.append("")

    return "\n".join(lines)


# ── main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 analyze_spec.py <path_to_spec.json>")
        sys.exit(1)

    spec_path = sys.argv[1]
    try:
        spec = load_spec(spec_path)
    except Exception as e:
        print(f"❌ Failed to load spec: {e}")
        sys.exit(1)

    all_issues = []
    all_issues += check_schema_validity(spec)
    all_issues += check_completeness(spec)
    all_issues += check_design(spec)
    all_issues += check_security(spec)

    report = format_report(spec, all_issues, spec_path)
    print(report)