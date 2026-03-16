# 第 15-16 讲：未雨绸缪 & 步步为营 · Hooks 事件驱动自动化

> 在 Claude 执行工具前后插入自定义检查——自动格式化、敏感词拦截、质量门控。第 15 讲打基础，第 16 讲进阶到 Stop Hook、SubAgent 事件验收和三维决策框架。

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
