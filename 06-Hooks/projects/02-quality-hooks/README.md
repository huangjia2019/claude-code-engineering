# 示例项目：代码质量 Hooks

这个项目展示如何使用 Hooks 自动化代码质量检查。

## 目录结构

```
02-quality-hooks/
├── .claude/
│   └── settings.json       # Hook 配置
├── hooks/
│   ├── auto-format.sh      # 自动格式化
│   ├── lint-check.sh       # Lint 检查
│   └── run-tests.sh        # 自动测试
└── README.md
```

## 包含的 Hooks

### 1. auto-format.sh (PostToolUse)

文件写入后自动格式化：

| 文件类型 | 格式化工具 |
|----------|-----------|
| `.js`, `.jsx`, `.ts`, `.tsx`, `.json`, `.md`, `.css` | Prettier |
| `.py` | Black |
| `.go` | gofmt |
| `.rs` | rustfmt |

**工作流程：**
```
Claude 写入文件 → PostToolUse 触发 → 检测文件类型 → 运行格式化工具
```

### 2. lint-check.sh (PostToolUse)

文件写入后检查代码质量：

| 文件类型 | Lint 工具 |
|----------|-----------|
| `.js`, `.jsx`, `.ts`, `.tsx` | ESLint |
| `.py` | flake8 / pylint |
| `.go` | golint / go vet |

**反馈机制：**
- Lint 通过：返回成功消息
- Lint 失败：返回错误详情，Claude 可以看到并修复

### 3. run-tests.sh (Stop)

Claude 完成任务时自动运行测试：

| 项目类型 | 检测文件 | 测试命令 |
|----------|----------|----------|
| Node.js | `package.json` | `npm test` |
| Python | `pytest.ini`, `pyproject.toml` | `pytest` |
| Go | `go.mod` | `go test ./...` |
| Rust | `Cargo.toml` | `cargo test` |

**关键功能：**
- 测试通过 → 允许停止
- 测试失败 → 返回 `continue: true`，让 Claude 继续修复

## 配置说明

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          { "command": "./hooks/auto-format.sh" },
          { "command": "./hooks/lint-check.sh" }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          { "command": "./hooks/run-tests.sh" }
        ]
      }
    ]
  }
}
```

## Hook 链执行顺序

对于 `Write` 操作：
```
1. Claude 写入文件
2. auto-format.sh 运行（格式化代码）
3. lint-check.sh 运行（检查代码质量）
4. 结果反馈给 Claude
```

对于任务完成：
```
1. Claude 准备停止
2. run-tests.sh 运行
3. 如果测试失败，Claude 继续工作
4. 如果测试通过，正常停止
```

## 工作流示例

### 场景：修复 Bug

1. 用户：「修复 login.js 中的认证 bug」
2. Claude 编辑 `login.js`
3. `auto-format.sh` 自动格式化代码
4. `lint-check.sh` 发现一个 ESLint 警告
5. Claude 看到反馈，修复警告
6. Claude 准备停止
7. `run-tests.sh` 运行测试
8. 测试失败：「LoginTest.testInvalidPassword failed」
9. Claude 收到 `continue: true`，继续修复
10. 再次尝试停止
11. 测试通过，任务完成

## 学习要点

1. **Hook 链**：多个 Hook 按顺序执行
2. **PostToolUse 反馈**：通过 `hookSpecificOutput` 向 Claude 提供信息
3. **Stop Hook**：质量门控，确保任务完成质量
4. **continue: true**：让 Claude 继续工作直到满足条件
5. **工具检测**：使用 `command -v` 检查工具是否存在
6. **项目类型检测**：通过配置文件判断项目类型

## 前置要求

根据项目类型，需要安装相应工具：

**Node.js 项目：**
```bash
npm install -D prettier eslint
```

**Python 项目：**
```bash
pip install black flake8 pytest
```

**Go 项目：**
```bash
go install golang.org/x/lint/golint@latest
```

## 扩展建议

- 添加类型检查（TypeScript `tsc`）
- 集成安全扫描（npm audit, bandit）
- 添加代码覆盖率检查
- 发送 Slack/邮件通知
