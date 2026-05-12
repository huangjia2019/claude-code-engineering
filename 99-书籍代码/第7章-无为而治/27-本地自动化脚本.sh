#!/bin/bash
# review.sh — 本地代码审查脚本
set -e

TARGET=${1:-.}

# 前置检查
[ -z "$ANTHROPIC_API_KEY" ] && echo "Error: ANTHROPIC_API_KEY not set" && exit 1
command -v claude &> /dev/null || { echo "Error: Claude Code not installed"; exit 1; }

echo "Starting review for: $TARGET"

# 构建文件列表
if [ -d "$TARGET" ]; then
    FILES=$(find "$TARGET" -type f \( -name "*.ts" -o -name "*.js" -o -name "*.py" \) | head -20)
else
    FILES="$TARGET"
fi

# 运行审查
# 注意：bash `set -e` 不会因为命令替换 `$(...)` 中的命令失败而退出，
# 所以必须把输出落盘后显式检查 $?，否则 claude 失败时 RESULT 为空，
# 脚本会静默生成一份空报告。
if ! claude -p "审查以下文件的代码质量和安全问题：
$FILES

输出格式：Markdown 审查报告，每个问题附文件名和行号。" \
    --output-format text \
    --max-turns 15 \
    --max-budget-usd 0.50 \
    --allowedTools Read,Grep,Glob > /tmp/review-result-$$.txt 2> /tmp/review-err-$$.txt; then
    echo "Error: claude command failed"
    cat /tmp/review-err-$$.txt
    rm -f /tmp/review-result-$$.txt /tmp/review-err-$$.txt
    exit 1
fi
RESULT=$(cat /tmp/review-result-$$.txt)
rm -f /tmp/review-result-$$.txt /tmp/review-err-$$.txt

if [ -z "$RESULT" ]; then
    echo "Error: claude returned empty result"
    exit 1
fi

# 保存报告
REPORT="review-$(date +%Y%m%d-%H%M%S).md"
echo -e "# Code Review Report\n\n**Date**: $(date)\n**Target**: $TARGET\n\n---\n\n$RESULT" > "$REPORT"
echo "Report saved: $REPORT"
