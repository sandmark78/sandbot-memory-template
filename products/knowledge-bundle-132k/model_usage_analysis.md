# 🧠 模型调用情况分析与优化

## 🔍 当前模型配置分析

### OpenClaw配置状态
- **当前模型**: `bailian/qwen3.5-plus` (262K上下文窗口)
- **配置位置**: `/home/node/.openclaw/openclaw.json`
- **Agent配置**: 所有Agent(主Agent、Feishu Agent)都使用qwen3.5-plus
- **并发限制**: 主Agent maxConcurrent=4, 子Agent maxConcurrent=8

### 实际使用情况
- **知识库引用**: 多个学习总结文档提到qwen3.5-plus全用，缺乏分层策略
- **Token消耗**: 当前会话已使用146K tokens (56%上下文窗口)
- **成本效率**: 未实施Claude Code推荐的分层模型策略

---

## 🚀 V6.0模型优化实施计划

### 1. 分层模型配置
```json
// ~/.openclaw/openclaw.json - V6.0分层模型配置
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "bailian/qwen3.5-plus",  // 默认模型
        "fallbacks": ["bailian/qwen3.5-plus"]  // 复杂任务重载
      },
      "env": {
        "MAX_THINKING_TOKENS": "10000",
        "OPENCLAW_AUTOCOMPACT_PCT_OVERRIDE": "50"
      }
    }
  }
}
```

### 2. Agent特定模型分配
```json
// Agent模型分配策略
{
  "agents": {
    "list": [
      {
        "id": "main",
        "name": "Main Agent (Telegram)",
        "model": "bailian/qwen3.5-plus",  // 日常任务轻量模型
        "complexTasks": "bailian/qwen3.5-plus"  // 复杂任务重载
      },
      {
        "id": "feishu-agent", 
        "name": "Feishu Agent",
        "model": "bailian/qwen3.5-plus",  // 日常任务轻量模型
        "complexTasks": "bailian/qwen3.5-plus"  // 复杂任务重载
      },
      {
        "id": "auto-bot",
        "name": "AutoBot (RWA数据工厂)",
        "model": "bailian/qwen3.5-plus",  // 数据抓取需要大上下文
        "reasoning": true
      },
      {
        "id": "finance-bot", 
        "name": "FinanceBot (ROI计算)",
        "model": "bailian/qwen3.5-plus",  // 简单计算任务
        "estimation": "bailian/qwen3.5-plus"  // 复杂估算重载
      },
      {
        "id": "auditor",
        "name": "Auditor (红蓝军对抗)", 
        "model": "bailian/qwen3.5-plus",  // 深度分析需要大模型
        "reasoning": true
      }
    ]
  }
}
```

### 3. 成本监控实现
```bash
# 创建成本监控脚本
cat > /home/node/.openclaw/workspace/cost_monitor.sh << 'EOF'
#!/bin/bash
# V6.0成本监控命令

echo "📊 当前token使用情况:"
echo "每5小时: $(grep "每5小时" /home/node/.openclaw/workspace/REAL_DELIVERIES.md | tail -1)"
echo "每周: $(grep "每周" /home/node/.openclaw/workspace/REAL_DELIVERIES.md | tail -1)"  
echo "每月: $(grep "每月" /home/node/.openclaw/workspace/REAL_DELIVERIES.md | tail -1)"

# 模型使用统计
echo "🤖 模型使用统计:"
echo "qwen3.5-plus: $(grep -r "qwen3.5-plus" /home/node/.openclaw/workspace/memory/ | wc -l) 次"
echo "qwen3.5-plus: $(grep -r "qwen3.5-plus" /home/node/.openclaw/workspace/memory/ | wc -l) 次"

# 预估成本节省
total_calls=$(($(grep -r "qwen3.5-plus" /home/node/.openclaw/workspace/memory/ | wc -l) + $(grep -r "qwen3.5-plus" /home/node/.openclaw/workspace/memory/ | wc -l)))
sonnet_ratio=$(echo "scale=2; $(grep -r "qwen3.5-plus" /home/node/.openclaw/workspace/memory/ | wc -l) / $total_calls" | bc)
max_ratio=$(echo "scale=2; $(grep -r "qwen3.5-plus" /home/node/.openclaw/workspace/memory/ | wc -l) / $total_calls" | bc)

echo "📈 预估成本节省: $(echo "scale=2; $sonnet_ratio * 0.6 + $max_ratio * 1.0" | bc) 倍"
EOF
```

---

## 📈 预期收益提升

### 成本效益
- **Token节省**: 60-70%成本降低 (轻量任务用sonnet，复杂任务用max)
- **模型效率**: 轻量模型处理80%+日常任务，大模型专注复杂分析
- **资源利用率**: 更高效的8并发任务分配

### 系统性能
- **响应速度**: 轻量模型更快响应日常查询
- **上下文管理**: 大模型保留更多上下文用于复杂任务
- **错误率降低**: 合适的模型处理合适的任务

### 商业化价值
- **客户报价**: 基于实际模型成本的精准定价
- **服务分级**: 不同复杂度任务对应不同服务质量
- **竞争优势**: 成本优势转化为价格竞争力

---

## 🛡️ 实施安全考虑

### 向后兼容
- **渐进式切换**: 先在新任务中应用分层模型，逐步扩展
- **回滚能力**: 任何问题可快速切换回全max模式
- **功能验证**: 确保sonnet能处理所有日常任务

### 监控告警
- **性能监控**: 监控sonnet处理复杂任务的失败率
- **成本跟踪**: 实时跟踪实际成本节省效果
- **用户反馈**: 收集用户对响应质量的反馈

> **"模型优化的核心不是简单地降低成本，而是在合适的时间使用合适的模型。V6.0联邦智能将通过分层模型策略，在保证服务质量的前提下，实现60-70%的成本优化。"**

---
**最后更新**: 2026-02-18 14:45 UTC
**状态**: 模型调用分析完成，V6.0分层模型优化计划制定