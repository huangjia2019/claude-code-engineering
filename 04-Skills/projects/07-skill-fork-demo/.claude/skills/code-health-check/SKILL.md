---
name: code-health-check
description: Perform a comprehensive code health check on a directory. Use when the user asks to analyze code quality, find issues, or get a health report.
context: fork
agent: general-purpose
allowed-tools:
  - Read
  - Grep
  - Glob
---

# Code Health Check

Analyze the codebase at `$ARGUMENTS` and produce a structured health report.

## Checks to Perform

### 1. File Organization
- Are files reasonably sized? (Flag files > 200 lines)
- Is the directory structure logical?
- Any files that look misplaced?

### 2. Error Handling
- Are async operations wrapped in try/catch?
- Are errors propagated correctly (not swallowed)?
- Is there a global error handler?

### 3. Security Basics
- Any hardcoded secrets, API keys, or passwords?
- Any use of `eval()` or similar dangerous functions?
- Are user inputs validated before use?

### 4. Code Quality
- Any obvious code duplication (similar blocks in multiple files)?
- Any unused variables or imports?
- Are function signatures reasonable (not too many parameters)?

### 5. Dependency Hygiene
- Are all imported modules actually used?
- Any circular dependencies?

## Severity Levels

Use these to categorize issues:

| Severity | Meaning | Example |
|----------|---------|---------|
| CRITICAL | Must fix immediately | Hardcoded secrets, SQL injection |
| WARNING | Should fix soon | Missing error handling, large files |
| INFO | Nice to improve | Minor duplication, naming conventions |

## Output Format

Return a structured report in this exact format:

```markdown
# Code Health Report: {directory}

## Overall Score: {A/B/C/D/F}

## Summary
- Files analyzed: {count}
- Issues found: {critical} critical, {warning} warnings, {info} info

## Critical Issues
{list each with file:line and description}

## Warnings
{list each with file:line and description}

## Info
{list each with file:line and description}

## Recommendations
{top 3 actionable recommendations}
```
