---
description: Express backend architecture, routing, auth, and logging conventions
globs: apps/api/src/**/*.ts
---

## Architecture
- Controllers: THIN — validate input, call service, format response.
- Services: all business logic and database calls.
- Services never import from controllers or routes.
- Middleware for cross-cutting concerns only.

## Routes
- RESTful conventions. Files in `apps/api/src/routes/{resource}.routes.ts`.
- All routes require `authMiddleware` unless documented as public.
- Mutation endpoints require rate limiting.
- Version prefix: `/api/v1/`. Breaking changes = new version.

## Response Format
```json
{ "success": true, "data": {...}, "meta": { "page": 1, "total": 150 } }
{ "success": false, "error": { "code": "PRODUCT_NOT_FOUND", "message": "..." } }
```

## Validation
- Zod schemas from `packages/shared`, applied via `validate(schema)` middleware.
- Validated body: `req.validated` (typed).
- Never trust client input.

## Error Handling
- Custom errors extend `AppError` (`lib/errors.ts`).
- `express-async-errors` — no manual try-catch.
- Never expose stack traces in responses.
- All errors logged via Winston.

## Authentication
- Access token: JWT, 15min, in memory.
- Refresh token: opaque, 7d, HTTP-only cookie.
- CSRF: double-submit cookie. Rate limit: 5 failed/IP/15min.
- OAuth2 via Passport.js. Sessions in Redis.

## Logging
- Winston only. NEVER `console.log`.
- Include `req.id` correlation ID in all entries.
- Structured JSON in production.
- NEVER log passwords, tokens, card numbers.
