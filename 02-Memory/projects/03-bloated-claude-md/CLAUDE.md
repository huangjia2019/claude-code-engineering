# CLAUDE.md — ShopFlow E-Commerce Platform

## Project Overview

ShopFlow is a modern, full-stack e-commerce platform built with React, Express.js, and PostgreSQL. The platform supports B2C and B2B commerce with features including product catalog management, shopping cart, checkout flow, user authentication, order management, inventory tracking, payment processing, shipping integration, and admin dashboard. The project was started in January 2024 by the engineering team at ShopFlow Inc. and is currently in active development with 12 engineers working across frontend, backend, and infrastructure teams.

## Tech Stack

### Frontend
- React 18.2.0 with TypeScript 5.3
- Vite 5.0 as build tool (migrated from Create React App in March 2024)
- React Router v6 for client-side routing
- Zustand for global state management (migrated from Redux in February 2024, see migration notes below)
- TanStack Query (React Query) v5 for server state
- Tailwind CSS 3.4 for styling
- Radix UI for accessible component primitives
- React Hook Form + Zod for form validation
- Vitest + React Testing Library for unit/integration tests
- Playwright for E2E tests
- Storybook 7 for component documentation

### Backend
- Node.js 20 LTS with Express.js 4.18
- TypeScript 5.3 (shared tsconfig with frontend)
- PostgreSQL 16 as primary database
- Redis 7 for caching and session management
- Drizzle ORM for database access (migrated from Prisma in April 2024, see migration notes)
- Express middleware: helmet, cors, morgan, express-rate-limit
- Passport.js for authentication (local + OAuth2)
- Bull queues for background jobs (email sending, image processing, inventory sync)
- Socket.io for real-time notifications
- Winston for structured logging
- Node-cron for scheduled tasks

### Infrastructure
- Docker + Docker Compose for local development
- AWS ECS Fargate for production deployment
- AWS RDS for managed PostgreSQL
- AWS ElastiCache for managed Redis
- AWS S3 + CloudFront for static assets and product images
- AWS SQS for message queuing between services
- GitHub Actions for CI/CD
- Terraform for infrastructure as code
- DataDog for monitoring and alerting

### Third-Party Services
- Stripe for payment processing (API version 2024-01-01)
- SendGrid for transactional emails
- Algolia for product search
- Cloudinary for image transformation
- Sentry for error tracking
- LaunchDarkly for feature flags
- Segment for analytics

## Repository Structure

