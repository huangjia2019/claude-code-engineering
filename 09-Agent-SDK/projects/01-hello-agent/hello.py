#!/usr/bin/env python3
"""
最简 Agent —— 5 行核心代码调用 Claude

这是 Agent SDK 的 Hello World。
运行: python hello.py
"""

import asyncio
from claude_code_sdk import query, ClaudeCodeOptions
from claude_code_sdk import AssistantMessage, ResultMessage, TextBlock


async def main():
    options = ClaudeCodeOptions(max_turns=1)

    async for msg in query(prompt="用一句话解释什么是递归。", options=options):
        if isinstance(msg, AssistantMessage):
            for block in msg.content:
                if isinstance(block, TextBlock):
                    print(block.text)

        elif isinstance(msg, ResultMessage):
            print(f"\n--- 统计 ---")
            print(f"耗时: {msg.duration_ms / 1000:.1f}s | 费用: ${msg.total_cost_usd:.4f}")


if __name__ == "__main__":
    asyncio.run(main())
