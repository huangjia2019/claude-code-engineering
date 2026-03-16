#!/bin/bash
# block-dangerous.sh
# 阻止危险的 Bash 命令
#
# 检查命令是否匹配危险模式，如果匹配则阻止执行

export PATH="$HOME/bin:/usr/local/bin:$PATH"

set -e

# 读取 stdin 输入
INPUT=$(cat)

# 提取命令
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // ""')

# 调试输出（到 stderr）
echo "DEBUG: Checking command: $COMMAND" >&2

# 危险命令模式
DANGEROUS_PATTERNS=(
    "rm -rf /"
    "rm -rf ~"
    "rm -rf \$HOME"
    "rm -rf /*"
    "> /dev/sd"
    "mkfs."
    "dd if="
    ":(){:|:&};:"
    "chmod -R 777 /"
    "chown -R"
    "git push --force origin main"
    "git push --force origin master"
    "git reset --hard origin"
    "DROP DATABASE"
    "DROP TABLE"
    "TRUNCATE"
    "curl.*| sh"
    "curl.*| bash"
    "wget.*| sh"
    "wget.*| bash"
)

# 检查每个危险模式
for pattern in "${DANGEROUS_PATTERNS[@]}"; do
    if [[ "$COMMAND" == *"$pattern"* ]]; then
        echo "BLOCKED: Command matches dangerous pattern: $pattern" >&2
        cat <<EOF
{
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "Blocked dangerous command pattern: $pattern. This command could cause irreversible damage."
    }
}
EOF
        exit 2
    fi
done

# 命令安全，允许执行
echo '{"decision": "allow"}'
exit 0