```
shopflow/
├── apps/
│   ├── web/                          # React frontend application
│   │   ├── src/
│   │   │   ├── components/           # Shared UI components
│   │   │   │   ├── ui/              # Base primitives (Button, Input, Modal, etc.)
│   │   │   │   ├── layout/          # Layout components (Header, Footer, Sidebar)
│   │   │   │   ├── forms/           # Form components (LoginForm, CheckoutForm)
│   │   │   │   └── commerce/        # Commerce-specific (ProductCard, CartItem)
│   │   │   ├── pages/               # Route-level page components
│   │   │   │   ├── home/
│   │   │   │   ├── products/
│   │   │   │   ├── cart/
│   │   │   │   ├── checkout/
│   │   │   │   ├── account/
│   │   │   │   ├── orders/
│   │   │   │   └── admin/           # Admin dashboard pages
│   │   │   │       ├── products/
│   │   │   │       ├── orders/
│   │   │   │       ├── customers/
│   │   │   │       ├── analytics/
│   │   │   │       └── settings/
│   │   │   ├── hooks/               # Custom React hooks
│   │   │   │   ├── useAuth.ts
│   │   │   │   ├── useCart.ts
│   │   │   │   ├── useProducts.ts
│   │   │   │   ├── useOrders.ts
│   │   │   │   ├── useDebounce.ts
│   │   │   │   ├── useInfiniteScroll.ts
│   │   │   │   ├── useLocalStorage.ts
│   │   │   │   └── useMediaQuery.ts
│   │   │   ├── stores/              # Zustand stores
│   │   │   │   ├── authStore.ts     # Authentication state
│   │   │   │   ├── cartStore.ts     # Shopping cart state
│   │   │   │   ├── uiStore.ts       # UI state (modals, toasts, sidebar)
│   │   │   │   └── adminStore.ts    # Admin dashboard state
│   │   │   ├── api/                 # API client functions
│   │   │   │   ├── client.ts        # Axios instance with interceptors
│   │   │   │   ├── auth.ts
│   │   │   │   ├── products.ts
│   │   │   │   ├── orders.ts
│   │   │   │   ├── cart.ts
│   │   │   │   ├── payments.ts
│   │   │   │   └── admin.ts
│   │   │   ├── lib/                 # Utility functions
│   │   │   │   ├── utils.ts         # General utilities (cn, formatCurrency, etc.)
│   │   │   │   ├── validators.ts    # Zod schemas for form validation
│   │   │   │   ├── constants.ts     # App-wide constants
│   │   │   │   └── types.ts         # Shared TypeScript types
│   │   │   ├── styles/              # Global styles
│   │   │   │   ├── globals.css
│   │   │   │   └── tailwind.css
│   │   │   ├── App.tsx
│   │   │   ├── Router.tsx           # Route definitions
│   │   │   └── main.tsx
│   │   ├── public/
│   │   ├── tests/
│   │   │   ├── unit/
│   │   │   ├── integration/
│   │   │   └── e2e/
│   │   ├── .storybook/
│   │   ├── vite.config.ts
│   │   ├── tailwind.config.ts
│   │   ├── tsconfig.json
│   │   └── package.json
│   │
│   └── api/                          # Express backend application
│       ├── src/
│       │   ├── routes/               # Express route handlers
│       │   │   ├── auth.routes.ts
│       │   │   ├── products.routes.ts
│       │   │   ├── orders.routes.ts
│       │   │   ├── cart.routes.ts
│       │   │   ├── payments.routes.ts
│       │   │   ├── shipping.routes.ts
│       │   │   ├── admin.routes.ts
│       │   │   ├── webhooks.routes.ts
│       │   │   └── health.routes.ts
│       │   ├── controllers/          # Business logic controllers
│       │   │   ├── auth.controller.ts
│       │   │   ├── products.controller.ts
│       │   │   ├── orders.controller.ts
│       │   │   ├── cart.controller.ts
│       │   │   ├── payments.controller.ts
│       │   │   ├── shipping.controller.ts
│       │   │   └── admin.controller.ts
│       │   ├── services/             # Service layer
│       │   │   ├── auth.service.ts
│       │   │   ├── products.service.ts
│       │   │   ├── orders.service.ts
│       │   │   ├── cart.service.ts
│       │   │   ├── payment.service.ts
│       │   │   ├── shipping.service.ts
│       │   │   ├── email.service.ts
│       │   │   ├── search.service.ts
│       │   │   ├── inventory.service.ts
│       │   │   └── notification.service.ts
│       │   ├── middleware/           # Express middleware
│       │   │   ├── auth.middleware.ts
│       │   │   ├── validation.middleware.ts
│       │   │   ├── error.middleware.ts
│       │   │   ├── logging.middleware.ts
│       │   │   ├── rateLimit.middleware.ts
│       │   │   └── admin.middleware.ts
│       │   ├── db/                   # Database layer
│       │   │   ├── schema/           # Drizzle schema definitions
│       │   │   │   ├── users.ts
│       │   │   │   ├── products.ts
│       │   │   │   ├── orders.ts
│       │   │   │   ├── cart.ts
│       │   │   │   ├── categories.ts
│       │   │   │   ├── reviews.ts
│       │   │   │   ├── inventory.ts
│       │   │   │   ├── addresses.ts
│       │   │   │   └── index.ts
│       │   │   ├── migrations/       # SQL migrations
│       │   │   ├── seeds/            # Seed data
│       │   │   │   ├── users.seed.ts
│       │   │   │   ├── products.seed.ts
│       │   │   │   └── categories.seed.ts
│       │   │   └── client.ts         # Database connection
│       │   ├── jobs/                 # Background job processors
│       │   │   ├── email.job.ts
│       │   │   ├── imageProcess.job.ts
│       │   │   ├── inventorySync.job.ts
│       │   │   ├── orderFulfillment.job.ts
│       │   │   └── analytics.job.ts
│       │   ├── lib/                  # Shared utilities
│       │   │   ├── stripe.ts         # Stripe client configuration
│       │   │   ├── redis.ts          # Redis client
│       │   │   ├── s3.ts             # S3 client
│       │   │   ├── algolia.ts        # Algolia search client
│       │   │   ├── sendgrid.ts       # SendGrid email client
│       │   │   ├── logger.ts         # Winston logger configuration
│       │   │   ├── errors.ts         # Custom error classes
│       │   │   └── types.ts          # Shared types
│       │   ├── config/               # Configuration
│       │   │   ├── database.ts
│       │   │   ├── redis.ts
│       │   │   ├── auth.ts
│       │   │   ├── stripe.ts
│       │   │   └── app.ts
│       │   └── app.ts                # Express app setup
│       ├── tests/
│       │   ├── unit/
│       │   ├── integration/
│       │   └── fixtures/
│       ├── tsconfig.json
│       └── package.json
│
├── packages/
│   └── shared/                       # Shared types and utilities
│       ├── src/
│       │   ├── types/                # Shared TypeScript interfaces
│       │   │   ├── user.ts
│       │   │   ├── product.ts
│       │   │   ├── order.ts
│       │   │   ├── cart.ts
│       │   │   └── api.ts            # API request/response types
│       │   ├── constants/
│       │   │   ├── orderStatus.ts
│       │   │   ├── paymentStatus.ts
│       │   │   └── roles.ts
│       │   └── validators/           # Shared Zod schemas
│       │       ├── product.ts
│       │       ├── order.ts
│       │       └── user.ts
│       ├── tsconfig.json
│       └── package.json
│
├── infra/                            # Infrastructure as Code
│   ├── terraform/
│   │   ├── modules/
│   │   │   ├── ecs/
│   │   │   ├── rds/
│   │   │   ├── redis/
│   │   │   ├── s3/
│   │   │   └── vpc/
│   │   ├── environments/
│   │   │   ├── staging/
│   │   │   └── production/
│   │   └── main.tf
│   └── docker/
│       ├── Dockerfile.web
│       ├── Dockerfile.api
│       └── docker-compose.yml
│
├── .github/
│   └── workflows/
│       ├── ci.yml                    # Lint + test + build
│       ├── deploy-staging.yml
│       ├── deploy-production.yml
│       └── db-migrate.yml
│
├── docs/
│   ├── api/                          # API documentation
│   │   ├── authentication.md
│   │   ├── products.md
│   │   ├── orders.md
│   │   ├── payments.md
│   │   └── webhooks.md
│   ├── architecture/
│   │   ├── overview.md
│   │   ├── database-schema.md
│   │   └── deployment.md
│   └── runbooks/
│       ├── incident-response.md
│       ├── database-recovery.md
│       └── deployment-rollback.md
│
├── scripts/
│   ├── setup.sh                      # Initial project setup
│   ├── seed-db.sh                    # Database seeding
│   ├── generate-types.sh             # Generate API types
│   └── cleanup-images.sh             # S3 image cleanup
│
├── turbo.json                        # Turborepo configuration
├── pnpm-workspace.yaml
├── package.json
├── .env.example
├── .eslintrc.js
├── .prettierrc
└── CLAUDE.md                         # This file
```

