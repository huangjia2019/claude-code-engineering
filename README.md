# Claude Code 工程化实战 · 课程大纲

<p align="center">
  <a href="https://time.geekbang.org/column/intro/101113501"><img src="https://img.shields.io/badge/平台-极客时间-00b4ab?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0id2hpdGUiIGQ9Ik0xMiAyTDIgN2wxMCA1IDEwLTV6Ii8+PC9zdmc+" alt="极客时间"/></a>
  <a href="https://time.geekbang.org/column/intro/101113501"><img src="https://img.shields.io/badge/2026-首发专栏-ff6b35?style=for-the-badge" alt="2026首发"/></a>
  <a href="https://time.geekbang.org/column/intro/101113501"><img src="https://img.shields.io/badge/Claude_Code-工程化实战-7c3aed?style=for-the-badge&logo=anthropic&logoColor=white" alt="Claude Code"/></a>
</p>

<div align="center">

<a href="https://time.geekbang.org/column/intro/101113501"><img src="91-Pictures/课程Banner.png" alt="Claude Code 工程化实战 Banner" width="600"/></a>

🎯 **这是我为极客时间2026年制作的最新专栏，目标：快速掌握 Claude Code 高阶技能，进行工程化的 Agent 实战**

</div>

<p align="center">
  <img src="https://img.shields.io/badge/📅_上线日期-2026年1月28日-success?style=flat-square&labelColor=2d3748" alt="上线日期"/>
  <img src="https://img.shields.io/badge/状态-已上线_🔥-brightgreen?style=flat-square" alt="已上线"/>
  <img src="https://img.shields.io/badge/🏆_总榜第一-万人订阅-ff6b35?style=flat-square&labelColor=2d3748" alt="总榜第一"/>
</p>

<h3 align="center">🚀 上线一个月，万人订阅，极客时间总榜第一</h3>

---

## 开篇词：极客与 AI 的共舞

---

## 第一部分：基础篇

### 第 1 讲：登高望远 · Claude Code 全景导览
Claude Code 不只是一个命令行助手，而是一个可扩展的 AI Agent 框架——理解其技术栈全貌是掌控它的第一步。

### 第 2 讲：过目不忘 · CLAUDE.md 记忆系统
让 Claude 记住你的项目规范、编码风格和团队约定，从每次重复说明到一次配置永久生效。

---

## 第二部分：子代理（Sub-Agents）专题

### 第 3 讲：分而治之 · 子代理核心概念
把"一个大脑"拆成多个"专职岗位"——理解隔离执行、权限边界和上下文管理的工程价值。

### 第 4 讲：明察秋毫 · 只读型子代理实战
**项目：代码审查员** — 用 `Read/Grep/Glob` 构建一个只能看、不能改的安全审计角色。

### 第 5 讲：去芜存菁 · 高噪声任务处理
**项目：测试运行器 & 日志分析器** — 让子代理去消化 500 行输出，只把结论带回主对话。

### 第 6 讲：众志成城 · 并行探索与流水线编排
**项目：多视角探索 & Bug 修复流水线** — 当任务可以并行或分阶段时，子代理如何协作。

### 第 7 讲：Agent Teams · 多会话协作架构
**项目：Agent 团队** — 从单次委派到多会话持久协作，构建具有角色分工和状态传递的 Agent 团队。

### 加餐：子代理专题总结

---

## 第三部分：Skills 技能系统专题

### 第 9 讲：触类旁通 · SKILL.md 结构与触发机制
Description 不只是说明文档，而是触发器——掌握让 Claude 自动发现并逐渐加载技能的关键写法。

### 第 10 讲：令行禁止 · 任务型 Skills 实战
**项目：团队标准命令集** — 用 `/review`、`/deploy`、`/commit` 固化团队最佳实践——它们的本质是设了 `disable-model-invocation: true` 的 Skill。

### 第 11 讲：循序渐进 · 渐进式披露架构设计
**项目：财务分析 Skill** — 目录页、章节、附录三层结构，把 token 利用率提升 98%。

### 第 12 讲：浑然天成 · Skills 高级模式与 SubAgent 配合实战
先理解组合的全貌，再动手构建组件，最后组装成完整的专家。

### 第 13 讲：登高望远 · Skills 架构定位与设计模式
先看清全景，再掌握利器，最后融会贯通。

### 第 14 讲：星火燎原 · Skills 出圈——从 Claude Code 到行业开放标准
一个 Markdown 文件格式，用 125 天从一个产品特性变成行业开放标准。这不是偶然——它揭示了 AI Agent 生态中，什么样的机制能活下来，什么样的知识能跨越边界。

### 加餐：Skills 专题总结

---

## 第四部分：扩展机制

### 第 15 讲：防微杜渐 · Hooks 事件驱动自动化（上）
在 Claude 执行工具前后插入自定义检查，阻止危险命令、保护敏感文件、自动格式化代码——在小问题萌芽时就防止它演变成灾难。

### 第 16 讲：步步为营 · Hooks 高级模式与工程实践（下）
从 Stop Hook 质量门控到 SubAgent 事件验收，从 frontmatter 精准配置到三维决策框架——每一步都设防，构建滴水不漏的 Hook 工程体系。

### 第 17 讲：海纳百川 · MCP 协议与外部工具连接
一个开放协议，让 Claude Code 从只能操作本地文件的工具，进化为能连接整个数字世界的智能枢纽——数据库、API、云服务，百川归海，一协议通。

---

## 第五部分：生产化与工程化

### 第 18 讲：庖丁解牛 · Tools 工具系统深度剖析
十几个精选的原语工具覆盖五个原子操作，通过涌现产生无限复杂能力——理解工具背后的设计哲学，用起来才能游刃有余。

### 第 19 讲：无人值守 · Headless 模式与 CI/CD 集成
当 Claude Code 脱离人的实时操控，以守护进程般的姿态嵌入流水线，开发团队获得的不只是效率提升，而是一种全新的人机协作节奏。

### 第 20 讲：有章可循 · Rules 规则系统深度剖析
指令规则告诉 Claude 该怎么做，权限规则告诉 Claude 能做什么——两套规则协同运作，构成整个系统的行为约束体系。

### 第 21 讲：登堂入室 · Agent SDK 基础
SDK 把 Claude Code 的能力拆解为可编程的接口——`query()` 和 `ClaudeCodeOptions`，让你像调用函数一样驱动 AI Agent。

### 第 22 讲：得心应手 · Agent SDK 高级应用
**项目：自动化测试修复 Agent** — 自定义工具、Hooks 拦截、权限分层和流式会话，构建生产级 AI Agent。

### 第 23 讲：化零为整 · Plugins 插件打包与分发
**项目：团队能力包** — 把 Commands、Skills、Agents、Hooks、MCP 配置打包成一个可安装、可升级、可分享的插件，实现团队资产沉淀与共享。

---

<p align="center">
  <a href="https://time.geekbang.org/column/intro/101113501">
    <img src="https://img.shields.io/badge/👉_点击这里开启课程之旅-极客时间-00b4ab?style=for-the-badge&labelColor=2d3748" alt="开启课程之旅"/>
  </a>
</p>

