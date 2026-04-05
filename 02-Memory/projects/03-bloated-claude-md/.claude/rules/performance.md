---
description: Frontend bundle budget, backend caching, monitoring targets
globs: ""
---

## Frontend
- Bundle: 200KB gzipped initial.
- Lazy load all routes except home + product listing.
- `loading="lazy"` on below-fold images.
- Prefetch on hover for product links.
- Web Vitals: LCP < 2.5s, FID < 100ms, CLS < 0.1.

## Backend
- p95: < 200ms reads, < 500ms writes.
- Redis: products 15min, categories 1hr, sessions 7d.
- Index all filtered/sorted columns.
- Batch bulk operations.
- N+1 queries = instant PR rejection.

## Monitoring
- DataDog APM on all requests.
- Alerts: p95 > 1s, error rate > 1%, queue > 1000.
