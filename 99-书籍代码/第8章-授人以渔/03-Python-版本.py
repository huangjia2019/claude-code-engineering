import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, ResultMessage


async def analyze_code():
    options = ClaudeAgentOptions(
        max_turns=5,
        allowed_tools=["Read", "Grep", "Glob"],
        system_prompt="你是一名代码架构分析师。",
    )

    async for message in query(
        prompt="分析 src/auth/ 目录的实现架构",
        options=options,
    ):
        # SDK 返回的是 dataclass 实例，没有 .type 属性，必须用 isinstance 判断
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    print(block.text, end="", flush=True)
        elif isinstance(message, ResultMessage):
            print(f"\n\n完成。费用：${message.total_cost_usd:.4f}")


asyncio.run(analyze_code())
