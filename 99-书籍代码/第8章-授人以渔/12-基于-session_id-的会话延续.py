# 第一次调用：分析问题
session_id = None
async for message in query(prompt="分析 src/auth 的安全问题", options=options):
    if message.type == "system" and message.subtype == "init":
        session_id = message.session_id
    if message.type == "result":
        print(message.result)

# 第二次调用：在上一轮的上下文中继续
resume_options = ClaudeAgentOptions(**options.__dict__, resume=session_id)
async for message in query(
    prompt="重点分析你发现的第一个 SQL 注入风险",
    options=resume_options
):
    if message.type == "result":
        print(message.result)
