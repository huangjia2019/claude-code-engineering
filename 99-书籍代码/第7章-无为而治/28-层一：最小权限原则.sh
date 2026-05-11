# 审查任务：只读
--allowedTools "Read,Grep,Glob"

# 格式修复任务：读写
--allowedTools "Read,Grep,Glob,Edit,Write"

# 需要 git 操作的任务：细粒度 Bash 白名单
--allowedTools "Read,Grep,Glob,Bash(git diff *),Bash(git log *)"
