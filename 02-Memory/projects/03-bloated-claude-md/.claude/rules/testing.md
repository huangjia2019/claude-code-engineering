---
description: Testing strategy, coverage targets, and test data rules
globs: "**/*.test.{ts,tsx}"
---

## Unit Tests
- Next to source or in `tests/unit/`.
- Mock externals (Stripe, SendGrid, Algolia) with `vi.mock()`.
- Test services, not HTTP handlers.
- Coverage: 80% services, 60% overall.
- Name: `it('should {behavior} when {condition}')`.

## Integration Tests
- In `tests/integration/`.
- Real PostgreSQL + Redis via testcontainers.
- Mock only external APIs.
- Fresh DB per test file.
- Full request-response through Express.

## E2E Tests
- Playwright in `tests/e2e/`.
- Critical flows: browse → cart → checkout → confirmation.
- `page.waitForResponse()` not timeouts.
- Visual regression for key pages. Run against staging.

## Test Data
- Factories in `tests/fixtures/factories.ts`.
- `faker` for data generation.
- NEVER production data. Clean up after each suite.
