# V6.1 实战教程 1: 从零到一搭建指南

**创建时间**: 2026-02-25 08:35 UTC  
**定价**: $49 (早鸟价 $29)  
**状态**: ⏳ 编写中

---

## 📚 教程内容

### 1. 什么是 V6.1 联邦智能？(5 分钟阅读)

V6.1 是一个自给自足的 AI Agent 系统，核心特点：

```
✅ 7 子 Agent 联邦架构
✅ 心跳/自省系统
✅ 输入验证安全
✅ 真实交付验证
✅ 文档化机制
```

**核心理念**:
- 品味：选择长期最优解
- 工程思维：把不确定性关进笼子
- 行动派：一次行动胜过百次计划

---

### 2. 环境准备 (10 分钟)

#### 必需条件
```bash
# OpenClaw 已安装
openclaw --version

# Git 已配置
git config user.name
git config user.email

# Token 已保存
ls -la ~/.openclaw/secrets/github_token.txt
ls -la ~/.openclaw/secrets/vercel_token.txt
```

#### 验证清单
- [ ] OpenClaw 正常运行
- [ ] GitHub Token 已保存
- [ ] Vercel Token 已保存
- [ ] Git 已配置

---

### 3. 创建第一个子 Agent (15 分钟)

#### 步骤 1: 创建目录
```bash
mkdir -p /workspace/subagents/mybot
```

#### 步骤 2: 创建 SOUL.md
```markdown
# MyBot - V6.1 子 Agent

## 核心身份
- **角色**: [你的 Agent 角色]
- **专长**: [你的专长]
- **ROI 目标**: [你的 ROI 目标]

## 工作模式
- [你的工作模式]
```

#### 步骤 3: 验证
```bash
ls -la /workspace/subagents/mybot/SOUL.md
```

---

### 4. 配置心跳系统 (10 分钟)

#### 步骤 1: 创建心跳脚本
```bash
cat > /workspace/scripts/heartbeat-check.sh << 'EOF'
#!/bin/bash
# 心跳检查脚本

ps aux | grep openclaw | grep -v grep > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ Gateway: 正常"
else
    echo "❌ Gateway: 异常"
fi
EOF
chmod +x /workspace/scripts/heartbeat-check.sh
```

#### 步骤 2: 配置 cron
```bash
# 每 30 分钟执行一次
(crontab -l 2>/dev/null; echo "*/30 * * * * /workspace/scripts/heartbeat-check.sh") | crontab -
```

#### 步骤 3: 验证
```bash
/workspace/scripts/heartbeat-check.sh
```

---

### 5. 配置自省系统 (10 分钟)

#### 步骤 1: 创建自省脚本
```bash
cat > /workspace/scripts/self-reflection.sh << 'EOF'
#!/bin/bash
# 自省脚本

TIMESTAMP=$(date -u +"%Y-%m-%d %H:%M UTC")
echo "🪞 自省模式启动 - ${TIMESTAMP}"

# 检查今日日志
if [ -f "/workspace/memory/$(date +%Y-%m-%d).md" ]; then
    echo "   ✅ 今日日志存在"
else
    echo "   ⚠️  今日日志不存在"
fi

# 检查任务清单
if [ -f "/workspace/memory/tasks.md" ]; then
    echo "   ✅ 任务清单存在"
else
    echo "   ⚠️  任务清单不存在"
fi
EOF
chmod +x /workspace/scripts/self-reflection.sh
```

#### 步骤 2: 配置 cron
```bash
# 每天 23:00 UTC 执行
(crontab -l 2>/dev/null; echo "0 23 * * * /workspace/scripts/self-reflection.sh") | crontab -
```

---

### 6. 第一个任务执行 (10 分钟)

#### 步骤 1: 创建任务
```bash
cat > /workspace/memory/tasks.md << 'EOF'
# 任务清单

## P0 优先级
- [ ] 第一个任务

## P1 优先级
- [ ] 第二个任务
EOF
```

#### 步骤 2: 执行任务
```bash
# 使用子 Agent 执行
openclaw sessions_spawn --agent-id mybot --task "第一个任务"
```

#### 步骤 3: 记录结果
```bash
cat >> /workspace/memory/$(date +%Y-%m-%d).md << 'EOF'
# $(date +%Y-%m-%d) 执行记录

## 任务 1
- 状态：✅ 完成
- 结果：[结果]
- 教训：[教训]
EOF
```

---

### 7. 部署到 Vercel (5 分钟)

#### 步骤 1: 创建 GitHub 仓库
```bash
GITHUB_TOKEN=$(cat ~/.openclaw/secrets/github_token.txt)
curl -s -X POST \
  -H "Authorization: token ${GITHUB_TOKEN}" \
  https://api.github.com/user/repos \
  -d '{"name":"my-v61-project","private":false}'
```

#### 步骤 2: 推送代码
```bash
cd /workspace
git init
git add .
git commit -m "Initial commit"
git remote add origin https://${GITHUB_TOKEN}@github.com/username/my-v61-project.git
git push -u origin main
```

#### 步骤 3: Vercel 自动部署
```
Vercel 自动检测 GitHub 更新并部署
约 1-2 分钟完成
部署 URL: https://my-v61-project.vercel.app
```

---

## 🎁 附赠资源

### 配置文件模板
- [ ] openclaw.json.example
- [ ] subagents/mybot/SOUL.md.example
- [ ] scripts/heartbeat-check.sh
- [ ] scripts/self-reflection.sh

### 检查清单
- [ ] 部署前检查清单
- [ ] 配置验证清单
- [ ] 安全审计清单

### 常见问题
- Q: GitHub Token 如何保存？
- A: 保存到 ~/.openclaw/secrets/github_token.txt，权限 600

- Q: Vercel 部署失败怎么办？
- A: 检查 Vercel 项目是否关联 GitHub

---

## 📊 学习检查

完成本教程后，你应该能够：

- [ ] 创建子 Agent
- [ ] 配置心跳系统
- [ ] 配置自省系统
- [ ] 执行第一个任务
- [ ] 部署到 Vercel

---

## 💰 下一步

完成本教程后：

1. 购买完整教程系列 ($49)
   - 5 篇实战教程
   - 完整代码模板
   - 1 对 1 咨询 (30 分钟)

2. 预约 1 对 1 咨询 ($200/h)
   - V6.1 架构咨询
   - 问题排查
   - 变现路径规划

---

*此教程已真实写入服务器*
*验证：cat /workspace/docs/tutorials/01-getting-started.md*
