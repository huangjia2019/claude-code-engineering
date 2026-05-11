#!/bin/bash
# .claude/hooks/security-check.sh
INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name')
TOOL_INPUT=$(echo "$INPUT" | jq -r '.tool_input')

if [ "$TOOL" = "Bash" ]; then
  COMMAND=$(echo "$TOOL_INPUT" | jq -r '.command')
  # 检查危险命令
  if echo "$COMMAND" | grep -qE 'rm\s+-rf\s+/|sudo\s+rm|chmod\s+777|curl.*\|\s*bash'; then
    echo '{"decision": "block", "reason": "危险命令被安全策略拦截"}' >&2
    exit 2
  fi
fi

exit 0
