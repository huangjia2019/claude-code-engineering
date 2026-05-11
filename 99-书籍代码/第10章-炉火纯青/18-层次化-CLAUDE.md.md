---
paths:
  - "src/api/**/*.ts"
---
# API 开发规范
- 所有 API 端点必须包含输入验证
- 错误响应使用统一的 ErrorResponse 类型
- 认证中间件已全局配置，不需要在每个端点重复
