# 《Claude Code 实战》书籍配套代码

本目录是《Claude Code 实战》（黄佳 著）全书 10 章配套代码片段的整理稿。

## 章节概览

| 章节 | 主题 | 代码片段数 |
|:--|:--|:--:|
| [第1章-登高望远](第1章-登高望远/) | Claude Code 技术架构全景 | 11 |
| [第2章-温故知新](第2章-温故知新/) | 记忆系统 CLAUDE.md 工程实践 | 11 |
| [第3章-庖丁解牛](第3章-庖丁解牛/) | Skills 技能系统工程实践 | 37 |
| [第4章-分而治之](第4章-分而治之/) | 子智能体与任务委派 | 17 |
| [第5章-防微杜渐](第5章-防微杜渐/) | Hooks 事件驱动自动化 | 28 |
| [第6章-海纳百川](第6章-海纳百川/) | MCP 模型上下文协议 | 12 |
| [第7章-无为而治](第7章-无为而治/) | Headless 模式与 CI/CD 集成 | 34 |
| [第8章-授人以渔](第8章-授人以渔/) | Agent SDK 智能体开发套件 | 24 |
| [第9章-集腋成裘](第9章-集腋成裘/) | Plugins 插件生态 | 20 |
| [第10章-炉火纯青](第10章-炉火纯青/) | 工程化实战 | 31 |
| **合计** |  | **225** |

## 使用说明

- 每个章节子目录下：
  - `NN-<前导小标题>.<ext>` — 按出现顺序编号的代码片段，可直接 copy-paste
  - `README.md` — 该章节片段索引
- 大部分片段是**配置或示例**，不构成可独立运行的项目。可运行的完整项目请见本仓库各章 `projects/` 子目录（如 `03-SubAgents/projects/`、`07-MCP/projects/`）。

## 与课程的对应

| 书章节 | 课程对应讲次 |
|:--|:--|
| 第1章 登高望远 | 第 1 讲 |
| 第2章 温故知新 | 第 2 讲 |
| 第3章 庖丁解牛 (Skills) | 第 9-14 讲（Skills 专题 6 讲） |
| 第4章 分而治之 (SubAgents) | 第 3-7 讲（子代理专题 5 讲） |
| 第5章 防微杜渐 (Hooks) | 第 15-16 讲 |
| 第6章 海纳百川 (MCP) | 第 17 讲 |
| 第7章 无为而治 (Headless) | 第 19 讲 |
| 第8章 授人以渔 (SDK) | 第 21-22 讲 |
| 第9章 集腋成裘 (Plugins) | 第 23 讲 |
| 第10章 炉火纯青 | 课程加餐与综合实践 |

---

## 勘误与改进

Claude Code 本身在 2025–2026 高速迭代，部分 API、字段名、配置结构在书稿付印后发生了变化，也有少量我在书稿中写错或表述不严谨的地方。下表列出**真正会影响读者跑代码或踩坑**的内容，供对照修订。

