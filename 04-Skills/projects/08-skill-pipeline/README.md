# 项目 07：Skill 流水线演示

> 第 12 讲配套项目 —— 演示模式三：流水线中的 Skill 分工（方向 B × N）

## 组合模式

本项目演示的是 **模式三（流水线中的 Skill 分工）**：多个 SubAgent 各自预加载不同的 Skill，按阶段串联执行。

```
阶段 1: route-scanner          阶段 2: doc-writer           阶段 3: quality-checker
skills: [route-scanning]       skills: [doc-writing]        skills: [quality-checking]

┌──────────────────┐    路由清单    ┌──────────────────┐   文档清单    ┌──────────────────┐
│ 扫描 src/ 目录    │ ──────────→ │ 读源码、写文档     │ ──────────→ │ 验证文档质量      │
│ 输出路由 JSON     │              │ 输出 docs/*.md    │              │ 输出质量报告      │
└──────────────────┘              └──────────────────┘              └──────────────────┘
       model: haiku                    model: sonnet                    model: haiku
       (轻量扫描)                       (需要理解力)                      (规则检查)
```

**关键特征：**
- 每个阶段是方向 B（SubAgent 包含 Skill）的一个实例
- 三个 SubAgent 各有不同的 Skill、不同的 model、不同的 tools
- 每阶段的输出是下一阶段的输入（数据流水线）
- CLAUDE.md 定义编排逻辑

## 项目结构

```
07-skill-pipeline/
├── CLAUDE.md                              ← 流水线编排指令
├── .claude/
│   ├── agents/
│   │   ├── route-scanner.md               ← 阶段 1: 路由扫描专家 (haiku)
│   │   ├── doc-writer.md                  ← 阶段 2: 文档编写专家 (sonnet)
│   │   └── quality-checker.md             ← 阶段 3: 质量检查专家 (haiku)
│   ├── skills/
│   │   ├── route-scanning/
│   │   │   ├── SKILL.md                   ← 扫描工作流程
│   │   │   └── scripts/scan-routes.py     ← 路由扫描脚本
│   │   ├── doc-writing/
│   │   │   ├── SKILL.md                   ← 文档生成工作流程
│   │   │   └── templates/endpoint-doc.md  ← 文档模板
│   │   └── quality-checking/
│   │       ├── SKILL.md                   ← 质量检查工作流程
│   │       └── rules/doc-standards.md     ← 质量标准规则
│   └── settings.local.json
├── src/routes/
│   ├── products.js                        ← 7 条路由（含链式路由）
│   └── categories.js                      ← 5 条路由
└── docs/                                  ← 生成的文档输出
```

## 每个阶段的角色分工

| 阶段 | SubAgent | Skill | Model | Tools | 输入 | 输出 |
|------|----------|-------|-------|-------|------|------|
| 1 | route-scanner | route-scanning | haiku | Read,Grep,Glob,Bash | src/ 目录 | 路由 JSON 清单 |
| 2 | doc-writer | doc-writing | sonnet | Read,Write,Glob | 路由清单 | docs/*.md 文件 |
| 3 | quality-checker | quality-checking | haiku | Read,Grep,Glob | 文档清单 | 质量报告 |

**为什么选不同的 model？**
- 阶段 1（扫描）和阶段 3（规则检查）是结构化任务，haiku 足够
- 阶段 2（文档编写）需要理解代码逻辑并生成自然语言，用 sonnet

## 使用方式

```bash
# 先验证扫描脚本
python3 .claude/skills/route-scanning/scripts/scan-routes.py src/

# 运行完整流水线
> 对 src/ 目录运行文档流水线

# 或者分阶段手动运行
> 用 route-scanner 扫描 src/ 目录的路由
> 用 doc-writer 根据上面的路由清单生成文档
> 用 quality-checker 验证 docs/ 目录下生成的文档
```

## 预期结果

- 阶段 1：发现 12 条路由（products 7 条 + categories 5 条）
- 阶段 2：生成 `docs/products-api.md` 和 `docs/categories-api.md`
- 阶段 3：质量报告（PASS 或 NEEDS_REVISION + 具体问题列表）

## 与其他项目的对比

| 项目 | 模式 | SubAgent 数量 | Skill 数量 | 编排方式 |
|------|------|-------------|-----------|---------|
| 05-agent-skill-combo | 模式一 | 1 | 1 | 单次调用 |
| 06-skill-fork-demo | 模式二 | 1（自动） | 1 | context: fork |
| **07-skill-pipeline** | **模式三** | **3** | **3** | **CLAUDE.md 编排** |

## 关联课程

- **第 12 讲 §12**：模式三实战——流水线中的 Skill 分工
- **对比项目**：`05-agent-skill-combo`（模式一）、`06-skill-fork-demo`（模式二）
