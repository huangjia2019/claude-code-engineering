#!/usr/bin/env python3
"""
测试修复 Agent —— 自动发现并修复代码 bug

演示:
  - 两阶段工作流（分析 → 修复）
  - 不同权限模式的切换 (plan → acceptEdits)
  - 工具白名单精确控制
  - 完整的 "发现 → 分析 → 修复 → 验证" 流程

运行: python fixer.py
前提: pip install pytest
"""

import asyncio
import subprocess
import os

from claude_code_sdk import query, ClaudeCodeOptions
from claude_code_sdk import AssistantMessage, ResultMessage, TextBlock, ToolUseBlock


PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))


async def phase_analyze():
    """阶段一：只读分析——找出 bug 原因"""

    options = ClaudeCodeOptions(
        allowed_tools=["Read", "Grep", "Glob", "Bash(python3:*)"],
        permission_mode="plan",
        max_turns=10,
        cwd=PROJECT_DIR,
    )

    prompt = """你是一个测试修复助手。当前项目有测试失败。

请完成：
1. 运行 `python3 -m pytest tests/ -v --tb=short` 查看失败的测试
2. 读取失败测试对应的测试文件和源代码
3. 分析失败原因，指出 bug 位置
4. 给出具体修复方案（文件、行号、修改内容）

只分析不修改。用中文回答。"""

    print("📖 阶段一：分析失败原因...\n")

    async for msg in query(prompt=prompt, options=options):
        if isinstance(msg, AssistantMessage):
            for block in msg.content:
                if isinstance(block, TextBlock):
                    print(block.text)
                elif isinstance(block, ToolUseBlock):
                    detail = block.input.get("command", block.input.get("file_path", block.input.get("pattern", "")))
                    print(f"  🔍 {block.name}: {detail}")
        elif isinstance(msg, ResultMessage):
            print(f"\n  [分析完成: {msg.duration_ms/1000:.1f}s, ${msg.total_cost_usd:.4f}]")


async def phase_fix():
    """阶段二：执行修复"""

    options = ClaudeCodeOptions(
        allowed_tools=["Read", "Edit", "Bash(python3:*)"],
        permission_mode="acceptEdits",
        max_turns=10,
        cwd=PROJECT_DIR,
    )

    prompt = """请修复 src/calculator.py 中 average() 函数的 bug。
修复后运行 `python3 -m pytest tests/ -v --tb=short` 验证所有测试通过。
只改必要的代码。"""

    print("\n🔨 阶段二：执行修复...\n")

    async for msg in query(prompt=prompt, options=options):
        if isinstance(msg, AssistantMessage):
            for block in msg.content:
                if isinstance(block, TextBlock):
                    print(block.text)
                elif isinstance(block, ToolUseBlock):
                    label = "✏️" if block.name == "Edit" else "🔍"
                    detail = block.input.get("file_path", block.input.get("command", ""))
                    print(f"  {label} {block.name}: {detail}")
        elif isinstance(msg, ResultMessage):
            print(f"\n  [修复完成: {msg.duration_ms/1000:.1f}s, ${msg.total_cost_usd:.4f}]")


async def main():
    print("=" * 55)
    print("  🔧 测试修复 Agent")
    print("=" * 55)

    # 先展示当前测试状态
    print("\n📋 当前测试状态:\n")
    result = subprocess.run(
        ["python3", "-m", "pytest", "tests/", "-v", "--tb=short"],
        capture_output=True, text=True, cwd=PROJECT_DIR,
    )
    print(result.stdout)

    if result.returncode == 0:
        print("✅ 所有测试通过，无需修复。")
        return

    print("❌ 存在失败的测试！\n")

    # 阶段一：分析
    await phase_analyze()

    # 用户确认
    print("\n" + "=" * 55)
    confirm = input("是否执行修复？(y/n): ")
    if confirm.lower() != "y":
        print("已取消。")
        return

    # 阶段二：修复
    await phase_fix()

    # 最终验证
    print("\n📋 最终验证:\n")
    result = subprocess.run(
        ["python3", "-m", "pytest", "tests/", "-v", "--tb=short"],
        capture_output=True, text=True, cwd=PROJECT_DIR,
    )
    print(result.stdout)
    if result.returncode == 0:
        print("✅ 所有测试通过！修复成功。")
    else:
        print("⚠️ 仍有测试失败，请检查。")


asyncio.run(main())
