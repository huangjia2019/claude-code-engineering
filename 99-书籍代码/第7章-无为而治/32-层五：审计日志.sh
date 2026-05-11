# JSON 输出天然包含审计信息
claude -p "任务" --output-format json | tee -a /var/log/claude-audit.jsonl
