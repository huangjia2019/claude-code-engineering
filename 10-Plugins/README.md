# 第 23 讲：化零为整 · Plugins 插件打包与分发

> Skills、Commands、Hooks、MCP——前面学的都是散装零件。Plugins 把它们打包成一个可安装、可分享、可复用的整体，这是工程化的最后一块拼图。

---

## 你将学到

- Plugin 的目录结构与 manifest 规范
- 如何将 Skills + Commands + Hooks 封装为一个 Plugin
- 发布与分发：团队内共享 vs 社区开源
- Plugin 设计的取舍：粒度、依赖、版本兼容

## 配套项目

```
projects/
├── 01-my-first-plugin/     # 第一个插件：团队能力包
│   ├── plugin.json          # 插件 manifest
│   ├── agents/quick-fix.md  # 预配置子代理
│   └── commands/            # 斜杠命令
│       ├── explain.md
│       └── todo.md
│
└── 02-mcp-example/         # MCP 服务器插件
    ├── plugin.json
    └── mcp-servers/
        ├── fetch.json
        └── filesystem.json
```

## 一句话预告

> **写一个好用的 Skill 是手艺，把它封装成 Plugin 分享出去是工程。**

> 祝大家学习顺利
