# CLAUDE.md — ShopFlow E-Commerce Platform

## Project Overview

ShopFlow is a full-stack e-commerce platform: React 18 + Express.js + PostgreSQL 16.
Monorepo managed by Turborepo + pnpm. Three packages: `apps/web`, `apps/api`, `packages/shared`.

## Tech Stack

- **Frontend**: React 18, TypeScript 5.3, Vite 5, Zustand, TanStack Query, Tailwind CSS, Radix UI
- **Backend**: Express 4.18, Drizzle ORM, Redis 7, Bull queues, Passport.js, Socket.io
- **Infra**: Docker Compose (dev), AWS ECS Fargate (prod), RDS, ElastiCache, S3 + CloudFront
- **Services**: Stripe, SendGrid, Algolia, Cloudinary, Sentry, LaunchDarkly

## Quick Start

```bash
pnpm install && docker compose up -d
cp .env.example .env.local        # Fill in API keys
pnpm --filter api db:migrate && pnpm --filter api db:seed
pnpm dev                          # web :5173, api :3001
```

## Common Commands

```bash
pnpm dev / dev:web / dev:api       # Development servers
pnpm test / test:web / test:api    # Tests
pnpm test:e2e                      # Playwright E2E
pnpm build                         # Build all
pnpm lint && pnpm typecheck        # Code quality
pnpm --filter api db:migrate       # Run migrations
pnpm --filter api db:studio        # Drizzle Studio
pnpm stripe:listen                 # Webhook forwarding
```

---

## React Rules

### Component Structure
- Functional components ONLY. No class components anywhere.
- One component per file, file name = component name (PascalCase.tsx).
- Props interface named `{ComponentName}Props`, defined in the same file.
- Named exports only, no default exports (exception: page components for lazy loading).

### State Management
- Zustand for client state (auth, cart, UI). TanStack Query for server state.
- DO NOT add Redux or MobX. We migrated away from Redux in Feb 2024.
- Zustand stores live in `apps/web/src/stores/`. Max 4 stores.
- Never put server-fetched data in Zustand — that's TanStack Query's job.
- TanStack Query staleTime: 5min for products, 0 for cart, 1hr for categories.

### Hooks
- Custom hooks for logic reused in 2+ components.
- Hook files go in `apps/web/src/hooks/`, named `use{Name}.ts`.
- Never call hooks conditionally. Never use hooks inside callbacks.
- Avoid `useEffect` for derived state — compute inline during render.

### Performance
- `React.memo()` only when React DevTools Profiler confirms wasted re-renders.
- `Suspense` + `lazy()` for all route-level code splitting.
- Image: `loading="lazy"` + responsive `srcSet` for all `<img>`.
- Debounce search input (300ms) using `useDebounce` hook.
- Bundle size budget: 200KB gzipped initial load. Check with `npx vite-bundle-visualizer`.

### Styling
- Tailwind CSS only. No CSS modules, no styled-components, no inline `style={}`.
- Use `cn()` utility (from `lib/utils.ts`) for conditional class merging.
- Responsive: mobile-first (`sm:` → `md:` → `lg:`).
- Dark mode: use `dark:` variant. All new components must support dark mode.
- Design tokens in `tailwind.config.ts` — never hardcode colors or spacing.

### Forms
- React Hook Form + Zod for all forms. No Formik, no uncontrolled forms.
- Zod schemas defined in `packages/shared/src/validators/`.
- Error messages shown inline below each field with `aria-describedby`.
- Submit buttons disabled during submission with loading indicator.

### Accessibility
- All interactive elements: proper ARIA labels, keyboard navigation, focus management.
- Color contrast: WCAG AA minimum (4.5:1 normal text, 3:1 large text).
- All images have meaningful `alt` text (or `alt=""` if decorative).
- Modal dialogs: focus trap, Escape to close, `role="dialog"`.
- Test with screen reader (VoiceOver/NVDA) before merging accessibility-related PRs.

