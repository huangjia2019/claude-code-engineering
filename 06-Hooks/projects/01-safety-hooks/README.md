# 示例项目：安全 Hooks

这个项目展示如何使用 Hooks 保护系统安全。

## 目录结构

```
01-safety-hooks/
├── .claude/
│   └── settings.json       # Hook 配置
├── hooks/
│   ├── block-dangerous.sh  # 阻止危险命令
│   ├── protect-files.sh    # 保护敏感文件
│   └── audit-log.sh        # 审计日志
└── README.md
```

## 包含的 Hooks

### 1. block-dangerous.sh (PreToolUse)

拦截危险的 Bash 命令：

**阻止的命令模式：**
- `rm -rf /` - 删除根目录
- `rm -rf ~` - 删除用户目录
- `git push --force origin main` - 强制推送到主分支
- `git reset --hard origin` - 硬重置
- `curl ... | sh` - 远程执行脚本
- `DROP DATABASE` / `TRUNCATE` - 危险 SQL

**工作原理：**
```
用户请求 → Claude 生成命令 → PreToolUse Hook 检查 → 允许/拒绝
```

### 2. protect-files.sh (PreToolUse)

保护敏感文件不被修改：

**保护的文件：**
- `.env*` - 环境变量
- `credentials.json` - 凭证文件
- `*.pem`, `*.key` - 密钥文件
- `package-lock.json`, `yarn.lock` - 锁文件
- `.git/` 目录

**触发场景：**
- Claude 尝试使用 Write 工具
- Claude 尝试使用 Edit 工具

### 3. audit-log.sh (PostToolUse)

记录所有工具调用：

**日志位置：** `.claude/logs/audit-YYYY-MM-DD.log`

**记录内容：**
- 时间戳
- 会话 ID
- 工具名称
- 执行成功/失败
- 工具输入参数

## 配置说明

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",           // 匹配 Bash 工具
        "hooks": [{ "command": "./hooks/block-dangerous.sh" }]
      },
      {
        "matcher": "Write",          // 匹配 Write 工具
        "hooks": [{ "command": "./hooks/protect-files.sh" }]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "*",              // 匹配所有工具
        "hooks": [{ "command": "./hooks/audit-log.sh" }]
      }
    ]
  }
}
```

## 测试方法

### 测试危险命令阻止

```bash
# 手动测试
echo '{"tool_input": {"command": "rm -rf /"}}' | ./hooks/block-dangerous.sh
# 预期：返回 deny 决策

echo '{"tool_input": {"command": "git status"}}' | ./hooks/block-dangerous.sh
# 预期：返回 allow 决策
```

### 测试文件保护

```bash
echo '{"tool_input": {"file_path": ".env"}}' | ./hooks/protect-files.sh
# 预期：返回 deny 决策

echo '{"tool_input": {"file_path": "src/app.js"}}' | ./hooks/protect-files.sh
# 预期：返回 allow 决策
```

## 学习要点

1. **PreToolUse 拦截**：在工具执行前进行检查
2. **模式匹配**：使用数组存储危险模式
3. **退出码**：`exit 2` 表示阻止执行
4. **JSON 响应**：返回结构化的决策和原因
5. **审计日志**：PostToolUse 记录所有操作
6. **调试输出**：使用 `>&2` 输出到 stderr

## 扩展建议

- 添加 IP 白名单检查
- 集成外部安全扫描工具
- 发送安全告警通知
- 添加用户确认机制
