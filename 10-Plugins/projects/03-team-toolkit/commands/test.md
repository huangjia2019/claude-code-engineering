---
name: test
description: 运行测试并分析结果，失败时提供修复建议
---

用法：`/test [scope] [options]`

## 参数

- `scope`（可选）：
  - `unit` - 只运行单元测试
  - `e2e` - 只运行端到端测试
  - `all` - 运行全部（默认）

- `options`：
  - `--fix` - 尝试自动修复失败的测试
  - `--coverage` - 生成覆盖率报告

## 工作流程

1. 运行指定范围的测试
2. 收集测试结果
3. 对失败的测试：
   - 分析失败原因
   - 检查是代码 bug 还是测试过时
   - 提供修复建议
4. 如果指定了 --fix，尝试自动修复

## 输出格式

```markdown
# 测试报告

## 结果

| 指标 | 值 |
|------|------|
| 总计 | 150 |
| 通过 | 147 |
| 失败 | 3 |
| 跳过 | 0 |
| 覆盖率 | 85% |

## 失败的测试

### test_user_creation
**文件**: tests/user.test.ts:42
**错误**: AssertionError: expected 'active' but got 'pending'

**分析**: User 模型的默认状态在 commit abc123 中从 'active' 改为 'pending'，但测试未更新。

**建议**: 更新测试以期望 'pending' 状态。

\`\`\`diff
- expect(user.status).toBe('active');
+ expect(user.status).toBe('pending');
\`\`\`

---
*由 team-toolkit 生成*
```
