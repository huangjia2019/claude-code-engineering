---
description: Branch naming, commit messages, and PR requirements
globs: ""
---

## Branches
- `feature/SF-123-short-description`
- `fix/SF-456-bug-name`
- `chore/SF-789-description`
- `hotfix/SF-999-critical-issue`

## Commits
- Conventional commits: `feat(cart): add quantity validation`
- Present tense, imperative mood.
- Subject: max 72 chars. Body: WHY not WHAT.

## PR Requirements
- CI pass (lint + tests + build).
- 1+ review approval.
- No `console.log` or `debugger`.
- DB migrations: senior engineer review.
- Breaking API: version bump.
- Max 400 lines per PR.

## Branch Protection
- `main`: 2 approvals, no force push, linear history.
- `develop`: 1 approval, no force push.
- All: CI required.
