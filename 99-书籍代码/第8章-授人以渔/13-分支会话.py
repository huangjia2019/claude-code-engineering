# 基于同一轮分析，探索不同方向
options_fork = ClaudeAgentOptions(**options.__dict__, resume=session_id, fork_session=True)

# 方向 A：重构为微服务
async for message in query(prompt="如果重构为微服务，需要改哪些？", options=options_fork):
    ...

# 方向 B：在原架构上加固（基于同一个 session_id，再次 fork）
async for message in query(prompt="如果保持现有架构，怎么加固安全？", options=options_fork):
    ...
