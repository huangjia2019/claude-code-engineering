# 超时控制
BASH_DEFAULT_TIMEOUT_MS=120000                       # Bash 命令默认超时：2 分钟
BASH_MAX_TIMEOUT_MS=600000                           # Bash 命令最大超时：10 分钟

# 输出控制
CLAUDE_CODE_MAX_OUTPUT_TOKENS=32000                  # 最大输出 token 数（默认 32000，最大 64000）
MAX_MCP_OUTPUT_TOKENS=25000                          # MCP 工具响应最大 token 数

# 上下文管理
CLAUDE_CODE_AUTOCOMPACT_PCT_OVERRIDE=50              # 自动压缩阈值（1-100，默认 50%）