📮 **欢迎读者提出问题或纠错** → [在本仓库提 Issue](https://github.com/huangjia2019/claude-code-engineering/issues)

> 严重程度说明：
> - 🔴 **Critical**：代码按书中写法**几乎肯定跑不通**，必须改
> - 🟠 **High**：代码会跑，但**结果错误或与设计意图相反**
> - 🟡 **Medium**：会**静默地以错误方式工作**，或读者可能找不到对应的文件/字段

### 第 1 章 · 登高望远

| 严重 | 位置 | 错误 | 修正 |
|:--:|:--|:--|:--|
| 🟠 High | §1.2.2 Hooks 配置 JSON 示例 | 用扁平结构 `{matcher, command, blocking: true}`，且 `blocking` 字段不存在，照抄会被 Claude Code 静默忽略 | 改为嵌套结构 `{matcher, hooks: [{type: "command", command: "..."}]}`；阻断由脚本退出码 2 实现，删除 `blocking` 字段 |
| 🟠 High | §1.2.4 Python SDK 示例 | `import claude_code` 和 `claude_code.query(...)` 不可运行，包名和调用方式都不对 | 正确写法：`from claude_agent_sdk import query, ClaudeAgentOptions`，且 `query()` 是 async generator，需要 `async for msg in query(...)` 消费 |
| 🟡 Medium | §1.2.1 记忆层级图 | 写作 `.claude.local.md`（前导点 + 全小写） | 实际文件名是 **`CLAUDE.local.md`**（大写 CLAUDE，无前导点），放在项目根目录 |

### 第 3 章 · 庖丁解牛（Skills）

| 严重 | 位置 | 错误 | 修正 |
|:--:|:--|:--|:--|
| 🟡 Medium | §3.7 / §3.9 位置参数表格 | 列出 `$ARGUMENTS[0]`、`$0`、`$1`、`$2` 等"索引语法" | Slash Command 只支持整串 `$ARGUMENTS` 替换，没有索引/位置参数语法；如需拆分，在 prompt 里让 Claude 自行解析 |

### 第 4 章 · 分而治之（Sub-Agents）

| 严重 | 位置 | 错误 | 修正 |
|:--:|:--|:--|:--|
| 🟡 Medium | §4.3 子代理 frontmatter | 写了 `permissionMode: plan` 和 `skills:` 字段——这两个字段都不是子代理 frontmatter 的合法 key | 子代理 frontmatter 只支持 `name` / `description` / `tools` / `model`；plan-mode 的行为放在 prose 描述，Skills 不需要在子代理里 preload |

### 第 5 章 · 防微杜渐（Hooks）

| 严重 | 位置 | 错误 | 修正 |
|:--:|:--|:--|:--|
| 🟠 High | §5.2 Hook 事件目录 | 出现的 `PostToolUseFailure` / `PermissionRequest` / `TeammateIdle` / `ConfigChange` / `TaskCompleted` / `WorktreeCreate` 等事件名**实际不存在**，写进 settings.json 会被静默忽略 | Claude Code 真实的 Hook 事件只有 9 个：`PreToolUse`、`PostToolUse`、`UserPromptSubmit`、`Notification`、`Stop`、`SubagentStop`、`PreCompact`、`SessionStart`、`SessionEnd` |
| 🟠 High | §5.10.1 Hook 环境变量表 + §5.3 `prettier` 示例 | 用 `$CLAUDE_FILE_PATH`、`$CLAUDE_TOOL_NAME`、`$CLAUDE_SESSION_ID` 等 env 变量。这些变量**不存在**——`prettier --write "$CLAUDE_FILE_PATH"` 实际执行的是 `prettier --write ""` | Hook 脚本通过 **stdin JSON** 拿上下文：`INPUT=$(cat); FILE=$(echo "$INPUT" \| jq -r '.tool_input.file_path')`。唯一真实的 env 变量是 `CLAUDE_PROJECT_DIR`（和 plugin hooks 的 `CLAUDE_PLUGIN_ROOT`） |
| 🟡 Medium | §5.4 / §5.9 Hook 类型与字段 | 写了 `type: "prompt"` / `type: "agent"` 两种 hook 类型，以及 `async: true` 字段——都不存在 | Hook handler 只支持 `type: "command"`；hooks 都是同步执行（在 `timeout` 内）。若需"LLM 评估型"逻辑，把 `command` 设为调用 `claude -p` 的脚本即可 |

### 第 6 章 · 海纳百川（MCP）

| 严重 | 位置 | 错误 | 修正 |
|:--:|:--|:--|:--|
| 🟠 High | §6.4.3 用户级 MCP 配置位置 | 描述位于 `~/.claude/` 目录下（例如 `~/.claude/.mcp.json`），但这个路径 Claude Code 不识别 | 用户级 MCP 必须写在 **`~/.claude.json`** 顶级的 `mcpServers` 字段；项目级在 `<项目根>/.mcp.json`；项目本地（私有）在 `~/.claude.json` 的 `projects.<项目路径>.mcpServers`。注意 `claude mcp add` **默认 scope 是 `local` 不是 `user`**，加 `--scope user` 才会全局生效 |

### 第 7 章 · 无为而治（Headless）

| 严重 | 位置 | 错误 | 修正 |
|:--:|:--|:--|:--|
| 🔴 **Critical** | §7.4 GitHub Actions 完整示例最后一步 `grep -qi "critical"` | 用 `grep -qi "critical"` 作为"是否有严重问题"的 verdict 检查。`-i` 大小写不敏感 + "critical" 是 PR review 输出里**几乎必然出现的词**（"no critical issues"、"non-critical"、prompt 自身提示 critical 类问题），导致**workflow 几乎每次都被自己的检查触发 exit 1，看上去像永远在失败** | 让 Claude 在 prompt 末尾输出唯一 sentinel token，例如 `<VERDICT>request_changes</VERDICT>` / `<VERDICT>approved</VERDICT>`，下游 `grep -qF "<VERDICT>request_changes</VERDICT>"` 判定。详见本仓库 [`08-Headless/projects/01-github-actions/.github/workflows/pr-review.yml`](../08-Headless/projects/01-github-actions/.github/workflows/pr-review.yml)（已修复版本） |
| 🟠 High | §7.4 同一示例 `Post Review Comment` 步骤 | `const result = \`${{ steps.review.outputs.result }}\`;`——把 GitHub Actions 多行 markdown 输出**直接拼进 JS 模板字面量**。Code Review 输出常含反引号代码块和 `${...}`，会破坏 JS 解析 | 把 review 内容写到 `review.md` 文件，github-script 里 `fs.readFileSync('review.md', 'utf8')` 读取——不要走 `${{ }}` 拼字符串。同时多行变量通过 `env:` 块传递，避免命令注入 |
| 🟡 Medium | §7.9 本地 `review.sh` 脚本 | `RESULT=$(claude -p ... )` 在 `set -e` 下**不会**因为 claude 失败而退出脚本——bash 的命令替换屏蔽了子命令退出码，会静默生成空报告 | 改为显式落盘 + 检查：`if ! claude -p "$PROMPT" ... > /tmp/result.txt 2> /tmp/err.txt; then cat /tmp/err.txt; exit 1; fi; RESULT=$(cat /tmp/result.txt)` |

### 第 8 章 · 授人以渔（Agent SDK）

⚠️ 这一章的 Python SDK API 在书稿付印后变动较大，几乎所有代码示例都需要小幅修正。

| 严重 | 位置 | 错误 | 修正 |
|:--:|:--|:--|:--|
| 🔴 **Critical** | §8.2 / §8.3 / §8.5 / §8.10 全部 `async for message in query(...)` 示例 | 访问 `message.type` 和按字符串判断分支——SDK 返回的是 **dataclass 实例**（`SystemMessage` / `AssistantMessage` / `UserMessage` / `ResultMessage`），它们**没有 `.type` 属性**，会抛 `AttributeError` | 用 `isinstance()` 判断：`if isinstance(message, AssistantMessage): for block in message.content: ...`；`SystemMessage` 通过 `message.subtype == "init"` 区分 |
| 🔴 **Critical** | §8.4 / §8.10 `ClaudeAgentOptions(...)` 实例化 | 用了不存在的字段：`append_system_prompt=...`（不存在）、`mcp_servers=[...]`（应为 dict 不是 list）、`no_session_persistence=False`（仅 CLI flag，不是 Options 字段） | `append` 用 `system_prompt={"type": "preset", "preset": "claude_code", "append": "..."}`；`mcp_servers={"db": {"command": "python", "args": ["./db_server.py"]}}`；删除 `no_session_persistence` |
| 🔴 **Critical** | §8.6 `@tool` 装饰器示例 | 用 `@tool(name="...", description="...", parameters={...})`——kwarg 写错了 | 正确 kwarg 是 **`input_schema=`**：`@tool(name="query_db", description="...", input_schema={"sql": str})` |

### 第 9 章 · 集腋成裘（Plugins）

| 严重 | 位置 | 错误 | 修正 |
|:--:|:--|:--|:--|
| 🔴 **Critical** | §9.2 `hooks/hooks.json` 示例 | 用了扁平数组 `{"hooks": [{"event": "PreToolUse", "matcher": "Bash", "command": [...]}]}`——这个格式 Claude Code 不识别，hook 不会触发 | 用与 `settings.json` 相同的嵌套格式：`{"hooks": {"PreToolUse": [{"matcher": "Bash", "hooks": [{"type": "command", "command": "..."}]}]}}`。§10.2 line 189-198 的写法是对的，可参照 |
| 🟡 Medium | §9.6 `marketplace.json` schema | 每个 plugin entry 只有 `name`/`description`/`repository`/`version` | 真实 schema 顶层需要 `owner: {name, email}` 字段；每个 plugin 用 `source: {source: "github", repo: "..."}` 对象，而不是 `repository` + `version` 平铺 |
| 🟡 Medium | §9.3 `/plugin install <github-url>` 语法 | 直接写 `/plugin install github.com/user/plugin` | 实际是两步：先 `/plugin marketplace add github.com/user/plugin` 把仓库注册成 marketplace，再 `/plugin install <plugin-name>@<marketplace-name>` |

---

如果你在书中发现其他问题，欢迎到 [Issues](https://github.com/huangjia2019/claude-code-engineering/issues) 提出。每条经核实的勘误都会更新到此表，并在新版印刷时同步修订。
