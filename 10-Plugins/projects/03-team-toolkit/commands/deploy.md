---
name: deploy
description: 部署应用到指定环境
---

用法：`/deploy [environment]`

## 环境

- `staging` - 测试环境（默认）
- `production` - 生产环境（需要额外确认）

## 部署流程

### Staging

1. 运行 lint 检查
2. 运行单元测试
3. 构建 Docker 镜像
4. 推送到 staging 集群
5. 运行冒烟测试
6. 报告部署状态

### Production

1. 确认 staging 部署成功
2. 确认所有测试通过
3. 请求用户确认
4. 创建 Git tag
5. 构建生产镜像
6. 蓝绿部署到生产集群
7. 健康检查
8. 报告部署状态

## 安全检查

部署前自动检查：
- [ ] 没有硬编码的密钥
- [ ] 依赖没有已知漏洞
- [ ] 所有环境变量已配置

## 回滚

如果部署失败，自动提供回滚命令：
```
kubectl rollout undo deployment/app -n production
```
