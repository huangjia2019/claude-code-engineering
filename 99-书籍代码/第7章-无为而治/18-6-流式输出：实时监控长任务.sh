claude -p "分析整个 src/ 目录的架构问题" \
  --output-format stream-json \
  --allowedTools "Read,Grep,Glob" | while read -r line; do
    TYPE=$(echo "$line" | jq -r '.type // ""')

    case "$TYPE" in
      "system")
        echo "[INIT] 模型: $(echo "$line" | jq -r '.model // "unknown"')"
        ;;
      "assistant")
        # 提取 Claude 的文本输出
        TEXT=$(echo "$line" | jq -r '.message.content[0].text // ""')
        [ -n "$TEXT" ] && echo "[CLAUDE] $TEXT"
        ;;
      "result")
        COST=$(echo "$line" | jq -r '.total_cost_usd // 0')
        TURNS=$(echo "$line" | jq -r '.num_turns // 0')
        echo "[DONE] 完成！$TURNS 轮，费用: \$$COST"
        ;;
    esac
done
