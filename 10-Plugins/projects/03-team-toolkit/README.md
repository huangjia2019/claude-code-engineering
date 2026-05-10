# Team Toolkit

团队标准开发工具包，把第 23 讲讲到的五种插件组件（Commands / Agents / Skills / Hooks / MCP）整合成一个完整的、可安装的团队能力包。

## 目录结构

```
team-toolkit/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── review.md       # /review 代码审查
│   ├── test.md         # /test 测试运行
│   └── deploy.md       # /deploy 部署
├── agents/
│   ├── security-scanner.md  # 安全扫描代理
│   └── quick-fix.md         # 快速修复代理
├── skills/
│   └── react-patterns/
│       ├── SKILL.md
│       └── chapters/        # 渐进式披露章节
│           ├── hooks.md
│           ├── context.md
│           └── performance.md
├── hooks/
│   ├── hooks.json
│   ├── check-bash.sh        # 危险命令拦截
│   └── auto-format.sh       # 文件写入后自动格式化
├── .mcp.json                # postgres / github / filesystem
└── README.md
```

## 安装

把这个目录作为 Git 仓库发布，然后：

```bash
/plugin install team-toolkit@<your-org>
```

或本地开发时直接通过 `--plugin-dir` 指向当前目录。

## 功能

### 命令

| 命令 | 说明 |
|------|------|
| `/review [target]` | 代码审查（覆盖 TS / React / 安全 / 测试维度）|
| `/test [scope]` | 运行测试，失败时自动分析原因 |
| `/deploy [env]` | 部署到 staging / production |

### 子代理

| 代理 | 说明 | 模型 |
|------|------|------|
| `security-scanner` | 安全漏洞扫描（只读权限）| sonnet |
| `quick-fix` | 拼写错误、缺 import 等小问题快修 | haiku |

### Skills

| Skill | 说明 |
|-------|------|
| `react-patterns` | React 最佳实践（Hooks / Context / 性能优化分章节加载）|

### Hooks

- `PreToolUse(Bash)` → 拦截 `rm -rf /`、`chmod 777`、`curl ... | sh` 等危险模式
- `PostToolUse(Write|Edit)` → 按文件扩展名自动调用 black / prettier / gofmt

### MCP 服务器

| 服务器 | 说明 | 需要的环境变量 |
|--------|------|--------------|
| `postgres` | 数据库查询 | `DATABASE_URL` |
| `github` | GitHub API | `GITHUB_TOKEN` |
| `filesystem` | 文件系统访问 | `ALLOWED_PATHS`（默认 `~/projects`）|

## 环境变量

```bash
export DATABASE_URL="postgres://user:pass@localhost/db"
export GITHUB_TOKEN="ghp_xxxxxxxxxxxx"
```

## 与第 23 讲的对应关系

这个项目是第 23 讲"实战项目——团队能力包"的可运行版本。讲稿里散落的 plugin.json、各组件文件、Hook 脚本、MCP 配置在这里被按规范组织起来——读完讲稿后，clone 下来直接安装就能跑。

## 使脚本可执行

首次使用前，给 Hook 脚本加执行权限：

```bash
chmod +x hooks/check-bash.sh hooks/auto-format.sh
```

## 更新日志

### v2.0.0
- 新增 `/deploy` 命令
- 新增 `security-scanner` 代理
- 改进 `/review` 输出格式

### v1.0.0
- 初始版本

## 许可证

MIT
