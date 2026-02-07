# CLAUDE.md — Claude Code 工程化实战

## Project Overview

This is the companion repository for the GeekTime (极客时间) course **"Claude Code 工程化实战"** — a comprehensive course teaching developers to advance from Claude Code users to Agent builders. All documentation is written in Chinese (zh-CN).

**Course URL:** https://time.geekbang.org/column/intro/101113501

## Repository Structure

```
├── 01-Introduction/          # Course intro and tech stack overview
├── 02-Memory/                # CLAUDE.md memory system (2 projects)
│   └── projects/
│       ├── 01-web-app/       # React 18 + TypeScript e-commerce frontend
│       └── 02-api-service/   # Node.js/Fastify/Prisma order microservice
├── 03-SubAgents/             # Sub-agent architecture (5 projects)
│   └── projects/
│       ├── 01-code-reviewer/ # Read-only security auditor
│       ├── 02-test-runner/   # Test execution + summarization
│       ├── 03-log-analyzer/  # Log parsing and error extraction
│       ├── 04-parallel-explore/ # Multi-threaded investigation
│       └── 05-bugfix-pipeline/  # Chained agents pipeline
├── 04-Skills/                # Skills system (4 projects)
│   └── projects/
│       ├── 01-basic-skill/       # Simple code review skill
│       ├── 02-progressive-skill/ # Progressive disclosure pattern
│       ├── 03-financial-skill/   # Financial analysis with Python scripts
│       └── 04-api-generator/     # Multi-framework API generation
├── 05-Commands/              # Slash commands (2 projects)
│   └── projects/
│       ├── 01-basic-commands/    # /commit, /review, /explain, /todo
│       └── 02-advanced-commands/ # /pr:create, /analyze, /safe:deploy
├── 06-Hooks/                 # Event-driven automation (coming soon)
├── 07-MCP/                   # MCP protocol integration (coming soon)
├── 08-Headless/              # CI/CD & headless mode (coming soon)
├── 09-Agent-SDK/             # Agent SDK programming (coming soon)
├── 10-Plugins/               # Plugin packaging & distribution (coming soon)
├── 91-Pictures/              # Course promotional images
└── .claude/                  # Claude Code project settings
```

## Section Status

| Section | Status | Projects |
|---------|--------|----------|
| 01-Introduction | Complete | — |
| 02-Memory | Complete | 2 projects |
| 03-SubAgents | Complete | 5 projects |
| 04-Skills | Complete | 4 projects |
| 05-Commands | Complete | 2 projects |
| 06-Hooks | Placeholder | Coming soon |
| 07-MCP | Placeholder | Coming soon |
| 08-Headless | Placeholder | Coming soon |
| 09-Agent-SDK | Placeholder | Coming soon |
| 10-Plugins | Placeholder | Coming soon |

## Content Conventions

### Section Layout
Each completed section follows this pattern:
```
XX-SectionName/
├── README.md (or readme.txt)   # Section overview and learning objectives
└── projects/                   # Hands-on example projects
    ├── 01-basic/               # Foundational example
    └── 0N-project-name/        # Additional examples
```

### Project Internal Layout
Individual projects contain:
```
project-name/
├── README.md                   # Project documentation
├── CLAUDE.md                   # Claude context file (in 02-Memory examples)
├── .claude/                    # Claude Code configuration
│   ├── settings.json           # Permissions and settings
│   ├── agents/                 # SubAgent definitions (.md files)
│   ├── skills/                 # Skill definitions (SKILL.md)
│   └── commands/               # Slash command definitions (.md files)
├── src/                        # Source code
├── scripts/                    # Utility scripts (Python/Bash)
├── templates/                  # Markdown templates
├── reference/                  # Reference documentation
└── tests/                      # Test files
```

## Claude Code Configuration Patterns

### Agent Definition Format (.claude/agents/*.md)
```yaml
---
name: agent-name
description: When and how to trigger this agent
tools: Read, Grep, Glob, Bash
model: haiku|sonnet|opus
---
[System prompt and instructions in Markdown]
```

### Skill Definition Format (.claude/skills/*/SKILL.md)
```yaml
---
name: skill-name
description: Auto-triggering description for LLM semantic matching
allowed-tools:
  - Read
  - Grep
  - Bash(python:*)
---
[Skill content with progressive disclosure structure]
```

### Command Definition Format (.claude/commands/*.md)
```yaml
---
description: What the command does
argument-hint: [expected arguments]
allowed-tools: Bash(git:*), Edit
model: haiku
---
[Prompt template using $ARGUMENTS or $1, $2, etc.]
```

## Technology Stacks Used in Examples

### Frontend Projects (02-Memory/01-web-app)
- React 18 + TypeScript, Vite, TanStack Query, Zustand, Tailwind CSS, React Router v6

### Backend Projects (02-Memory/02-api-service)
- Node.js 20 + TypeScript, Fastify, Prisma, PostgreSQL, Redis, Zod

### Scripts
- Python 3.10+ (financial calculations, route detection)
- Bash (OpenAPI validation)

## Naming Conventions in Example Projects

- **React components:** PascalCase (`ProductCard.tsx`)
- **Utility files:** kebab-case or camelCase (`auth.js`, `api.js`)
- **Custom hooks:** `use` prefix (`useAuth`, `useCart`)
- **TypeScript interfaces:** PascalCase with descriptive suffix (`UserProps`, `ApiResponse`)
- **Database tables:** snake_case plural (`order_items`)
- **Git commits:** `type(scope): message` (e.g., `feat(orders): add pagination`)

## Development Commands (for individual projects)

```bash
pnpm dev              # Start development server
pnpm build            # Production build
pnpm test             # Run tests
pnpm lint             # Code linting
pnpm prisma migrate   # Run database migrations (backend)
pnpm prisma generate  # Generate Prisma Client (backend)
```

## Important Notes for AI Assistants

1. **Language:** All course documentation is in Chinese (zh-CN). Maintain Chinese when editing existing content files. Use the same language as the file being edited.
2. **No root build system:** This is a course repository, not a single application. There is no root-level `package.json`, build tool, or test runner. Each project under `projects/` is self-contained.
3. **Educational intent:** Some projects intentionally include vulnerabilities (hardcoded credentials, SQL injection, XSS) as teaching examples for code review. Do not "fix" these unless explicitly asked.
4. **Sections 06-10 are placeholders:** Only `README.md` files exist in these directories. Content is forthcoming.
5. **Progressive disclosure:** Skills use a 3-tier loading strategy (index ~100 tokens → main content <5k tokens → appendices on-demand) to optimize token usage.
6. **No CI/CD:** There are no GitHub Actions workflows or CI pipelines configured.
7. **Git conventions:** Commit messages in this repository are informal (Chinese). The example projects demonstrate conventional commit format.
8. **.gitignore:** `ARCHITECTURE.md`, `**/tutorial.md`, and sections 06-10 content (except README.md) are gitignored. Planned future sections (11-16, 80-81, 90) are also ignored.

## Learning Paths

| Path | Focus | Sections |
|------|-------|----------|
| A: Quick Start | Basics & daily usage | 02 → 05 → 03 |
| B: Team Collaboration | Shared workflows | 02 → 04 → 05 → 06 → 07 |
| C: Complete | Full curriculum | All in order |
| D: Automation | CI/CD focus | 07 → 09 → 10 |

## External Resources

- [Claude Code Docs](https://code.claude.com/docs)
- [Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview)
- [MCP Protocol](https://modelcontextprotocol.io)
- [Official Skills Repository](https://github.com/anthropics/skills)
