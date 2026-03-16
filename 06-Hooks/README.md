# 第 16 讲：令行禁止 · Hooks 事件驱动自动化

> Claude Code 每次调用工具，都会触发一个事件。Hooks 让你在这些事件上挂载自己的逻辑——审计、拦截、自动格式化，甚至阻止危险操作。

---

## 你将学到

- Hooks 的事件模型：`PreToolUse` / `PostToolUse` / `Stop` / `SubAgentStop`
- 安全钩子：危险命令拦截、敏感文件保护、操作审计日志
- 质量钩子：自动格式化、Lint 检查、测试守卫
- Hooks 与 Commands、Skills、MCP 的协同

## 配套项目

```
projects/
├── 01-safety-hooks/     # 安全三件套：拦截 + 保护 + 审计
│   ├── hooks/
│   │   ├── block-dangerous.sh
│   │   ├── protect-files.sh
│   │   └── audit-log.sh
│   └── .claude/settings.json
│
└── 02-quality-hooks/    # 质量三件套：格式化 + Lint + 测试
    ├── hooks/
    │   ├── auto-format.sh
    │   ├── lint-check.sh
    │   └── run-tests.sh
    └── .claude/settings.json
```

## 一句话预告

> **没有 Hooks 的 Claude Code 是信任；有了 Hooks 的 Claude Code 是信任但核实。**
