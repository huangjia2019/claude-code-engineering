---
description: PostgreSQL schema conventions, Drizzle ORM patterns, and migration rules
globs: apps/api/src/db/**/*.ts
---

## Schema Conventions
- UUID primary keys via `gen_random_uuid()`.
- All tables: `created_at`, `updated_at` timestamps.
- Soft deletes: `deleted_at` nullable. NEVER hard delete user data.
- Money: `integer` (cents). Frontend handles formatting.
- Booleans prefixed: `is_active`, `is_published`, `has_shipping`.
- JSON columns only for schemaless data.
- Foreign keys: explicit `ON DELETE` behavior.
- Indexes: FKs, WHERE columns, sort columns.
- Tables: snake_case plural. Columns: camelCase in Drizzle, snake_case in PG.

## Migrations
- Must be reversible (include `down`).
- NEVER modify existing migrations.
- Data migrations separate from schema migrations.
- Destructive ops: 2-step (deprecate → deploy → remove).
- Test on production data copy before deploying.

## Queries
- Drizzle query builder for ALL access. No raw SQL unless necessary.
- Transactions for multi-table writes.
- N+1 forbidden — use `with` or joins.
- Prepared statements for hot queries.
- Timeout: 5 seconds. Complex queries in service layer only.

## Connection Pool
- Dev: 20 max. Prod: 100.
- Drizzle manages lifecycle. Raw `pg` must manage manually.

## Soft Deletes
- Global filter excludes deleted records by default.
- Admin queries include deleted (audit).
- Explicit `.where(isNull(table.deletedAt))` for clarity.
- Hard delete only for GDPR compliance (legal approval required).
