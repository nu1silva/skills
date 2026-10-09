# Gherkin Best Practices Reference

## Structure

Every `.feature` file follows this structure:
```
Feature: <API or resource name>
  <optional description>

  Background: (optional, shared setup for all scenarios)
    Given ...

  Scenario: <descriptive title>
    Given <precondition>
    When  <action>
    Then  <assertion>
    And   <additional assertion>
```

## Scenario naming convention

Use this prefix pattern for clarity:

| Prefix | Meaning |
|---|---|
| `[HAPPY]` | Successful request — 2xx |
| `[ERROR]` | Client error — 4xx (except auth) |
| `[AUTH]` | Authentication/authorisation — 401/403 |
| `[VALIDATION]` | Missing/invalid field — 400/422 |
| `[REDIRECT]` | Redirect response — 3xx |
| `[RATE LIMIT]` | Rate limiting — 429 |
| `[SERVER ERROR]` | Server-side failure — 5xx |

## Given / When / Then patterns

### Given (preconditions)
```gherkin
Given I am authenticated with valid credentials
Given I am not authenticated
Given I am authenticated as a user without sufficient permissions
Given I have exceeded the allowed request rate
Given the API is available
Given the resource with id "123" exists
Given the resource with id "999" does not exist
```

### When (actions)
```gherkin
When I send a GET request to "/users/123"
When I send a POST request to "/users" with body:
  """
  { "name": "Alice", "email": "alice@example.com" }
  """
When I send a DELETE request to "/users/123"
```

### Then (assertions)
```gherkin
Then the response status code should be 200
Then the response status code should be 400 or 422
Then the response body should be valid JSON
Then the response body should contain error details
Then the response body should reference the missing field "email"
Then the response should include a Retry-After header
Then the response should contain a Location header
Then the response body should not expose internal stack traces
```

## Scenario Outline (parameterised tests)

Use when testing the same flow with multiple input variants:
```gherkin
Scenario Outline: POST /users — invalid email formats
  Given I am authenticated with valid credentials
  When I send a POST request to "/users" with email "<email>"
  Then the response status code should be 422

  Examples:
    | email          |
    | notanemail     |
    | @nodomain.com  |
    | missing@       |
    | ""             |
```

## Background (shared setup)

Use Background when all scenarios in a feature share the same preconditions:
```gherkin
Background:
  Given the API base URL is "https://api.example.com/v1"
  And I am authenticated with a valid bearer token
```

## Tags

Tag scenarios for selective test execution:
```gherkin
@smoke @happy_path
Scenario: [HAPPY] GET /users returns list

@regression @auth
Scenario: [AUTH] GET /users — unauthenticated returns 401

@slow @integration
Scenario: [SERVER ERROR] POST /orders — handles timeout
```

## Common step library (reusable steps)

Define these steps once in your step definitions:

```python
# Authentication
@given('I am authenticated with valid credentials')
@given('I am not authenticated')
@given('I am authenticated as a user without sufficient permissions')

# Request
@when('I send a {method} request to "{path}"')
@when('I send a {method} request to "{path}" with body:')

# Assertions
@then('the response status code should be {code:d}')
@then('the response body should be valid JSON')
@then('the response body should contain error details')
@then('the response body should reference the missing field "{field}"')
@then('the response should include a {header} header')
```

## Do's and Don'ts

**Do:**
- Write scenarios in plain business language — avoid implementation details
- One behaviour per scenario
- Use `And` to chain related steps of the same type
- Make scenario titles unique and self-describing

**Don't:**
- Put SQL or code inside Gherkin steps
- Make scenarios depend on execution order
- Test multiple distinct behaviours in one scenario
- Use vague terms like "correctly" or "properly"