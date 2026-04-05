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

## Rules

All coding standards and conventions are organized in `.claude/rules/`:

| Rule File | Scope |
|-----------|-------|
| `react.md` | Component structure, state management, hooks, styling, a11y |
| `express.md` | Controller/service pattern, routing, auth, logging |
| `database.md` | Schema conventions, migrations, query patterns |
| `typescript.md` | Strict mode, type safety, naming conventions |
| `testing.md` | Unit/integration/E2E strategy, coverage targets |
| `security.md` | Auth, input validation, data protection, rate limiting |
| `api-design.md` | REST conventions, pagination, versioning, response format |
| `git-workflow.md` | Branch naming, commit messages, PR requirements |
| `performance.md` | Bundle budget, caching, monitoring, Web Vitals |
| `deployment.md` | Staging/production process, checklist, rollback |
| `payments.md` | Stripe integration rules, webhook idempotency |

## Known Issues

- **Cart race condition**: `SELECT FOR UPDATE` in `cart.service.ts:L45-L80`. Test concurrent requests.
- **Algolia sync lag**: 2-5s delay after product update. Expected.
- **Redis clock skew**: NTP sync mitigates premature session expiration on ECS.
