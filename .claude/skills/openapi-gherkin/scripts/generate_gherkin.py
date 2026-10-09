#!/usr/bin/env python3
"""
generate_gherkin.py
===================
Parses an OpenAPI 3.x or Swagger 2.x spec file (JSON or YAML) and generates
a comprehensive Gherkin (.feature) file covering:
  - Happy path for every endpoint + method
  - Every documented response code (2xx, 3xx, 4xx, 5xx)
  - Required field validation (missing required fields → 400/422)
  - Auth/permission error paths (401, 403)
  - Not found paths (404)
  - Server error paths (500)

Usage:
    python generate_gherkin.py <spec_file> [output_file]

    spec_file   : path to OpenAPI JSON or YAML file
    output_file : path for .feature output (default: ./output.feature)
"""

import sys
import json
import re
from pathlib import Path

# ── optional YAML support ─────────────────────────────────────────────────────
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


# ── helpers ───────────────────────────────────────────────────────────────────

def load_spec(path: str) -> dict:
    text = Path(path).read_text(encoding="utf-8")
    if path.endswith((".yaml", ".yml")):
        if not HAS_YAML:
            raise RuntimeError("PyYAML not installed. Run: pip install pyyaml --break-system-packages")
        return yaml.safe_load(text)
    return json.loads(text)


def resolve_ref(spec: dict, ref: str) -> dict:
    """Resolve a $ref string like '#/components/schemas/Pet'."""
    if not ref.startswith("#/"):
        return {}
    parts = ref.lstrip("#/").split("/")
    node = spec
    for p in parts:
        node = node.get(p, {})
    return node


def schema_example(spec: dict, schema: dict, depth: int = 0) -> str:
    """Return a short human-readable example value for a schema."""
    if depth > 3:
        return "<value>"
    if "$ref" in schema:
        schema = resolve_ref(spec, schema["$ref"])
    t = schema.get("type", "string")
    fmt = schema.get("format", "")
    if "example" in schema:
        return json.dumps(schema["example"])
    if "enum" in schema:
        return json.dumps(schema["enum"][0])
    if t == "integer" or t == "number":
        return "1" if not fmt else ("1.0" if fmt in ("float", "double") else "1")
    if t == "boolean":
        return "true"
    if t == "array":
        items = schema.get("items", {})
        return f"[{schema_example(spec, items, depth+1)}]"
    if t == "object":
        props = schema.get("properties", {})
        pairs = [f'"{k}": {schema_example(spec, v, depth+1)}' for k, v in list(props.items())[:3]]
        return "{" + ", ".join(pairs) + "}"
    if fmt == "date":
        return '"2024-01-15"'
    if fmt in ("date-time", "datetime"):
        return '"2024-01-15T10:00:00Z"'
    if fmt == "email":
        return '"user@example.com"'
    if fmt == "uuid":
        return '"550e8400-e29b-41d4-a716-446655440000"'
    return f'"{schema.get("title", t)}_value"'


def get_request_body_fields(spec: dict, operation: dict):
    """Return (required_fields, optional_fields, example_body) from requestBody."""
    rb = operation.get("requestBody", {})
    if not rb:
        return [], [], "{}"
    content = rb.get("content", {})
    schema = {}
    for mime in ("application/json", "application/x-www-form-urlencoded", "*/*"):
        if mime in content:
            s = content[mime].get("schema", {})
            if "$ref" in s:
                s = resolve_ref(spec, s["$ref"])
            schema = s
            break
    if not schema:
        return [], [], "{}"

    props = schema.get("properties", {})
    required = schema.get("required", [])
    req_fields = [k for k in props if k in required]
    opt_fields = [k for k in props if k not in required]

    example = {}
    for k, v in props.items():
        example[k] = json.loads(schema_example(spec, v))
    return req_fields, opt_fields, json.dumps(example, indent=2)


def get_path_params(parameters: list) -> list:
    return [p for p in parameters if p.get("in") == "path"]


def get_query_params(parameters: list) -> list:
    return [p for p in parameters if p.get("in") == "query"]


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


def title_case(text: str) -> str:
    return re.sub(r"[_\-]+", " ", text).title()


def method_verb(method: str) -> str:
    return {
        "get": "retrieve", "post": "create", "put": "update",
        "patch": "modify", "delete": "delete", "head": "check", "options": "inspect"
    }.get(method, method)


def status_description(code: str) -> str:
    return {
        "200": "successful response", "201": "resource created",
        "202": "accepted for processing", "204": "no content returned",
        "301": "permanently redirected", "302": "temporarily redirected",
        "304": "not modified",
        "400": "bad request due to invalid input",
        "401": "authentication required",
        "403": "forbidden — insufficient permissions",
        "404": "resource not found",
        "405": "method not allowed",
        "409": "conflict with existing resource",
        "410": "resource gone",
        "422": "validation error — unprocessable entity",
        "429": "rate limit exceeded",
        "500": "internal server error",
        "502": "bad gateway",
        "503": "service unavailable",
        "504": "gateway timeout",
    }.get(code, f"HTTP {code} response")


