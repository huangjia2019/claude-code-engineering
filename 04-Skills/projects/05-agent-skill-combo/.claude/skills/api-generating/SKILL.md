---
name: api-generating
description: Generate API endpoint documentation from Express route files. Use when the user asks to generate, update, or review API docs for Express.js routes.
allowed-tools: [Read, Grep, Glob, Write, Bash(python *)]
---

# API 文档生成 Skill

## 工作流程 — MANDATORY

**IMPORTANT**: You MUST follow these steps in order. DO NOT skip or substitute any step.

### Step 1: Route Discovery（路由发现）

**You MUST use the Python script for route detection:**

```bash
python3 skills/scripts/detect-routes.py src/
```

DO NOT manually search for routes using Grep — the script handles edge cases
(dynamic routes, middleware-mounted sub-routers, re-exported routes) that Grep
patterns will miss.

### Step 2: Route Analysis（路由分析）

For each route discovered by the script:

1. Read the route handler source file
2. Identify: HTTP method, path, parameters, request body schema, response schema
3. Check for authentication middleware (e.g., `requireAuth`, `isAdmin`)
4. Check for validation middleware (e.g., `validate(schema)`)

### Step 3: Documentation Generation（文档生成）

Use the template at `templates/api-doc.md` to generate documentation.

**Output rules:**
- One markdown file per route group (e.g., `docs/api/users.md`)
- Include request/response examples
- Mark authenticated endpoints with 🔒

## Reference Files

- Route detection script: `scripts/detect-routes.py`
- Documentation template: `templates/api-doc.md`
- Express routing patterns: see PATTERNS.md (same directory)

## Quality Checklist

Before finishing, verify:
- [ ] All routes from script output are documented
- [ ] Request/response schemas match actual code
- [ ] Auth requirements are marked
- [ ] Examples are valid JSON
