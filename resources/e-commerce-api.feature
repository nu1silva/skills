# Generated from: sample-api.yaml
# API: E-commerce API 1.0.0
# Total scenarios generated: 46
# Endpoints covered: 11
# Revised: added 404s, boundary validation, payment failure, tightened assertions


Feature: E-commerce API
  This is an e-commerce API spec for a storefront.
  It includes authentication, product browsing, cart, and checkout operations.
  Auth is token-based. Explore, test, and mock this API freely.
  Base URL: https://api.demo-ecommerce.com/v1

  # ── POST /auth/register ─────────────────────────
  # Create a new user account
  # Tag: General | OperationId: post_auth_register

  Scenario: [HAPPY] Create a new user account
    Given the API is available
    And I provide a valid request body:
      """
      {
  "email": "user@example.com",
  "password": "string_value",
  "name": "string_value"
}
      """
    When I send a POST request to "/auth/register"
    Then the response status code should be 201
    And the response should indicate resource created
    And the response body should be valid JSON

  Scenario: [ERROR] POST /auth/register returns 400 — Invalid input
    Given the API is available
    And I provide an invalid or malformed request body
    When I send a POST request to "/auth/register"
    Then the response status code should be 400
    And the response body should contain a field "message"

  Scenario: [VALIDATION] POST /auth/register — missing required field "email"
    Given the API is available
    And I provide a request body missing the required field "email"
    When I send a POST request to "/auth/register"
    Then the response status code should be 400 or 422
    And the response body should reference the missing field "email"

  Scenario: [VALIDATION] POST /auth/register — missing required field "password"
    Given the API is available
    And I provide a request body missing the required field "password"
    When I send a POST request to "/auth/register"
    Then the response status code should be 400 or 422
    And the response body should reference the missing field "password"

  # ── POST /auth/login ─────────────────────────
  # Login and get access token
  # Tag: General | OperationId: post_auth_login

  Scenario: [HAPPY] Login and get access token
    Given the API is available
    And I provide a valid request body:
      """
      {
  "email": "string_value",
  "password": "string_value"
}
      """
    When I send a POST request to "/auth/login"
    Then the response status code should be 200
    And the response should indicate successful response
    And the response body should be valid JSON

  Scenario: [AUTH] POST /auth/login returns 401 — Unauthorized
    Given I am not authenticated
    When I send a POST request to "/auth/login"
    Then the response status code should be 401
    And the response should include a WWW-Authenticate header

  Scenario: [VALIDATION] POST /auth/login — missing required field "email"
    Given the API is available
    And I provide a request body missing the required field "email"
    When I send a POST request to "/auth/login"
    Then the response status code should be 400 or 422
    And the response body should reference the missing field "email"

  Scenario: [VALIDATION] POST /auth/login — missing required field "password"
    Given the API is available
    And I provide a request body missing the required field "password"
    When I send a POST request to "/auth/login"
    Then the response status code should be 400 or 422
    And the response body should reference the missing field "password"

  # ── GET /products ─────────────────────────
  # List all products with filters
  # Tag: General | OperationId: get_products

  Scenario: [HAPPY] List all products with filters
    Given the API is available
    When I send a GET request to "/products"
    Then the response status code should be 200
    And the response should indicate successful response
    And the response body should be valid JSON

  # ── GET /products/{id} ─────────────────────────
  # Get product details by ID
  # Tag: General | OperationId: get_products_id

  Scenario: [HAPPY] Get product details by ID
    Given the API is available
    And the path parameter "id" is "550e8400-e29b-41d4-a716-446655440000"
    When I send a GET request to "/products/550e8400-e29b-41d4-a716-446655440000"
    Then the response status code should be 200
    And the response should indicate successful response
    And the response body should be valid JSON

  Scenario: [ERROR] GET /products/{id} returns 404 — product not found
    Given the API is available
    And the path parameter "id" is "00000000-0000-0000-0000-000000000000"
    When I send a GET request to "/products/00000000-0000-0000-0000-000000000000"
    Then the response status code should be 404
    And the response body should contain a field "message"

  # ── GET /cart ─────────────────────────
  # Get current user's cart
  # Tag: General | OperationId: get_cart

  Scenario: [HAPPY] Get current user's cart
    Given I am authenticated with valid credentials
    When I send a GET request to "/cart"
    Then the response status code should be 200
    And the response should indicate successful response
    And the response body should be valid JSON

  Scenario: [AUTH] GET /cart — unauthenticated request
    Given I am not authenticated
    When I send a GET request to "/cart"
    Then the response status code should be 401
    And the response should indicate authentication is required

  Scenario: [AUTH] GET /cart — forbidden for unprivileged user
    Given I am authenticated as a user without sufficient permissions
    When I send a GET request to "/cart"
    Then the response status code should be 403
    And the response should indicate access is denied

  # ── POST /cart/items ─────────────────────────
  # Add item to cart
  # Tag: General | OperationId: post_cart_items

  Scenario: [HAPPY] Add item to cart
    Given I am authenticated with valid credentials
    And I provide a valid request body:
      """
      {
  "product_id": "550e8400-e29b-41d4-a716-446655440000",
  "quantity": 1
}
      """
    When I send a POST request to "/cart/items"
    Then the response status code should be 200
    And the response should indicate successful response
    And the response body should be valid JSON

  Scenario: [ERROR] POST /cart/items — product_id references a non-existent product
    Given I am authenticated with valid credentials
    And I provide a valid request body:
      """
      {
  "product_id": "00000000-0000-0000-0000-000000000000",
  "quantity": 1
}
      """
    When I send a POST request to "/cart/items"
    Then the response status code should be 404 or 422
    And the response body should contain a field "message"

  Scenario: [VALIDATION] POST /cart/items — quantity below minimum (0)
    Given I am authenticated with valid credentials
    And I provide a valid request body:
      """
      {
  "product_id": "550e8400-e29b-41d4-a716-446655440000",
  "quantity": 0
}
      """
    When I send a POST request to "/cart/items"
    Then the response status code should be 400 or 422
    And the response body should contain a field "message"

  Scenario: [VALIDATION] POST /cart/items — missing required field "product_id"
    Given I am authenticated with valid credentials
    And I provide a request body missing the required field "product_id"
    When I send a POST request to "/cart/items"
    Then the response status code should be 400 or 422
    And the response body should reference the missing field "product_id"

  Scenario: [VALIDATION] POST /cart/items — missing required field "quantity"
    Given I am authenticated with valid credentials
    And I provide a request body missing the required field "quantity"
    When I send a POST request to "/cart/items"
    Then the response status code should be 400 or 422
    And the response body should reference the missing field "quantity"

  Scenario: [AUTH] POST /cart/items — unauthenticated request
    Given I am not authenticated
    When I send a POST request to "/cart/items"
    Then the response status code should be 401
    And the response should indicate authentication is required

  Scenario: [AUTH] POST /cart/items — forbidden for unprivileged user
    Given I am authenticated as a user without sufficient permissions
    When I send a POST request to "/cart/items"
    Then the response status code should be 403
    And the response should indicate access is denied

  # ── POST /checkout ─────────────────────────
  # Checkout and place order
  # Tag: General | OperationId: post_checkout

  Scenario: [HAPPY] Checkout and place order
    Given I am authenticated with valid credentials
    And I provide a valid request body:
      """
      {
  "address_id": "string_value",
  "payment_method_id": "string_value"
}
      """
    When I send a POST request to "/checkout"
    Then the response status code should be 201
    And the response should indicate resource created
    And the response body should be valid JSON

  Scenario: [ERROR] POST /checkout — payment method declined
    Given I am authenticated with valid credentials
    And I provide a valid request body:
      """
      {
  "address_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "payment_method_id": "declined-payment-method-id"
}
      """
    When I send a POST request to "/checkout"
    Then the response status code should be 402 or 422
    And the response body should contain a field "message"

  Scenario: [VALIDATION] POST /checkout — missing required field "address_id"
    Given I am authenticated with valid credentials
    And I provide a request body missing the required field "address_id"
    When I send a POST request to "/checkout"
    Then the response status code should be 400 or 422
    And the response body should reference the missing field "address_id"

  Scenario: [VALIDATION] POST /checkout — missing required field "payment_method_id"
    Given I am authenticated with valid credentials
    And I provide a request body missing the required field "payment_method_id"
    When I send a POST request to "/checkout"
    Then the response status code should be 400 or 422
    And the response body should reference the missing field "payment_method_id"

  Scenario: [AUTH] POST /checkout — unauthenticated request
    Given I am not authenticated
    When I send a POST request to "/checkout"
    Then the response status code should be 401
    And the response should indicate authentication is required

  Scenario: [AUTH] POST /checkout — forbidden for unprivileged user
    Given I am authenticated as a user without sufficient permissions
    When I send a POST request to "/checkout"
    Then the response status code should be 403
    And the response should indicate access is denied

  # ── GET /orders ─────────────────────────
  # List your past orders
  # Tag: General | OperationId: get_orders

  Scenario: [HAPPY] List your past orders
    Given I am authenticated with valid credentials
    When I send a GET request to "/orders"
    Then the response status code should be 200
    And the response should indicate successful response
    And the response body should be valid JSON

  Scenario: [AUTH] GET /orders — unauthenticated request
    Given I am not authenticated
    When I send a GET request to "/orders"
    Then the response status code should be 401
    And the response should indicate authentication is required

  Scenario: [AUTH] GET /orders — forbidden for unprivileged user
    Given I am authenticated as a user without sufficient permissions
    When I send a GET request to "/orders"
    Then the response status code should be 403
    And the response should indicate access is denied

  # ── GET /orders/{orderId} ─────────────────────────
  # Get order details
  # Tag: General | OperationId: get_orders_orderid

  Scenario: [HAPPY] Get order details
    Given I am authenticated with valid credentials
    And the path parameter "orderId" is "550e8400-e29b-41d4-a716-446655440000"
    When I send a GET request to "/orders/550e8400-e29b-41d4-a716-446655440000"
    Then the response status code should be 200
    And the response should indicate successful response
    And the response body should be valid JSON

  Scenario: [ERROR] GET /orders/{orderId} returns 404 — order not found
    Given I am authenticated with valid credentials
    And the path parameter "orderId" is "00000000-0000-0000-0000-000000000000"
    When I send a GET request to "/orders/00000000-0000-0000-0000-000000000000"
    Then the response status code should be 404
    And the response body should contain a field "message"

  Scenario: [AUTH] GET /orders/{orderId} — unauthenticated request
    Given I am not authenticated
    When I send a GET request to "/orders/550e8400-e29b-41d4-a716-446655440000"
    Then the response status code should be 401
    And the response should indicate authentication is required

  Scenario: [AUTH] GET /orders/{orderId} — forbidden for unprivileged user
    Given I am authenticated as a user without sufficient permissions
    When I send a GET request to "/orders/550e8400-e29b-41d4-a716-446655440000"
    Then the response status code should be 403
    And the response should indicate access is denied

  # ── GET /addresses ─────────────────────────
  # Get your saved addresses
  # Tag: General | OperationId: get_addresses

  Scenario: [HAPPY] Get your saved addresses
    Given I am authenticated with valid credentials
    When I send a GET request to "/addresses"
    Then the response status code should be 200
    And the response should indicate successful response
    And the response body should be valid JSON

  Scenario: [AUTH] GET /addresses — unauthenticated request
    Given I am not authenticated
    When I send a GET request to "/addresses"
    Then the response status code should be 401
    And the response should indicate authentication is required

  Scenario: [AUTH] GET /addresses — forbidden for unprivileged user
    Given I am authenticated as a user without sufficient permissions
    When I send a GET request to "/addresses"
    Then the response status code should be 403
    And the response should indicate access is denied

  # ── POST /addresses ─────────────────────────
  # Add a new address
  # Tag: General | OperationId: post_addresses

  Scenario: [HAPPY] Add a new address
    Given I am authenticated with valid credentials
    And I provide a valid request body:
      """
      {
  "line1": "string_value",
  "line2": "string_value",
  "city": "string_value",
  "state": "string_value",
  "postal_code": "string_value",
  "country": "string_value"
}
      """
    When I send a POST request to "/addresses"
    Then the response status code should be 201
    And the response should indicate resource created
    And the response body should be valid JSON

  Scenario: [VALIDATION] POST /addresses — missing required field "line1"
    Given I am authenticated with valid credentials
    And I provide a request body missing the required field "line1"
    When I send a POST request to "/addresses"
    Then the response status code should be 400 or 422
    And the response body should reference the missing field "line1"

  Scenario: [VALIDATION] POST /addresses — missing required field "city"
    Given I am authenticated with valid credentials
    And I provide a request body missing the required field "city"
    When I send a POST request to "/addresses"
    Then the response status code should be 400 or 422
    And the response body should reference the missing field "city"

  Scenario: [VALIDATION] POST /addresses — missing required field "state"
    Given I am authenticated with valid credentials
    And I provide a request body missing the required field "state"
    When I send a POST request to "/addresses"
    Then the response status code should be 400 or 422
    And the response body should reference the missing field "state"

  Scenario: [VALIDATION] POST /addresses — missing required field "postal_code"
    Given I am authenticated with valid credentials
    And I provide a request body missing the required field "postal_code"
    When I send a POST request to "/addresses"
    Then the response status code should be 400 or 422
    And the response body should reference the missing field "postal_code"

  Scenario: [VALIDATION] POST /addresses — missing required field "country"
    Given I am authenticated with valid credentials
    And I provide a request body missing the required field "country"
    When I send a POST request to "/addresses"
    Then the response status code should be 400 or 422
    And the response body should reference the missing field "country"

  Scenario: [AUTH] POST /addresses — unauthenticated request
    Given I am not authenticated
    When I send a POST request to "/addresses"
    Then the response status code should be 401
    And the response should indicate authentication is required

  Scenario: [AUTH] POST /addresses — forbidden for unprivileged user
    Given I am authenticated as a user without sufficient permissions
    When I send a POST request to "/addresses"
    Then the response status code should be 403
    And the response should indicate access is denied
