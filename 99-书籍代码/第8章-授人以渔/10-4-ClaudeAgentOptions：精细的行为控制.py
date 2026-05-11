from claude_agent_sdk import ClaudeAgentOptions

options = ClaudeAgentOptions(
    # === 模型与执行 ===
    model="claude-sonnet-4-6",       # 模型选择
    max_turns=10,                     # 最大执行轮数
    max_budget_usd=1.0,              # 成本上限（美元）

    # === 工具权限 ===
    allowed_tools=["Read", "Grep", "Glob", "Write"],
    disallowed_tools=["Bash"],

    # === 权限模式 ===
    permission_mode="default",        # default / acceptEdits / plan / bypassPermissions

    # === 提示词 ===
    system_prompt="你是一名高级代码审查员。",
    append_system_prompt="务必检查 SQL 注入漏洞。",

    # === 工作环境 ===
    cwd="/path/to/project",           # 工作目录
    env={"PROJECT_NAME": "MyApp"},    # 环境变量

    # === 会话管理 ===
    resume="session-id-to-resume",    # 恢复指定会话
    no_session_persistence=False,     # 是否禁用会话持久化

    # === 输出格式 ===
    output_format={"type": "json_schema", "schema": my_schema},  # 结构化输出

    # === MCP 服务器 ===
    mcp_servers=[
        {"name": "db", "command": "python", "args": ["./db_server.py"]}
    ],
)
