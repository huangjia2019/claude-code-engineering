# 第 17 讲：海纳百川 · MCP 协议与外部工具连接

> Claude Code 原生只能读写本地文件和执行命令。MCP（Model Context Protocol）让它连接 GitHub、Notion、数据库、实时文档——从单机工具进化为开放平台。

---

## 你将学到

- MCP 协议架构：三种传输方式（stdio / HTTP / SSE）
- 五大实战服务器：Context7、GitHub、Notion、数据库、Fetch
- 从零构建自定义 MCP 服务器（TypeScript）
- Token 成本管控与安全最佳实践

## 配套项目

```
projects/
├── 01-basic-config/        # MCP 配置模板
│   ├── .mcp.json           # 基础配置（4 个开箱即用）
│   ├── .mcp.json.example   # 完整开发者工具箱（7 个服务器）
│   ├── .env.example        # API Key 模板
│   └── README.md
│
└── 02-custom-server/       # 自定义 MCP 服务器
    ├── src/index.ts         # TypeScript 实现（Todo + Notes + Timer）
    ├── package.json
    └── tsconfig.json
```

## 一句话预告

> **MCP 之于 Claude Code，就像 USB 之于电脑——标准化的扩展接口，插上就能用。**
