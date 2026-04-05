---
description: Authentication, input validation, data protection, and rate limiting rules
globs: apps/api/src/**/*.ts
---

## Auth & Authorization
- Passwords: bcrypt, cost factor 12.
- JWT secrets: min 32 chars, rotated quarterly.
- Admin routes: `adminMiddleware` after `authMiddleware`.
- API keys: stored hashed, shown once, never retrievable.

## Input Validation
- Sanitize all user input. XSS: helmet + DOMPurify.
- SQL injection: Drizzle parameterizes. Never concatenate SQL.
- File uploads: validate MIME, max 10MB, ClamAV scan.
- URL params: validate UUID format before DB queries.

## Data Protection
- PII encrypted at rest (RDS encryption).
- NEVER store raw card numbers (Stripe only).
- NEVER log passwords, tokens, API keys, card numbers.
- CORS: whitelist origins, no `*` in production.
- HTTPS only. HSTS. Secure + SameSite cookies.

## Rate Limiting
- Global: 100 req/IP/min.
- Auth: 5 attempts/IP/15min.
- Writes: 30 req/user/min.
- Webhooks: Stripe IP whitelist only.

## Dependencies
- `pnpm audit` in CI — fail on high/critical.
- Dependabot enabled.
- Review new deps: downloads, maintenance, license.
