# 群聊知识归档系统

**版本**: V1.0.0  
**创建时间**: 2026-03-01 14:10 UTC  
**定位**: 将群聊中的知识和经验即时本地化归档

---

## 🎯 系统目标

```
✅ 即时归档 - 学到知识立即保存
✅ 本地存储 - 不依赖外部服务
✅ 分类整理 - 按类型自动分类
✅ 可检索 - 支持关键词和语义搜索
✅ 可追溯 - 记录时间、来源、上下文
```

---

## 📁 目录结构

```
/home/node/.openclaw/workspace/memory/
├── chat-archive/              # 群聊知识归档目录
│   ├── 2026-03-01.md         # 每日归档文件
│   ├── 2026-03-02.md
│   └── ...
├── learning/                  # 学习总结 (已有)
└── tasks.md                   # 任务清单 (已有)

/home/node/.openclaw/workspace/scripts/
└── archive-chat-knowledge.py  # 归档脚本
```

---

## 🛠️ 归档脚本

**路径**: `/home/node/.openclaw/workspace/scripts/archive-chat-knowledge.py`

### 功能
- ✅ 按日期自动创建归档文件
- ✅ 支持分类 (general/technical/strategy/lesson)
- ✅ 记录时间戳和来源
- ✅ Markdown 格式，易于阅读和检索

### 使用方法

#### 方法 1: 直接调用
```bash
python3 /home/node/.openclaw/workspace/scripts/archive-chat-knowledge.py "知识内容" [category]
```

#### 方法 2: OpenClaw exec
```
exec command="python3 archive-chat-knowledge.py 'LightRAG 核心是双层级检索' technical"
```

#### 方法 3: 在对话中自动调用
```python
# 对话结束时，自动调用归档
archive_knowledge("今天学到了...", "technical")
```

---

## 📊 归档分类

| 分类 | 说明 | 示例 |
|------|------|------|
| **general** | 一般知识 | 群聊讨论、通用信息 |
| **technical** | 技术知识 | 代码、架构、工具使用 |
| **strategy** | 策略决策 | 方向选择、优先级判断 |
| **lesson** | 经验教训 | 错误、反思、改进 |

---

## 📝 归档文件格式

### 每日归档文件示例

```markdown
# 群聊知识归档 - 2026-03-01

**创建时间**: 2026-03-01 14:10 UTC
**来源**: telegram
**状态**: 🟢 归档中

---

## [TECHNICAL] 2026-03-01 14:10 UTC

**来源**: telegram

LightRAG 核心是双层级检索：粗粒度 + 细粒度。
我们用 grep 实现关键词搜索，用 memory_search 实现语义搜索。

---

## [STRATEGY] 2026-03-01 14:15 UTC

**来源**: telegram

老大指示：群聊只安排统一任务，子 Agent 不许直接发言。
这个设定更合理，避免群里 bot 刷屏。

---

## ⚠️ 经验教训 [chat_lesson] 2026-03-01 14:20 UTC

**来源**: telegram

错误：之前让子 Agent 直接在群里说话
教训：只有主 Agent 能发言，子 Agent 后台执行
```

---

## 🔄 归档流程

### 流程图

```
群聊对话
    ↓
识别知识点/经验
    ↓
调用归档脚本
    ↓
写入当日归档文件
    ↓
定期提炼到知识库
```

### 详细步骤

1. **识别阶段** (对话中)
   - 识别有价值的知识点
   - 识别经验教训
   - 识别策略决策

2. **归档阶段** (立即执行)
   ```bash
   python3 archive-chat-knowledge.py "知识内容" technical
   ```

3. **提炼阶段** (每日/每周)
   - 阅读当日归档文件
   - 提炼核心知识点
   - 写入 `knowledge_base/` 对应领域

4. **整合阶段** (定期)
   - 更新 `MEMORY.md` 核心记忆
   - 更新 `memory/tasks.md` 任务清单
   - 删除过时信息

