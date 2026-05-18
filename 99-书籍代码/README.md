# 《Claude Code 实战》书籍配套代码

本目录是《Claude Code 实战》（黄佳 著）全书 10 章配套代码片段的整理稿。

## 维护信息

- GitHub 仓库：https://github.com/huangjia2019/claude-code-engineering
- 本地公开仓目录：`/home/huangj2/Documents/05-Engineering/claude-code-engingeering`
- 私有讨论/书稿工作仓：`/home/huangj2/Documents/05-Engineering/claude-code-engingeering-private`

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

Claude Code 本身在 2025–2026 高速迭代，部分 API、字段名、配置结构在书稿付印后发生了变化，也有少量是我在书稿中写错或表述不严谨的地方，不是API迭代问题。下表所有条目都已**对照官方文档与实际跑过的 SDK 代码逐条核实**。

📮 **欢迎读者提出问题或纠错** → [在本仓库提 Issue](https://github.com/huangjia2019/claude-code-engineering/issues)

> 严重程度说明：
> - 🔴 **Critical**：代码必须修改
> - 🟠 **High**：代码会跑，但结果错误或与设计意图相反
> - 🟡 **Medium**：会以不标准的方式工作，或CC找不到对应的文件/字段


### 第1，2次印刷勘误

**下面列出的是第1，2次印刷时的错误，会在第3次印刷时改正**

### 第 1 章 · 登高望远

| 严重等级 | 位置 | 错误 | 修正 |
|:--:|:--|:--|:--|
| 🟠 High | §1.2.2 Hooks 配置 JSON 示例 | 用扁平结构 `{matcher, command, blocking: true}`，且 `blocking` 字段不存在，照抄会被 Claude Code 静默忽略 | 改为嵌套结构 `{matcher, hooks: [{type: "command", command: "..."}]}`；阻断由脚本退出码 2 实现，删除 `blocking` 字段 |
| 🔴 **Critical** | §1.2.4 Python SDK 示例 | `import claude_code` 和 `claude_code.query(...)` 不可运行，包名和调用方式都不对 | 正确写法：`from claude_agent_sdk import query, ClaudeAgentOptions`，且 `query()` 是 async generator，需要 `async for msg in query(...)` 消费 |
| 🟡 Medium | §1.2.1 记忆层级图 | 写作 `.claude.local.md`（前导点 + 全小写） | 实际文件名是 **`CLAUDE.local.md`**（大写 CLAUDE，无前导点），放在项目根目录 |

### 第 5 章 · 防微杜渐（Hooks）

| 严重等级 | 位置 | 错误 | 修正 |
|:--:|:--|:--|:--|
| 🟠 High | §5.10.1 Hook 环境变量表 + §5.3 `prettier` 示例 | 表里列出的 `CLAUDE_FILE_PATH`、`CLAUDE_TOOL_NAME`、`CLAUDE_SESSION_ID`、`CLAUDE_NOTIFICATION` 这四个环境变量**不存在**。`prettier --write "$CLAUDE_FILE_PATH"` 实际执行的是 `prettier --write ""`（空字符串） | 这四个字段实际通过 **stdin JSON** 传递。Hook 脚本应该：`INPUT=$(cat); FILE=$(echo "$INPUT" \| jq -r '.tool_input.file_path'); prettier --write "$FILE"`。Claude Code 真正暴露的 env 变量是 `CLAUDE_PROJECT_DIR` / `CLAUDE_PLUGIN_ROOT` / `CLAUDE_PLUGIN_DATA` / `CLAUDE_ENV_FILE` / `CLAUDE_EFFORT` / `CLAUDE_CODE_REMOTE`，其余字段都从 stdin 拿 |

### 第 6 章 · 海纳百川（MCP）

| 严重等级 | 位置 | 错误 | 修正 |
|:--:|:--|:--|:--|
| 🟠 High | §6.4.3 表格 + §6.4 关于 `.claude/settings.local.json` 存放凭证的说法 | 写"用户级 MCP 在 `~/.claude/` 目录"——但 Claude Code 不识别这个位置；以及"凭证放在 `.claude/settings.local.json`"——但 `mcpServers` 不是 settings.json 的合法顶级键，写进去会被静默忽略 | 用户级 MCP 在 **`~/.claude.json`** 顶级 `mcpServers`；项目级在 `<项目根>/.mcp.json`；项目私有（含凭证）在 `~/.claude.json` 的 `projects.<项目路径>.mcpServers`。最简单的做法是 `claude mcp add --scope user/project/local`，CLI 写到正确位置。注意 `claude mcp add` 默认 scope 是 `local` 不是 `user` |

### 第 7 章 · 无为而治（Headless）

| 严重等级 | 位置 | 错误 | 修正 |
|:--:|:--|:--|:--|
| 🔴 **Critical** | §7.4 GitHub Actions 完整示例最后一步 `grep -qi "critical"` | 用 `grep -qi "critical"` 作为"是否有严重问题"的 verdict 检查。`-i` 大小写不敏感 + "critical" 是 PR review 输出里**几乎必然出现的词**（"no critical issues"、"non-critical"、prompt 自身提示 critical 类问题），导致**workflow 几乎每次都被自己的检查触发 exit 1，看上去像永远在失败** | 让 Claude 在 prompt 末尾输出唯一 sentinel token，例如 `<VERDICT>request_changes</VERDICT>` / `<VERDICT>approved</VERDICT>`，下游用 `grep -qF "<VERDICT>request_changes</VERDICT>"` 判定。修复版可直接参考本仓库 [`08-Headless/projects/01-github-actions/.github/workflows/pr-review.yml`](../08-Headless/projects/01-github-actions/.github/workflows/pr-review.yml) |
| 🟠 High | §7.4 同一示例 `Post Review Comment` 步骤 | `const result = \`${{ steps.review.outputs.result }}\`;`——把 GitHub Actions 多行 markdown 输出**直接拼进 JS 模板字面量**。Code Review 输出常含反引号代码块和 `${...}`，会破坏 JS 解析 | 把 review 内容写到 `review.md` 文件，github-script 里 `fs.readFileSync('review.md', 'utf8')` 读取——不要走 `${{ }}` 拼字符串。多行变量通过 `env:` 块传递，避免命令注入 |
| 🟡 Medium | §7.9 本地 `review.sh` 脚本 | `RESULT=$(claude -p ... )` 在 `set -e` 下**不会**因为 claude 失败而退出脚本——bash 的命令替换屏蔽了子命令退出码，会静默生成空报告 | 改为显式落盘 + 检查：`if ! claude -p "$PROMPT" ... > /tmp/result.txt 2> /tmp/err.txt; then cat /tmp/err.txt; exit 1; fi; RESULT=$(cat /tmp/result.txt)` |

### 第 8 章 · 授人以渔（Agent SDK）

⚠️ 这一章的 Python SDK API 在书稿付印后变动较大，三个核心模式的所有代码示例都需要修正。下面三条都已在 `claude-agent-sdk==0.1.81` 实际 import 验证。

| 严重等级 | 位置 | 错误 | 修正 |
|:--:|:--|:--|:--|
| 🔴 **Critical** | §8.2 / §8.3 / §8.5 / §8.10 全部 `async for message in query(...)` 示例 | 访问 `message.type` 并按字符串判断分支——SDK 返回的是 **dataclass 实例**（`SystemMessage` / `AssistantMessage` / `UserMessage` / `ResultMessage`），它们**没有 `.type` 属性**，会抛 `AttributeError` | 用 `isinstance()` 判断：`if isinstance(message, AssistantMessage): for block in message.content: ...`；`SystemMessage` 通过 `message.subtype == "init"` 区分 |
| 🔴 **Critical** | §8.4 / §8.10 `ClaudeAgentOptions(...)` 实例化 | 用了不存在的字段：`append_system_prompt=...`（不存在）、`mcp_servers=[...]`（应为 dict 不是 list）、`no_session_persistence=False`（仅 CLI flag，不是 Options 字段） | append system prompt 改用 `system_prompt={"type": "preset", "preset": "claude_code", "append": "..."}`；`mcp_servers={"db": {"command": "python", "args": ["./db_server.py"]}}`；删除 `no_session_persistence` |
| 🔴 **Critical** | §8.6 `@tool` 装饰器示例 | 用 `@tool(name="...", description="...", parameters={...})`——kwarg 名错了 | 正确 kwarg 是 **`input_schema=`**：`@tool(name="query_db", description="...", input_schema={"sql": str})` |

### 第 9 章 · 集腋成裘（Plugins）

| 严重等级 | 位置 | 错误 | 修正 |
|:--:|:--|:--|:--|
| 🔴 **Critical** | §9.2 `hooks/hooks.json` 示例 | 用了扁平数组 `{"hooks": [{"event": "PreToolUse", "matcher": "Bash", "command": [...]}]}`——这个格式 Claude Code 不识别，hook 不会触发 | 用与 `settings.json` 完全相同的嵌套格式：`{"hooks": {"PreToolUse": [{"matcher": "Bash", "hooks": [{"type": "command", "command": "..."}]}]}}` |
| 🟡 Medium | §9.6 `marketplace.json` schema | 顶层缺 `owner` 对象，每个 plugin 用了 `repository` + `version` 平铺字段 | 真实 schema 顶层需要 **`owner: {name, email?}`**；每个 plugin 用 **`source`**（字符串路径或 `{source: "github", repo: "..."}` 对象）替代 `repository`。`version` 字段属于 `plugin.json`，不在 marketplace 入口里 |

---

如果你在书中发现其他问题，欢迎到 [Issues](https://github.com/huangjia2019/claude-code-engineering/issues) 提出。每条经核实的勘误都会更新到此表，并在新版印刷时同步修订。
