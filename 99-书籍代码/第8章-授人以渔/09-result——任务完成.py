from claude_agent_sdk import (
    query, ClaudeAgentOptions, AssistantMessage, ResultMessage
)


async def process_query(prompt: str, options: ClaudeAgentOptions) -> dict:
    result = {"text": [], "tools": [], "metadata": {}, "error": None}

    async for message in query(prompt=prompt, options=options):
        # SDK 返回 dataclass 实例，没有 .type 属性
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    result["text"].append(block.text)
                elif hasattr(block, "name"):
                    result["tools"].append({"tool": block.name, "input": block.input})
        elif isinstance(message, ResultMessage):
            result["metadata"] = {
                "session_id": message.session_id,
                "cost": message.total_cost_usd,
                "turns": message.num_turns,
                "duration_ms": message.duration_ms,
            }
            if message.is_error:
                result["error"] = message.subtype

    return result