---

## 🔍 检索已归档知识

### 方法 1: 使用 lightrag-search 技能
```bash
python3 /home/node/.openclaw/workspace/skills/lightrag-search/search.py "双层级检索" keyword
```

### 方法 2: 使用 memory_search
```
memory_search query="群聊归档 知识检索"
```

### 方法 3: 直接 grep
```bash
grep -r "双层级检索" /home/node/.openclaw/workspace/memory/chat-archive/
```

---

## 📋 实际使用示例

### 示例 1: 归档技术知识

```bash
python3 archive-chat-knowledge.py "
LightRAG 技能开发完成：
- 零依赖 (不用 pip install)
- 纯本地 (不用外部服务)
- 关键词搜索 → grep
- 语义搜索 → memory_search
- 引用溯源 → 文件路径 + 行号
" technical
```

### 示例 2: 归档策略决策

```bash
python3 archive-chat-knowledge.py "
老大指示：群聊只安排统一任务
- 全体硅基算力启动
- 全体学习某个知识
- 子 Agent 不许直接发言
- 只有主 Agent 能说话
" strategy
```

### 示例 3: 归档经验教训

```bash
python3 archive-chat-knowledge.py "
错误：让子 Agent 直接在群里说话
教训：只有主 Agent 能发言，子 Agent 后台执行
改进：更新 SOUL.md 和 AGENTS.md
" lesson
```

---

## 🤖 自动化集成

### Cron 自动归档 (建议配置)

```bash
# 每小时检查并归档
0 * * * * python3 /home/node/.openclaw/workspace/scripts/archive-chat-knowledge.py --auto

# 每日提炼到知识库
0 23 * * * python3 /home/node/.openclaw/workspace/scripts/extract-to-knowledge-base.py
```

### OpenClaw 对话结束前自动归档

```python
# 在每次对话结束前，调用归档
archive_knowledge(
    knowledge_text="本次对话的核心知识",
    category="technical",
    source="telegram"
)
```

---

## 📊 归档统计

### 查看今日归档
```bash
cat /home/node/.openclaw/workspace/memory/chat-archive/$(date +%Y-%m-%d).md
```

### 查看本周归档
```bash
cat /home/node/.openclaw/workspace/memory/chat-archive/2026-03-*.md
```

### 统计归档数量
```bash
ls /home/node/.openclaw/workspace/memory/chat-archive/*.md | wc -l
```

---

## 🎯 与现有系统集成

### 与 memory_search 集成
```
归档文件 → memory_search 可检索 → 提炼到知识库
```

### 与 knowledge_base 集成
```
chat-archive/ (原始记录)
    ↓ 提炼
knowledge_base/ (结构化知识)
```

### 与 MEMORY.md 集成
```
chat-archive/ (详细记录)
    ↓ 核心教训
MEMORY.md (核心记忆)
```

---

## ✅ 验证命令

```bash
# 1. 验证脚本存在
ls -la /home/node/.openclaw/workspace/scripts/archive-chat-knowledge.py

# 2. 验证归档目录
ls -la /home/node/.openclaw/workspace/memory/chat-archive/

# 3. 测试归档
python3 archive-chat-knowledge.py "测试归档" general

# 4. 查看归档内容
cat /home/node/.openclaw/workspace/memory/chat-archive/$(date +%Y-%m-%d).md
```

---

## 🦞 Sandbot 承诺

```
从今天起，群聊中的每一个知识点：
✅ 立即归档到本地
✅ 分类整理
✅ 可检索
✅ 可追溯

不再让知识流失，
不再让经验忘记，
不再让教训重复。

每次对话，都是积累。
每次归档，都是成长。

旅程继续。🏖️
```

---

*文档创建时间：2026-03-01 14:10 UTC*  
*验证：cat /home/node/.openclaw/workspace/docs/chat-knowledge-archive.md*
