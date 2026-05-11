# 完全替换系统提示词（Claude 将忘记默认的代码助手身份）
claude -p "分析代码" --system-prompt "你是一名专注于 OWASP Top 10 的应用安全专家。"

# 在默认提示词基础上追加（推荐——保留 Claude 的基础能力）
claude -p "审查 PR" --append-system-prompt "务必检查敏感信息硬编码。"

# 从文件加载追加提示词（适合复杂的审查规范）
claude -p "审查代码" --append-system-prompt-file ./review-guidelines.txt
