# 添加一个本地 stdio MCP 服务器
claude mcp add filesystem npx -y @modelcontextprotocol/server-filesystem /workspace

# 添加一个远程 HTTP MCP 服务器
claude mcp add --transport http company-jira https://jira.company.com/mcp

# 添加到用户级别（所有项目可用）
claude mcp add --scope user github -- npx -y @modelcontextprotocol/server-github

# 带认证头添加
claude mcp add --transport http --header "Authorization: Bearer ${TOKEN}" api https://api.example.com/mcp

# 管理命令
claude mcp list        # 列出所有已配置的服务器
claude mcp test github # 测试服务器连接
claude mcp remove github  # 删除服务器
