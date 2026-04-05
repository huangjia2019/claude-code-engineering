---
description: React component patterns, state management, hooks, styling, and accessibility rules
globs: apps/web/src/**/*.{ts,tsx}
---

## Component Structure
- Functional components ONLY. No class components.
- One component per file, file name = component name (PascalCase.tsx).
- Props interface: `{ComponentName}Props`, defined in same file.
- Named exports only (exception: page components for lazy loading).

## State Management
- Zustand for client state (auth, cart, UI). TanStack Query for server state.
- DO NOT add Redux or MobX.
- Zustand stores in `apps/web/src/stores/`. Max 4 stores.
- Never put server-fetched data in Zustand.
- TanStack Query staleTime: 5min products, 0 cart, 1hr categories.

## Hooks
- Custom hooks for logic reused in 2+ components.
- `apps/web/src/hooks/use{Name}.ts`.
- Never call hooks conditionally or inside callbacks.
- Avoid `useEffect` for derived state — compute inline.

## Performance
- `React.memo()` only when Profiler confirms wasted re-renders.
- `Suspense` + `lazy()` for route-level code splitting.
- Images: `loading="lazy"` + responsive `srcSet`.
- Debounce search: 300ms via `useDebounce`.
- Bundle budget: 200KB gzipped initial.

## Styling
- Tailwind CSS only. No CSS modules, styled-components, or inline styles.
- `cn()` utility for conditional class merging.
- Mobile-first responsive: `sm:` → `md:` → `lg:`.
- All new components must support dark mode (`dark:` variant).
- Design tokens in `tailwind.config.ts`.

## Forms
- React Hook Form + Zod. No Formik.
- Zod schemas in `packages/shared/src/validators/`.
- Inline error messages with `aria-describedby`.
- Disabled submit during submission + loading indicator.

## Accessibility
- ARIA labels on all interactive elements.
- WCAG AA contrast (4.5:1 text, 3:1 large).
- Meaningful `alt` text. Modal: focus trap + Escape.
- Screen reader test before merging a11y PRs.

## Error Handling
- Error boundaries at route level and critical sections.
- User-friendly messages displayed, technical details to Sentry.
- Network errors: retry button with exponential backoff.
