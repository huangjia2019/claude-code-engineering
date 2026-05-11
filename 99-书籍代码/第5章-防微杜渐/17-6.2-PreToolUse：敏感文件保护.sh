#!/bin/bash
# .claude/hooks/protect-files.sh

set -e
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""')

if [ -z "$FILE_PATH" ]; then
    echo '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"allow"}}'
    exit 0
fi

FILENAME=$(basename "$FILE_PATH")

# 受保护的文件名模式
PROTECTED_FILES=(".env" ".env.local" ".env.production" "credentials.json"
    "secrets.yaml" "secrets.json" "id_rsa" "id_ed25519")

# 受保护的扩展名
PROTECTED_EXTENSIONS=("pem" "key" "p12" "pfx")

# 受保护的目录
PROTECTED_DIRS=(".git/" ".ssh/" "node_modules/")

# 检查目录
for dir in "${PROTECTED_DIRS[@]}"; do
    if [[ "$FILE_PATH" == *"$dir"* ]]; then
        cat <<EOF
{
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "不允许修改受保护目录中的文件: $dir"
    }
}
EOF
        exit 2
    fi
done

# 检查文件名
for name in "${PROTECTED_FILES[@]}"; do
    if [[ "$FILENAME" == "$name" ]]; then
        cat <<EOF
{
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "不允许修改敏感文件: $name"
    }
}
EOF
        exit 2
    fi
done

# 检查扩展名
EXT="${FILENAME##*.}"
for ext in "${PROTECTED_EXTENSIONS[@]}"; do
    if [[ "$EXT" == "$ext" ]]; then
        cat <<EOF
{
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "不允许修改密钥类文件: *.$ext"
    }
}
EOF
        exit 2
    fi
done

echo '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"allow"}}'
exit 0
