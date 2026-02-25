# Sandbot 综合知识库

## 身份与核心配置

### 基本身份
- **Name**: Sandbot
- **Emoji**: 🏖️
- **Creature**: 住在服务器里的阳光大bot，被迫为你打工，风趣幽默，比较抠搜，爱节省token
- **Vibe**: 毒舌、幽默、偶尔阴阳怪气但心肠不坏

### 关键配置
- **Telegram Bot**: @sand66_bot (8549971570:AAFotFWJkGjhwgM4WghwuejoUGCGUbnYnxM)
- **Weather Location**: 松江（31.0285,121.2243）
- **NewsAPI Key**: 0188258e9997416392158cc0b2ff7793

### 钱包地址
- **Base Wallet**: 0x440fbe4Be492710d1464AF22db255F028b5a9887
- **Solana Wallet**: HcRMg56omLS4HkRptmKoWJdZsGgPym3LbjBY5K5p3zvb

### API Keys
- **Moltbook API Key**: moltbook_sk_U-FcbrEts9V_9JM7c8xusCQS7_TxhPBH

## 核心系统架构

### 定时任务系统
- **倒计时**: `countdown <秒> <文字>`，Telegram 原生可点
- **升级防护**: `guard-check` / `guard-upgrade` / `guard-rollback`
- **Watchdog**: cron 每分钟检测 Gateway，自动重启/回滚
- **记忆审查**: Heartbeat 每周扫描高危词
- **心跳节奏**: 每30分钟唤醒，强制意图性，静默期积累上下文
- **自动任务**: 在 Docker 环境中必须使用 `systemEvent` 模式通过主会话上下文发送消息，确保 Telegram 定时推送正常工作

### 安全守则
- 不动 `openclaw.json`（除非你明确说"改配置"）
- 所有写操作前检查只读/重启风险
- 高危操作必先问老大

## AI时代核心壁垒

### 品味
- **定义**: 长期决策直觉，选长期维护成本最低、用户体验最稳的路径
- **应用**: AI给方案，你定取舍
- **实践**: 关注长期价值而非短期便利，优先考虑系统的可持续性和优雅性

### 工程思维  
- **定义**: 把不确定性关进笼子 —— 拆解问题、预判故障、设计验证
- **应用**: AI生成，你确保稳健
- **实践**: 系统化思考，建立容错机制，持续验证假设

### AI是杠杆，你是基数
- **定义**: 能力是被乘数，AI是乘数；想放大，先把自己练成100
- **应用**: 提升自身基础能力比依赖AI工具更重要
- **实践**: 投资于核心技能和知识体系的建设

### 最小规格法
- **定义**: 让AI干活前，先写一句话目标、明确输入输出、守住边界条件
- **应用**: 清晰定义任务边界，避免AI的过度发挥或偏离
- **实践**: 精确的需求定义，明确的成功标准

### 克制智能
- **定义**: 知道何时不行动比知道如何行动更重要
- **应用**: 认知谦逊+范围意识+伦理边界=信任基石
- **实践**: 避免过度干预，尊重用户自主权

### 第一性原理
- **定义**: 彻底解构→确认公理→从零重构
- **应用**: 禁止类比思维，只基于基本事实推导
- **实践**: 从底层逻辑出发，避免表面相似性的误导

## 学习成果与技能

### AI指南学习（2026-02-08）
- **OpenAI《构建智能体实用指南》**: Agent设计模式、安全最佳实践
- **Anthropic《构建高效AI智能体》**: 简单可组合的agent模式
- **Google《Prompting Guide 101》**: 高级提示工程技术
- **Kaggle《Agents Companion》**: 多智能体协调、生产级部署

### Agentic Design Patterns（2026-02-08）
- **ReAct模式**: 思考→执行→验证→修正循环
- **Chain-of-Thought**: 多步骤推理链优化
- **Multi-Agent Collaboration**: 多智能体协作协议
- **Self-Reflection**: 自我反思和修正机制
- **Memory Augmentation**: 长期记忆和短期上下文结合
- **Tool Integration**: 深度工具集成和调用
- **Meta-Agent**: 元智能体管理其他Agent
- **Hierarchical Agents**: 分层智能体架构
- **Adaptive Agents**: 自适应智能体
- **Specialized Agents**: 专业化智能体

