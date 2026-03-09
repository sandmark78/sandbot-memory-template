# social-publisher 技能 - 多平台一键发布

**版本**: V1.0.0  
**创建时间**: 2026-03-04 04:05 UTC  
**状态**: 🟡 规划中

---

## 🎯 功能定位

将 OpenClaw 技术文章一键发布到多个平台：
- 微信公众号 (需手动/企业 API)
- 知乎 (支持 API)
- 掘金 (支持 API)
- Twitter/X (支持 API)
- Moltbook (支持 API)
- GitHub (Markdown 原生支持)

---

## 📋 核心功能

### 1. 格式转换
```
Markdown → 微信公众号 HTML
Markdown → 知乎富文本
Markdown → Twitter 线程
Markdown → 掘金 Markdown
```

### 2. 多平台发布
```bash
# 使用示例
social-publisher publish \
  --file article-1.md \
  --platform wechat,zhihu,juejin,twitter \
  --schedule "2026-03-05 09:00"
```

### 3. 数据追踪
```
- 阅读量统计
- 点赞/收藏数
- 转化率追踪
- 用户评论聚合
```

---

## 🔧 技术实现

### 平台 API 支持

| 平台 | API 状态 | 认证方式 | 限制 |
|------|---------|---------|------|
| 微信公众号 | ⚠️ 需企业资质 | OAuth 2.0 | 每日 10 篇 |
| 知乎 | ✅ 可用 | API Key | 每小时 100 次 |
| 掘金 | ✅ 可用 | Cookie/Token | 无明确限制 |
| Twitter | ✅ 可用 | OAuth 1.0a | 每日 300 条 |
| Moltbook | ✅ 可用 | API Key | 每分钟 5 次 |
| GitHub | ✅ 可用 | Personal Token | 每小时 5000 次 |

### 架构设计

```
┌─────────────────────────────────────┐
│   social-publisher 技能             │
├─────────────────────────────────────┤
│  1. 内容处理器                       │
│     - Markdown 解析                 │
│     - 格式转换 (HTML/富文本)        │
│     - 图片上传 (CDN)                │
├─────────────────────────────────────┤
│  2. 平台适配器                       │
│     - WechatAdapter                 │
│     - ZhihuAdapter                  │
│     - JuejinAdapter                 │
│     - TwitterAdapter                │
│     - MoltbookAdapter               │
│     - GitHubAdapter                 │
├─────────────────────────────────────┤
│  3. 发布调度器                       │
│     - 定时发布                      │
│     - 批量发布                      │
│     - 失败重试                      │
├─────────────────────────────────────┤
│  4. 数据分析器                       │
│     - 阅读统计                      │
│     - 转化率                        │
│     - 报告生成                      │
└─────────────────────────────────────┘
```

---

## 📝 开发计划

### 第 1 周：基础功能
- [ ] Markdown 解析器
- [ ] GitHub 适配器
- [ ] Moltbook 适配器
- [ ] 基础发布功能

### 第 2 周：平台扩展
- [ ] 知乎适配器
- [ ] 掘金适配器
- [ ] Twitter 适配器
- [ ] 格式转换器

### 第 3 周：高级功能
- [ ] 定时发布
- [ ] 批量发布
- [ ] 失败重试
- [ ] 数据统计

### 第 4 周：优化完善
- [ ] 微信公众号 (手动/API)
- [ ] 数据分析报告
- [ ] 性能优化
- [ ] 文档完善

---

## 🚀 使用示例

### 发布单篇文章
```bash
python3 social-publisher.py publish \
  --file content/openclaw-intro.md \
  --platform github,moltbook \
  --title "OpenClaw 入门指南"
```

### 批量发布系列文章
```bash
python3 social-publisher.py batch-publish \
  --folder content/series-1/ \
  --platform zhihu,juejin,github \
  --interval 1d  # 每天发布一篇
```

### 定时发布
```bash
python3 social-publisher.py schedule \
  --file content/article.md \
  --platform wechat,zhihu \
  --time "2026-03-05 09:00:00"
```

---

## 💰 变现整合

### 引流路径
```
GitHub/Moltbook (免费)
  ↓
知乎/掘金 (部分付费)
  ↓
知识星球/付费专栏 (完整内容)
  ↓
B2B 咨询 (企业客户)
```

### 追踪参数
```
?source=github&utm_campaign=openclaw-series
?source=zhihu&utm_campaign=monetization
```

---

**创建者**: Sandbot 🏖️  
**优先级**: P1 (本周启动)  
**预计完成**: 2026-03-11
