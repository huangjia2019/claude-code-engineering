#!/bin/bash
# lint-check.sh
# 检查代码质量并向 Claude 反馈
#
# 作为 PostToolUse hook，在文件写入后运行 linter

export PATH="$HOME/bin:/usr/local/bin:$PATH"

# 读取 stdin 输入
INPUT=$(cat)

# 提取文件路径
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""')

# 如果没有文件路径，跳过
if [ -z "$FILE_PATH" ] || [ ! -f "$FILE_PATH" ]; then
    echo '{}'
    exit 0
fi

echo "DEBUG: Linting file: $FILE_PATH" >&2

# 获取文件扩展名
EXTENSION="${FILE_PATH##*.}"

# 存储 lint 结果
LINT_RESULT=""
LINT_PASSED=true

case "$EXTENSION" in
    js|jsx|ts|tsx)
        # 使用 ESLint
        if command -v npx &> /dev/null; then
            LINT_RESULT=$(npx eslint "$FILE_PATH" 2>&1) || LINT_PASSED=false
        fi
        ;;
    py)
        # 使用 flake8 或 pylint
        if command -v flake8 &> /dev/null; then
            LINT_RESULT=$(flake8 "$FILE_PATH" 2>&1) || LINT_PASSED=false
        elif command -v pylint &> /dev/null; then
            LINT_RESULT=$(pylint "$FILE_PATH" 2>&1) || LINT_PASSED=false
        fi
        ;;
    go)
        # 使用 golint 或 go vet
        if command -v golint &> /dev/null; then
            LINT_RESULT=$(golint "$FILE_PATH" 2>&1) || LINT_PASSED=false
        elif command -v go &> /dev/null; then
            LINT_RESULT=$(go vet "$FILE_PATH" 2>&1) || LINT_PASSED=false
        fi
        ;;
    *)
        # 未知文件类型，跳过
        echo '{}'
        exit 0
        ;;
esac

# 转义 JSON 特殊字符
LINT_RESULT_ESCAPED=$(echo "$LINT_RESULT" | jq -Rs '.')

if [ "$LINT_PASSED" = true ]; then
    # Lint 通过
    cat <<EOF
{
    "hookSpecificOutput": {
        "hookEventName": "PostToolUse",
        "additionalContext": "Lint check passed"
    }
}
EOF
else
    # Lint 失败，提供反馈让 Claude 修复
    cat <<EOF
{
    "hookSpecificOutput": {
        "hookEventName": "PostToolUse",
        "additionalContext": $LINT_RESULT_ESCAPED
    }
}
EOF
fi

exit 0
