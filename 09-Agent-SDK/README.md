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
├── 01-hello-agent/         # 第 21 讲「安装与第一次调用」
│   └── hello.py            #   最简 Agent：5 行核心代码的 Hello World
│
├── 01-basic-agent/         # 第 21 讲「安装与第一次调用」（早期版本）
│   └── code_analyzer.py    #   基础代码分析器
│
├── 02-code-analyzer/       # 第 21 讲「实战项目：代码分析 Agent」
│   └── analyzer.py         #   只读分析 Agent：ClaudeCodeOptions 配置 + 消息分类处理
│
├── 03-custom-tools/        # 第 22 讲「自定义工具：给 Agent 装上新技能」
│   └── tool_demo.py        #   @tool 装饰器 + create_sdk_mcp_server 演示
│
└── 04-test-fixer/          # 第 22 讲「实战项目：测试修复 Agent」
    ├── fixer.py             #   两阶段工作流：分析(plan) → 修复(acceptEdits)
    ├── src/calculator.py    #   被测代码（故意留有 bug）
    └── tests/test_calculator.py  #   测试用例（会失败，等 Agent 来修）
```

## 一句话预告

> **Headless 是给 Claude 写剧本，Agent SDK 是给 Claude 写操作系统。**

> 祝大家学习顺利
