# 示例项目：基础 Skill

这个项目展示最简单的 Skill 结构 - 只有一个 SKILL.md 文件。

## 目录结构

```
01-basic-skill/
└── SKILL.md          # 唯一必需的文件
```

## Skill 说明

这是一个代码审查 Skill，当用户请求代码审查时 Claude 会自动激活它。

## 关键特性

### 1. 最小结构

Skill 只需要一个 SKILL.md 文件。所有指令都在这个文件中。

### 2. 有效的 description

```yaml
description: Review code for quality, security, and best practices. Use when the user asks for code review, wants feedback on their code, mentions reviewing changes, or asks about code quality.
```

这个 description 之所以有效：
- 说明了 Skill 做什么（review code）
- 列出了具体方面（quality, security, best practices）
- 包含了触发场景（asks for code review, wants feedback, mentions reviewing changes）
- 包含了用户可能说的关键词（code quality）

### 3. 工具限制

```yaml
allowed-tools:
  - Read
  - Grep
  - Glob
```

只允许读取操作，确保代码审查是只读的、安全的。

## 测试方法

在 Claude Code 中，尝试以下请求：
- "帮我审查一下 src/auth.js"
- "这段代码有什么问题吗？"
- "review my changes"
- "check this code for security issues"

Claude 应该会自动激活这个 Skill 并按照指定格式进行代码审查。

## 学习要点

1. **Skill 最小化**：一个 SKILL.md 就是完整的 Skill
2. **description 是触发器**：写得越具体，触发越准确
3. **allowed-tools 增强安全**：限制工具防止意外操作
4. **结构化输出**：提供明确的输出格式模板
