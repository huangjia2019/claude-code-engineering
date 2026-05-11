# CI/CD 中的代码审查：只需要读权限
claude -p "审查 PR 变更" \
  --allowedTools "Read" "Grep" "Glob" \
  --max-turns 5

# 允许特定的 Bash 命令模式
claude -p "运行测试并分析结果" \
  --allowedTools "Read" "Grep" "Bash(npm run test *)" "Bash(npm run lint)"
