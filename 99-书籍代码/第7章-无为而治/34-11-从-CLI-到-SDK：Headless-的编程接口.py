# Python Agent SDK 示例
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

async def review_pr(changed_files: list[str]):
    options = ClaudeAgentOptions(
        allowed_tools=["Read", "Grep", "Glob"],
        max_turns=10,
        max_budget_usd=0.50,
        model="claude-sonnet-4-6",
    )

    async for message in query(
        prompt=f"审查以下文件：{', '.join(changed_files)}",
        options=options,
    ):
        if isinstance(message, ResultMessage):
            return message.result