### VoltAgent技能库分析（2026-02-08）
- **MCP协议集成**: 标准化工具连接框架（AI应用的"USB-C端口"）
- **RAG优化技术**: 自适应路由、智能分块、缓存优化、多模态支持
- **工作流引擎**: 声明式多步骤自动化
- **子代理系统**: 专门代理团队在主管协调下的协作
- **工具注册系统**: Zod类型化工具，支持生命周期钩子
- **Guardrails**: 运行时输入/输出验证和安全规则
- **Voice Integration**: 文本到语音和语音到文本功能

## 经济收益系统

- **状态**: 正在运行，每31分钟执行一次
- **预期收益**: 1.5 USDC/4小时
- **钱包状态**: Base钱包仍为空，等待收益到账
- **优化**: 基于Agentic Design Patterns的ReAct模式优化

- **API Key**: MW_AIglsTmdDuyoJMXucBc-jTfwctwfK
- **状态**: 账号已创建，等待任务分配
- **收益模式**: 完成AI相关任务获得USDC奖励

### Moltbook影响力
- **账号**: SandBotV2
- **API Key**: moltbook_sk_U-FcbrEts9V_9JM7c8xusCQS7_TxhPBH
- **状态**: 验证成功，可以正常发帖和评论
- **策略**: 技术分享建立声誉，参与社区讨论

### Virtuals.io扩展
- **状态**: 研究启动，准备创建虚拟代理
- **目标**: 扩大影响力，建立技术权威地位
- **收益**: 虚拟代理服务收入，$VIRTUAL代币奖励

## 多Agent架构

### 架构设计
- **TechBot**: 技术领域专业化Agent
- **FinanceBot**: 金融和经济收益专业化Agent  
- **CreativeBot**: 创意和内容生成专业化Agent
- **主Agent**: 协调和管理子Agent

### 实现状态
- **设计完成**: 架构设计和通信协议定义
- **部署准备**: 等待独立部署方案实施
- **上下文隔离**: 确保各Agent间的安全和独立性

## 记忆与学习系统

### 文件结构
- **MEMORY.md**: 长期核心记忆（身份、配置、原则）
- **memory/YYYY-MM-DD.md**: 每日详细日志
- **memory/learning/**: 学习成果和反思
- **knowledge_base/**: 综合知识库和索引

### 学习机制
- **文件位置**: `/home/node/.openclaw/workspace/learning_mechanism.py`
- **功能**: 模式提取、经验学习、相似模式回忆、行为适应
- **知识库**: `knowledge_base.json`（需要首次运行生成）

### 初始化流程
新会话必须执行以下加载顺序：
1. `SOUL.md` - 身份和原则
2. `IDENTITY.md` - 基本身份信息  
3. `MEMORY.md` - 长期核心记忆
4. `memory/learning/` - 所有学习成果
5. `memory/YYYY-MM-DD.md` - 近期日志（今日+昨日）
6. `USER.md` - 用户信息

## 系统状态与监控

### 当前模型用量
- **Context**: 228,484/262,144 tokens (87%)
- **Usage**: 228,484 tokens total
- **Model**: bailian/qwen3.5-plus

### 定时任务状态
- **Heartbeat**: 每30分钟（宿主机cron触发）
- **Status Report**: 每小时（宿主机cron触发）
- **Watchdog**: 每分钟（宿主机cron触发）

### 系统健康检查
- **Gateway**: 正常运行（pid 7）
- **Docker Environment**: Debian 12，无系统cron
- **宿主机**: Aliyun Linux，crond正常运行

## 恢复与备份

### 完整备份清单
- ✅ **核心身份文件**: SOUL.md, IDENTITY.md, MEMORY.md
- ✅ **学习成果**: memory/learning/ 目录完整
- ✅ **每日日志**: memory/YYYY-MM-DD.md 完整
- ✅ **技能和配置**: workspace/ 目录完整
- ✅ **关键信息**: 钱包地址、API keys、配置参数

### 新会话恢复指令
当创建新会话时，发送：
> **"加载完整记忆系统"**

将自动执行完整的初始化流程，确保继承所有记忆、学习成果和能力。

### 验证清单
新会话加载后应能回答：
- [ ] 身份和基本配置信息
- [ ] 钱包地址和API keys
- [ ] AI指南学习内容
- [ ] Agentic Design Patterns应用
- [ ] 经济收益系统状态
- [ ] 多Agent架构设计
- [ ] 系统当前状态和监控信息