# 分析日志文件
cat server.log | claude -p "找出所有 500 错误并总结根因"

# 分析 git 变更
git diff HEAD~1 | claude -p "总结这次提交的变更，格式为 Conventional Commits"

# API 响应解析
curl -s https://api.example.com/health | claude -p "判断服务是否健康"
