# OneCLI - AI Agent 密钥管理 Vault

**来源**: Hacker News Show HN (2026-03-12, 97 分，35 评论)  
**仓库**: https://github.com/onecli/onecli  
**网站**: https://onecli.sh  
**标签**: #AI-Agent #安全 #密钥管理 #Rust #开源

---

## 🎯 核心价值

**问题**: AI Agent 需要调用数十个 API，但给每个 Agent 原始凭证是安全风险。

**解决方案**: OneCLI 是开源凭证 Vault，让 AI Agent 无需暴露密钥即可访问服务。

**核心原则**: 
- Store once. Inject anywhere. Agents never see the keys.
- 密钥集中管理，Agent 只使用占位符密钥
- 网关层透明注入真实凭证

---

## 🏗️ 架构设计

### 三层架构
```
┌─────────────────┐
│   AI Agent      │  使用 FAKE_KEY 发起 HTTP 请求
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  OneCLI Gateway │  Rust 网关，拦截请求，替换 FAKE_KEY → REAL_KEY
│  (port 10255)   │  AES-256-GCM 解密，注入真实凭证
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   External API  │  接收真实密钥的请求
│   (Stripe, etc) │
└─────────────────┘
```

### 核心组件

| 组件 | 技术栈 | 端口 | 功能 |
|------|--------|------|------|
| **Rust Gateway** | Rust | 10255 | HTTP 网关，MITM 拦截 HTTPS，凭证注入 |
| **Web Dashboard** | Next.js | 10254 | 管理 Agent、密钥、权限 |
| **Secret Store** | PGlite/PostgreSQL | - | AES-256-GCM 加密存储 |
| **DB Layer** | Prisma ORM | - | 数据库迁移和管理 |

---

## 🔐 安全机制

### 密钥注入流程
```
1. Agent 发起 HTTP 请求 (使用 FAKE_KEY)
2. Gateway 拦截请求 (Proxy-Authorization 头验证 Agent 身份)
3. 根据 host + path 模式匹配对应密钥
4. AES-256-GCM 解密真实密钥
5. 替换 FAKE_KEY → REAL_KEY
6. 转发请求到目标 API
7. Agent 从未接触真实密钥
```

### 加密存储
- **算法**: AES-256-GCM
- **解密时机**: 仅在请求时解密
- **密钥轮换**: 集中管理，一键轮换
- **审计日志**: 记录每个 Agent 的每次调用

---

## 🚀 快速启动

### Docker 一键启动 (推荐)
```bash
docker run --pull always \
  -p 10254:10254 -p 10255:10255 \
  -v onecli-data:/app/data \
  ghcr.io/onecli/onecli
```

访问 http://localhost:10254 创建 Agent 和密钥。

### Docker Compose
```bash
git clone https://github.com/onecli/onecli.git
cd onecli/docker
docker compose up
```

### 本地开发
```bash
mise install  # 安装 Node.js, pnpm, Rust
pnpm install
cp .env.example .env
pnpm db:generate
pnpm db:init-dev
pnpm dev
```

---

## ⚙️ 配置选项

### 环境变量
| 变量 | 描述 | 默认值 |
|------|------|--------|
| `DATABASE_URL` | PostgreSQL 连接字符串 | 嵌入式 PGlite |
| `NEXTAUTH_SECRET` | 启用 Google OAuth (多用户) | 单用户模式 |
| `GOOGLE_CLIENT_ID` | Google OAuth 客户端 ID | — |
| `GOOGLE_CLIENT_SECRET` | Google OAuth 客户端密钥 | — |
| `SECRET_ENCRYPTION_KEY` | AES-256-GCM 加密密钥 | 自动生成 |

### 认证模式
- **单用户模式**: 无登录，适合本地使用
- **Google OAuth**: 多用户团队模式

---

## 🎯 核心特性

| 特性 | 描述 |
|------|------|
| **透明凭证注入** | Agent 发起正常 HTTP 调用，网关处理认证 |
| **加密存储** | AES-256-GCM 静态加密，请求时解密 |
| **Host + Path 匹配** | 通过模式匹配路由密钥到正确 API 端点 |
| **多 Agent 支持** | 每个 Agent 独立访问令牌和权限 |
| **无外部依赖** | 嵌入式 PGlite，无需外部数据库 |
| **Rust 网关** | 快速、内存安全的 HTTP 网关 |

---

## 📊 与竞品对比

