import dataclasses
from claude_agent_sdk import query, ClaudeAgentOptions, SystemMessage, ResultMessage

# 第一次调用：分析问题
session_id = None
async for message in query(prompt="分析 src/auth 的安全问题", options=options):
    # SystemMessage 有 subtype="init" 字段，会话 ID 在这里
    if isinstance(message, SystemMessage) and message.subtype == "init":
        session_id = message.data.get("session_id")
    if isinstance(message, ResultMessage):
        print(message.result)

# 第二次调用：在上一轮的上下文中继续
# 用 dataclasses.replace() 而不是 **options.__dict__——避免 resume 字段冲突
resume_options = dataclasses.replace(options, resume=session_id)
async for message in query(
    prompt="重点分析你发现的第一个 SQL 注入风险",
    options=resume_options,
):
    if isinstance(message, ResultMessage):
        print(message.result)
