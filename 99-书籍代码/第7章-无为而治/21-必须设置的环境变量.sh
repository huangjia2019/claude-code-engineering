# 认证
ANTHROPIC_API_KEY=sk-ant-...                         # API 密钥

# 禁用非必要功能（一个变量覆盖多项）
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1           # 禁用自动更新、遥测、错误上报

# 或者分别禁用
DISABLE_AUTOUPDATER=1                                # 禁用自动更新（CI 中必须）
DISABLE_TELEMETRY=1                                  # 禁用遥测
DISABLE_ERROR_REPORTING=1                            # 禁用错误上报
