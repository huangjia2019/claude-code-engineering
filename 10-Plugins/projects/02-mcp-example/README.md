# 示例插件：MCP 服务器集成

这个示例展示如何在插件中集成 MCP 服务器，让 Claude Code 能够连接外部工具和数据源。

## 什么是 MCP？

MCP (Model Context Protocol) 是一个开放协议，定义了 AI 如何与外部工具通信。

通过 MCP 服务器，Claude Code 可以：
- 执行数据库查询
- 调用 API
- 读写文件系统
- 连接任何支持 MCP 的服务

## 目录结构

```
02-mcp-example/
├── plugin.json
├── mcp-servers/
│   ├── filesystem.json    # 文件系统增强
│   └── fetch.json         # HTTP 请求能力
└── README.md
```

## MCP 服务器类型

### 1. Stdio 类型（本示例使用）

运行本地进程，通过 stdin/stdout 通信。

```json
{
  "type": "stdio",
  "command": "npx",
  "args": ["-y", "@anthropic/mcp-server-xxx"]
}
```

适用于：本地工具、NPM 包、自定义脚本

### 2. HTTP 类型

连接远程 HTTP 服务。

```json
{
  "type": "http",
  "url": "https://api.example.com/mcp"
}
```

适用于：云服务、需要认证的 API

### 3. SSE 类型

通过 Server-Sent Events 流式通信。

适用于：实时数据、长时间运行的任务

## 学习要点

1. **MCP 是桥梁**：连接 Claude 和外部世界
2. **环境变量**：敏感信息通过 `${VAR_NAME}` 引用
3. **按需加载**：插件启用时才启动服务器

## 常用 MCP 服务器

| 服务器 | 用途 |
|--------|------|
| `@anthropic/mcp-server-postgres` | PostgreSQL 数据库 |
| `@anthropic/mcp-server-github` | GitHub API |
| `@anthropic/mcp-server-filesystem` | 增强文件操作 |
| `@anthropic/mcp-server-fetch` | HTTP 请求 |

## 安全注意

- MCP 服务器运行在你的机器上
- 拥有你授予的权限
- 谨慎配置数据库连接等敏感服务器
