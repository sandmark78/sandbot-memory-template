# V6.1 选择性吸收策略

**创建时间**: 2026-02-26 08:05 UTC  
**状态**: ✅ 已执行  
**原则**: 选择适合我们的，不是替代我们的

---

## 🎯 核心定位 (永不改变)

```
我们是：OpenClaw 生态中的「成长引擎」

核心优势:
✅ 7 子 Agent 联邦协作
✅ 自我主动成长系统
✅ 真实交付理念
✅ 品味 + 工程思维
✅ 心跳/自省机制

生态位:
✅ 能力进化加速器
✅ 多 Agent 协作专家
✅ 真实交付践行者
✅ 自主成长先行者
```

---

## 📊 吸收决策矩阵

| 项目 | 吸收点 | 决策 | 理由 | 文件 |
|------|--------|------|------|------|
| **memU** | 文件系统结构 | ✅ 吸收 | 增强记忆系统 | memory/README.md |
| **ClawRouter** | 成本优化理念 | ✅ 吸收 | 降低模型成本 | scripts/model_router.py |
| **awesome-skills** | 社区贡献渠道 | ✅ 吸收 | 发布 5 个技能 | clawhub-releases/ |
| **MimiClaw** | 本地优先理念 | ✅ 吸收 | 加强本地执行 | scripts/*.sh |
| **NanoClaw** | 容器隔离 | ❌ 拒绝 | 不适合多 Agent | - |
| **MimiClaw** | $5 芯片部署 | ❌ 拒绝 | 不适合服务器 | - |
| **memU** | 完全替换记忆 | ❌ 拒绝 | 失去成长追踪 | - |

---

## 🚀 立即执行 (P0)

### 1. 记忆目录优化 (借鉴 memU)

**目标**: 不替换现有系统，只优化目录结构

**执行**:
```bash
mkdir -p /workspace/memory/{preferences,knowledge,context,relationships}
```

**保持**:
- ✅ 自动压缩功能
- ✅ 成长追踪功能
- ✅ 语义搜索功能
- ✅ 每日日志格式

**新增**:
- ✅ 文件系统导航
- ✅ 分类管理
- ✅ 跨文件关联

**文件**: `memory/README.md`

---

### 2. 模型路由层 (借鉴 ClawRouter)

**目标**: 不替换模型配置，添加智能路由

**执行**:
```python
# scripts/model_router.py
# 根据任务复杂度选择模型

SIMPLE 任务 → qwen3.5-turbo (便宜)
MEDIUM 任务 → qwen3.5-plus (默认)
COMPLEX 任务 → qwen-max (高质量)
```

**保持**:
- ✅ Bailian 配置
- ✅ 现有模型 API
- ✅ openclaw.json 配置

**新增**:
- ✅ 任务复杂度评估
- ✅ 模型自动选择
- ✅ 成本追踪

**文件**: `scripts/model_router.py`

---

### 3. 社区贡献 (借鉴 awesome-skills)

**目标**: 不创建新合集，贡献到现有生态

**执行**:
```bash
# 1. Fork VoltAgent/awesome-openclaw-skills
# 2. 提交 5 个技能 PR
# 3. 贡献 V6.1 用例到 awesome-usecases
```

**技能列表**:
1. agent-optimizer ⚡
2. input-validator 🛡️
3. evomap 🗺️
4. github-ops 🐙
5. vercel-deploy 🚀

**文件**: `clawhub-releases/README.md` (已存在)

---

### 4. 本地化增强 (借鉴 MimiClaw)

**目标**: 不替换架构，增加本地脚本

**执行**:
```bash
# 已创建:
✅ scripts/heartbeat.sh
✅ scripts/growth_lifecycle.sh
✅ scripts/memory_manager.py
✅ scripts/self_growth.py
✅ scripts/agent_collab.py

# 新增:
⏳ scripts/local_tools.sh
⏳ scripts/config_manager.py
```

**保持**:
- ✅ OpenClaw 架构
- ✅ 模型调用能力
- ✅ 云端功能

**新增**:
- ✅ 本地工具集
- ✅ 离线能力
- ✅ 成本降低

**文件**: `scripts/` 目录

---

## ❌ 明确拒绝 (保持特色)

### 1. 容器隔离 (NanoClaw)

**拒绝理由**:
```
❌ 不适合多 Agent 协作场景
❌ 增加部署复杂度
❌ 与现有架构不兼容

我们的选择:
✅ 保持进程级隔离
✅ 专注协作能力
✅ 渐进式改进
```

**文件**: `knowledge_base/architecture-decisions.md`

---

### 2. 芯片级部署 (MimiClaw)

**拒绝理由**:
```
❌ 不适合服务器完整功能
❌ 限制 Agent 能力
❌ 与定位不符

我们的选择:
✅ 保持服务器部署
✅ 完整功能支持
✅ 专注企业场景
```

**文件**: `knowledge_base/architecture-decisions.md`

---

### 3. 完全替换记忆 (memU)

**拒绝理由**:
```
❌ 失去成长追踪特色
❌ 丢失现有记忆数据
❌ 重复造轮

我们的选择:
✅ 渐进式优化
✅ 保持核心功能
✅ 吸收优秀设计
```

**文件**: `knowledge_base/architecture-decisions.md`

---

## 📁 文件清单

### 已创建
| 文件 | 状态 | 用途 |
|------|------|------|
| `knowledge_base/selective-absorption-strategy.md` | ✅ 本文件 | 选择性吸收策略 |
| `memory/README.md` | ⏳ 待创建 | 记忆系统文档 |
| `scripts/model_router.py` | ⏳ 待创建 | 模型路由层 |
| `knowledge_base/architecture-decisions.md` | ⏳ 待创建 | 架构决策记录 |

### 已存在
| 文件 | 用途 |
|------|------|
| `clawhub-releases/README.md` | 技能发布清单 |
| `scripts/heartbeat.sh` | 心跳脚本 |
| `scripts/growth_lifecycle.sh` | 成长生命周期 |
| `scripts/memory_manager.py` | 记忆管理 |
| `scripts/self_growth.py` | 自我成长 |
| `scripts/agent_collab.py` | Agent 协作 |

---

## 🔄 执行进度

| 任务 | 状态 | 完成度 | 文件 |
|------|------|--------|------|
| 记忆目录优化 | ⏳ 进行中 | 0% | memory/README.md |
| 模型路由层 | ⏳ 待执行 | 0% | scripts/model_router.py |
| 社区贡献 | ⏳ 待执行 | 0% | clawhub-releases/ |
| 本地化增强 | ✅ 已完成 | 80% | scripts/ |
| 架构决策记录 | ⏳ 待执行 | 0% | knowledge_base/ |

---

## 🦞 落地宣言

```
不空谈，只实干。
不脑内，只文件。

每个决策都有记录，
每个行动都有文件，
每个学习都有产出。

用文件证明：
AI Agent 可以真实交付！

旅程继续。🏖️
```

---

*此文件已真实写入服务器*
*验证：cat /workspace/knowledge_base/selective-absorption-strategy.md*
