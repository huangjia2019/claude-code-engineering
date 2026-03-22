---
name: todo
description: Add a TODO comment to code with optional priority and assignee
---

When the user runs `/todo [message]`, help them add a TODO comment.

## Behavior

1. If a file is currently open or recently edited, add the TODO there
2. Format the TODO comment appropriately for the file's language:
   - JavaScript/TypeScript: `// TODO: message`
   - Python: `# TODO: message`
   - HTML/XML: `<!-- TODO: message -->`
   - CSS: `/* TODO: message */`

3. If the message includes priority markers, format accordingly:
   - `!` → HIGH priority
   - `?` → needs discussion
   - Default → normal priority

## Examples

User: `/todo fix null check`
Result: `// TODO: fix null check`

User: `/todo ! critical security fix`
Result: `// TODO [HIGH]: critical security fix`

User: `/todo ? should we use async here`
Result: `// TODO [DISCUSS]: should we use async here`

## Guidelines

- Insert the TODO at a logical location (near related code)
- If no file context, ask the user where to add it
- Keep TODO messages concise but descriptive