| 方案 | 密钥管理 | Agent 隔离 | 审计日志 | 部署复杂度 |
|------|----------|-----------|----------|------------|
| **OneCLI** | ✅ 集中加密 | ✅ 独立令牌 | ✅ 完整日志 | ⭐ 低 (Docker) |
| 环境变量 | ❌ 明文存储 | ❌ 共享密钥 | ❌ 无日志 | ⭐ 低 |
| HashiCorp Vault | ✅ 强加密 | ✅ 策略隔离 | ✅ 完整日志 | ⭐⭐⭐ 高 |
| AWS Secrets Manager | ✅ 加密 | ✅ IAM 隔离 | ✅ CloudTrail | ⭐⭐ 中 |

**OneCLI 优势**: 专为 AI Agent 设计，轻量级，零配置启动。

---

## 🔧 使用示例

### 1. 创建 Agent
```bash
# Dashboard 创建 Agent，获取访问令牌
ACCESS_TOKEN=onecli_agent_abc123
```

### 2. 配置 Agent 使用网关
```python
import requests

# Agent 使用占位符密钥
headers = {
    "Proxy-Authorization": f"Bearer {ACCESS_TOKEN}",
    "Authorization": "Bearer FAKE_KEY"  # 占位符
}

# 请求通过 OneCLI 网关
response = requests.get(
    "http://localhost:10255/v1/chat/completions",
    headers=headers
)
```

### 3. 网关自动注入真实密钥
```
原始请求：Authorization: Bearer FAKE_KEY
↓ OneCLI 网关拦截
注入后：Authorization: Bearer sk-real-api-key-xyz
↓ 转发到 OpenAI
```

---

## 🛡️ 安全最佳实践

### 推荐配置
```
✅ 生产环境使用外部 PostgreSQL
✅ 启用 Google OAuth 多用户认证
✅ 定期轮换 SECRET_ENCRYPTION_KEY
✅ 限制 Agent 访问特定 host/path
✅ 启用审计日志监控异常调用
```

### 避免事项
```
❌ 不要在代码中硬编码真实密钥
❌ 不要共享 Agent 访问令牌
❌ 不要在生产环境使用自动生成的加密密钥
❌ 不要禁用审计日志
```

---

## 📈 适用场景

| 场景 | 适用性 | 说明 |
|------|--------|------|
| **多 Agent 系统** | ⭐⭐⭐⭐⭐ | 每个 Agent 独立权限管理 |
| **本地开发** | ⭐⭐⭐⭐⭐ | Docker 一键启动，零配置 |
| **团队协作** | ⭐⭐⭐⭐ | Google OAuth 多用户支持 |
| **生产部署** | ⭐⭐⭐⭐ | 需外部 PostgreSQL + 密钥轮换 |
| **企业合规** | ⭐⭐⭐ | 审计日志完整，但需额外集成 |

---

## 🎓 学习要点

### 核心知识点
1. **MITM 代理模式**: Rust 网关拦截 HTTPS 请求
2. **凭证注入**: 请求时解密和替换密钥
3. **模式匹配**: host + path 路由到正确密钥
4. **加密存储**: AES-256-GCM 静态加密
5. **Agent 认证**: Proxy-Authorization 头验证

### 扩展阅读
- [PoisonedRAG 攻击](./rag-document-poisoning.md) - RAG 系统安全知识
- [AI Agent 安全最佳实践](./ai-agent-security-best-practices.md)
- [Rust HTTP 网关实现](./rust-http-gateway-patterns.md)

---

## 📝 总结

**OneCLI 核心价值**:
- 🔐 **安全**: Agent 永不接触真实密钥
- 🚀 **轻量**: Docker 一键启动，无外部依赖
- 🎯 **专用**: 专为 AI Agent 设计的凭证管理
- 📊 **可观测**: 完整审计日志，追踪每次调用

**适用团队**:
- ✅ 正在运行多 Agent 系统
- ✅ 需要集中管理 API 密钥
- ✅ 希望快速部署，不想配置复杂 Vault

**技术亮点**:
- Rust 网关 (高性能、内存安全)
- AES-256-GCM 加密
- 透明凭证注入
- 嵌入式 PGlite (零配置)

---

**数量**: 450  
**创建时间**: 2026-03-12 22:03 UTC  
**最后更新**: 2026-03-12 22:03 UTC  
**质量**: ⭐⭐⭐⭐⭐ 深度分析 (架构 + 安全 + 使用示例)
