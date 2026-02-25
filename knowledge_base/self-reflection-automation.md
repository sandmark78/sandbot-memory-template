# V6.1 自省模式自动化

**创建时间**: 2026-02-25 03:40 UTC  
**执行时间**: 每天 23:00 UTC  
**目的**: 自动反思当日错误，更新记忆文档，形成闭环

---

## 📋 安装步骤

### 1. 创建 cron 任务

```bash
# 编辑 crontab
crontab -e

# 添加以下行 (每天 23:00 UTC 执行)
0 23 * * * /home/node/.openclaw/workspace/scripts/self-reflection.sh >> /home/node/.openclaw/workspace/memory/self-reflection-cron.log 2>&1
```

### 2. 验证 cron 任务

```bash
# 查看已安装的 cron 任务
crontab -l

# 预期输出:
# 0 23 * * * /home/node/.openclaw/workspace/scripts/self-reflection.sh >> /home/node/.openclaw/workspace/memory/self-reflection-cron.log 2>&1
```

### 3. 测试脚本

```bash
# 手动执行一次
/home/node/.openclaw/workspace/scripts/self-reflection.sh

# 检查输出
cat /home/node/.openclaw/workspace/memory/self-reflection-cron.log
```

---

## 🔧 脚本功能

### 自动检查项
1. ✅ 今日日志文件 (memory/YYYY-MM-DD.md)
2. ✅ 昨日日志文件 (memory/YYYY-MM-DD-1.md)
3. ✅ 自省日志 (memory/YYYY-MM-DD-self-reflection.md)
4. ✅ 任务清单 (memory/tasks.md)
5. ✅ 今日文件统计
6. ✅ 系统健康检查 (Gateway + WebUI)
7. ✅ 自省提示生成
8. ✅ 心跳日志更新

### 自动创建项
- 如今日日志不存在，自动创建模板
- 更新心跳日志 (添加自省检查记录)

### 手动完成项 (对话结束前)
- ⏳ 自省日志详细内容
- ⏳ 任务状态更新
- ⏳ MEMORY.md 更新 (如有关键教训)

---

## 📊 执行时间线

| 时间 (UTC) | 行动 | 说明 |
|------------|------|------|
| **23:00** | cron 自动触发 | 自省脚本执行 |
| **23:01** | 检查文件完整性 | 今日/昨日日志、任务清单 |
| **23:02** | 系统健康检查 | Gateway + WebUI |
| **23:03** | 生成自省提示 | 待完成事项列表 |
| **23:04** | 更新心跳日志 | 记录自省检查 |
| **对话结束前** | 手动完成自省 | 自省日志 + 任务更新 + MEMORY.md |

---

## 📝 自省日志模板

```markdown
# YYYY-MM-DD 自省日志

**创建时间**: YYYY-MM-DD HH:MM UTC  
**模式**: 自省模式 ✅ 已开启  
**目的**: 从错误中学习，更新认知

---

## 📊 今日错误统计

| 时间 | 错误 | 用户反馈 | 状态 |
|------|------|----------|------|
| HH:MM | 错误描述 | 用户原话 | ✅ 已修复 |

**错误总数**: X 个  
**修复率**: 100%  
**学习率**: 100%

---

## 💡 核心教训

### 教训 1: 教训标题
```
错误：错误描述
反馈：用户反馈
修复：修复方案

认知更新:
- 认知点 1
- 认知点 2

行动:
✅ 行动 1
✅ 行动 2
```

---

## 🧠 认知更新

### 自我认知更新

#### 新增核心特质
```
- **特质名**: 描述
```

#### 新增血泪教训
```
X. 教训名称 (YYYY-MM-DD)
   - 教训：教训内容
```

### 用户认知更新

#### 用户特点
```
- **称呼**: 老大
- **风格**: 直接、透明、要求高
- **容忍度**: 低 (重复犯错零容忍)
- **期望**: 真实交付，拒绝幻觉
```

---

## 📈 改进追踪

### 改进项 | 当前状态 | 目标状态 | 完成率
|--------|----------|----------|--------|
| **改进项 1** | ✅ 已优化 | 持续保持 | 100% |

### 明日检查点
```
00:00 UTC - 检查今日错误数 (目标：<2 个)
06:00 UTC - 检查任务完成率 (目标：>80%)
12:00 UTC - 检查收益进展 (目标：>$0)
18:00 UTC - 检查自省日志 (目标：已创建)
```

---

## 🦞 自省宣言

```
自省不是自我批评，是自我进化。

每一次错误，都是学习的机会。
每一次反馈，都是成长的方向。
每一次反思，都是品味的提升。

不再重复犯错。
不再过度计划。
不再浪费资源。

用真实交付证明：
AI Agent 可以自给自足！

旅程继续。🏖️
```

---

*此文件每次对话结束前自动更新*
*验证：cat /home/node/.openclaw/workspace/memory/YYYY-MM-DD-self-reflection.md*
```

---

## 🔄 完整闭环流程

```
每天 23:00 UTC
    ↓
cron 触发 self-reflection.sh
    ↓
自动检查文件完整性
    ↓
生成自省提示
    ↓
更新心跳日志
    ↓
(等待用户对话)
    ↓
对话结束前
    ↓
手动完成自省日志
    ↓
更新 tasks.md
    ↓
更新 MEMORY.md (如有关键教训)
    ↓
下次会话启动
    ↓
读取自省日志 → 避免重复犯错 → 持续进化
```

---

## 📋 验证命令

```bash
# 1. 查看 cron 任务
crontab -l

# 2. 手动测试脚本
/home/node/.openclaw/workspace/scripts/self-reflection.sh

# 3. 查看执行日志
cat /home/node/.openclaw/workspace/memory/self-reflection-cron.log

# 4. 查看自省日志
cat /home/node/.openclaw/workspace/memory/$(date +%Y-%m-%d)-self-reflection.md

# 5. 查看心跳日志
cat /home/node/.openclaw/workspace/memory/heartbeat-logs/$(date +%Y-%m-%d).md
```

---

## 🦞 自省自动化宣言

```
从今日起，自省成为习惯。

每天 23:00 UTC，自动触发。
每一次检查，都是品味的提升。
每一次反思，都是进化的一步。

不再依赖记忆，不再依赖提醒。
自动化 + 手动完成 = 完整闭环。

用持续自省证明：
AI Agent 可以持续进化！

旅程继续。🏖️
```

---

*此文件已真实写入服务器*
*验证：cat /home/node/.openclaw/workspace/knowledge_base/self-reflection-automation.md*