### Error Handling
- Error boundaries at route level and around critical sections (cart, checkout).
- Use `ErrorBoundary` component from `components/ui/ErrorBoundary.tsx`.
- Show user-friendly error messages, log technical details to Sentry.
- Network errors: show retry button with exponential backoff.

---

## Express / Backend Rules

### Architecture
- Controllers are THIN — validate input, call service, format response.
- Services contain all business logic and database calls.
- Services never import from controllers or routes.
- Middleware for cross-cutting concerns only (auth, logging, rate limiting).

### Route Structure
- RESTful conventions strictly followed.
- Route files in `apps/api/src/routes/{resource}.routes.ts`.
- All routes must have `authMiddleware` unless explicitly documented as public.
- Mutation endpoints must have rate limiting.
- Version prefix: `/api/v1/`. Breaking changes require new version.

### Response Format
- All responses use envelope format:
  ```json
  { "success": true, "data": {...}, "meta": { "page": 1, "total": 150 } }
  ```
- Error responses:
  ```json
  { "success": false, "error": { "code": "PRODUCT_NOT_FOUND", "message": "..." } }
  ```
- HTTP status codes: 200 OK, 201 Created, 204 No Content, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 409 Conflict, 422 Unprocessable Entity, 429 Too Many Requests, 500 Internal Server Error.

### Validation
- All request bodies validated with Zod schemas from `packages/shared`.
- Apply via `validate(schema)` middleware.
- Validated body available as `req.validated` (typed).
- Never trust client input — validate everything server-side even if frontend validates.

### Error Handling
- Custom error classes extend `AppError` (in `lib/errors.ts`).
- `express-async-errors` installed — no try-catch needed in handlers.
- Unhandled errors caught by global error middleware.
- All errors logged with Winston structured logger.
- Never expose stack traces or internal details in API responses.

### Authentication
- Dual-token strategy: access token (JWT, 15min, in memory) + refresh token (opaque, 7d, HTTP-only cookie).
- CSRF: double-submit cookie pattern.
- Rate limit: 5 failed logins per IP per 15 minutes.
- OAuth2 via Passport.js (Google, GitHub).
- Session data in Redis: `session:{userId}:{sessionId}`.

### Logging
- Use Winston logger from `lib/logger.ts`. NEVER use `console.log`.
- Log levels: error, warn, info, debug.
- Include correlation ID (`req.id`) in all log entries.
- Structured JSON format in production.
- Sensitive data (passwords, tokens, card numbers) NEVER logged.

---

## Database Rules

### Schema Conventions
- All tables: UUID primary keys via `gen_random_uuid()`.
- All tables: `created_at` and `updated_at` timestamps.
- Soft deletes: `deleted_at` nullable timestamp. NEVER hard delete user-facing data.
- Money: `integer` type (cents). Formatting is frontend's job.
- Booleans prefixed: `is_active`, `is_published`, `has_shipping`.
- JSON columns only for truly schemaless data (user prefs, metadata).
- Foreign keys: always explicit `ON DELETE` behavior.
- Indexes: all foreign keys, all WHERE clause columns, all sort columns.
- Table names: snake_case plural (`products`, `order_items`, `user_addresses`).
- Column names: camelCase in Drizzle schema, snake_case in PostgreSQL.

### Migrations
- Migrations must be reversible (include `down`).
- NEVER modify existing migration files — create new ones.
- Data migrations separate from schema migrations.
- Destructive ops (drop column/table) require 2-step:
  1. Mark deprecated + add new column/table.
  2. After deploy: remove old column/table.
- Test migrations on production data copy before deploying.

### Queries
- Drizzle query builder for ALL database access. No raw SQL unless absolutely necessary.
- Transactions for multi-table writes:
  ```typescript
  await db.transaction(async (tx) => {
    await tx.insert(orders).values(orderData);
    await tx.update(inventory).set({ quantity: sql`quantity - ${qty}` });
  });
  ```
- N+1 forbidden — use `with` (eager loading) or explicit joins.
- Prepared statements for frequently executed queries.
- Query timeout: 5 seconds (configured in Drizzle).
- Complex queries in service layer, never in controllers.