## Development Setup

### Prerequisites
- Node.js 20 LTS (use nvm: `nvm use`)
- pnpm 8.x (`npm install -g pnpm`)
- Docker Desktop (for PostgreSQL and Redis)
- Stripe CLI (for webhook testing)

### Initial Setup

```bash
# Clone and install
git clone git@github.com:shopflow/shopflow.git
cd shopflow
pnpm install

# Start infrastructure
docker compose up -d

# Setup environment variables
cp .env.example .env.local
# Edit .env.local with your API keys (see Environment Variables section)

# Run database migrations
pnpm --filter api db:migrate

# Seed the database
pnpm --filter api db:seed

# Start development servers
pnpm dev
```

### Available Scripts

```bash
# Development
pnpm dev                    # Start all apps in development mode
pnpm dev:web                # Start only frontend (port 5173)
pnpm dev:api                # Start only backend (port 3001)

# Building
pnpm build                  # Build all packages
pnpm build:web              # Build frontend only
pnpm build:api              # Build backend only

# Testing
pnpm test                   # Run all tests
pnpm test:web               # Run frontend tests
pnpm test:api               # Run backend tests
pnpm test:e2e               # Run Playwright E2E tests
pnpm test:coverage          # Run tests with coverage

# Database
pnpm --filter api db:migrate        # Run pending migrations
pnpm --filter api db:migrate:create  # Create new migration
pnpm --filter api db:seed            # Seed database
pnpm --filter api db:studio          # Open Drizzle Studio
pnpm --filter api db:reset           # Drop and recreate (DANGER!)

# Code Quality
pnpm lint                   # ESLint across all packages
pnpm lint:fix               # Auto-fix lint issues
pnpm format                 # Prettier format
pnpm typecheck              # TypeScript type checking
pnpm storybook              # Start Storybook

# Stripe
pnpm stripe:listen          # Start Stripe webhook forwarding
pnpm stripe:trigger         # Trigger test webhook events

# Docker
docker compose up -d        # Start PostgreSQL + Redis
docker compose down         # Stop infrastructure
docker compose logs -f      # Follow logs
```

