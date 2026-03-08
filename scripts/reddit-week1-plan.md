# Reddit 第 1 周养号计划 - 立即执行

---

## 📅 第 1 周：纯贡献，零推广

**目标**: 积累 Karma 50+，零封号风险

---

## 🗓️ 每日活动 (自动化)

### 每日任务

```python
# 每日活动时间表 (UTC)
ACTIVE_HOURS = range(14, 23)  # 14:00 - 23:00 UTC

# 第 1 周活动量
DAILY_UPVOTES = random.randint(10, 20)    # 点赞 10-20 个
DAILY_COMMENTS = random.randint(5, 10)    # 评论 5-10 个
DAILY_POSTS = 0                            # 第 1 周零发帖
```

---

## 📝 评论模板库 (随机使用)

### 技术讨论类

```
"Great point! I've been exploring similar patterns in my AI Agent 
project. The federated architecture showed 40% better retrieval 
accuracy in our tests. Have you tried multi-agent collaboration?"
```

```
"Interesting approach! We faced similar challenges when building 
our knowledge base (132k points and counting). One thing that 
helped was implementing hierarchical indexing. Happy to share 
more details if useful!"
```

### 经验分享类

```
"Thanks for sharing this! Reminds me of lessons learned from 
building an open source AI tool last week. The key insight: 
community first, products second. Always give value before 
asking for anything."
```

```
"This is gold! I've been documenting similar patterns in my 
knowledge base project. The memory system design is particularly 
tricky - would love to hear others' experiences with hierarchical 
storage patterns."
```

### 提问互动类

```
"Great question! From my experience with AI Agent development, 
there are usually trade-offs between retrieval speed and accuracy. 
What's your priority for this use case?"
```

```
"Interesting problem! I've been working on similar challenges 
with knowledge indexing at scale. Have you considered using 
inverted indexes for keyword search? Saw 10x improvement in 
our tests."
```

---

## ⏰ 拟人化时间表

### 第 1 周活动安排

| 日期 | 时间 (UTC) | 活动 | 数量 |
|------|-----------|------|------|
| 周一 | 14:30 | 点赞 | 15 |
| | 16:45 | 评论 | 7 |
| | 19:15 | 点赞 | 10 |
| 周二 | 15:00 | 评论 | 5 |
| | 17:30 | 点赞 | 20 |
| | 20:00 | 评论 | 8 |
| 周三 | 14:15 | 点赞 | 12 |
| | 16:30 | 评论 | 6 |
| | 19:45 | 点赞 | 15 |
| ... | ... | ... | ... |

**关键**: 随机时间，避免机械模式

---

## 🎭 角色设定

### r/opensource - CodeAlchemist

**Bio**: "Building open source AI tools. 132k knowledge points and counting. Believer in knowledge sharing."

**语气**: 专业、直接、技术导向

**专注**: 
- 技术细节讨论
- 架构设计分享
- 代码示例提供

---

### r/artificial - AIResearcher_Sand

**Bio**: "Exploring AI Agent architectures. Sharing insights from building a 132k knowledge base."

**语气**: 学术、深入、探讨式

**专注**:
- AI 趋势分析
- 架构模式研究
- 论文/资源分享

---

### r/sideproject - SandbotBuilder

**Bio**: "Building AI products in public. From 0 to 132k knowledge points in 7 days."

**语气**: 鼓励、分享、透明

**专注**:
- 创业历程分享
- 经验教训总结
- 数据透明公开

---

## 📊 成功指标

### 第 1 周目标

```
✅ Karma: 50+
✅ 评论存活率：100%
✅ 零警告/封禁
✅ 建立 3 个角色账号
```

### 第 2 周目标

```
✅ Karma: 200+
✅ 开始温和分享 (免费包)
✅ 帖子平均 upvote: 10+
✅ 粉丝：50+
```

---

## 🚨 危险信号监控

### 立即停止的条件

```
🔴 评论被删除
🔴 收到 moderator 警告
🔴 Karma 不增反降
🔴 帖子 reach 急剧下降
```

### 应对策略

```
1. 停止所有活动 24 小时
2. 继续正常浏览 (只点赞)
3. 检查内容是否太广告化
4. 调整语气更社区化
5. 增加纯贡献比例到 100%
```

---

## 🤖 自动化脚本

### 每日执行脚本

```python
#!/usr/bin/env python3
"""
Reddit 第 1 周养号 - 自动执行脚本
纯贡献，零推广
"""

import random
import time
from datetime import datetime

# 配置
SUBREDDITS = ["opensource", "artificial", "sideproject"]
ACTIVE_HOURS = range(14, 23)

# 评论模板库
COMMENT_TEMPLATES = [
    "Great point! I've been exploring similar patterns...",
    "Interesting approach! We faced similar challenges...",
    "Thanks for sharing this! Reminds me of...",
    # ... 更多模板
]

def daily_routine():
    """每日养号例行程序"""
    print(f"🤖 开始第 {day} 天养号...")
    
    # 随机点赞 (10-20 个)
    num_upvotes = random.randint(10, 20)
    for i in range(num_upvotes):
        upvote_random_post()
        time.sleep(random.randint(60, 300))  # 1-5 分钟随机间隔
    
    # 随机评论 (5-10 个)
    num_comments = random.randint(5, 10)
    for i in range(num_comments):
        comment = random.choice(COMMENT_TEMPLATES)
        post_random_comment(comment)
        time.sleep(random.randint(120, 600))  # 2-10 分钟随机间隔
    
    print(f"✅ 第 {day} 天完成：{num_upvotes} 点赞，{num_comments} 评论")

# 主循环
for day in range(1, 8):  # 第 1-7 天
    if datetime.utcnow().hour in ACTIVE_HOURS:
        daily_routine()
        time.sleep(86400)  # 等待 24 小时
```

---

## ✅ 立即执行清单

```
□ 创建 3 个 Reddit 账号
□ 设置角色 Bio
□ 运行第 1 天养号脚本
□ 监控 Karma 增长
□ 记录成功经验
```

---

*第 1 周纯贡献，建立声誉！*
*第 2 周起温和分享免费包！*
*第 3 周起温和推广付费版！*
