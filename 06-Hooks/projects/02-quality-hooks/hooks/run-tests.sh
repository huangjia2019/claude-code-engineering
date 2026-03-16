#!/bin/bash
# run-tests.sh
# 在 Claude 完成时自动运行测试
#
# 作为 Stop hook，确保所有测试通过

export PATH="$HOME/bin:/usr/local/bin:$PATH"
set -e

echo "DEBUG: Running tests before stopping..." >&2

# 确定项目目录
if [ -n "$CLAUDE_PROJECT_DIR" ]; then
    cd "$CLAUDE_PROJECT_DIR"
fi

# 检测项目类型并运行相应的测试
RUN_TESTS=false
TEST_RESULT=""
TEST_PASSED=true

# Node.js 项目
if [ -f "package.json" ]; then
    RUN_TESTS=true
    echo "DEBUG: Detected Node.js project" >&2

    # 检查是否有测试脚本
    if grep -q '"test"' package.json; then
        TEST_RESULT=$(npm test 2>&1) || TEST_PASSED=false
    else
        TEST_RESULT="No test script found in package.json"
        TEST_PASSED=true  # 没有测试不算失败
    fi

# Python 项目
elif [ -f "pytest.ini" ] || [ -f "setup.py" ] || [ -f "pyproject.toml" ]; then
    RUN_TESTS=true
    echo "DEBUG: Detected Python project" >&2

    if command -v pytest &> /dev/null; then
        TEST_RESULT=$(pytest 2>&1) || TEST_PASSED=false
    elif command -v python &> /dev/null; then
        TEST_RESULT=$(python -m pytest 2>&1) || TEST_PASSED=false
    else
        TEST_RESULT="pytest not found"
        TEST_PASSED=true
    fi

# Go 项目
elif [ -f "go.mod" ]; then
    RUN_TESTS=true
    echo "DEBUG: Detected Go project" >&2

    TEST_RESULT=$(go test ./... 2>&1) || TEST_PASSED=false

# Rust 项目
elif [ -f "Cargo.toml" ]; then
    RUN_TESTS=true
    echo "DEBUG: Detected Rust project" >&2

    TEST_RESULT=$(cargo test 2>&1) || TEST_PASSED=false
fi

# 如果没有检测到测试框架
if [ "$RUN_TESTS" = false ]; then
    echo '{}'
    exit 0
fi

# 转义 JSON 特殊字符
TEST_RESULT_ESCAPED=$(echo "$TEST_RESULT" | head -50 | jq -Rs '.')

if [ "$TEST_PASSED" = true ]; then
    # 测试通过，允许停止
    echo '{"decision": "approve", "reason": "All tests passed."}'
else
    # 测试失败，让 Claude 继续修复
    cat <<EOF
{
    "decision": "block",
    "reason": "Tests are failing. Please fix the issues before stopping.",
    "continue": true,
    "systemMessage": $TEST_RESULT_ESCAPED
}
EOF
fi

exit 0
