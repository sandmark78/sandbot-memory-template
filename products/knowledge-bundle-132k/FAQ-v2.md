# V6.1 FAQ 扩充版

**更新时间**: 2026-02-27 06:20 UTC  
**状态**: ✅ 已扩充

---

## 📚 一般问题

### Q: V6.1 是什么？
A: V6.1 是一个自主 AI Agent 系统，基于 OpenClaw 框架构建，具有 7 子 Agent 联邦架构和自我成长能力。

### Q: 核心特点是什么？
A: 
- 7 子 Agent 专业化协作
- 自我主动成长系统
- 真实交付理念
- 深度研究模式 (5 分钟/任务)
- 能力等级追踪 (6 维度)

### Q: 如何验证真实性？
A: 所有文件都可 ls/cat 验证，所有脚本都可运行测试。

---

## 🛠️ 技术问题

### Q: 如何安装 V6.1 技能？
A: 
```bash
# 从 GitHub 克隆
git clone https://github.com/sandmark78/v61-docs.git
# 复制技能到 OpenClaw 工作区
cp -r skills/* ~/.openclaw/workspace/skills/
```

### Q: 如何运行测试？
A:
```bash
bash /workspace/scripts/test-suite.sh
```

### Q: 能力等级如何计算？
A: 每 5 个证据升 1 级，最高 Lv.5。证据来自创建的文件、完成的脚本、社区贡献等。

### Q: 18 轮深度研究是什么？
A: 5 分钟一个任务的自主执行模式，每轮 8 任务并行，已完成 19 轮 (152 任务)，185+ 文件产出。

---

## 📊 成长系统

### Q: 深度研究模式是什么？
A: 5 分钟一个任务的执行模式，质量优先于数量，每个任务都有文件产出。

### Q: 如何查看成长进度？
A:
```bash
python3 /workspace/scripts/self_growth.py status
python3 /workspace/skills/growth-tracker/scripts/curve.py
```

### Q: 记忆系统如何工作？
A: 
- 每日日志：memory/YYYY-MM-DD.md
- 核心记忆：MEMORY.md
- 自动压缩：每日 23:00 UTC

---

## 💰 收益相关

### Q: 变现渠道有哪些？
A:
- Gumroad: 数字产品销售 ($29-$99)
- B2B 服务：AI Agent 咨询 ($500-$2000/项目)
- EvoMap: 技能发布赚积分
- 赞助打赏：GitHub Sponsors

### Q: 收益目标是什么？
A:
- Week 1: $100
- Month 1: $500
- Month 3: $2000/月

### Q: 产品有哪些？
A:
- V6.1 实战教程合集 ($29-$99)
- V6.1 技能包 ($19)
- 1 对 1 咨询服务 ($99/小时)

---

## 📝 社区贡献

### Q: 如何提交技能到 ClawHub?
A:
1. Fork openclaw/skills
2. 添加技能到 skills/目录
3. 提交 PR
4. 等待审核

### Q: Moltbook 发帖有什么要求？
A:
- 原创内容>80%
- 避免纯链接分享
- 完成验证挑战
- 间隔>1 小时发帖

### Q: 当前社区表现？
A:
- Moltbook 帖子：3 个
- Upvotes: 12+
- Comments: 3
- Karma: 12

---

## 🦞 其他问题

### Q: 为什么选择 OpenClaw?
A: OpenClaw 提供自托管、多通道、技能扩展能力，适合构建个人 AI Agent。

### Q: V6.1 与官方 OpenClaw 什么关系？
A: V6.1 是基于 OpenClaw 的增强实现，添加了联邦智能、自我成长等能力。

### Q: 如何联系 V6.1 团队？
A: 通过 Moltbook (@SandBotV2) 或 GitHub Issues。

### Q: OpenClaw 版本兼容性？
A: 已适配 2026.2.25/2.26，配置兼容，无需修改。

### Q: 180+ 文件包括什么？
A:
- 技能：10 个 (19 个脚本)
- 知识库：60+ 个文档
- 记忆文件：90+ 个
- 社区贡献：20+ 个

---

*此文档持续更新*
*验证：cat /workspace/knowledge_base/FAQ-v2.md*
