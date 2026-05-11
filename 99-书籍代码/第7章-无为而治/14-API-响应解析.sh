# Claude 分析 → jq 提取 → 发送通知
claude -p "检查是否有安全漏洞" --output-format json | \
  jq -r '.result' | \
  mail -s "安全扫描报告" security@company.com

# grep 预过滤 → Claude 深度分析
grep -r "TODO" src/ | claude -p "将这些 TODO 按优先级分类"

# Claude 生成代码 → 直接写入文件
claude -p "生成一个 Express 健康检查路由" --output-format text > routes/health.js