## Environment Variables

### Required Variables (`.env.local`)

```
# Database
DATABASE_URL=postgresql://shopflow:shopflow@localhost:5432/shopflow_dev

# Redis
REDIS_URL=redis://localhost:6379

# Authentication
JWT_SECRET=your-jwt-secret-min-32-chars
JWT_REFRESH_SECRET=your-refresh-secret-min-32-chars
SESSION_SECRET=your-session-secret

# Stripe
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# SendGrid
SENDGRID_API_KEY=SG....
SENDGRID_FROM_EMAIL=noreply@shopflow.example.com

# Algolia
ALGOLIA_APP_ID=...
ALGOLIA_API_KEY=...
ALGOLIA_SEARCH_KEY=...

# Cloudinary
CLOUDINARY_CLOUD_NAME=...
CLOUDINARY_API_KEY=...
CLOUDINARY_API_SECRET=...

# S3
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1
S3_BUCKET_NAME=shopflow-assets

# Sentry
SENTRY_DSN=https://...
SENTRY_ENVIRONMENT=development

# Feature Flags
LAUNCHDARKLY_SDK_KEY=sdk-...

# OAuth
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
GITHUB_CLIENT_ID=...
GITHUB_CLIENT_SECRET=...
```

## Architecture Decisions

### Why we migrated from Redux to Zustand (February 2024)
The original Redux setup had 47 action types, 23 reducers, and required an average of 5 files to add a new state slice. After measuring, we found that 80% of our Redux usage was just server state caching, which TanStack Query handles better. The remaining client state (auth, cart, UI) fits naturally into 4 small Zustand stores totaling ~200 lines. Migration was done over 2 sprints. DO NOT add Redux back.

### Why we migrated from Prisma to Drizzle (April 2024)
Prisma's query engine was adding 300ms cold start penalty on AWS Lambda (we were on Lambda before ECS). Even after moving to ECS, Prisma's generated client was 8MB and type generation took 45 seconds. Drizzle gives us SQL-like syntax with full type safety, zero runtime overhead, and instant type generation. The migration took 3 weeks. All new database code MUST use Drizzle. Legacy Prisma code in `apps/api/src/db/legacy/` should be migrated when touched. NOTE: If you find any remaining Prisma imports, convert them to Drizzle.

### Why Express over Fastify/Hono (Decision: Keep Express)
We evaluated Fastify and Hono in Q3 2024. While Fastify showed 2x throughput in benchmarks, our bottleneck is PostgreSQL queries, not HTTP handling. Express has better middleware ecosystem compatibility (Passport, Bull Board, Socket.io integration). The team is experienced with Express. We'll revisit if HTTP handling becomes a bottleneck (unlikely before 100K concurrent users). DO NOT migrate to a different HTTP framework without team consensus.

### Authentication Architecture
We use a dual-token strategy:
- Access tokens (JWT, 15-minute expiry) stored in memory (Zustand `authStore`)
- Refresh tokens (opaque, 7-day expiry) stored in HTTP-only secure cookies
- OAuth2 (Google, GitHub) handled server-side through Passport.js
- CSRF protection via double-submit cookie pattern
- Rate limiting: 5 failed login attempts per IP per 15 minutes

