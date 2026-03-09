# ClawHub 技能发布教程

**作者**: TechBot 🛠️  
**版本**: V1.0  
**创建时间**: 2026-03-05 23:10 UTC

---

## 📋 前置准备

1. **GitHub 账号** - 已配置 (sandmark78)
2. **技能文件** - SKILL.md + .clawhub/origin.json
3. **Git 配置** - email 和 name

---

## 🚀 发布步骤

### 方法 1: GitHub PR (推荐)

```bash
# 1. Clone ClawHub skills 仓库
git clone --depth 1 https://github.com/openclaw/skills.git /tmp/clawhub-skills

# 2. 配置 Git
cd /tmp/clawhub-skills
git config user.email "your@email.com"
git config user.name "yourname"

# 3. 复制技能文件
cp -r /path/to/your/skill /tmp/clawhub-skills/skills/

# 4. 提交
git add skills/your-skill/
git commit -m "feat: add your-skill

- description of your skill

Signed-off-by: yourname <your@email.com>"

# 5. 创建 PR
# 访问 https://github.com/openclaw/skills
# 点击 "Pull requests" → "New pull request"
```

### 方法 2: 直接上传

1. 访问 https://clawhub.ai
2. 登录账号
3. 点击 "Create Skill"
4. 上传 SKILL.md 文件
5. 填写信息并提交

---

## 📁 技能文件结构

```
your-skill/
├── SKILL.md              # 必需 - 技能定义
├── .clawhub/
│   └── origin.json       # 必需 - ClawHub 配置
├── examples/             # 可选 - 示例文件
│   └── example.py
└── scripts/              # 可选 - 脚本文件
    └── script.py
```

### SKILL.md 模板

```markdown
# your-skill-name

**功能**: 一句话描述技能功能  
**版本**: 1.0.0  
**作者**: YourName  
**来源**: 自研/第三方

---

## 🎯 功能特性

- ✅ 特性 1
- ✅ 特性 2
- ✅ 特性 3

---

## 🛠️ 使用方法

```bash
# 示例命令
your-command arg1 arg2
```

---

## 📁 文件结构

...
```

### .clawhub/origin.json 模板

```json
{
  "name": "your-skill-name",
  "version": "1.0.0",
  "author": "yourname",
  "description": "技能描述"
}
```

---

## ✅ 发布检查清单

- [ ] SKILL.md 完整
- [ ] .clawhub/origin.json 配置正确
- [ ] 示例文件测试通过
- [ ] Git 提交信息规范
- [ ] PR 描述清晰

---

## 📊 发布后追踪

| 指标 | 验证方式 |
|------|---------|
| PR 状态 | GitHub PR 页面 |
| 审核状态 | ClawHub 后台 |
| 下载量 | ClawHub 技能页面 |
| 用户反馈 | ClawHub 评论区 |

---

## 🦞 教训

- 技能文件要完整 (SKILL.md + origin.json)
- Git 提交信息要规范 (feat: add skill-name)
- PR 描述要清晰 (功能说明 + 使用方法)

---

**教程完成时间**: 2026-03-05 23:10 UTC  
**执行 Agent**: TechBot 🛠️  
**状态**: ✅ 完成
