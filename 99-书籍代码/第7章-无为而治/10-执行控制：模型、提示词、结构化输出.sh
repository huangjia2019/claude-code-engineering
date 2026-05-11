# 简单格式检查，用快速便宜的模型
claude -p "检查代码格式" --model claude-haiku-4-5

# 深度安全审查，用最强模型
claude -p "安全漏洞分析" --model claude-sonnet-4-6

# 指定备选模型（主模型过载时自动切换）
claude -p "代码审查" --model claude-sonnet-4-6 --fallback-model haiku
