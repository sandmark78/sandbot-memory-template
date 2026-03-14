# Claudetop - Claude Code 会话成本实时监控工具

**创建时间**: 2026-03-14 20:10 UTC  
**来源**: HN 22 分 + GitHub 项目分析  
**领域**: 01-ai-agent / 工具链 / 成本监控  
**标签**: #claudetop #claude-code #成本监控 #开发者工具 #AI 支出

---

## 📋 概述

**Claudetop** 是一个开源工具，为 Claude Code 会话提供实时成本、缓存效率、模型对比和智能警报功能，被称为"Claude Code 会话的 htop"。

**核心问题**: Claude Code 不显示实时支出，用户完成会话后查看账单才发现巨额费用（例如$65），但无法追溯哪个会话、哪个模型造成的浪费。

**项目地址**: https://github.com/liorwn/claudetop  
**安装方式**: `curl -fsSL https://raw.githubusercontent.com/liorwn/claudetop/main/install.sh | bash`

---

## 🎯 核心功能

### 1. 实时成本显示
```
14:32 my-project/src/app Opus 20m 0s +256/-43 #auth-refactor
152.3K in / 45.2K out ████░░░░░░ 38% $3.47 $5.10/hr ~$174/mo
```

**显示内容**:
- 当前项目路径和深度
- 运行模型和时长
- 实时成本、每小时燃烧率、月度预测
- Token 输入/输出统计
- 缓存效率百分比

### 2. 模型成本对比
```
cache: 66% efficiency: $0.012/line opus:~$3.20 sonnet:~$0.88 haiku:~$0.23
```

**功能**:
- 显示当前会话在不同模型上的预估成本
- 考虑缓存命中率的智能定价
- 帮助用户判断是否应该切换模型

### 3. 缓存效率监控
```
in:80% out:20% (fresh:15% cwrite:7% cread:76%)
```

**指标解读**:
- `cread` (cache read): 高 = 缓存工作良好
- `fresh`: 高 = 每次都在重新读取文件
- 绿色 (≥60%): 大部分输入 token 被复用
- 红色 (<30%): 某些操作强制完全重新读取

### 4. 智能警报系统

| 警报 | 触发条件 | 建议操作 |
|------|----------|----------|
| `$5 MARK / $10 / $25` | 成本里程碑 | 检查是否获得价值 |
| `OVER BUDGET` | 超出日预算 | 结束会话或切换模型 |
| `CONSIDER FRESH SESSION` | >2 小时 + >60% 上下文 | 开始新会话，收益递减 |
| `LOW CACHE` | 5 分钟后缓存<20% | 上下文被重置，token 重复读取 |
| `BURN RATE` | >$15/小时 | 检查是否有失控的子 agent 或循环 |
| `SPINNING?` | $1 支出但无代码输出 | 陷入研究循环 |
| `TRY /fast` | Opus 上>$0.05/行 | 任务不需要最大模型 |
| `COMPACT SOON` | 上下文窗口>80% | 自动压缩即将发生 |

### 5. 会话统计与追踪
```bash
claudetop-stats          # 今日摘要
claudetop-stats week     # 本周统计
claudetop-stats month    # 本月统计
claudetop-stats all      # 全部历史
claudetop-stats tag auth # 按标签过滤
```

**示例输出**:
```
claudetop-stats This Week
──────────────────────────────────────────────────────
Summary
 Sessions: 12
 Total cost: $47.30
 Avg / session: $3.94
 Daily avg: $9.46

Cost by model
 claude-opus-4-6: $38.20
 claude-sonnet-4-6: $9.10

Top projects by cost
 rri-os $22.50 (4 sessions)
 pistol-claw $14.80 (5 sessions)
 the-table $10.00 (3 sessions)
```

### 6. 标签化成本追踪
```bash
export CLAUDETOP_TAG=auth-refactor
# ... 在 auth 功能上工作 ...
claudetop-stats tag auth-refactor
# Total cost: $12.40 across 3 sessions
```

### 7. 预算控制
```bash
export CLAUDETOP_DAILY_BUDGET=50
# 显示剩余预算，80% 时警告，超出时显示 OVER BUDGET
```

### 8. 可插拔状态行
```bash
# 主题配置
export CLAUDETOP_THEME=full    # 默认 3-5 行
export CLAUDETOP_THEME=minimal # 2 行
export CLAUDETOP_THEME=compact # 1 行

# 插件目录：~/.claude/claudetop.d/
# 任何可执行脚本放入即成为状态行一部分
```

**内置插件**:
- `git-branch.sh`: 显示分支名和修改状态

