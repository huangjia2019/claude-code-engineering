options = ClaudeAgentOptions(
    mcp_servers={"app-tools": tools_server},
    allowed_tools=[
        "Read", "Grep", "Glob",                  # 内置工具
        "mcp__app-tools__query_database",          # 自定义工具
        "mcp__app-tools__send_notification",
    ]
)
