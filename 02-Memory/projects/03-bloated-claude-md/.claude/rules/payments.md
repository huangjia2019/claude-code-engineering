---
description: Stripe integration rules, webhook idempotency, currency handling
globs: apps/api/src/**/*payment*
---

- ALL payment logic through `payment.service.ts`. No direct Stripe calls elsewhere.
- Stripe Payment Intents API for cards.
- NEVER store raw card numbers. Frontend: Stripe Elements only.
- Webhook: verify `stripe-signature` header.
- Idempotent handlers: deduplicate via `webhook_events.stripe_event_id`.
- Currency: integer cents. No floating-point money.
- Refunds: admin API only, not Stripe dashboard.
- Errors: Sentry with `payment` tag.
