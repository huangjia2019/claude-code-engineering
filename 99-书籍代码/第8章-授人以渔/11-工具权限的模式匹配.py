options = ClaudeAgentOptions(
    allowed_tools=[
        "Read",
        "Grep",
        "Glob",
        "Bash(git diff *)",      # 只允许 git diff 命令
        "Bash(npm test *)",       # 只允许 npm test 命令
        "mcp__database__query",   # 只允许 MCP 数据库查询工具
    ]
)
