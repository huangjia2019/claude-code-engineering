# 项目 05：SubAgent + Skill 配合实战

> 第 12 讲配套项目（阶段二）—— 用 Skill 武装 SubAgent，从通用工人变成领域专家

## 定位：本讲的第二个项目

本项目是 `04-api-generator` 的**进化版本**。核心变化是引入了 SubAgent，将 Skill 从"独立运行的操作手册"升级为"专家的专业知识"。

这是**组合模式一（SubAgent 预加载 Skills）** 的实战示例——方向 B 的典型应用。

```
学习路径：04-api-generator（学 Skill 设计） → 05-agent-skill-combo（学组合配装）
               ↑ 6 组件全展示                        ↑ 精简 Skill + SubAgent 定义
```

## 核心理念：从技能到技师

```
Skill 单独运行    = 一本操作手册放在桌上（Claude 自己看着做）
SubAgent 裸跑     = 一个什么都能干的通用工人（聪明但没有领域知识）
SubAgent + Skill  = 一个经过培训的专业技师（有工作流程、专用工具、输出模板）
```

同一个 SubAgent，注入不同的 Skill，就变成不同的专家。这就是组合的力量。

## 组合模式说明

本项目体现的是**方向 B（SubAgent 包含 Skill）**：

```
SubAgent (api-doc-generator.md)
  ├── 角色定义: "You are an API documentation specialist"
  ├── 使命: "Generate API documentation for Express routes"
  └── skills: [api-generating]  ← 预加载 Skill 作为领域知识
        ├── SKILL.md            ← 工作流程（HOW）
        ├── scripts/            ← 专用工具
        └── templates/          ← 输出模板
```

## 从 04 到 05：关键进化对比

| 维度 | 04-api-generator | 05-agent-skill-combo |
|------|------------------|---------------------|
| 定位 | 完整 Skill 架构展示 | SubAgent + Skill 组合实战 |
| Skill 组件数 | 6（全展示） | 3（精简实战） |
| SubAgent | 无 | `api-doc-generator.md` 角色定义 |
| 测试目标 | 无源代码 | Express 路由（含链式路由） |
| 学习重点 | Skill 结构设计 | 组合模式与职责划分 |

## 项目结构

```
05-agent-skill-combo/
├── .claude/
│   ├── agents/
│   │   └── api-doc-generator.md       ← SubAgent：角色 + 使命（WHO/WHAT）
│   ├── skills/
│   │   └── api-generating/
│   │       ├── SKILL.md               ← Skill：工作流程 + 规则（HOW）
│   │       ├── scripts/
│   │       │   └── detect-routes.py   ← 路由发现脚本（处理链式路由）
│   │       └── templates/
│   │           └── api-doc.md         ← 文档模板
│   └── settings.local.json            ← 权限预配置
├── src/routes/
│   ├── users.js                       ← 标准 CRUD（5 条路由）
│   └── orders.js                      ← 含 router.route().get().put() 链式路由（5 条路由）
├── docs/api/                          ← 生成的文档输出目录
└── README.md
```

## 职责划分

```
SubAgent（api-doc-generator.md）负责：
  WHO:    "You are an API documentation specialist"
  WHAT:   "Generate API documentation for Express routes"
  WHERE:  "Write to docs/api/"
  OUTPUT: "Return summary with route count and warnings"

Skill（SKILL.md + 附属文件）负责：
  HOW:        "Step 1: Run detect-routes.py → Step 2: Analyze → Step 3: Generate"
  WITH WHAT:  scripts/detect-routes.py, templates/api-doc.md
  STANDARD:   "Check auth middleware, mark with 🔒"
  QUALITY:    "All routes documented, schemas match code"
```

## 使用方式

```bash
# Step 1: 验证脚本可用
python .claude/skills/api-generating/scripts/detect-routes.py src/
# 预期：发现 10 条路由（含 2 条链式路由）

# Step 2: 通过 SubAgent 执行
> 用 api-doc-generator 为 src/ 生成 API 文档

# Step 3: 验证结果
# 检查 docs/api/users.md — 应包含 5 个端点
# 检查 docs/api/orders.md — 应包含 5 个端点（含链式路由）
# 检查 🔒 标记 — 需要认证的端点应有标记
# 检查工具调用日志 — SubAgent 应调用了 detect-routes.py
```

## 对比实验

| 维度 | SubAgent 裸跑 | SubAgent + Skill |
|------|--------------|-----------------|
| 路由发现 | Grep 搜索模式 | 执行 detect-routes.py |
| 链式路由 | 通常遗漏 | 脚本专门处理 |
| 输出格式 | 随机 | 模板统一 |
| 质量自检 | 没有 | Quality Checklist |

## 关联课程

- **第 12 讲**：Skills 高级模式与 SubAgent 配合实战
  - 第一部分 §1-3：组合的全貌（两个原子方向、三种组合模式、选型框架）
  - 第二部分 §4-7：构建生产级 Skill（项目 04）
  - 第三部分 §8-10：把 Skill 装进 SubAgent（本项目）
- **前置项目**：`04-api-generator`（先学会 Skill 设计，再学组合配装）