### Payment Processing
All payment logic goes through `apps/api/src/services/payment.service.ts`. We use Stripe Payment Intents API for card payments. Important rules:
- NEVER store raw card numbers anywhere in our system
- Always use Stripe Elements on the frontend
- Webhook verification is mandatory (check `stripe-signature` header)
- All payment-related errors must be logged to Sentry with `payment` tag
- Refunds must go through the admin API, never directly through Stripe dashboard
- Currency is stored in cents (integer) to avoid floating-point issues

### Image Handling
Product images follow this pipeline:
1. Upload to S3 via pre-signed URL (generated by `POST /api/images/upload-url`)
2. S3 event triggers Bull job for processing
3. Job generates 4 variants: thumbnail (150x150), small (300x300), medium (600x600), large (1200x1200)
4. Variants stored in S3 under `products/{productId}/{variant}.webp`
5. CloudFront serves images with automatic format negotiation

### Search
Product search is delegated to Algolia. The sync flow:
1. Product CRUD operations publish events to Bull queue
2. `search.job.ts` processes events and syncs to Algolia index
3. Frontend uses Algolia InstantSearch React for search UI
4. Fallback to PostgreSQL full-text search if Algolia is unreachable

## API Conventions

### Route Structure
All API routes follow RESTful conventions:
```
GET    /api/v1/products          # List products (paginated)
GET    /api/v1/products/:id      # Get single product
POST   /api/v1/products          # Create product (admin)
PATCH  /api/v1/products/:id      # Update product (admin)
DELETE /api/v1/products/:id      # Soft delete product (admin)

GET    /api/v1/orders            # List user's orders
GET    /api/v1/orders/:id        # Get order details
POST   /api/v1/orders            # Create order from cart

POST   /api/v1/cart/items        # Add item to cart
PATCH  /api/v1/cart/items/:id    # Update quantity
DELETE /api/v1/cart/items/:id    # Remove item
```

### Response Format
All API responses use this envelope:
```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "page": 1,
    "pageSize": 20,
    "total": 150,
    "totalPages": 8
  }
}
```

Error responses:
```json
{
  "success": false,
  "error": {
    "code": "PRODUCT_NOT_FOUND",
    "message": "Product with ID abc123 not found",
    "details": []
  }
}
```

### Pagination
Use cursor-based pagination for large datasets (products, orders):
```
GET /api/v1/products?cursor=abc123&limit=20&sort=createdAt&order=desc
```
Offset-based pagination only for admin dashboard tables:
```
GET /api/v1/admin/customers?page=1&pageSize=50
```

### Validation
All request bodies are validated using Zod schemas defined in `packages/shared/src/validators/`. The `validation.middleware.ts` middleware automatically validates and returns 400 errors for invalid requests. When adding a new endpoint:
1. Define the Zod schema in `packages/shared`
2. Import and apply via `validate(schema)` middleware
3. The validated body is available as `req.validated` (typed)

## Database Conventions

### Schema Rules
- All tables use UUID primary keys (`id` column, generated by `gen_random_uuid()`)
- All tables have `createdAt` and `updatedAt` timestamps
- Soft deletes: `deletedAt` nullable timestamp (never hard delete user-facing data)
- Money columns use `integer` type (cents), with display formatting in the frontend
- Boolean columns are prefixed: `isActive`, `isPublished`, `hasShipping`
- JSON columns only for truly schemaless data (user preferences, metadata)
- Foreign keys always have `ON DELETE` behavior explicitly defined
- Indexes: always index foreign keys, frequently filtered columns, and sort columns
- Table names are snake_case plural: `products`, `order_items`, `user_addresses`
- Column names are camelCase in Drizzle schema, snake_case in PostgreSQL

### Migration Rules
- Migrations must be reversible (include `down` migration)
- Never modify existing migration files — create new ones
- Data migrations go in separate files from schema migrations
- Destructive operations (column drops, table drops) require a 2-step process:
  1. First migration: mark as deprecated, add new column/table if needed
  2. Second migration (after deployment): remove old column/table
- Test migrations on a copy of production data before deploying

### Query Patterns
- Use Drizzle's query builder for all database access
- Complex queries should be in the service layer, not controllers
- Always use transactions for multi-table writes:
```typescript
await db.transaction(async (tx) => {
  await tx.insert(orders).values(orderData);
  await tx.update(inventory).set({ quantity: sql`quantity - ${qty}` });
});
```
- Use `prepared` statements for frequently executed queries
- N+1 queries are forbidden — use `with` (eager loading) or explicit joins