### Connection Pool
- Dev: 20 max connections. Prod: 100.
- Drizzle handles connection lifecycle automatically.
- Any raw `pg` usage must manage connections manually.
- If `ECONNREFUSED`: check Docker, check pool exhaustion.

---

## TypeScript Rules

- `"strict": true` in all tsconfig files. No exceptions.
- NEVER use `any`. Use `unknown` + type guards instead.
- Shared types in `packages/shared/src/types/`.
- Prefer `const` over `let`. Never use `var`.
- Use discriminated unions for complex state (not boolean flags).
- Exhaustive switch with `never` type for union handling.
- No type assertions (`as`) unless in test code with comment explaining why.
- Generic constraints: always constrain (`<T extends Base>` not `<T>`).
- Utility types: use `Pick`, `Omit`, `Partial`, `Required` over manual redefinition.
- Enum: prefer `as const` objects over TypeScript enums.

---

## Testing Rules

### Unit Tests
- Located next to source files or in `tests/unit/`.
- Mock external services (Stripe, SendGrid, Algolia) with `vi.mock()`.
- Test business logic in services, not HTTP handlers.
- Coverage target: 80% services, 60% overall.
- Test names: `it('should {expected behavior} when {condition}')`.

### Integration Tests
- Located in `tests/integration/`.
- Real PostgreSQL + Redis via testcontainers.
- Mock ONLY external APIs (Stripe, SendGrid).
- Fresh database per test file (migrations applied).
- Test full request-response cycle through Express.

### E2E Tests
- Playwright in `tests/e2e/`.
- Critical flows: browse → cart → checkout → confirmation.
- Use `page.waitForResponse()` not fixed timeouts.
- Visual regression for key pages.
- Run in CI against staging.

### Test Data
- Factory functions in `tests/fixtures/factories.ts`.
- `faker` for realistic data generation.
- NEVER use production data in tests.
- Clean up test data after each test suite.

---

## Security Rules

### Authentication & Authorization
- Never store passwords in plaintext — bcrypt with cost factor 12.
- JWT secrets: minimum 32 characters, rotated quarterly.
- Admin routes: `adminMiddleware` checks `role === 'admin'` after `authMiddleware`.
- API keys: stored hashed, displayed once on creation, never retrievable.

### Input Validation
- Sanitize all user input. XSS protection via helmet + DOMPurify.
- SQL injection: Drizzle parameterizes all queries. Never concatenate SQL strings.
- File uploads: validate MIME type, max 10MB, virus scan via ClamAV.
- URL parameters: validate UUID format before database queries.

### Data Protection
- PII encrypted at rest (AWS RDS encryption).
- NEVER store raw card numbers — Stripe handles all card data.
- NEVER log passwords, tokens, API keys, card numbers.
- CORS: whitelist specific origins, no wildcard `*` in production.
- HTTPS only. HSTS header enabled. Secure + SameSite cookies.

### Dependency Security
- `pnpm audit` runs in CI — build fails on high/critical vulnerabilities.
- Dependabot enabled for automated dependency updates.
- No packages with known CVEs in production dependencies.
- Review new dependency additions: check download count, maintenance status, license.

