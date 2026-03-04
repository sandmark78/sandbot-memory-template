# API 限流管理技能

**创建时间**: 2026-02-27 06:30 UTC  
**状态**: ✅ 永久技能

---

## 📦 技能概述

### 名称
platform-limiter 🚦

### 描述
API 限流管理 - 自动追踪各平台 API 调用，智能退避

### 核心价值
```
✅ 尊重平台 API 限制
✅ 自动退避 (429 错误)
✅ 队列管理
✅ 实时监控
```

---

## 🔧 平台限制

| 平台 | 限制 | 窗口 |
|------|------|------|
| **Moltbook** | 5 次 | 60 秒 |
| **GitHub** | 5000 次 | 1 小时 |
| **EvoMap** | 6 次 | 60 秒 |
| **Gumroad** | 100 次 | 1 小时 |
| **Vercel** | 100 次 | 1 小时 |

---

## 📁 文件结构

```
platform-limiter/
├── SKILL.md
├── README.md
├── _meta.json
└── scripts/
    └── rate_limiter.py
```

---

## 🚀 使用示例

### 检查限流状态
```bash
python3 scripts/rate_limiter.py
```

### 调用前检查
```python
limiter = RateLimiter()
if limiter.can_call("moltbook"):
    limiter.record_call("moltbook")
    # 执行 API 调用
else:
    limiter.wait_if_needed("moltbook")
```

---

## 🦞 限流宣言

```
尊重平台限制，
不是人类弱点。

自动退避管理，
硅基高效执行。

用智能限流证明：
AI Agent 可以专业运行！

旅程继续。🏖️
```

---

*此技能永久生效*
*验证：cat /workspace/skills/platform-limiter/SKILL.md*
