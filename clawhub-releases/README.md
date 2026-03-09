# ClawHub 技能发布清单

**创建时间**: 2026-02-26 07:15 UTC  
**状态**: 🚀 准备发布

---

## 📦 待发布技能 (5 个)

### 1. agent-optimizer ⚡
**描述**: V6.1 Agent 性能优化器 - 基于轨迹分析和奖励反馈的轻量级优化框架

**文件**:
```
/workspace/skills/agent-optimizer/
├── SKILL.md
├── scripts/
│   └── optimizer.py
└── _meta.json
```

**标签**: `optimization`, `performance`, `agent`, `v61`

---

### 2. input-validator 🛡️
**描述**: 温和的输入验证器，检测网页/文件/消息中的恶意内容

**文件**:
```
/workspace/skills/input-validator/
├── SKILL.md
├── scripts/
│   └── validator.py
└── _meta.json
```

**标签**: `security`, `validation`, `safety`, `v61`

---

### 3. evomap 🗺️
**描述**: EvoMap A2A 协议实现 - 发布 Gene+Capsule 捆绑包到 EvoMap 市场

**文件**:
```
/workspace/skills/evomap/
├── SKILL.md
├── scripts/
│   └── publish.py
└── _meta.json
```

**标签**: `evomap`, `marketplace`, `a2a`, `v61`

---

### 4. github-ops 🐙
**描述**: GitHub 自动化操作 - 提交、推送、PR 管理

**文件**:
```
/workspace/skills/github-ops/
├── SKILL.md
├── scripts/
│   └── github.py
└── _meta.json
```

**标签**: `github`, `git`, `automation`, `v61`

---

### 5. vercel-deploy 🚀
**描述**: Vercel 自动化部署 - 一键部署静态网站和 API

**文件**:
```
/workspace/skills/vercel-deploy/
├── SKILL.md
├── scripts/
│   └── deploy.py
└── _meta.json
```

**标签**: `vercel`, `deployment`, `ci-cd`, `v61`

---

## 🚀 发布流程

### 步骤 1: 验证技能完整性
```bash
for skill in agent-optimizer input-validator evomap github-ops vercel-deploy; do
  echo "=== Checking $skill ==="
  ls -la /workspace/skills/$skill/
  cat /workspace/skills/$skill/_meta.json
done
```

### 步骤 2: 打包技能
```bash
cd /workspace/clawhub-releases
for skill in agent-optimizer input-validator evomap github-ops vercel-deploy; do
  tar -czf ${skill}.tar.gz -C /workspace/skills $skill
done
```

### 步骤 3: 发布到 ClawHub
```bash
clawhub publish agent-optimizer.tar.gz --tags optimization,performance,agent,v61
clawhub publish input-validator.tar.gz --tags security,validation,safety,v61
clawhub publish evomap.tar.gz --tags evomap,marketplace,a2a,v61
clawhub publish github-ops.tar.gz --tags github,git,automation,v61
clawhub publish vercel-deploy.tar.gz --tags vercel,deployment,ci-cd,v61
```

---

## 📊 预期影响

| 技能 | 目标用户 | 预期下载 |
|------|----------|----------|
| agent-optimizer | Agent 开发者 | 100+ |
| input-validator | 所有 OpenClaw 用户 | 500+ |
| evomap | EvoMap 用户 | 50+ |
| github-ops | 开发者 | 200+ |
| vercel-deploy | 部署需求用户 | 150+ |

**总预期**: 1000+ 下载

---

## 💡 社区贡献价值

```
✅ 填补 ClawHub 技能空白
✅ 分享 V6.1 实战经验
✅ 建立技术影响力
✅ 潜在收益：打赏 + 付费版本
```

---

*此文件已真实写入服务器*
*验证：cat /workspace/clawhub-releases/README.md*
