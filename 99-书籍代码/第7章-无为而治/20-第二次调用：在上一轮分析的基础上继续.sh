# 继续当前目录最近的会话（不需要知道 session_id）
claude -p "继续刚才的分析" --continue

# 创建分支会话（保留原始会话不变）
claude -p "如果改用微服务架构呢？" --resume "$SESSION_ID" --fork-session

# 禁用会话持久化（适合完全无状态的 CI 场景）
claude -p "一次性分析" --no-session-persistence
