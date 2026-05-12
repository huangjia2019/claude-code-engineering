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
    # 注意：没有 append_system_prompt 字段。要追加 system prompt，用 dict 形式：
    system_prompt={
        "type": "preset",
        "preset": "claude_code",
        "append": "你是一名高级代码审查员，务必检查 SQL 注入漏洞。",
    },

    # === 工作环境 ===
    cwd="/path/to/project",           # 工作目录
    env={"PROJECT_NAME": "MyApp"},    # 环境变量

    # === 会话管理 ===
    resume="session-id-to-resume",    # 恢复指定会话（必须是合法 UUID）
    # 注意：no_session_persistence 不是 Options 字段，是 CLI flag，已删除

    # === 输出格式 ===
    output_format={"type": "json_schema", "schema": {"type": "object"}},

    # === MCP 服务器（注意：mcp_servers 是 dict 不是 list） ===
    mcp_servers={
        "db": {
            "command": "python",
            "args": ["./db_server.py"],
        }
    },
)