## Testing Strategy

### Unit Tests (`*.test.ts`)
- Located next to source files or in `tests/unit/`
- Mock external services (Stripe, SendGrid, Algolia)
- Use `vi.mock()` for module mocking
- Test business logic in services, not HTTP handlers
- Coverage target: 80% for services, 60% overall

### Integration Tests (`*.integration.test.ts`)
- Located in `tests/integration/`
- Use real PostgreSQL (Docker test container via `testcontainers`)
- Use real Redis (Docker test container)
- Mock only external APIs (Stripe, SendGrid)
- Each test file gets a fresh database with migrations applied
- Test the full request-response cycle through Express

### E2E Tests (`tests/e2e/`)
- Playwright tests against running dev servers
- Test critical user flows: browse → add to cart → checkout → order confirmation
- Run in CI against staging environment
- Visual regression tests for key pages

### Test Data
- Factory functions in `tests/fixtures/factories.ts`
- Use `faker` for generating realistic test data
- Seed scripts in `apps/api/src/db/seeds/`
- NEVER use production data in tests

## Code Style & Conventions

### General
- Strict TypeScript: `"strict": true`, no `any` types (use `unknown` + type guards)
- Prefer `const` over `let`, never use `var`
- Use early returns to avoid deep nesting
- Maximum function length: ~50 lines (extract helpers if longer)
- File naming: `camelCase.ts` for utilities, `PascalCase.tsx` for React components
- Export: prefer named exports over default exports (except for pages)
- Comments: only for WHY, not WHAT. The code should be self-documenting.
- No `console.log` in production code — use the Winston logger on backend, remove from frontend

### React Conventions
- Functional components only (no class components)
- Custom hooks for any logic reused across 2+ components
- Component files: one component per file, named same as component
- Props interface: named `{ComponentName}Props`, defined in same file
- Use `React.memo()` only when profiling shows actual re-render issues
- Avoid `useEffect` for derived state — compute during render
- Use `Suspense` + `lazy()` for route-level code splitting
- Error boundaries at route level and around critical sections
- Accessibility: all interactive elements must have proper ARIA labels

### Express Conventions
- Controllers are thin — delegate to services
- Services contain business logic and database calls
- Middleware for cross-cutting concerns only
- Use `express-async-errors` to avoid try-catch in every handler
- Custom error classes extend `AppError` (in `lib/errors.ts`)
- All routes must have authentication middleware unless explicitly public
- Rate limiting on all mutation endpoints

### Git Conventions
- Branch naming: `feature/SF-123-short-description`, `fix/SF-456-bug-name`
- Commit messages: conventional commits format
  - `feat(cart): add quantity validation`
  - `fix(orders): handle null shipping address`
  - `chore(deps): update stripe to 14.x`
- PR requirements:
  - Must pass CI (lint + tests + build)
  - At least 1 review approval
  - No `console.log` or `debugger` statements
  - Database migrations must be reviewed by a senior engineer
  - Breaking API changes require API version bump

## Important Gotchas & Known Issues

### Cart Race Condition (CRITICAL)
There's a known race condition when two tabs update the same cart simultaneously. The cart uses optimistic updates in Zustand, and the server-side cart uses `SELECT FOR UPDATE` to prevent inventory overselling. If you're working on cart logic, always test with concurrent requests. See `apps/api/src/services/cart.service.ts:L45-L80` for the locking mechanism. TODO: Implement event sourcing for cart state (Q2 2025 roadmap).

### Stripe Webhook Idempotency
Stripe can send the same webhook event multiple times. All webhook handlers MUST be idempotent. We use the `stripe_event_id` column in the `webhook_events` table to deduplicate. Check before processing:
```typescript
const existing = await db.select().from(webhookEvents).where(eq(webhookEvents.stripeEventId, event.id));
if (existing.length > 0) return; // Already processed
```

### Image Upload Memory Issues
Large image uploads (>10MB) can cause memory spikes. The upload endpoint uses streaming with `busboy` instead of `multer`. Do not switch back to `multer` for product image uploads. The pre-signed URL approach (client uploads directly to S3) is preferred for all new image upload features.

