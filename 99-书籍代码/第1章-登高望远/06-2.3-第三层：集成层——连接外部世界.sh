# 在 CI/CD 流水线中调用 Claude
claude -p "审查最近一次提交的代码变更，关注安全隐患和性能问题" \
  --output-format json \
  --max-turns 10 \
  --allowed-tools Read,Grep,Glob
