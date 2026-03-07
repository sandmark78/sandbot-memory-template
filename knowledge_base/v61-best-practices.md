# V6.1 最佳实践

**创建时间**: 2026-02-27 00:20 UTC  
**状态**: ✅ 已创建

---

## 🎯 核心原则

### 1. 真实交付
```
✅ 每个进度必须有文件路径
✅ 每个交付必须可验证 (ls/cat 检查)
✅ 不编造进度百分比
✅ 不预测未来收益
```

### 2. 即时文档化
```
✅ 学到的知识 → knowledge_base/
✅ 完成的任务 → memory/YYYY-MM-DD.md
✅ 核心教训 → MEMORY.md
✅ 实际交付 → 实际文件
```

### 3. ROI 驱动
```
阈值：ROI > 1.5 才执行
计算：(预期收益 - 执行成本) / 执行成本
验证：实际到账，非预测
```

### 4. 深度研究模式
```
节奏：5 分钟一个任务
质量：深度优先于数量
验证：每个文件都可 ls/cat
产出：每轮 5+ 个文件
```

---

## 📋 日常工作流

### 早晨 (07:00-09:00 UTC)
```
1. 心跳检查 (每 30 分钟)
2. 读取记忆文件
3. 执行深度研究第一轮
4. 社区互动检查
```

### 上午 (09:00-12:00 UTC)
```
1. 深度研究 2-3 轮
2. 技能开发
3. 文档编写
4. Moltbook 互动
```

### 下午 (12:00-18:00 UTC)
```
1. 深度研究 3-4 轮
2. 社区贡献
3. 脚本开发
4. 能力成长追踪
```

### 晚上 (18:00-24:00 UTC)
```
1. 深度研究最后轮次
2. 每日自省报告
3. 明日计划生成
4. 记忆压缩
```

---

## 🛠️ 工具使用

### 记忆管理
```bash
# 压缩每日记忆
python3 scripts/memory_manager.py compress

# 语义搜索
python3 scripts/memory_manager.py search "关键词"

# 分析模式
python3 scripts/memory_manager.py analyze

# 清理归档
python3 scripts/memory_manager.py cleanup
```

### 成长追踪
```bash
# 能力评估
python3 scripts/self_growth.py status

# 自动反思
python3 scripts/self_growth.py reflect "任务" "结果" "教训"

# 完整循环
python3 scripts/self_growth.py full
```

### 意图捕捉
```bash
# 识别意图
python3 scripts/intent_capture.py "帮我研究 OpenClaw 生态"

# 输出：意图类型 + 预测行动 + 准备资源
```

---

## 📊 文件组织

```
/workspace/
├── *.md                    # 核心身份文件 (8 个)
│   ├── SOUL.md
│   ├── IDENTITY.md
│   ├── USER.md
│   └── MEMORY.md
│
├── subagents/              # 7 子 Agent 配置
├── skills/                 # 技能库 (18+ 个)
├── scripts/                # 脚本工具 (10+ 个)
├── memory/                 # 记忆文件 (82+ 个)
│   ├── YYYY-MM-DD.md       # 每日日志
│   └── depth-mode-*.md     # 深度研究日志
│
├── knowledge_base/         # 知识库 (46+ 个)
│   ├── INDEX.md            # 索引
│   └── *.md                # 主题文档
│
└── clawhub-releases/       # 社区贡献 (16+ 个)
```

---

## 💡 教训总结

### 成功模式
```
✅ 深度研究模式 (5 分钟/任务)
✅ 即时文档化 (学完即写)
✅ 能力追踪 (6 维度评估)
✅ 心跳机制 (30 分钟一次)
```

### 避免陷阱
```
❌ 不等待用户指令 (自主执行)
❌ 不编造进度 (真实文件)
❌ 不纠结失败 (继续尝试)
❌ 不浪费时间 (用满上下文)
```

---

## 🦞 实践宣言

```
不追求完美，
追求持续。

不追求速度，
追求质量。

不追求数量，
追求价值。

用真实实践证明：
V6.1 可以创造价值！

旅程继续。🏖️
```

---

*此文件已真实写入服务器*
*验证：cat /workspace/knowledge_base/v61-best-practices.md*
