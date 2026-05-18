#!/usr/bin/env python3
"""代码分析 Web 服务——一个可运行的完整示例"""

import asyncio
import sys
from claude_agent_sdk import (
    query, ClaudeAgentOptions, AssistantMessage, ResultMessage
)


async def analyze_codebase(directory: str, focus: str = "general"):
    """
    分析指定目录的代码。

    Args:
        directory: 要分析的目录路径
        focus: 分析重点 - "security" / "performance" / "quality" / "general"
    """
    focus_prompts = {
        "security": "专注于安全漏洞：SQL 注入、XSS、敏感信息硬编码、权限控制。",
        "performance": "专注于性能问题：N+1 查询、内存泄漏、不必要的计算、缺少缓存。",
        "quality": "专注于代码质量：命名规范、DRY 原则、复杂度、测试覆盖。",
        "general": "全面分析：安全、性能、质量、架构。",
    }

    options = ClaudeAgentOptions(
        model="claude-sonnet-4-6",
        max_turns=15,
        max_budget_usd=0.50,
        allowed_tools=["Read", "Grep", "Glob"],
        permission_mode="plan",       # 只读模式
        cwd=directory,
        # 没有 append_system_prompt 字段，用 dict 形式追加
        system_prompt={
            "type": "preset",
            "preset": "claude_code",
            "append": focus_prompts.get(focus, focus_prompts["general"]),
        },
    )

    output_text: list[str] = []
    tools_used: list[str] = []
    metadata: dict = {}

    async for message in query(
        prompt=f"分析当前项目的代码，{focus_prompts.get(focus, '')}。输出 Markdown 格式的分析报告。",
        options=options,
    ):
        # 用 isinstance 判断，不是 message.type
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    output_text.append(block.text)
                    # 流式输出——在实际 Web 服务中，这里发送 SSE 事件
                    print(block.text, end="", flush=True)
                elif hasattr(block, "name"):
                    tools_used.append(block.name)
        elif isinstance(message, ResultMessage):
            metadata = {
                "session_id": message.session_id,
                "cost_usd": message.total_cost_usd,
                "turns": message.num_turns,
                "duration_ms": message.duration_ms,
                "success": not message.is_error,
            }

    return {
        "report": "\n".join(output_text),
        "tools_used": tools_used,
        "metadata": metadata,
    }


async def main():
    directory = sys.argv[1] if len(sys.argv) > 1 else "."
    focus = sys.argv[2] if len(sys.argv) > 2 else "general"

    print(f"分析 {directory}（重点：{focus}）...\n")
    result = await analyze_codebase(directory, focus)

    print(f"\n\n--- 统计 ---")
    print(f"费用：${result['metadata'].get('cost_usd', 0):.4f}")
    print(f"耗时：{result['metadata'].get('duration_ms', 0) / 1000:.1f}s")
    print(f"工具调用：{', '.join(result['tools_used'])}")


if __name__ == "__main__":
    asyncio.run(main())
