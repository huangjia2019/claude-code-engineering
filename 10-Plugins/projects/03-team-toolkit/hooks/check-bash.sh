#!/bin/bash
# 检查 Bash 命令是否安全

# 从 stdin 读取输入
INPUT=$(cat)

# 提取命令
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# 危险模式列表
DANGEROUS_PATTERNS=(
    "rm -rf /"
    "rm -rf ~"
    "sudo rm"
    "> /dev/"
    "chmod 777"
    "curl.*|.*sh"
    "wget.*|.*sh"
)

# 检查每个危险模式
for pattern in "${DANGEROUS_PATTERNS[@]}"; do
    if echo "$COMMAND" | grep -qE "$pattern"; then
        # 输出拒绝决定
        cat << EOF
{
  "decision": "deny",
  "reason": "Blocked potentially dangerous command pattern: $pattern"
}
EOF
        exit 0
    fi
done

# 允许执行
echo '{"decision": "allow"}'
