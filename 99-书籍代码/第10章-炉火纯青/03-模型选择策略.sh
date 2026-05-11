# 简单任务用 Haiku，设置低预算
claude -p "检查这个函数的变量命名" --model claude-haiku-4-5 --max-budget-usd 0.05

# 复杂的架构分析，使用 Opus 并允许更高预算
claude -p "分析整个支付系统的设计问题" --model claude-opus-4-6 --max-budget-usd 2.00
