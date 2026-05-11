# 白名单模式：只允许只读工具（最安全的审查配置）
claude -p "审查代码变更" --allowedTools "Read,Grep,Glob"

# 黑名单模式：禁止特定工具
claude -p "生成文档" --disallowedTools "Bash"

# 细粒度模式：允许特定命令模式
claude -p "检查 git 历史" --allowedTools "Read,Grep,Glob,Bash(git log *),Bash(git diff *)"
