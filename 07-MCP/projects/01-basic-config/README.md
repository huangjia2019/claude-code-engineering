# 示例项目：MCP 配置（对应第 17 讲）

这个项目展示如何配置 MCP (Model Context Protocol) 服务器，与第 17 讲《海纳百川 · MCP 协议与外部工具连接》配套使用。

## 目录结构

```
01-basic-config/
├── .mcp.json           # 基础配置（3 个无需 API Key 的服务器）
├── .mcp.json.example   # 完整配置（与第 17 讲"开发者工具箱"对应）
├── .env.example        # 环境变量模板
└── README.md
```

## 快速开始

### 1. 零配置体验（推荐入门）

`.mcp.json` 已配置好 3 个不需要 API Key 的服务器，可以直接体验：

```bash
# 在 Claude Code 中验证
claude mcp list
```

包含的服务器：

| 服务器 | 用途 | 需要 API Key |
|--------|------|-------------|
| `filesystem` | 文件系统访问 | 否 |
| `fetch` | HTTP 请求 | 否 |
| `memory` | 持久化记忆 | 否 |

### 2. 添加 Context7（强烈推荐）

Context7 是开发者最常用的 MCP 服务器，写代码时自动拉取最新官方文档，无需 API Key：

```bash
claude mcp add context7 -- npx -y @upstash/context7-mcp@latest
```

使用方式——在提示中加 `use context7`：

```
你：帮我用 Next.js 15 的 App Router 写一个 API 路由 use context7
```

### 3. 完整开发者工具箱

要使用完整配置（GitHub、Notion、数据库等），需要配置 API Key：

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 填入你的 API Key
# 然后用 .mcp.json.example 替换 .mcp.json
cp .mcp.json.example .mcp.json
```

完整配置包含的服务器（与第 17 讲"完整开发者工具箱"一致）：

| 服务器 | 用途 | 连接方式 | 需要 API Key |
|--------|------|----------|-------------|
| `context7` | 实时技术文档 | stdio | 否 |
| `github` | 仓库/Issue/PR 管理 | HTTP | 是（GITHUB_TOKEN） |
| `notion` | Notion 页面读写 | HTTP | 是（NOTION_API_KEY） |
| `database` | 数据库查询 | stdio | 是（DATABASE_URL） |
| `fetch` | HTTP 请求 | stdio | 否 |
| `filesystem` | 文件系统访问 | stdio | 否 |
| `memory` | 持久化记忆 | stdio | 否 |

## API Key 获取指南

### GitHub Token
1. 打开 GitHub → Settings → Developer settings → Personal access tokens → Fine-grained tokens
2. 点击 "Generate new token"
3. 勾选需要的仓库权限（Issues: Read/Write, Pull requests: Read/Write）
4. 复制 token 到 `.env` 的 `GITHUB_TOKEN`

### Notion API Key
1. 打开 https://www.notion.so/profile/integrations
2. 点击 "New integration" 创建 Internal Integration
3. 复制 token 到 `.env` 的 `NOTION_API_KEY`
4. **重要**：在 Notion 页面的 "..." → "Connections" 里添加你的 Integration

### Database URL
格式：`postgresql://用户名:密码@主机:端口/数据库名`

建议使用只读账户：
```sql
CREATE USER readonly WITH PASSWORD 'your_password';
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly;
```

## 测试方法

在 Claude Code 中测试各个 MCP 服务器：

```
# 测试 Context7（无需 API Key）
"帮我查一下 React 19 的最新 API 变化 use context7"

# 测试 Fetch（无需 API Key）
"获取 https://api.github.com 的内容"

# 测试 GitHub（需要 GITHUB_TOKEN）
"列出我最近的 GitHub Issue"

# 测试 Database（需要 DATABASE_URL）
"查一下数据库里有哪些表"
```

## 安全提示

1. **绝对不要提交 .env** — 确保 `.gitignore` 包含 `.env`
2. **限制 filesystem 路径** — 只允许访问需要的目录
3. **数据库使用只读账户** — 防止 Claude 误操作修改数据
4. **定期轮换 Token** — 不要使用永不过期的 Token
