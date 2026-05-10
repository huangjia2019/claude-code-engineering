---
name: React 最佳实践
description: React 组件设计模式、Hooks 使用指南、性能优化技巧
---

# React 最佳实践

本技能包含 React 开发的最佳实践，帮助你编写高质量的 React 代码。

## 目录

当用户需要特定主题时，加载对应章节：

- **Hooks 基础** → 加载 [chapters/hooks.md](./chapters/hooks.md)
- **Context 使用** → 加载 [chapters/context.md](./chapters/context.md)
- **性能优化** → 加载 [chapters/performance.md](./chapters/performance.md)

只在用户明确需要时加载完整内容，避免浪费上下文窗口。

## 核心原则

1. **组件单一职责**：一个组件做一件事
2. **状态提升最小化**：状态放在需要它的最近公共祖先
3. **避免过早优化**：先让它工作，再让它快
4. **优先组合而非继承**：使用 children 和 render props

## 快速参考

### 自定义 Hook 命名

```javascript
// 好的命名
useUser()
useLocalStorage()
useDebounce()

// 不好的命名
fetchUser()      // 不是 use 开头
useData()        // 太模糊
```

### 组件文件结构

```
ComponentName/
├── index.ts           # 导出
├── ComponentName.tsx  # 组件实现
├── ComponentName.test.tsx
├── ComponentName.styles.ts
└── types.ts           # 类型定义
```