def build_path_example(path: str, path_params: list, spec: dict) -> str:
    """Replace {param} placeholders with example values."""
    result = path
    for p in path_params:
        s = p.get("schema", {})
        ex = schema_example(spec, s).strip('"')
        result = result.replace("{" + p["name"] + "}", ex)
    if not path_params:
        result = re.sub(r"\{[^}]+\}", "123", result)
    return result


# ── Gherkin builder ────────────────────────────────────────────────────────────

def generate_feature(spec: dict, spec_path: str) -> str:
    info = spec.get("info", {})
    title = info.get("title", "API")
    version = info.get("version", "")
    description = info.get("description", "")
    servers = spec.get("servers", [])
    base_url = servers[0].get("url", "") if servers else spec.get("basePath", "")

    lines = []
    lines.append(f"# Generated from: {Path(spec_path).name}")
    lines.append(f"# API: {title} {version}")
    lines.append("")
    lines.append(f"Feature: {title}")
    if description:
        for ln in description.strip().splitlines()[:3]:
            lines.append(f"  {ln.strip()}")
    if base_url:
        lines.append(f"  Base URL: {base_url}")
    lines.append("")

    # Collect security schemes for auth scenarios
    security_schemes = {}
    components = spec.get("components", spec.get("securityDefinitions", {}))
    if isinstance(components, dict):
        security_schemes = components.get("securitySchemes", components.get("securityDefinitions", {}))

    paths = spec.get("paths", {})
    scenario_count = 0

    for path, path_item in paths.items():
        if not isinstance(path_item, dict):
            continue

        # Path-level parameters
        path_level_params = path_item.get("parameters", [])

        for method in ("get", "post", "put", "patch", "delete", "head", "options"):
            operation = path_item.get(method)
            if not operation or not isinstance(operation, dict):
                continue

            op_id = operation.get("operationId", f"{method}_{slugify(path)}")
            summary = operation.get("summary", f"{title_case(method_verb(method))} {path}")
            tags = operation.get("tags", ["General"])
            tag = tags[0] if tags else "General"

            # Merge path-level + operation-level parameters
            op_params = operation.get("parameters", [])
            all_params = {p.get("name"): p for p in path_level_params}
            all_params.update({p.get("name"): p for p in op_params})
            parameters = list(all_params.values())

            path_params = get_path_params(parameters)
            query_params = get_query_params(parameters)
            req_fields, opt_fields, example_body = get_request_body_fields(spec, operation)
            path_example = build_path_example(path, path_params, spec)

            responses = operation.get("responses", {})
            security = operation.get("security", spec.get("security", []))
            requires_auth = bool(security)

            lines.append(f"  # ── {method.upper()} {path} ─────────────────────────")
            lines.append(f"  # {summary}")
            lines.append(f"  # Tag: {tag} | OperationId: {op_id}")
            lines.append("")

            # ── Happy path scenario ────────────────────────────────────────────
            scenario_count += 1
            success_code = next(
                (c for c in ("200", "201", "202", "204") if c in responses), "200"
            )
            lines.append(f"  Scenario: [HAPPY] {summary}")
            if requires_auth:
                lines.append(f"    Given I am authenticated with valid credentials")
            else:
                lines.append(f"    Given the API is available")
            if path_params:
                for p in path_params:
                    ex = schema_example(spec, p.get("schema", {})).strip('"')
                    lines.append(f"    And the path parameter \"{p['name']}\" is \"{ex}\"")
            if query_params:
                req_q = [p for p in query_params if p.get("required")]
                for p in req_q[:3]:
                    ex = schema_example(spec, p.get("schema", {})).strip('"')
                    lines.append(f"    And the query parameter \"{p['name']}\" is \"{ex}\"")
            if req_fields:
                lines.append(f"    And I provide a valid request body:")
                lines.append(f"      \"\"\"")
                lines.append(f"      {example_body}")
                lines.append(f"      \"\"\"")
            lines.append(f"    When I send a {method.upper()} request to \"{path_example}\"")
            lines.append(f"    Then the response status code should be {success_code}")
            lines.append(f"    And the response should indicate {status_description(success_code)}")
            if success_code not in ("204",):
                lines.append(f"    And the response body should be valid JSON")
            lines.append("")

            # ── One scenario per documented response code ──────────────────────
            for code, resp_obj in sorted(responses.items()):
                if code in ("200", "201", "202", "204", "default"):
                    continue  # already covered by happy path or handled below
                if not isinstance(resp_obj, dict):
                    continue

                scenario_count += 1
                resp_desc = resp_obj.get("description", status_description(code))
                code_int = int(code) if code.isdigit() else 0

                if code_int in range(300, 400):
                    scenario_type = "REDIRECT"
                    given = "Given I am authenticated with valid credentials" if requires_auth else "Given the API is available"
                    when_extra = ""
                    then_extra = f"    And the response should contain a Location header"
                elif code == "400":
                    scenario_type = "ERROR"
                    given = "Given I am authenticated with valid credentials" if requires_auth else "Given the API is available"
                    when_extra = "    And I provide an invalid or malformed request body"
                    then_extra = f"    And the response body should contain error details"
                elif code == "401":
                    scenario_type = "AUTH"
                    given = "Given I am not authenticated"
                    when_extra = ""
                    then_extra = f"    And the response should include a WWW-Authenticate header"
                elif code == "403":
                    scenario_type = "AUTH"
                    given = "Given I am authenticated as a user without sufficient permissions"
                    when_extra = ""
                    then_extra = f"    And the response body should indicate access is denied"
                elif code == "404":
                    scenario_type = "ERROR"
                    given = "Given I am authenticated with valid credentials" if requires_auth else "Given the API is available"
                    when_extra = "    And the requested resource does not exist"
                    then_extra = f"    And the response body should indicate the resource was not found"
                elif code == "409":
                    scenario_type = "ERROR"
                    given = "Given I am authenticated with valid credentials" if requires_auth else "Given the API is available"
                    when_extra = "    And the resource already exists or conflicts with current state"
                    then_extra = f"    And the response body should describe the conflict"
                elif code == "422":
                    scenario_type = "VALIDATION"
                    given = "Given I am authenticated with valid credentials" if requires_auth else "Given the API is available"
                    when_extra = "    And I provide a request body that fails validation rules"
                    then_extra = f"    And the response body should list validation errors per field"
                elif code == "429":
                    scenario_type = "RATE LIMIT"
                    given = "Given I have exceeded the allowed request rate"
                    when_extra = ""
                    then_extra = f"    And the response should include a Retry-After header"
                elif code_int >= 500:
                    scenario_type = "SERVER ERROR"
                    given = "Given I am authenticated with valid credentials" if requires_auth else "Given the API is available"
                    when_extra = "    And the server encounters an internal error"
                    then_extra = f"    And the response body should not expose internal stack traces"
                else:
                    scenario_type = "RESPONSE"
                    given = "Given I am authenticated with valid credentials" if requires_auth else "Given the API is available"
                    when_extra = ""
                    then_extra = ""

                lines.append(f"  Scenario: [{scenario_type}] {method.upper()} {path} returns {code} — {resp_desc}")
                lines.append(f"    {given}")
                if when_extra:
                    lines.append(f"{when_extra}")
                lines.append(f"    When I send a {method.upper()} request to \"{path_example}\"")
                lines.append(f"    Then the response status code should be {code}")
                if then_extra:
                    lines.append(f"{then_extra}")
                lines.append("")

            # ── Required field validation (if POST/PUT/PATCH with body) ────────
            if method in ("post", "put", "patch") and req_fields:
                for field in req_fields[:5]:  # cap at 5 to avoid bloat
                    scenario_count += 1
                    lines.append(f"  Scenario: [VALIDATION] {method.upper()} {path} — missing required field \"{field}\"")
                    if requires_auth:
                        lines.append(f"    Given I am authenticated with valid credentials")
                    else:
                        lines.append(f"    Given the API is available")
                    lines.append(f"    And I provide a request body missing the required field \"{field}\"")
                    lines.append(f"    When I send a {method.upper()} request to \"{path_example}\"")
                    lines.append(f"    Then the response status code should be 400 or 422")
                    lines.append(f"    And the response body should reference the missing field \"{field}\"")
                    lines.append("")

            # ── Auth scenarios (if not already covered by documented codes) ────
            if requires_auth and "401" not in responses:
                scenario_count += 1
                lines.append(f"  Scenario: [AUTH] {method.upper()} {path} — unauthenticated request")
                lines.append(f"    Given I am not authenticated")
                lines.append(f"    When I send a {method.upper()} request to \"{path_example}\"")
                lines.append(f"    Then the response status code should be 401")
                lines.append(f"    And the response should indicate authentication is required")
                lines.append("")

            if requires_auth and "403" not in responses:
                scenario_count += 1
                lines.append(f"  Scenario: [AUTH] {method.upper()} {path} — forbidden for unprivileged user")
                lines.append(f"    Given I am authenticated as a user without sufficient permissions")
                lines.append(f"    When I send a {method.upper()} request to \"{path_example}\"")
                lines.append(f"    Then the response status code should be 403")
                lines.append(f"    And the response should indicate access is denied")
                lines.append("")

    # ── Summary comment ────────────────────────────────────────────────────────
    lines.insert(2, f"# Total scenarios generated: {scenario_count}")
    lines.insert(3, f"# Endpoints covered: {len(paths)}")
    lines.insert(4, "")

    return "\n".join(lines)


# ── Entry point ────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_gherkin.py <spec_file> [output_file]")
        sys.exit(1)

    spec_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "output.feature"

    print(f"Loading spec: {spec_path}", file=sys.stderr)
    spec = load_spec(spec_path)

    print("Generating Gherkin scenarios...", file=sys.stderr)
    feature = generate_feature(spec, spec_path)

    Path(output_path).write_text(feature, encoding="utf-8")
    print(f"Done. Written to: {output_path}", file=sys.stderr)

    # Print summary stats
    scenarios = feature.count("\n  Scenario:")
    print(f"Scenarios: {scenarios}", file=sys.stderr)


if __name__ == "__main__":
    main()