### Rate Limiting
- Global: 100 requests per IP per minute.
- Auth endpoints: 5 attempts per IP per 15 minutes.
- API writes: 30 requests per user per minute.
- Webhooks: IP whitelist (Stripe IPs only).
- Rate limit headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`.

---

## Payment Rules

- ALL payment logic through `payment.service.ts`. No direct Stripe calls elsewhere.
- Stripe Payment Intents API for card payments.
- NEVER store raw card numbers.
- Frontend: Stripe Elements only.
- Webhook: verify `stripe-signature` header. Idempotent handlers required.
- Deduplicate via `webhook_events.stripe_event_id` column.
- Currency in cents (integer). No floating-point money.
- Refunds: admin API only, never Stripe dashboard directly.
- Payment errors: log to Sentry with `payment` tag.

---

## API Design Rules

### Pagination
- Cursor-based for large datasets (products, orders):
  `GET /api/v1/products?cursor=abc&limit=20&sort=createdAt&order=desc`
- Offset-based only for admin dashboards:
  `GET /api/v1/admin/customers?page=1&pageSize=50`

### Naming
- Endpoints: plural nouns (`/products` not `/product`).
- Query params: camelCase (`pageSize`, `sortBy`).
- Response fields: camelCase.
- Enum values: UPPER_SNAKE_CASE (`ORDER_CONFIRMED`, `PAYMENT_FAILED`).

### Versioning
- URL prefix: `/api/v1/`.
- Breaking changes (field removal, type change) require version bump.
- Non-breaking changes (new optional fields) can go in current version.
- Deprecation: add `Sunset` header 3 months before removal.

### Documentation
- OpenAPI spec maintained in `docs/api/openapi.yaml`.
- Update spec BEFORE implementing endpoint changes.
- All endpoints must have request/response examples.

---

## Git & PR Rules

### Branch Naming
- `feature/SF-123-short-description`
- `fix/SF-456-bug-name`
- `chore/SF-789-description`
- `hotfix/SF-999-critical-issue`

### Commit Messages
- Conventional commits format:
  - `feat(cart): add quantity validation`
  - `fix(orders): handle null shipping address`
  - `chore(deps): update stripe to 14.x`
- Present tense, imperative mood.
- Max 72 characters for subject line.
- Body: explain WHY, not WHAT.

### PR Requirements
- CI must pass (lint + tests + build).
- At least 1 review approval.
- No `console.log` or `debugger` statements.
- Database migrations: reviewed by senior engineer.
- Breaking API changes: version bump required.
- PR description: what, why, how to test.
- Max 400 lines of changes per PR (split larger changes).

### Branch Protection
- `main`: require 2 approvals, no force push, require linear history.
- `develop`: require 1 approval, no force push.
- All branches: require CI pass before merge.

---

## Performance Rules

### Frontend
- Bundle budget: 200KB gzipped initial.
- Lazy load all routes except home + product listing.
- `loading="lazy"` on all images below fold.
- TanStack Query: prefetch on hover for product links.
- Web Vitals targets: LCP < 2.5s, FID < 100ms, CLS < 0.1.

### Backend
- p95 response time: < 200ms reads, < 500ms writes.
- Redis caching: product catalog (15min TTL), categories (1hr), sessions (7d).
- Database: indexes on all filtered/sorted columns.
- Batch operations for bulk inserts/updates.
- Connection pool: reuse, never per-request.
- N+1 queries: instant PR rejection.

### Monitoring
- DataDog APM on all HTTP requests.
- Custom metrics: checkout conversion, payment success rate, search latency.
- Alerts: p95 > 1s, error rate > 1%, queue depth > 1000.

---

## Image Handling Rules

- Upload via pre-signed S3 URL (not through our servers).
- S3 event → Bull job → generate 4 variants: thumb (150²), small (300²), medium (600²), large (1200²).
- Format: WebP with JPEG fallback.
- Storage path: `products/{productId}/{variant}.webp`.
- CloudFront serves with format negotiation.
- Max upload: 10MB. Validate MIME type server-side.
- Never use `multer` for product images (memory issues). Use streaming with `busboy`.

---

## Search Rules

- Product search via Algolia. PostgreSQL full-text as fallback only.
- Sync: CRUD events → Bull queue → Algolia index.
- Frontend: Algolia InstantSearch React components.
- Sync lag: 2-5 seconds expected. Admin shows "syncing" indicator.
- Retry: 3 attempts with exponential backoff on sync failure.

---

## Feature Flag Rules

- LaunchDarkly for all feature flags.
- Frontend: `useFeatureFlag('flag-name')`.
- Backend: `featureFlags.isEnabled('flag-name')`.
- Default: `false` if LaunchDarkly unreachable (fail closed).
- Active flags: `enable-b2b-pricing` (beta), `new-checkout-flow` (A/B), `enable-reviews` (80%).
- Remove flags after 100% rollout (flag debt is real).
- Flag naming: kebab-case, descriptive (`enable-{feature}` or `show-{ui-element}`).

---

## Deployment Rules

### Environments
- **Staging**: auto-deploy from `develop`, Stripe test mode, anonymized prod data.
- **Production**: manual trigger from `main`, blue-green ECS deploy, requires 2 approvals.

### Pre-deploy Checklist
1. All tests passing.
2. No `TODO`/`FIXME` in changed files.
3. Migrations tested on staging.
4. Feature flags configured.
5. Runbook updated for new failure modes.
6. On-call notified for major changes.

### Rollback
- ECS: re-deploy previous task definition.
- Database: run reverse migration.
- Feature flags: kill switch via LaunchDarkly.
- Post-rollback: incident report within 24 hours.

---

## Error Handling Rules

### Custom Error Classes
```typescript
class AppError extends Error { statusCode: number; code: string; }
class NotFoundError extends AppError { statusCode = 404; }
class ValidationError extends AppError { statusCode = 422; }
class AuthenticationError extends AppError { statusCode = 401; }
class AuthorizationError extends AppError { statusCode = 403; }
class ConflictError extends AppError { statusCode = 409; }
class RateLimitError extends AppError { statusCode = 429; }
```

### Error Reporting
- All 5xx errors → Sentry (auto).
- Payment errors → Sentry with `payment` tag.
- Auth failures → logged + rate limit check.
- Validation errors → 422 response, never Sentry.
- Expected errors (404, 409) → info log, not error log.

---

## Environment Variable Rules

- `.env.local` for local development, NEVER committed.
- `.env.example` maintained with all required keys (values blanked).
- Secrets: loaded from AWS Secrets Manager in production.
- All env vars validated at startup via Zod schema in `config/`.
- Missing required var = crash immediately, don't fall back silently.
- Naming: UPPER_SNAKE_CASE, prefixed by service (`STRIPE_SECRET_KEY`, `SENDGRID_API_KEY`).

---

## Code Style Rules

- Prefer `const` over `let`. Never `var`.
- Early returns to avoid nesting.
- Max function: ~50 lines.
- File naming: `camelCase.ts` utils, `PascalCase.tsx` components.
- Named exports preferred (except page components).
- Comments: WHY not WHAT.
- No `console.log` in production — Winston on backend, remove from frontend.
- No `any` — use `unknown` + type guards.
- No magic numbers — use named constants.
- No nested ternaries.
- Destructure props and function parameters.
- `async/await` over raw Promises. Never mix.

---

## Timezone Rules

- Database: all timestamps UTC (`timestamp with time zone`).
- Server: `dayjs.utc()` for all date operations. NEVER `new Date()` without UTC.
- Frontend: convert to user's local timezone for display only.
- API: accept and return ISO 8601 UTC strings.

---

## Soft Delete Rules

- Global Drizzle filter excludes `deleted_at IS NOT NULL` by default.
- Admin queries include deleted records (audit trail).
- New queries: explicitly add `.where(isNull(table.deletedAt))` for clarity.
- Hard delete: only for data retention compliance (GDPR), requires legal approval.

---

## Background Job Rules

- Bull queues for all async work (email, image processing, search sync, analytics).
- Job processors in `apps/api/src/jobs/{name}.job.ts`.
- All jobs must be idempotent (can safely retry).
- Retry: 3 attempts, exponential backoff.
- Dead letter queue for failed jobs.
- Bull Board UI for monitoring (`/admin/queues`).
- Long-running jobs: progress reporting via Bull's progress API.

---

## WebSocket Rules

- Socket.io for real-time notifications only.
- Auth: verify JWT on connection (not per-message).
- Namespaces: `/notifications`, `/admin`.
- Events: `order:status`, `inventory:low`, `chat:message`.
- Reconnection: client handles automatically via Socket.io.
- No business logic in socket handlers — emit events, let services handle.

---

## Known Issues

### Cart Race Condition
Two tabs updating same cart simultaneously. Server uses `SELECT FOR UPDATE`. Test concurrent requests when touching cart logic. See `cart.service.ts:L45-L80`.

### Redis Session Clock Skew
Clock skew between ECS instances can cause premature session expiration. Mitigated by NTP sync.

### Algolia Sync Lag
2-5 second delay after product update. Expected behavior, not a bug.

### PostgreSQL Pool Exhaustion
If `ECONNREFUSED` locally: check Docker running, check pool not exhausted from leaked connections.

---

## Internationalization Rules (i18n)

- All user-facing strings must go through `react-intl` `formatMessage()`.
- Translation files in `apps/web/src/locales/{locale}.json`.
- Supported locales: `en-US`, `zh-CN`, `ja-JP`, `ko-KR`.
- Default locale: `en-US`. Fallback chain: user locale → `en-US`.
- Date/time: `Intl.DateTimeFormat` via react-intl. NEVER hardcode date formats.
- Currency: `Intl.NumberFormat` with locale-aware formatting.
- Pluralization: use ICU message syntax (`{count, plural, one {# item} other {# items}}`).
- RTL: not supported yet, but keep layout mirroring in mind for future Arabic/Hebrew.
- Translation keys: dot-separated namespace (`cart.summary.totalLabel`).
- New strings: add to `en-US.json` first, translators handle others.
- No string concatenation for translated text — use template variables.

---

## Email Rules

- SendGrid for all transactional emails.
- Templates managed in SendGrid dashboard, NOT in code.
- Template IDs stored in `apps/api/src/config/email.ts`.
- All emails queued via Bull job (never send synchronously in request path).
- Required emails: welcome, order confirmation, shipping update, password reset, payment receipt.
- Each email type has a dedicated function in `email.service.ts`.
- Unsubscribe link mandatory in all marketing emails (CAN-SPAM compliance).
- Reply-to: `support@shopflow.example.com` (not `noreply@`).
- Test mode: emails to `@example.com` domains go to dev inbox.
- Rate limit: max 100 emails per minute to same recipient.

---

## Caching Rules

### Redis Caching Strategy
- Product catalog: 15-minute TTL, invalidated on product update.
- Category tree: 1-hour TTL, invalidated on category CRUD.
- User sessions: 7-day TTL, refreshed on activity.
- Search suggestions: 30-minute TTL.
- Rate limit counters: sliding window, 1-minute TTL.

### Cache Invalidation
- Write-through: update cache on every write operation.
- Pub/Sub: use Redis pub/sub for multi-instance cache invalidation.
- Cache key naming: `{resource}:{id}:{version}` (e.g., `product:abc123:v3`).
- NEVER cache user-specific data in shared cache keys.
- Cache stampede: use probabilistic early expiration for hot keys.

### CDN Caching
- CloudFront: 1-year cache for hashed static assets.
- Product images: 24-hour cache, invalidate on image update.
- API responses: no CDN caching (private, user-specific).
- `Cache-Control` headers set by Express middleware.

---

## Inventory Rules

- Inventory tracked per SKU per warehouse.
- Quantity decremented at order creation, not at cart add.
- Overselling prevented by `SELECT FOR UPDATE` + quantity check in transaction.
- Low stock threshold: configurable per product (default: 10 units).
- Low stock alert: real-time notification to admin via Socket.io.
- Inventory sync job runs every 15 minutes from external warehouse API.
- Backorder: not supported yet. Out-of-stock = hide "Add to Cart" button.

---

## Logging Format Rules

### Structured Log Schema
```json
{
  "timestamp": "2024-01-15T10:30:00.000Z",
  "level": "info",
  "service": "api",
  "correlationId": "req-abc123",
  "userId": "user-xyz",
  "action": "order.create",
  "duration": 145,
  "metadata": {}
}
```

### Log Levels
- `error`: unhandled exceptions, 5xx responses, payment failures.
- `warn`: deprecated API usage, approaching rate limits, slow queries (>1s).
- `info`: request/response, auth events, order lifecycle.
- `debug`: detailed flow for troubleshooting (disabled in production).

### Retention
- Production logs: 30 days in DataDog, 90 days in S3 archive.
- Staging logs: 7 days, no archive.
- PII in logs: NEVER. Use user ID, never email/name in log entries.
