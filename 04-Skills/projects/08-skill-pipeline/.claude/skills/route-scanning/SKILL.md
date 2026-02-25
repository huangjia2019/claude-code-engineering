---
name: route-scanning
description: Scan Express.js source files to discover all API route definitions.
allowed-tools: [Read, Grep, Glob, Bash(python3 *)]
---

# Route Scanning Skill

Discover all API route definitions in Express.js source files.

## Process

### Step 1: Run Route Scanner

Execute the scanning script:

```bash
python3 scripts/scan-routes.py <source_directory>
```

The script outputs a structured route list with method, path, file, and line number.

### Step 2: Enrich Route Data

For each discovered route, also identify:
- Middleware applied (auth, validation, etc.)
- Whether it's a standard route or chained route (`router.route()`)

### Output Format

Return a JSON-compatible route manifest:

```json
[
  {
    "method": "GET",
    "path": "/api/products",
    "file": "src/routes/products.js",
    "line": 8,
    "middleware": ["requireAuth"],
    "type": "standard"
  }
]
```

This manifest will be consumed by the next pipeline stage (doc-writing).