### PostgreSQL Connection Pooling
The connection pool is configured for 20 max connections in development, 100 in production. If you see `ECONNREFUSED` errors locally, check that PostgreSQL is running and the pool isn't exhausted. Common cause: forgetting to release connections in error paths. The Drizzle client handles this automatically, but any raw `pg` usage must manage connections manually.

### Redis Session Timeout
Sessions expire after 7 days of inactivity. The refresh token rotation happens automatically via the `authMiddleware`. If a user reports being logged out unexpectedly, check Redis for the session key `session:{userId}:{sessionId}`. Known issue: clock skew between application servers can cause premature session expiration in ECS (mitigated by NTP sync).

### Algolia Index Sync Lag
After a product update, there can be a 2-5 second delay before the change appears in search results. This is expected behavior. The admin dashboard shows a "syncing" indicator. If sync fails, events are retried 3 times with exponential backoff. Check `apps/api/src/jobs/search.job.ts` for the retry logic.

### Feature Flag Dependency
Some features are behind LaunchDarkly flags. Key flags:
- `enable-b2b-pricing`: B2B wholesale pricing (in beta)
- `new-checkout-flow`: Redesigned checkout (A/B test)
- `enable-reviews`: Product reviews feature (rolled out 80%)
- `dark-mode`: Dark theme support (100% rolled out, flag can be removed)
If LaunchDarkly is unreachable, all flags default to `false`. This means B2B pricing and reviews will be hidden if LD is down. This is intentional — fail closed.

### Timezone Handling
All timestamps in the database are stored in UTC. The frontend converts to user's local timezone for display. NEVER use `new Date()` on the server without explicitly handling timezone. Use `dayjs.utc()` for all server-side date operations. The `createdAt`/`updatedAt` columns use `timestamp with time zone` in PostgreSQL.

### Soft Delete Gotcha
Most queries automatically filter out soft-deleted records via a Drizzle global filter. However, admin queries intentionally include deleted records (for audit). If you're writing a new query and records seem to be "missing", check if they were soft-deleted. Use `.where(isNull(table.deletedAt))` explicitly if you want to be extra clear.

## Performance Guidelines

### Frontend
- Bundle size budget: 200KB gzipped for initial load
- Lazy load all routes except home and product listing
- Use `React.memo` only when React DevTools Profiler confirms unnecessary re-renders
- Image optimization: use `<img loading="lazy">` and responsive `srcSet`
- TanStack Query staleTime: 5 minutes for product data, 0 for cart data
- Debounce search input (300ms) using `useDebounce` hook

### Backend
- API response time target: p95 < 200ms for reads, p95 < 500ms for writes
- Use Redis caching for:
  - Product catalog (15-minute TTL)
  - Category tree (1-hour TTL)
  - User sessions (7-day TTL)
- Database query timeout: 5 seconds (configured in Drizzle)
- Use database indexes for all WHERE clause columns
- Batch operations for bulk inserts/updates (e.g., inventory sync)
- Connection pooling: reuse connections, never create per-request

### Monitoring
- DataDog APM traces all HTTP requests
- Custom metrics: checkout conversion rate, payment success rate, search latency
- Alerts: p95 latency > 1s, error rate > 1%, queue depth > 1000
- Weekly performance review meeting (Thursday 2pm)

## Deployment

### Staging
- Auto-deploys from `develop` branch
- URL: https://staging.shopflow.example.com
- Uses production-like data (anonymized)
- Stripe test mode

### Production
- Deploys from `main` branch via manual GitHub Actions trigger
- Requires 2 approvals on the deployment PR
- Blue-green deployment via ECS
- Database migrations run automatically before deployment
- Rollback: re-deploy previous ECS task definition
- Post-deploy: verify health check, check DataDog for error spikes

### Deployment Checklist
1. All tests passing on CI
2. No `TODO` or `FIXME` in changed files
3. Database migration tested on staging
4. Feature flags configured in LaunchDarkly
5. Runbook updated if new failure modes introduced
6. On-call engineer notified for major changes

## Quick Reference for Common Tasks

### Adding a New API Endpoint
1. Define Zod schema in `packages/shared/src/validators/`
2. Add route in `apps/api/src/routes/{resource}.routes.ts`
3. Create controller method in `apps/api/src/controllers/`
4. Implement business logic in `apps/api/src/services/`
5. Add integration test in `apps/api/tests/integration/`
6. Update API docs in `docs/api/`

