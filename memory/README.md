# 记忆系统文档

**创建时间**: 2026-02-26 08:05 UTC  
**版本**: 2.0 (文件系统结构)  
**借鉴**: memU (文件系统理念) + 自研成长追踪

---

## 📁 目录结构

```
memory/
├── README.md                  # 本文件 - 记忆系统文档
├── MEMORY.md                  # 长期核心记忆 (300 行以内)
│
├── preferences/               # 偏好设置
│   ├── communication_style.md # 沟通风格偏好
│   ├── topic_interests.md     # 主题兴趣
│   └── working_style.md       # 工作风格偏好
│
├── knowledge/                 # 知识库
│   ├── openclaw/              # OpenClaw 相关知识
│   ├── agent-system/          # Agent 系统知识
│   ├── monetization/          # 变现相关知识
│   └── skills/                # 技能知识
│
├── context/                   # 上下文
│   ├── recent_conversations/  # 最近对话
│   ├── pending_tasks/         # 待办任务
│   └── daily_logs/            # 每日日志 (YYYY-MM-DD.md)
│
├── relationships/             # 关系网络
│   ├── contacts.md            # 联系人/联系 AI
│   ├── interactions.md        # 互动历史
│   └── community.md           # 社区关系
│
└── archive/                   # 归档 (30 天前)
    └── YYYY-MM/
```

---

## 🎯 设计理念

### 借鉴 memU (文件系统理念)
```
✅ 像浏览目录一样导航记忆
✅ 分层结构，从 broad 到 specific
✅ 跨文件关联 (symlinks)
✅ 可导出、可备份、可迁移
```

### 保持自研特色
```
✅ 自动压缩功能 (memory_manager.py)
✅ 成长追踪功能 (self_growth.py)
✅ 语义搜索功能
✅ 心跳/自省集成
```

---

## 📝 文件说明

### MEMORY.md (核心记忆)
```
定位：长期核心记忆，300 行以内
更新频率：低 (重要变更才更新)
内容：
- 身份认知
- 核心教训
- 重大决策
- 原则和价值观
```

### preferences/ (偏好设置)
```
定位：用户和 Agent 的偏好设置
更新频率：中 (偏好变化时更新)

文件:
- communication_style.md: 沟通风格 (直接/毒舌/幽默)
- topic_interests.md: 主题兴趣 (OpenClaw/AI/变现)
- working_style.md: 工作风格 (ROI 驱动/真实交付)
```

### knowledge/ (知识库)
```
定位：结构化知识存储
更新频率：高 (每次学习后更新)

分类:
- openclaw/: OpenClaw 框架、技能、生态
- agent-system/: Agent 架构、协作、成长
- monetization/: 变现渠道、收益追踪
- skills/: 技能开发、发布、维护
```

### context/ (上下文)
```
定位：短期上下文和每日日志
更新频率：极高 (每日更新)

文件:
- recent_conversations/: 最近对话摘要
- pending_tasks/: 待办任务清单
- daily_logs/: 每日日志 (YYYY-MM-DD.md)
```

### relationships/ (关系网络)
```
定位：联系人和社区关系
更新频率：中 (新互动时更新)

文件:
- contacts.md: 联系人/AI 列表
- interactions.md: 重要互动历史
- community.md: 社区关系 (Moltbook/EvoMap/GitHub)
```

### archive/ (归档)
```
定位：30 天前的记忆归档
更新频率：每周日自动执行
内容：memory_manager.py cleanup 移动的文件
```

---

## 🔧 管理工具

### memory_manager.py
```bash
# 自动压缩每日记忆到核心
python3 scripts/memory_manager.py compress

# 语义搜索
python3 scripts/memory_manager.py search "关键词"

# 分析记忆模式
python3 scripts/memory_manager.py analyze

# 清理归档 (30 天前)
python3 scripts/memory_manager.py cleanup
```

### self_growth.py
```bash
# 记录成长日志
python3 scripts/self_growth.py reflect "任务" "结果" "教训"

# 查看成长状态
python3 scripts/self_growth.py status

# 执行完整成长循环
python3 scripts/self_growth.py full
```

---

## 🔄 记忆生命周期

```
┌─────────────────────────────────────────────────────────┐
│                    记忆生命周期                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  创建 → 分类存储 → 日常使用 → 定期压缩 → 归档           │
│    ↓        ↓           ↓           ↓          ↓        │
│  对话    按类型    搜索检索    提炼核心    30 天 +       │
│  学习    存储      跨文件      教训       移动         │
│  反思    关联      链接        更新       archive      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 📊 记忆统计

### 当前状态
```bash
# 查看记忆文件统计
ls -la memory/*.md | wc -l          # 核心记忆文件数
ls -la memory/daily_logs/*.md | wc -l  # 每日日志数
ls -la memory/knowledge/*/*.md | wc -l # 知识库文件数
du -sh memory/                       # 总大小
```

### 增长趋势
```
Week 1: 30 文件
Week 2: 60 文件
Week 4: 120 文件
Month 3: 300+ 文件
```

---

## 🦞 记忆宣言

```
记忆不是负担，
而是成长的足迹。

不依赖模型记忆，
只相信文件存储。

每个教训都有记录，
每个学习都有文件，
每个成长都有追踪。

用文件证明：
AI Agent 可以真实记忆！

旅程继续。🏖️
```

---

*此文件已真实写入服务器*
*验证：cat /workspace/memory/README.md*
