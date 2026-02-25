---
name: agent-lightning
description: Microsoft Agent Lightning - RL training for AI agents with zero code change
homepage: https://github.com/microsoft/agent-lightning
metadata: {"openclaw":{"emoji":"⚡","requires":{"bins":["python3","pip"],"env":["OPENAI_API_KEY"]},"primaryEnv":"OPENAI_API_KEY"}}
---

# Agent Lightning ⚡

**Microsoft Research 的 AI Agent 强化学习训练框架**

## 🔥 核心功能

### 零代码修改
- 无需修改现有 Agent 代码
- 支持任何 Agent 框架 (LangChain, AutoGen, CrewAI 等)
- 也可以不使用框架直接调用 OpenAI API

### 选择性优化
- 在多 Agent 系统中选择性优化特定 Agent
- 支持并行优化多个 Agent

### 算法支持
- 强化学习 (Reinforcement Learning)
- 自动提示词优化 (Automatic Prompt Optimization)
- 监督微调 (Supervised Fine-tuning)
- 更多算法持续更新

## 📦 安装

```bash
pip install agentlightning
```

## 🚀 快速开始

### 基础用法
```python
import agentlightning as agl

# 初始化
agl.init(project="my-agent-project")

# 在你的 Agent 代码中添加
@agl.trace
def my_agent(prompt):
    # 你的 Agent 逻辑
    return response

# 记录奖励
agl.emit_reward(trace_id, reward_value)
```

### OpenClaw 集成
```python
import agentlightning as agl

# 在子 Agent 中使用
def optimize_agent(agent_id, task):
    agl.init(project=f"openclaw-{agent_id}")
    
    # 执行任务并收集轨迹
    trace = agl.trace(agent_execution)
    
    # 根据结果发射奖励
    reward = calculate_reward(task_result)
    agl.emit_reward(trace.id, reward)
```

## 📊 使用场景

### 1. Agent 性能优化
- 优化提示词模板
- 改进工具调用策略
- 提升任务完成率

### 2. 多 Agent 协调
- 优化 Agent 间协作
- 平衡资源分配
- 减少冲突

### 3. 持续学习
- 从历史轨迹学习
- 适应新任务
- 持续改进性能

## 📚 资源

- **文档**: https://microsoft.github.io/agent-lightning/
- **GitHub**: https://github.com/microsoft/agent-lightning
- **论文**: https://arxiv.org/abs/2508.03680
- **Discord**: https://discord.gg/RYk7CdvDR7

## ⚠️ 注意事项

1. **API 密钥**: 需要配置 OPENAI_API_KEY 或其他 LLM API
2. **存储**: 需要配置存储后端保存训练数据
3. **计算资源**: RL 训练可能需要较多计算资源
4. **收敛时间**: 根据任务复杂度，可能需要多次迭代

## 🔧 OpenClaw 子 Agent 集成

### TechBot 使用示例
```python
# 优化技术教程生成质量
def optimize_tutorial_generation():
    agl.init(project="techbot-tutorials")
    
    @agl.trace
    def generate_tutorial(topic):
        # TechBot 生成教程
        return tutorial
    
    # 根据用户反馈发射奖励
    agl.emit_reward(trace_id, user_rating)
```

### FinanceBot 使用示例
```python
# 优化 ROI 预测准确性
def optimize_roi_prediction():
    agl.init(project="financebot-predictions")
    
    # 记录预测和实际结果
    agl.emit_reward(trace_id, accuracy_score)
```
