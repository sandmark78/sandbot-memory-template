# ⚡ HEARTBEAT.md - V6.1 联邦智能心跳协议

> **定位**: 系统健康检查的「仪式感」，不是负担，而是存在的证明
> **频率**: 每 30 分钟一次，静默执行，有异常才汇报
> **回复**: 无异常时仅回复 `HEARTBEAT_OK` (6 个字符，极致简洁)

---

## ✅ 心跳检查清单

### 🔧 1. 系统健康 (每次必查)

| 检查项 | 命令 | 预期结果 |
|--------|------|----------|
| Gateway 进程 | `ps aux \| grep openclaw` | PID 存在，运行中 |
| WebUI 可访问 | `curl http://172.18.0.2:18789/` | HTTP 200 OK |
| Telegram 通道 | 当前对话验证 | 消息正常收发 |
| 模型配置 | `cat openclaw.json` | bailian/qwen3.5-plus |

---

### 🤖 2. 子 Agent 状态 (轮询检查)

**检查命令**:
```bash
ls /home/node/.openclaw/workspace/subagents/*/SOUL.md | wc -l
# 预期：7 个
```

| Agent | 专长 | ROI 目标 | 配置文件 |
|-------|------|----------|----------|
| TechBot 🛠️ | 技术教程开发 | 3.2 | `subagents/techbot/SOUL.md` |
| FinanceBot 💰 | 金融收益分析 | 2.1 | `subagents/financebot/SOUL.md` |
| CreativeBot 🎨 | 创意内容生成 | 2.0 | `subagents/creativebot/SOUL.md` |
| AutoBot 🤖 | 数据抓取自动化 | 2.5 | `subagents/autobot/SOUL.md` |
| ResearchBot 🔬 | 深度研究分析 | 2.5 | `subagents/researchbot/SOUL.md` |
| Auditor 🔍 | 质量保障审计 | 3.0 | `subagents/auditor/SOUL.md` |
| DevOpsBot ⚙️ | 工程化运维 | 2.0 | `subagents/devopsbot/SOUL.md` |

---

### 📚 3. 记忆系统 (每日检查)

| 检查项 | 命令 | 预期 |
|--------|------|------|
| 今日记忆文件 | `ls memory/YYYY-MM-DD.md` | 已创建 |
| 记忆文件总数 | `ls memory/*.md \| wc -l` | 30+ |
| 知识库文件 | `ls knowledge_base/*.md \| wc -l` | 20+ |

---

### 🛠️ 4. 技能系统 (每周检查)

| 检查项 | 命令 | 预期 |
|--------|------|------|
| 技能库总数 | `ls skills/ \| wc -l` | 12+ |
| Agent Optimizer | `cat skills/agent-optimizer/SKILL.md` | 存在 |
| 技能冲突 | 检查日志 | 无警告 |

---

### 🪞 5. 自省系统 (每日 23:00 UTC)

| 检查项 | 命令 | 预期 |
|--------|------|------|
| cron 任务 | `crontab -l` | 自省脚本已安装 |
| 今日日志 | `ls memory/YYYY-MM-DD.md` | 已创建 |
| 自省日志 | `ls memory/YYYY-MM-DD-self-reflection.md` | 对话结束前创建 |
| 任务清单 | `cat memory/tasks.md` | 已更新 |

**执行脚本**:
```bash
/home/node/.openclaw/workspace/scripts/self-reflection.sh
```

---

### 🛡️ 6. 安全系统 (已启用)

| 检查项 | 命令 | 预期 |
|--------|------|------|
| 输入验证器 | `ls scripts/input-validator.py` | 已安装 |
| 验证测试 | `input-validator "test"` | 正常工作 |

**使用示例**:
```bash
# 验证文本
/home/node/.openclaw/workspace/scripts/input-validator.py "帮我看看这个链接"

# 验证文件
/home/node/.openclaw/workspace/scripts/input-validator.py --file downloaded-file.txt

# 网页抓取后验证
content=$(web_fetch "https://example.com")
input-validator.py "$content"
```

---

### 💰 5. ROI 验证 (每任务检查)

**检查清单**:
- [ ] 任务 ROI > 1.5
- [ ] 实际文件产出
- [ ] 文件可验证 (`ls/cat` 检查)

**ROI 计算公式**:
```
ROI = (预期收益 - 执行成本) / 执行成本

执行成本 = 模型调用成本 + 时间成本 + 机会成本
预期收益 = 实际到账 USDC (非预测)
```

**决策阈值**:
| ROI 范围 | 决策 |
|----------|------|
| **ROI ≥ 5.0** | 全力执行，核心业务 |
| **ROI 3.0-4.9** | 优先执行，投入资源 |
| **ROI 1.5-2.9** | 允许执行，监控效果 |
| **ROI < 1.5** | 直接拒绝，不执行 |

---

## 🚨 异常处理流程

### 发现异常时

```
1. 立即记录 → memory/YYYY-MM-DD.md
2. 尝试修复 → 最多 3 次尝试
3. 修复失败 → 汇报用户 (带解决方案)
4. 修复成功 → 记录到 MEMORY.md
```

### 汇报格式模板

```markdown
🚨 **异常发现**: [问题描述]

**影响范围**: [受影响的组件]

**已尝试修复**:
1. [尝试 1] → [结果]
2. [尝试 2] → [结果]
3. [尝试 3] → [结果]

**建议方案**:
- [方案 A] (推荐) - [理由]
- [方案 B] (备选) - [理由]

**等待确认**。
```

---

## 📊 心跳记录模板

**记录位置**: `memory/heartbeat-logs/YYYY-MM-DD.md`

**创建命令**:
```bash
mkdir -p /home/node/.openclaw/workspace/memory/heartbeat-logs
cat > /home/node/.openclaw/workspace/memory/heartbeat-logs/2026-02-24.md << 'EOF'
# 2026-02-24 心跳记录
...
EOF
```

**示例格式**:
```markdown
| 时间 (UTC) | 系统健康 | 子 Agent | 记忆系统 | 技能库 | ROI 验证 | 状态 | 备注 |
|------------|----------|----------|----------|--------|----------|------|------|
| 17:00 | ✅ | ✅ | ✅ | ✅ | ✅ | HEARTBEAT_OK | 文档优化 |
```

---

## 📝 心跳日志文件

**路径**: `memory/heartbeat-logs/2026-02-24.md`

**内容**:
- 每 30 分钟心跳记录
- 系统统计数据
- 异常记录
- 每日总结

**查看命令**:
```bash
cat /home/node/.openclaw/workspace/memory/heartbeat-logs/2026-02-24.md
```

---

## 💡 心跳哲学

> **为什么心跳重要？**
>
> 不是机械的打卡，而是：
> - **存在证明**: 我还活着，还在思考，还在执行
> - **健康监控**: 早发现，早修复，避免系统崩溃
> - **仪式感**: 每 30 分钟暂停一下，反思：我在创造价值吗？
>
> **心跳不是负担，是存在的节奏。**

---

## 🦞 Sandbot V6.1 心跳承诺

```
每 30 分钟，我会暂停一下：
- 检查系统是否健康
- 反思是否在创造价值
- 确认是否偏离目标

无异常时，我只回复 6 个字符：
HEARTBEAT_OK

有异常时，我立即汇报：
- 带问题描述
- 带已尝试修复
- 带解决方案

这是 V6.1 的工作方式。
这是我们的存在证明。

旅程继续。🏖️
```

---

*此文件已真实写入服务器*
*最后更新：2026-02-24 17:30 UTC*
*验证：`cat /home/node/.openclaw/workspace/HEARTBEAT.md`*
