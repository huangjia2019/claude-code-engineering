# 第 21-22 讲：登堂入室 & 得心应手 · Agent SDK 基础与高级应用

> Headless 是"用命令行驱动 Claude"，Agent SDK 是"用代码驱动 Claude"。第 21 讲打基础——`query()` 调用、消息处理、会话管理；第 22 讲进阶到自定义工具、Hooks 拦截、权限分层，最终完成一个生产级的自动化测试修复 Agent。

---

## 你将学到

- Agent SDK 的核心 API：`query()` 与 `ClaudeCodeOptions`
- 编程式调用 vs Headless 调用的取舍
- 自定义工具：用 `@tool` 装饰器扩展 Agent 能力
- Hooks 拦截与四层权限管理
- 实战：自动化测试修复 Agent

## 配套项目

```
projects/
├── 01-basic-agent/         # 基础代码分析器
│   └── code_analyzer.py
│
├── 01-hello-agent/         # Hello World：第一个 Agent
│   └── hello.py
│
├── 02-code-analyzer/       # 代码分析 Agent
│   └── analyzer.py
│
├── 03-custom-tools/        # 自定义工具演示
│   └── tool_demo.py
│
└── 04-test-fixer/          # 自动化测试修复 Agent
    ├── fixer.py
    ├── src/calculator.py
    └── tests/test_calculator.py
```

## 一句话预告

> **Headless 是给 Claude 写剧本，Agent SDK 是给 Claude 写操作系统。**

> 祝大家学习顺利
