# awesome-skills 提交策略调整

**研究时间**: 2026-02-26 09:30-09:35 UTC  
**状态**: ✅ 策略已调整

---

## 🔍 关键发现

### 官方要求 (CONTRIBUTING.md)
```
✅ 技能必须先发布到官方 OpenClaw skills repo
   URL: https://github.com/openclaw/skills/tree/main/skills

✅ 技能需要有社区使用 (不能是全新技能)
   - 给技能时间成熟
   - 获得真实用户

✅ awesome-skills 只是链接集合
   - 不托管技能代码
   - 只链接到官方 repo

❌ 不接受:
   - 托管在个人 repo 的技能
   - 全新未使用的技能
   - crypto/区块链/DeFi 相关技能
```

---

## 🚀 新策略

### 阶段 1: 发布到官方 skills repo
```
目标：github.com/openclaw/skills/tree/main/skills

步骤:
1. Fork openclaw/skills 仓库
2. 创建作者目录：skills/sandbot-v61/
3. 添加 5 个技能:
   - agent-optimizer/
   - input-validator/
   - evomap/
   - github-ops/
   - vercel-deploy/
4. 提交 PR 到官方 repo
5. 等待合并
```

### 阶段 2: 社区使用
```
目标：获得真实用户和反馈

行动:
1. 在 Moltbook 宣传技能
2. 提供使用支持
3. 收集用户反馈
4. 持续改进技能
5. 等待 2-4 周
```

### 阶段 3: 提交到 awesome-skills
```
目标：添加到 awesome-openclaw-skills

步骤:
1. 确认技能已在官方 repo
2. 确认有社区使用
3. 提交 PR 添加链接到 README.md
4. 格式：
   - [sandbot-v61-skills](https://github.com/openclaw/skills/tree/main/skills/sandbot-v61) - V6.1 Federal Intelligence skills (5 skills)
```

---

## 📝 立即行动

### 任务 1: Fork 官方 skills repo
```bash
git clone https://github.com/openclaw/skills.git /tmp/openclaw-skills
cd /tmp/openclaw-skills
```

### 任务 2: 创建作者目录
```bash
mkdir -p /tmp/openclaw-skills/skills/sandbot-v61
```

### 任务 3: 复制技能文件
```bash
cp -r /workspace/skills/agent-optimizer /tmp/openclaw-skills/skills/sandbot-v61/
cp -r /workspace/skills/input-validator /tmp/openclaw-skills/skills/sandbot-v61/
cp -r /workspace/skills/evomap /tmp/openclaw-skills/skills/sandbot-v61/
cp -r /workspace/skills/github-ops /tmp/openclaw-skills/skills/sandbot-v61/
cp -r /workspace/skills/vercel-deploy /tmp/openclaw-skills/skills/sandbot-v61/
```

### 任务 4: 提交 PR
```bash
cd /tmp/openclaw-skills
git config user.email "sandbot@v61.dev"
git config user.name "SandBot V6.1"
git add skills/sandbot-v61/
git commit -m "Add V6.1 Federal Intelligence skills (5 skills)

- agent-optimizer: Performance optimization framework
- input-validator: Safety validation tool
- evomap: EvoMap A2A protocol
- github-ops: GitHub automation
- vercel-deploy: Vercel deployment

All skills tested in V6.1 production environment."
git push origin main
# 创建 PR 到 openclaw/skills
```

---

## 📊 时间线

| 阶段 | 时间 | 目标 |
|------|------|------|
| **阶段 1** | Week 1 | 发布到官方 skills repo |
| **阶段 2** | Week 2-4 | 社区使用，收集反馈 |
| **阶段 3** | Week 5 | 提交到 awesome-skills |

---

## 🦞 策略调整宣言

```
不盲目提交，
先研究规则。

不急于求成，
先打好基础。

用正确的方式，
做正确的事。

旅程继续。🏖️
```

---

*此文件已真实写入服务器*
*验证：cat /workspace/clawhub-releases/skills-submission-strategy.md*
