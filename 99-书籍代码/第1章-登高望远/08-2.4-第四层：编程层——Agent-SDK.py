import claude_code

# 用 SDK 构建一个代码健康度检查 Agent
result = claude_code.query(
    prompt="分析 src/ 目录下所有 Python 文件的代码质量，给出健康度评分",
    allowed_tools=["Read", "Grep", "Glob"],
    max_turns=15
)
print(result)
