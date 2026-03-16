#!/bin/bash
# protect-files.sh
# 保护敏感文件不被修改
#
# 阻止对配置文件、密钥文件等敏感文件的写入操作

export PATH="$HOME/bin:/usr/local/bin:$PATH"
set -e

# 读取 stdin 输入
INPUT=$(cat)

# 提取文件路径
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""')

# 如果没有文件路径，允许执行
if [ -z "$FILE_PATH" ]; then
    echo '{"decision": "allow"}'
    exit 0
fi

echo "DEBUG: Checking file: $FILE_PATH" >&2

# 获取文件名
FILENAME=$(basename "$FILE_PATH")

# 受保护的文件模式
PROTECTED_PATTERNS=(
    ".env"
    ".env.local"
    ".env.production"
    ".env.development"
    "credentials.json"
    "secrets.yaml"
    "secrets.json"
    "config.production.json"
    "id_rsa"
    "id_ed25519"
    "*.pem"
    "*.key"
    "*.p12"
    "*.pfx"
    ".git/config"
    ".gitconfig"
    "package-lock.json"
    "yarn.lock"
    "pnpm-lock.yaml"
)

# 受保护的目录
PROTECTED_DIRS=(
    ".git/"
    "node_modules/"
    ".ssh/"
)

# 检查受保护的目录
for dir in "${PROTECTED_DIRS[@]}"; do
    if [[ "$FILE_PATH" == *"$dir"* ]]; then
        cat <<EOF
{
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "Cannot modify files in protected directory: $dir"
    }
}
EOF
        exit 2
    fi
done

# 检查受保护的文件模式
for pattern in "${PROTECTED_PATTERNS[@]}"; do
    # 处理通配符模式
    if [[ "$pattern" == \** ]]; then
        # 通配符匹配（如 *.pem）
        extension="${pattern#\*}"
        if [[ "$FILENAME" == *"$extension" ]]; then
            cat <<EOF
{
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "Cannot modify protected file type: $pattern"
    }
}
EOF
            exit 2
        fi
    else
        # 精确匹配
        if [[ "$FILENAME" == "$pattern" ]]; then
            cat <<EOF
{
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "Cannot modify protected file: $pattern"
    }
}
EOF
            exit 2
        fi
    fi
done

# 文件不受保护，允许执行
echo '{"decision": "allow"}'
exit 0