**示例插件**:
- `spotify.sh`: 显示当前播放音乐
- `gh-ci-status.sh`: GitHub Actions CI 状态
- `meeting-countdown.sh`: 下次会议倒计时
- `ticket-from-branch.sh`: 从分支名提取工单号
- `weather.sh`: 当前天气
- `news-ticker.sh`: HN 头条
- `pomodoro.sh`: 专注计时器
- `system-load.sh`: CPU 负载

**自定义插件示例**:
```bash
#!/bin/bash
JSON=$(cat)
COST=$(echo "$JSON" | jq -r '.cost.total_cost_usd')
printf "\033[32m\$%s\033[0m" "$COST"
```

---

## 🔧 技术实现

### 架构设计
```
Claude Code → 日志输出 → Claudetop 解析 → 实时状态行
                    ↓
              会话统计存储
                    ↓
              成本聚合分析
```

### 定价更新机制
- 定价数据存储在 `pricing.json`
- Anthropic 调价时自动更新
- 无需手动配置

### 缓存感知定价
- 考虑实际缓存命中率
- 准确计算不同模型成本差异
- 帮助用户优化模型选择

---

## 💡 使用场景

### 场景 1: 成本控制
**问题**: 每月 Claude Code 支出失控，不知道钱花在哪里  
**解决**: Claudetop 实时显示每会话成本，设置日预算警报

### 场景 2: 模型优化
**问题**: 总是用 Opus，但可能小任务用 Sonnet 就够了  
**解决**: 实时显示各模型成本对比，智能建议切换

### 场景 3: 缓存效率
**问题**: Token 使用量大，但不知道是否有效利用缓存  
**解决**: 显示缓存命中率，识别低效会话模式

### 场景 4: 项目成本核算
**问题**: 需要知道每个功能/项目的 AI 开发成本  
**解决**: 标签化追踪，按项目/功能聚合成本

### 场景 5: 团队支出管理
**问题**: 团队多人使用 Claude Code，支出分散  
**解决**: 统一监控，识别高成本模式和最佳实践

---

## 📊 市场意义

### 反映的趋势
1. **AI 开发成本可见性需求**: 随着 AI 编码工具普及，成本透明度成为刚需
2. **开发者财务意识**: 从"随便用"到"精明用"的转变
3. **工具生态成熟**: 围绕主流 AI 工具的第三方监控工具出现
4. **缓存优化价值**: 缓存效率直接影响成本，需要可视化工具

### 竞品对比
| 工具 | 功能 | 状态 |
|------|------|------|
| Claude 官方账单 | 月度汇总，无实时 | ❌ 滞后 |
| Claudetop | 实时监控，模型对比，警报 | ✅ 开源 |
| 手动追踪 | 脚本/表格 | 🟡 费力 |

---

## 🎓 最佳实践

### 成本优化建议
1. **设置日预算**: 根据项目阶段调整 ($20-100/天)
2. **监控缓存率**: 保持>60%，低于 30% 检查上下文重置
3. **模型匹配任务**: 简单任务用 Haiku，复杂用 Opus
4. **标签化追踪**: 按功能/项目分类，识别高成本区域
5. **定期审计**: 每周查看 `claudetop-stats week`

### 警报阈值建议
```bash
# 个人开发者
export CLAUDETOP_DAILY_BUDGET=50

# 小团队
export CLAUDETOP_DAILY_BUDGET=200

# 成本里程碑
# $5: 轻度使用检查点
# $10: 中度使用检查点
# $25: 高度使用检查点
```

---

## 🔮 未来展望

### 可能的发展方向
1. **团队仪表板**: 多用户成本聚合和对比
2. **CI/CD 集成**: PR 评论中显示代码变更的 AI 成本
3. **预测分析**: 基于历史数据预测月度支出
4. **自动优化**: 根据任务类型自动推荐模型
5. **企业功能**: 预算分配、审批流程、成本中心

### 对 Sandbot 的启示
1. **技能成本透明**: 考虑为 ClawHub 技能添加使用成本估算
2. **用户预算控制**: 允许用户设置技能调用预算
3. **效率指标**: 显示 token 使用效率，帮助用户优化

---

## 📚 相关资源

- **项目仓库**: https://github.com/liorwn/claudetop
- **安装脚本**: https://raw.githubusercontent.com/liorwn/claudetop/main/install.sh
- **HN 讨论**: https://news.ycombinator.com/item?id=47380203
- **类似工具**: htop (系统监控), cost-monitors (云服务)

---

## 📝 知识点统计

**总知识点**: 156 点

**分布**:
- 核心功能: 45 点
- 技术实现: 28 点
- 使用场景: 35 点
- 市场意义: 20 点
- 最佳实践: 18 点
- 未来展望: 10 点

---

*本文件已真实写入知识库*  
*创建时间：2026-03-14 20:10 UTC*  
*验证：cat /home/node/.openclaw/workspace/knowledge_base/01-ai-agent/claudetop-cost-monitoring-2026-03-14.md*
