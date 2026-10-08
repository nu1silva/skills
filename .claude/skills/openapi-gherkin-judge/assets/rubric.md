# Gherkin Judge Rubric

Each criterion is scored 1–5. Overall score = average. PASS threshold = 3.5.

| Score | Meaning                                |
| ----- | -------------------------------------- |
| 5     | Excellent — no issues found            |
| 4     | Good — minor gaps only                 |
| 3     | Adequate — notable gaps but functional |
| 2     | Poor — significant issues              |
| 1     | Very poor or criterion entirely absent |

---

## Criteria

### 1. Endpoint Coverage

Every endpoint + HTTP method in the spec has at least one `[HAPPY]` scenario.

**Pass indicators:**

- Count of `[HAPPY]` scenarios matches count of endpoint+method combinations
- Each happy path uses the correct success code (200/201/204)

**Fail indicators:**

- Endpoints with no happy path scenario
- Wrong success code used

---

### 2. Error Code Coverage

Every documented response status code (4xx, 5xx) in the spec has a corresponding scenario.

**Pass indicators:**

- Each `responses:` entry maps to exactly one scenario
- Scenario prefix matches the code range ([ERROR], [AUTH], [SERVER ERROR] etc.)

**Fail indicators:**

- Documented codes with no scenario
- Scenarios for undocumented codes (hallucination)

---

### 3. Auth Coverage

All secured endpoints (those with a `security` block) have:

- A 401 scenario (unauthenticated)
- A 403 scenario (insufficient permissions)

**Pass indicators:**

- Both 401 and 403 present for every secured endpoint
- `Given I am not authenticated` used for 401
- `Given I am authenticated as a user without sufficient permissions` used for 403

**Fail indicators:**

- Secured endpoints missing 401 or 403
- Auth scenarios on unsecured endpoints

---

### 4. Validation Depth

Each required field in a request body has its own missing-field `[VALIDATION]` scenario.

**Pass indicators:**

- One `[VALIDATION]` scenario per required field
- Scenario references the specific field name
- Asserts 400 or 422 response

**Fail indicators:**

- Required fields not individually tested
- Only a generic "invalid body" scenario with no field specificity

---

### 5. Step Clarity

Given/When/Then steps are unambiguous, specific, and implementable.

**Pass indicators:**

- Steps read like instructions a developer can implement in one afternoon
- Paths use concrete example values, not placeholders like `{id}`
- Assertions are specific (exact status code, named headers)

**Fail indicators:**

- Vague steps like "the request succeeds"
- Unresolved path parameter placeholders
- Duplicate or contradictory steps

---

### 6. BDD Correctness

Each scenario tests exactly one behaviour. Step types are not mixed.

**Pass indicators:**

- One `When` per scenario
- `Given` = precondition only, `Then` = assertion only
- Scenarios are independent (no shared state assumptions)

**Fail indicators:**

- Multiple `When` steps in one scenario
- Business logic inside `Given` steps
- Scenarios that depend on previous scenario outcomes

---

### 7. Spec Fidelity

No hallucinated content — all paths, methods, codes, and parameters are traceable to the spec.

**Pass indicators:**

- Every path in the feature exists in the spec
- Every status code in the feature is documented in the spec
- Parameter names match the spec exactly

**Fail indicators:**

- Paths not in the spec
- Status codes not documented
- Wrong HTTP methods used

---

### 8. Completeness

No obvious test cases missing that a thorough QA engineer would include.

**Pass indicators:**

- Rate limiting (429) tested if documented
- Boundary values considered for numeric fields
- Conflict scenarios (409) present where relevant
- Empty/null values considered for optional fields

**Fail indicators:**

- Missing rate limit scenarios
- No boundary value tests for numeric parameters
- Conflict/state scenarios absent
