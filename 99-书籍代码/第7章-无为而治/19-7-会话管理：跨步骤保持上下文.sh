# 第一次调用：分析代码结构
RESULT=$(claude -p "分析 src/ 的模块依赖关系" \
  --output-format json \
  --allowedTools "Read,Grep,Glob")

# 提取 session_id
SESSION_ID=$(echo "$RESULT" | jq -r '.session_id')

# 第二次调用：在上一轮分析的基础上继续
claude -p "基于刚才的分析，指出循环依赖问题" \
  --resume "$SESSION_ID" \
  --output-format text
