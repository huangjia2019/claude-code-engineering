from claude_agent_sdk import tool, create_sdk_mcp_server

@tool(
    name="query_database",
    description="Execute a read-only SQL query on the application database",
    parameters={
        "query": str,
        "limit": int
    }
)
async def query_database(args):
    sql = args["query"]
    limit = args.get("limit", 100)

    # 安全检查：只允许 SELECT
    if not sql.strip().upper().startswith("SELECT"):
        return {
            "content": [{"type": "text", "text": "Error: Only SELECT queries allowed"}],
            "isError": True
        }

    results = await db.execute(f"{sql} LIMIT {limit}")
    return {
        "content": [{"type": "text", "text": json.dumps(results, indent=2)}]
    }

@tool(
    name="send_notification",
    description="Send a notification to the team Slack channel",
    parameters={"channel": str, "message": str}
)
async def send_notification(args):
    await slack.post_message(args["channel"], args["message"])
    return {
        "content": [{"type": "text", "text": f"Notification sent to #{args['channel']}"}]
    }

# 创建 MCP 服务器承载这些工具
tools_server = create_sdk_mcp_server(
    name="app-tools",
    version="1.0.0",
    tools=[query_database, send_notification]
)
