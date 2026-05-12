import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, ResultMessage


async def main():
    # 用 SDK 构建一个代码健康度检查 Agent
    options = ClaudeAgentOptions(
        allowed_tools=["Read", "Grep", "Glob"],
        max_turns=15,
    )

    async for message in query(
        prompt="分析 src/ 目录下所有 Python 文件的代码质量，给出健康度评分",
        options=options,
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    print(block.text)
        elif isinstance(message, ResultMessage):
            print(f"\n[done] cost=${message.total_cost_usd}")


asyncio.run(main())
