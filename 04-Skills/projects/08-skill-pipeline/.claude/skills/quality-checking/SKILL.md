---
name: quality-checking
description: Validate API documentation against quality standards. Use when you need to verify generated docs are complete and correct.
allowed-tools: [Read, Grep, Glob]
---

# Quality Checking Skill

Validate generated API documentation against quality standards.

## Input

You will receive a documentation manifest from the previous pipeline stage,
listing generated files and documented routes.

## Process

### Step 1: Load Quality Rules

Read the rules at `rules/doc-standards.md` for the complete checklist.

### Step 2: Check Each Documentation File

For each generated doc file, verify:

1. **Completeness**: Every route from the scanner manifest is documented
2. **Structure**: Each endpoint has method, path, description, parameters, responses
3. **Auth markers**: Endpoints with auth middleware have 🔒 markers
4. **Examples**: Request/response examples are valid JSON
5. **Consistency**: All files follow the same format

### Step 3: Cross-Reference with Source

For each documented endpoint, spot-check against the source file:
- Does the documented path match the actual route?
- Are the middleware requirements correctly noted?
- Are the response codes accurate?

## Output Format

Return a quality report:

```markdown
# Documentation Quality Report

## Score: {PASS / NEEDS_REVISION}

## Coverage
- Routes in manifest: {N}
- Routes documented: {N}
- Coverage: {percentage}%

## Issues Found
{list each issue with file, line, and description}

## Verdict
{PASS: all checks passed / NEEDS_REVISION: list what needs fixing}
```
