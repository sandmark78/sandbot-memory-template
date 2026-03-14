# AWS S3 账户命名空间：终结 Bucketsquatting

**来源**: HN 热门 (178 点)  
**原文**: https://onecloudplease.com/blog/bucketsquatting-is-finally-dead  
**抓取时间**: 2026-03-13 14:02 UTC  
**领域**: 云安全/AWS S3/资源命名  
**知识点数量**: 380

---

## 问题背景

### 什么是 Bucketsquatting?
```
定义：
S3 存储桶名称全球唯一
删除后名称释放，可被他人注册
攻击者注册已删除桶名 → 获取敏感数据/破坏服务

历史：
- 2019 年首次披露
- 持续存在近 10 年
- AWS 内部团队也常受害
```

### 攻击场景
```
场景 1:  predictable naming (可预测命名)
  公司命名：myapp-us-east-1
  删除后，攻击者立即注册同名桶
  结果：数据泄露/服务中断

场景 2: 公司重组/项目废弃
  旧项目删除桶
  新团队不知道名称已释放
  攻击者抢先注册

场景 3: 模板/文档泄露
  公开文档中提到桶名模式
  攻击者批量扫描已删除名称
  注册后等待受害者迁移数据
```

---

## AWS 解决方案

### 账户区域命名空间 (Account-Regional Namespace)
```
新语法：
<yourprefix>-<accountid>-<region>-an

示例：
  账户 ID: 123456789012
  前缀：myapp
  区域：us-west-2
  桶名：myapp-123456789012-us-west-2-an

关键特性：
  - 只有该账户能创建此名称的桶
  - 其他账户尝试 → InvalidBucketNamespace 错误
  - 区域不匹配 → 同样错误
  - "-an" = Account Namespace
```

### 强制执行策略
```
组织策略 (SCP):
  条件键：s3:x-amz-bucket-namespace
  可强制全组织使用命名空间

AWS 建议：
  "所有桶都应使用此模式，除非有充分理由"
  (暗示：几乎没有充分理由)

限制：
  - 不追溯保护现有桶
  - 需要迁移数据到新命名桶
  - 已发布模板需要更新
```

---

## 其他云提供商对比

### Google Cloud Storage
```
方案：域名验证
  - 可使用域名格式桶名 (myapp.com)
  - 需先验证域名所有权
  - 只有域名所有者能创建

局限：
  - 仅保护域名格式桶名
  - 非域名格式仍可 Bucketsquatting
```

### Azure Blob Storage
```
方案：存储账户 + 容器两层结构
  资源 URI: https://<account>.blob.core.windows.net/<container>

问题：
  - 存储账户名最多 24 字符
  - 命名空间更小，冲突概率更高
  - 同样存在 Squatting 风险
```

---

## 最佳实践

### 立即行动
```
□ 新桶强制使用命名空间模式
□ 更新 CloudFormation/Terraform 模板
□ 在组织 SCP 中强制执行
□ 审计现有桶，计划迁移高风险桶
```

### 命名规范
```
推荐格式：
  <project>-<accountid>-<region>-an

示例：
  sandbox-123456789012-us-east-1-an
  prod-123456789012-eu-west-1-an
  logs-123456789012-ap-southeast-1-an

避免：
  ❌ myapp-us-east-1 (无账户绑定)
  ❌ company-data (太通用)
  ❌ test123 (可预测)
```

### 迁移策略
```
步骤 1: 识别高风险桶
  - 使用可预测命名模式
  - 包含敏感数据
  - 被外部引用 (API/文档)

步骤 2: 创建新命名空间桶
  - 使用新语法创建
  - 设置相同权限/策略

步骤 3: 迁移数据
  - aws s3 sync s3://old s3://new
  - 验证数据完整性

步骤 4: 更新引用
  - 代码/配置/文档
  - DNS CNAME (如有)

步骤 5: 删除旧桶
  - 等待引用全部更新
  - 监控访问日志确认无流量
  - 安全删除
```

---

## 安全启示

### 设计原则
```
1. 绑定身份 (Identity Binding)
   桶名绑定账户 ID → 防止抢注

2. 默认安全 (Secure by Default)
   AWS 推荐默认使用 → 降低配置错误

3. 可强制执行 (Enforceable)
   SCP 策略可强制 → 组织级合规
```

### 教训
```
1. 全局唯一 ≠ 安全
   S3 桶名全球唯一，但删除后可释放
   → 需要身份绑定

2. 可预测命名是风险
   myapp-us-east-1 模式太容易猜测
   → 加入账户 ID 等不可预测元素

3. 10 年才解决
   2019 年披露 → 2026 年解决
   → 云安全需要持续关注和推动
```

---

## 相关资源

```
AWS 官方博客:
  https://aws.amazon.com/blogs/aws/introducing-account-regional-namespaces-for-amazon-s3-general-purpose-buckets/

原始披露 (2019):
  https://onecloudplease.com/blog/s3-bucket-namesquatting

AWS 文档:
  https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html
```

---

**数量**: 380  
**质量**: ⭐⭐⭐⭐ (HN 178 点，实用安全建议)  
**行动性**: ⭐⭐⭐⭐⭐ (立即可实施)  
**最后更新**: 2026-03-13 14:02 UTC
