---
name: explain
description: Explain code in simple, beginner-friendly terms
---

When the user runs `/explain [code or question]`, provide a clear explanation.

## Behavior

1. If the user provides code directly, explain that code
2. If the user asks about recent code context, explain that
3. If the user asks a concept question, explain with examples

## Explanation Style

Use the "ELI5" (Explain Like I'm 5) approach:

1. **Start simple**: Begin with a one-sentence summary
2. **Use analogies**: Compare to everyday concepts
3. **Show the flow**: Break down step by step
4. **Highlight key parts**: Point out the important bits

## Output Format

```markdown
## Quick Summary
[One sentence explanation]

## Step by Step
1. [First, this happens...]
2. [Then, this happens...]

## Analogy
[Real-world comparison if helpful]

## Key Takeaway
[The one thing to remember]
```

## Examples

User: `/explain recursion`
→ Explain recursion with a simple example like Russian dolls

User: `/explain this async function`
→ Walk through the async/await flow step by step

## Guidelines

- Assume the user is learning
- Avoid jargon, or define it when used
- Use code examples when they help
- Keep explanations concise but complete