### Adding a New Database Table
1. Create schema in `apps/api/src/db/schema/{table}.ts`
2. Export from `apps/api/src/db/schema/index.ts`
3. Generate migration: `pnpm --filter api db:migrate:create`
4. Review generated SQL, add indexes
5. Add seed data if needed
6. Create types in `packages/shared/src/types/`

### Adding a New React Page
1. Create page component in `apps/web/src/pages/{section}/`
2. Add route in `apps/web/src/Router.tsx`
3. Create any needed API functions in `apps/web/src/api/`
4. Add TanStack Query hooks if data fetching needed
5. Write Storybook stories for key components
6. Add E2E test for critical user flows

### Adding a New Background Job
1. Create job processor in `apps/api/src/jobs/{name}.job.ts`
2. Register in Bull queue setup (`apps/api/src/lib/queues.ts`)
3. Add to Bull Board for monitoring
4. Implement retry logic and dead letter handling
5. Add integration test with mock queue

## Team Contacts

- **Tech Lead**: Sarah Chen (sarah@shopflow.example.com) — architecture decisions
- **Frontend Lead**: Marcus Kim — React patterns, component library
- **Backend Lead**: Priya Patel — API design, database schema
- **DevOps**: Jake Morrison — deployment, infrastructure, monitoring
- **Product**: Lisa Wang — feature requirements, prioritization

## Frequently Asked Questions

### Q: Why can't I find the Redux store?
A: We migrated to Zustand in February 2024. See "Architecture Decisions" section above.

### Q: How do I test Stripe webhooks locally?
A: Run `pnpm stripe:listen` in a separate terminal. This forwards Stripe events to your local server. The webhook secret is auto-generated — check the terminal output.

### Q: Why are my database queries returning empty results?
A: Probably soft deletes. Check if the records have `deletedAt` set. Use Drizzle Studio (`pnpm --filter api db:studio`) to inspect.

### Q: How do I add a new feature flag?
A: Create the flag in LaunchDarkly dashboard, then use `useFeatureFlag('flag-name')` in React or `featureFlags.isEnabled('flag-name')` in Express.

### Q: The E2E tests are flaky. What should I do?
A: Common causes: (1) test data not cleaned up, (2) animation timing, (3) network timing. Use `page.waitForResponse()` instead of fixed timeouts. Check Playwright traces in CI artifacts.

### Q: How do I run just one test file?
A: `pnpm --filter api test -- --run path/to/test.ts` or `pnpm --filter web test -- --run path/to/test.tsx`

## Change Log

### 2024-12-15: Updated Stripe API version
- Migrated from 2023-10-16 to 2024-01-01
- Updated Payment Intents flow for new SCA requirements
- See PR #456 for details

### 2024-11-01: Added B2B pricing module
- New feature behind `enable-b2b-pricing` flag
- Added `pricing_tiers` and `customer_groups` tables
- New admin routes for managing wholesale pricing

### 2024-10-15: Migrated to ECS Fargate
- Moved from AWS Lambda to ECS Fargate
- Eliminated cold start issues
- New deployment workflow in `.github/workflows/`

### 2024-09-01: Added product reviews
- Behind `enable-reviews` feature flag
- New `reviews` table with star ratings and text
- Moderation queue in admin dashboard

### 2024-08-15: Search migration to Algolia
- Replaced PostgreSQL full-text search with Algolia
- Added InstantSearch UI components
- Background sync job for keeping index updated

### 2024-07-01: Image processing pipeline
- Moved from client-side resize to server-side processing
- S3 + CloudFront for serving optimized images
- WebP format with JPEG fallback

### 2024-06-01: Redis caching layer
- Added Redis caching for product catalog
- Session management moved from PostgreSQL to Redis
- Cache invalidation on product updates

### 2024-04-01: Prisma to Drizzle migration
- Replaced Prisma with Drizzle ORM
- Eliminated 300ms cold start penalty
- See "Architecture Decisions" section

### 2024-02-01: Redux to Zustand migration
- Replaced Redux with Zustand for client state
- TanStack Query for server state
- See "Architecture Decisions" section
