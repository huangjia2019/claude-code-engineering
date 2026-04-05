---
description: Staging/production deployment process, checklist, and rollback
globs: .github/workflows/**/*.yml
---

## Environments
- **Staging**: auto-deploy from `develop`. Stripe test mode. Anonymized prod data.
- **Production**: manual trigger from `main`. Blue-green ECS. 2 approvals.

## Pre-deploy Checklist
1. All tests passing.
2. No `TODO`/`FIXME` in changed files.
3. Migrations tested on staging.
4. Feature flags configured.
5. Runbook updated for new failure modes.
6. On-call notified for major changes.

## Rollback
- ECS: re-deploy previous task definition.
- Database: run reverse migration.
- Feature flags: kill switch via LaunchDarkly.
- Post-rollback: incident report within 24 hours.
