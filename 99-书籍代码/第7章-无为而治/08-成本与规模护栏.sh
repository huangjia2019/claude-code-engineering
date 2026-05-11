# 限制 Claude 的执行轮数（防止过度分析）
claude -p "审查代码" --max-turns 5

# 设置硬性成本上限（美元）
claude -p "分析日志" --max-budget-usd 0.50

# 同时限制两者——双重保险
claude -p "分析整个代码库" --max-turns 10 --max-budget-usd 2.00
