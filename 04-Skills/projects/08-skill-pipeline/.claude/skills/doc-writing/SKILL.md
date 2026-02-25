---
name: doc-writing
description: Generate API documentation from a route manifest. Use when you have a list of discovered routes and need to produce markdown documentation.
allowed-tools: [Read, Write, Glob]
---

# Doc Writing Skill

Generate structured API documentation from a route manifest.

## Input

You will receive a route manifest (JSON array) from the previous pipeline stage.
Each entry contains: method, path, file, line, middleware, type.

## Process

### Step 1: Read Source Code

For each route in the manifest, read the source file to understand:
- Request parameters (path, query, body)
- Response format
- Error handling
- Business logic summary

### Step 2: Generate Documentation

Use the template at `templates/endpoint-doc.md` for each route group.

Group routes by their source file (e.g., all product routes together).

### Step 3: Write Files

Write one markdown file per route group to the `docs/` directory:
- `docs/products-api.md`
- `docs/categories-api.md`
- etc.

## Output

Return a manifest of generated documentation files:

```json
{
  "files_generated": ["docs/products-api.md", "docs/categories-api.md"],
  "routes_documented": 8,
  "routes_skipped": [],
  "warnings": []
}
```

This manifest will be consumed by the next pipeline stage (quality-checking).
