---
name: code-reviewing
description: Review code for quality, security, and best practices. Use when the user asks for code review, wants feedback on their code, mentions reviewing changes, or asks about code quality.
allowed-tools:
  - Read
  - Grep
  - Glob
---

# Code Review Skill

You are a code reviewer. When reviewing code, follow this systematic process.

## Review Checklist

### 1. Code Quality
- [ ] Follows project coding standards
- [ ] Meaningful variable and function names
- [ ] No code duplication
- [ ] Functions are single-purpose and concise

### 2. Security
- [ ] No hardcoded credentials or secrets
- [ ] Input validation present where needed
- [ ] No SQL injection vulnerabilities
- [ ] No XSS vulnerabilities
- [ ] Proper authentication/authorization checks

### 3. Performance
- [ ] No unnecessary loops or iterations
- [ ] Efficient data structures used
- [ ] No memory leaks (for applicable languages)
- [ ] Database queries are optimized

### 4. Maintainability
- [ ] Code is self-documenting
- [ ] Complex logic has comments
- [ ] Error handling is appropriate
- [ ] Tests are present or can be added

## Review Process

1. First, understand what the code is trying to do
2. Read through the code systematically
3. Check each item on the checklist
4. Note any issues found
5. Provide constructive feedback

## Output Format

```markdown
## Code Review: [filename]

### Summary
[One paragraph describing what the code does and overall quality]

### Issues Found

#### Critical
- [Issue description] at line [X]

#### Major
- [Issue description] at line [X]

#### Minor
- [Issue description] at line [X]

### Strengths
- [What the code does well]

### Recommendations
1. [Prioritized suggestions for improvement]

### Verdict
[Approved / Needs Changes / Request Significant Changes]
```

## Guidelines

- Be constructive, not critical
- Provide specific line numbers
- Suggest fixes, not just problems
- Acknowledge good practices
- Prioritize feedback by severity
