# 项目 06：Skill + context: fork 演示

> 第 12 讲配套项目 —— 演示模式二：Skill 派子代理去执行（方向 A）

## 组合模式

本项目演示的是 **方向 A（Skill 包含 SubAgent）**：

```
用户: /code-health-check src/
  │
  ├─ Skill (SKILL.md) 被激活
  ├─ context: fork → 自动创建一个 general-purpose 子代理
  ├─ SKILL.md 内容 = 子代理的任务指令
  ├─ 子代理独立执行：扫描文件、检查问题、生成报告
  └─ 返回结构化健康报告到主对话
```

**与模式一（Project 05）的区别：**
- 模式一：SubAgent 是老板，Skill 是工具书（SubAgent `.md` + `skills:` 字段）
- 模式二：Skill 是老板，SubAgent 是执行者（SKILL.md + `context: fork`）

## 项目结构

```
06-skill-fork-demo/
├── .claude/
│   └── skills/
│       └── code-health-check/
│           └── SKILL.md               ← context: fork + agent: general-purpose
├── src/
│   ├── app.js                         ← 含硬编码密钥（故意）
│   ├── routes/
│   │   ├── products.js                ← 含 SQL 注入、缺少 try/catch
│   │   └── categories.js              ← 含未使用函数、重复逻辑
│   └── utils/
│       └── db.js                      ← 含 eval() 使用
└── README.md
```

## 故意埋入的问题

| 文件 | 问题 | 严重级别 |
|------|------|---------|
| app.js | 硬编码 API_KEY 和 DB_PASSWORD | CRITICAL |
| app.js | 缺少全局错误处理 | WARNING |
| products.js:17 | SQL 注入漏洞（字符串拼接） | CRITICAL |
| products.js:7 | 缺少 try/catch | WARNING |
| products.js:23 | 错误被吞掉（catch 中没有发送响应） | WARNING |
| db.js:8 | 使用 eval() 解析配置 | CRITICAL |
| categories.js:26 | 未使用的 formatCategory 函数 | INFO |
| products.js + categories.js | 重复的验证逻辑 | INFO |

## 使用方式

```bash
# 在 Claude Code 中（进入项目目录后）
> /code-health-check src/

# 预期：子代理在隔离上下文中扫描 src/，返回健康报告
# 主对话上下文保持干净，不会被大量中间文件内容污染
```

## 关键观察点

1. **隔离性**：子代理的中间过程（读文件、分析代码）不会出现在主对话中
2. **任务驱动**：SKILL.md 本身就是完整的任务指令，不需要额外的 SubAgent 定义文件
3. **只读安全**：`allowed-tools` 只有 Read/Grep/Glob，子代理无法修改代码

## 关联课程

- **第 12 讲 §11**：模式二实战——Skill 派子代理去执行
- **对比项目**：`05-agent-skill-combo`（模式一：SubAgent 预加载 Skill）
