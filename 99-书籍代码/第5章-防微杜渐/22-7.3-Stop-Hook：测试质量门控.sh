#!/bin/bash
# .claude/hooks/run-tests.sh

INPUT=$(cat)

# 防止无限循环：检查 stop_hook_active
STOP_ACTIVE=$(echo "$INPUT" | jq -r '.stop_hook_active // false')
if [ "$STOP_ACTIVE" = "true" ]; then
    exit 0  # 已经重试过一次，这次让 Claude 停下来
fi

# 切换到项目目录
if [ -n "$CLAUDE_PROJECT_DIR" ]; then
    cd "$CLAUDE_PROJECT_DIR"
fi

# 检测项目类型并运行测试
TEST_PASSED=true
TEST_RESULT=""

if [ -f "package.json" ] && grep -q '"test"' package.json; then
    TEST_RESULT=$(npm test 2>&1) || TEST_PASSED=false
elif [ -f "pyproject.toml" ] || [ -f "pytest.ini" ]; then
    TEST_RESULT=$(pytest 2>&1) || TEST_PASSED=false
elif [ -f "go.mod" ]; then
    TEST_RESULT=$(go test ./... 2>&1) || TEST_PASSED=false
else
    echo '{"hookSpecificOutput":{"additionalContext":"未检测到测试框架"}}'
    exit 0
fi

if [ "$TEST_PASSED" = true ]; then
    echo '{"hookSpecificOutput":{"additionalContext":"所有测试通过"}}'
else
    TEST_ESCAPED=$(echo "$TEST_RESULT" | head -50 | jq -Rs '.')
    cat <<EOF
{
    "decision": "block",
    "reason": "测试失败，请修复后再停止",
    "hookSpecificOutput": {
        "additionalContext": $TEST_ESCAPED
    }
}
EOF
fi
exit 0
