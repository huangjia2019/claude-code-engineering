# 第 20 讲：有章可循 · Rules 规则系统深度剖析

> 指令规则告诉 Claude 该怎么做，权限规则告诉 Claude 能做什么——两套规则协同运作，构成整个系统的行为约束体系。

---

## 你将学到

- 指令规则：`.claude/rules/*.md` 的 paths 条件匹配与加载机制
- 权限规则：`deny → ask → allow` 三层评估顺序
- Rules 与 CLAUDE.md 的分工：全局 vs 领域，常驻 vs 按需
- 企业级管理：托管设置与纵深防御

## 代码与文件参考

本讲内容与 Memory 模块紧密关联，配置示例参考：

- Rules 配置示例 → [02-Memory/projects/](../02-Memory/projects/)
- 权限与安全实践 → [06-Hooks/projects/01-safety-hooks/](../06-Hooks/projects/01-safety-hooks/)
> 祝大家学习顺利
