---
description: REST conventions, pagination, versioning, and response format
globs: apps/api/src/routes/**/*.ts
---

## Pagination
- Cursor-based for large datasets: `?cursor=abc&limit=20&sort=createdAt&order=desc`
- Offset-based for admin dashboards only: `?page=1&pageSize=50`

## Naming
- Endpoints: plural nouns (`/products`).
- Query params: camelCase (`pageSize`, `sortBy`).
- Response fields: camelCase.
- Enum values: UPPER_SNAKE_CASE.

## Versioning
- URL prefix: `/api/v1/`.
- Breaking changes = new version.
- Non-breaking (new optional fields) = current version.
- Deprecation: `Sunset` header 3 months before removal.

## Documentation
- OpenAPI spec in `docs/api/openapi.yaml`.
- Update spec BEFORE implementation.
- All endpoints: request/response examples.
