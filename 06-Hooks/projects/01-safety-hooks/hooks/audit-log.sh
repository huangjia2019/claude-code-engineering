#!/bin/bash
# audit-log.sh
# 记录所有工具调用到审计日志
#
# 作为 PostToolUse hook，记录每次工具调用的详细信息

export PATH="$HOME/bin:/usr/local/bin:$PATH"

# 读取 stdin 输入
INPUT=$(cat)

# 确定日志目录
if [ -n "$CLAUDE_PROJECT_DIR" ]; then
    LOG_DIR="$CLAUDE_PROJECT_DIR/.claude/logs"
else
    LOG_DIR="./.claude/logs"
fi

# 创建日志目录
mkdir -p "$LOG_DIR"

# 日志文件（按日期分割）
LOG_FILE="$LOG_DIR/audit-$(date +%Y-%m-%d).log"

# 提取关键信息
TIMESTAMP=$(date -Iseconds)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // "unknown"')
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // "unknown"')

# 提取工具输入（简化版本）
TOOL_INPUT=$(echo "$INPUT" | jq -c '.tool_input // {}')

# 提取工具响应状态
TOOL_SUCCESS=$(echo "$INPUT" | jq -r '.tool_response.success // true')

# 写入日志
cat >> "$LOG_FILE" << EOF
================================================================================
Timestamp: $TIMESTAMP
Session: $SESSION_ID
Tool: $TOOL_NAME
Success: $TOOL_SUCCESS
Input: $TOOL_INPUT
================================================================================

EOF

# 输出空 JSON（不阻止后续操作）
echo '{}'
