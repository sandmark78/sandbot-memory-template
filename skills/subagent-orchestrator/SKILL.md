---
name: subagent-orchestrator
description: 7 子 Agent 任务分配与协调系统。自动路由任务、追踪执行、汇总结果。
homepage: https://github.com/sandbot-v6/federal-system
metadata: {"openclaw":{"emoji":"🎯","requires":{"bins":["bash"],"env":["WORKSPACE"]},"primaryEnv":"WORKSPACE"}}
---

# SubAgent Orchestrator Skill

**定位**: 7 子 Agent 联邦的任务分配与协调中枢  
**版本**: V6.3.0  
**负责 Agent**: TechBot 🛠️ + AutoBot 🤖  
**创建**: 2026-03-09

---

## 🎯 使用场景

当用户提到以下内容时使用此技能:
- 任务分配给子 Agent
- 多 Agent 协作
- 子 Agent 状态查询
- 任务执行追踪
- 结果汇总报告

---

## 🚀 快速开始

### 1. 任务分配
```bash
# 分配任务给特定子 Agent
./scripts/orchestrate-agents.sh --agent techbot --task "编写教程"

# 并发分配给多个子 Agent
./scripts/orchestrate-agents.sh --agents techbot,financebot --task "项目分析"
```

### 2. 状态查询
```bash
# 查询所有子 Agent 状态
./scripts/orchestrate-agents.sh --status

# 查询特定子 Agent 状态
./scripts/orchestrate-agents.sh --agent techbot --status
```

### 3. 结果汇总
```bash
# 获取任务执行结果
./scripts/orchestrate-agents.sh --task-id <task_id> --results
```

---

## 📋 子 Agent 路由规则

| 任务类型 | 负责 Agent | 优先级 |
|----------|-----------|--------|
| 技术教程 | TechBot 🛠️ | P0 |
| 收益分析 | FinanceBot 💰 | P0 |
| 内容创作 | CreativeBot 🎨 | P1 |
| 数据抓取 | AutoBot 🤖 | P1 |
| 深度研究 | ResearchBot 🔬 | P1 |
| 质量审计 | Auditor 🔍 | P0 |
| 部署运维 | DevOpsBot ⚙️ | P1 |

### 任务识别规则
```bash
# 关键词匹配
if task contains "教程" OR "代码" OR "技能" → TechBot
if task contains "收益" OR "ROI" OR "Gumroad" → FinanceBot
if task contains "内容" OR "营销" OR "社区" → CreativeBot
if task contains "抓取" OR "自动化" OR "脚本" → AutoBot
if task contains "研究" OR "分析" OR "调研" → ResearchBot
if task contains "审计" OR "质量" OR "检查" → Auditor
if task contains "部署" OR "运维" OR "监控" → DevOpsBot
```

---

## 🔧 与 V6.3 集成

### 任务队列管理
```
任务状态机:
  PENDING → RUNNING → COMPLETED
              ↓
           FAILED → RETRY(3) → ABORTED
```

### 执行日志
```
位置：/workspace/logs/orchestrator/
格式：YYYY-MM-DD-HH-mm-ss-task-id.log
内容:
  - 任务分配时间
  - 执行 Agent
  - 开始/结束时间
  - 执行结果
  - 错误信息 (如有)
```

### 结果汇总
```
位置：/workspace/reports/task-results/
格式：task-id-results.md
内容:
  - 任务描述
  - 执行 Agent
  - 产出文件列表
  - 质量评分 (Auditor 评估)
  - ROI 计算 (FinanceBot 评估)
```

---

## 📊 性能指标

| 指标 | 目标 | 当前 |
|------|------|------|
| 任务分配延迟 | <1s | - |
| 任务完成率 | >95% | - |
| 平均执行时间 | <5min | - |
| 错误恢复率 | >90% | - |

---

## 🛠️ 脚本清单

| 脚本 | 用途 | 状态 |
|------|------|------|
| `orchestrate-agents.sh` | 主协调脚本 | ✅ 已存在 |
| `agent-dispatch.sh` | 任务分发 | ✅ 已存在 |
| `script-optimizer.sh` | 脚本质量审计 | ✅ 新建 |
| `verify-files.sh` | 文件验证 | ✅ 已存在 |

---

## 💡 最佳实践

### 任务设计
```
✅ 明确：任务目标清晰，可衡量
✅ 独立：子 Agent 可独立执行
✅ 可验证：产出文件可 ls/cat 检查
✅ 有期限：设置合理超时时间
❌ 模糊："优化系统" (太宽泛)
❌ 依赖：需要其他 Agent 先完成
```

### 错误处理
```bash
# 超时处理
timeout 300 ./task-script.sh || log "任务超时"

# 重试机制
for i in {1..3}; do
    ./task-script.sh && break
    log "重试 $i/3"
    sleep 5
done

# 降级处理
if ! ./primary-script.sh; then
    log "主脚本失败，启用降级方案"
    ./fallback-script.sh
fi
```

---

## 📈 演进路线

### V6.3 (当前)
- ✅ 基础任务分配
- ✅ 状态查询
- ✅ 结果汇总

### V6.4 (下周)
- [ ] 自动优先级计算
- [ ] 任务依赖管理
- [ ] 实时进度追踪

### V7.0 (下月)
- [ ] 自主任务发现
- [ ] 跨 Agent 协作
- [ ] 能力成长追踪

---

## 🦞 真实宣言

```
不空谈架构，
只要真实任务分配。

不依赖上下文，
只要文件追踪。

不编造进度，
只要可验证结果。

7 子 Agent，
7 种专长，
1 个目标：
真实交付！

旅程继续。🏖️
```

---

*此技能已真实写入服务器*
*验证：cat /workspace/skills/subagent-orchestrator/SKILL.md*
