#!/usr/bin/env python3
"""
代码分析 Agent —— 只读分析任意目录的代码结构

演示:
  - ClaudeCodeOptions 配置（权限模式、工具白名单）
  - 消息类型分类处理（TextBlock / ToolUseBlock）
  - ResultMessage 统计信息

运行: python analyzer.py <目录路径>
示例: python analyzer.py ../01-hello-agent
"""

import asyncio
import sys

from claude_code_sdk import query, ClaudeCodeOptions
from claude_code_sdk import AssistantMessage, ResultMessage, TextBlock, ToolUseBlock


async def analyze(directory: str):
    """分析指定目录的代码结构"""

    options = ClaudeCodeOptions(
        allowed_tools=["Read", "Grep", "Glob"],  # 只读工具
        permission_mode="plan",                    # 只��模式
        max_turns=10,
        cwd=directory,
    )

    prompt = """请分析当前目录的代码。要求：
1. 列出所有文件及用途
2. 识别使用的技术栈
3. 指出可改进之处（如果有）
用中文简洁回答。"""

    tools_used = 0
    try:
        async for msg in query(prompt=prompt, options=options):
            if isinstance(msg, AssistantMessage):
                for block in msg.content:
                    if isinstance(block, TextBlock):
                        print(block.text)
                    elif isinstance(block, ToolUseBlock):
                        tools_used += 1
                        detail = block.input.get("file_path", block.input.get("pattern", ""))
                        print(f"  📂 {block.name}: {detail}")

            elif isinstance(msg, ResultMessage):
                print(f"\n{'=' * 50}")
                print(f"  耗时: {msg.duration_ms / 1000:.1f}s")
                print(f"  费用: ${msg.total_cost_usd:.4f}")
                print(f"  轮次: {msg.num_turns} | 工具调用: {tools_used} 次")
                print(f"{'=' * 50}")
    except Exception as e:
        if "Unknown message type" not in str(e):
            raise


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python analyzer.py <目录路径>")
        sys.exit(1)

    print(f"🔍 正在分析: {sys.argv[1]}\n")
    asyncio.run(analyze(sys.argv[1]))
