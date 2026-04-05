---
description: TypeScript strict mode, type safety, and naming conventions
globs: "**/*.{ts,tsx}"
---

- `"strict": true` in all tsconfig files. No exceptions.
- NEVER use `any`. Use `unknown` + type guards.
- Shared types in `packages/shared/src/types/`.
- `const` over `let`. Never `var`.
- Discriminated unions for complex state (not boolean flags).
- Exhaustive switch with `never` type.
- No `as` assertions (except test code with comment).
- Always constrain generics: `<T extends Base>`.
- Use `Pick`, `Omit`, `Partial`, `Required` over manual types.
- Prefer `as const` objects over TypeScript enums.
- No magic numbers — named constants.
- No nested ternaries.
- Destructure props and parameters.
- `async/await` over raw Promises. Never mix.
- Max function: ~50 lines.
- Comments: WHY not WHAT.
