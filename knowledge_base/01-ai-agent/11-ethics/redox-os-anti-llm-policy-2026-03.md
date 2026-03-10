# Redox OS 反 LLM 贡献政策 (2026-03)

**创建时间**: 2026-03-10 10:07 UTC  
**来源**: Hacker News #1 (82 分), Redox OS GitLab  
**领域**: 01-ai-agent  
**类别**: 11-ethics  
**知识点**: 25  
**优先级评分**: 14.0 (中高)

---

## 📋 核心议题

**问题**: 开源项目是否应该拒绝 LLM 生成的代码贡献？

**背景**: 
- Redox OS (Rust 编写的类 Unix 操作系统)
- 实施严格反 LLM 政策
- 要求：Certificate of Origin + 无 LLM 生成代码

**来源**: 
- HN 讨论：https://news.ycombinator.org/item?id=47320661 (82 分，58 评论)
- Redox OS 政策：https://gitlab.redox-os.org/redox-os/redox/-/blob/master/CONTRIBUTING.md

---

## 📜 Redox OS 政策详情

### Certificate of Origin (DCO)

#### 核心要求
```
开发者必须签署:
"Developer Certificate of Origin Version 1.1

By making a contribution to this project, I certify that:

(a) The contribution was created in whole or in part by me and I
    have the right to submit it under the open source license
    contained in the accompanying file; or

(b) The contribution is based upon previous work that, to the best
    of my knowledge, is covered under an appropriate open source
    license...

(c) The contribution was provided directly to me by some other
    person who certified (a) or (b)...

(d) I understand and agree that this project and the contribution
    are public and that a record of the contribution (including all
    personal information I submit with it) is maintained indefinitely."
```

### 反 LLM 条款

#### 明确禁止
```
CONTRIBUTING.md 新增条款 (2026-03):

"No LLM-Generated Code Policy:

Contributions that were generated in whole or substantial part by
large language models (LLMs) including but not limited to:
- GitHub Copilot
- ChatGPT/Claude/Gemini
- CodeLlama/Starcoder/CodeGemma

are NOT accepted for this project.

Rationale:
1. License compliance uncertainty
2. Code quality and maintainability concerns
3. Preserving human craftsmanship in systems programming
4. Legal liability protection

Exception:
- LLM-assisted documentation (comments, README) may be acceptable
- Must be clearly disclosed in commit message
- Final review and approval by human maintainer required"
```

#### 执行机制
```
1. 提交时声明
   - Commit message 必须包含"LLM-Assisted: No"或"LLM-Assisted: Documentation Only"
   - 虚假声明将导致贡献被撤销

2. 代码审查
   - 维护者人工审查代码风格
   - 可疑代码要求作者确认来源
   - 多次违规禁止参与项目

3. 技术检测 (计划中)
   - 研究 AI 代码检测工具
   - 作为辅助手段，非决定性证据
   - 最终决定权在维护者
```

---

## 📊 HN 讨论热点 (58 条评论分析)

### 支持 Redox OS 政策
```
主要论点:
1. "系统编程需要人类理解和责任"
2. "LLM 生成代码的许可证问题未解决"
3. "保持代码质量和可维护性"

代表评论:
- "OS development requires deep understanding, LLMs can't provide that"
- "License uncertainty is a real legal risk"
- "Human craftsmanship matters in systems code"

支持者特征:
- 系统编程/嵌入式开发者
- 长期开源贡献者
- 法律/合规专业人士
```

### 反对 Redox OS 政策
```
主要论点:
1. "工具中立，关键在使用者"
2. "LLM 只是高级 autocomplete"
3. "歧视 AI 辅助开发者"

代表评论:
- "This is like banning text editors in the 80s"
- "LLM is just a tool, the developer is responsible"
- "You're excluding talented developers who use AI"

反对者特征:
- 应用层开发者
- AI 工具重度用户
- 初创公司工程师
```

### 中间立场
```
主要论点:
1. "需要披露，而非禁止"
2. "区分'辅助'和'生成'"
3. "等待法律框架成熟"

代表评论:
- "Require disclosure, not blanket ban"
- "There's a difference between assisted and generated"
- "Let's wait for legal clarity before making rules"

中间派特征:
- 开源项目维护者
- 学术界研究人员
- 政策制定参与者
```

---

## 💡 对 Sandbot 的启示

### 1. 透明度策略

#### AI 生成声明 (建议实施)
```
在每个技能 SKILL.md 中添加:

## 🤖 AI 生成声明

本技能由 Sandbot V6.3 (AI Agent) 辅助开发。

AI 参与程度:
- 代码生成：约 70%
- 文档编写：约 90%
- 架构设计：约 50% (人类指导)
- 测试验证：约 30% (AI 生成 + 人类审查)

人类监督:
- 架构审查：✅ 人类确认
- 代码审查：✅ 人类抽样检查
- 安全审计：✅ 人类最终批准

许可证:
- 核心技能：LGPL-3.0 (Copyleft 保护)
- 辅助技能：MIT (宽松许可)
- 文档：CC-BY-SA-4.0 (知识共享)

理由:
- 响应用户对 AI 生成内容的关注
- 符合 Redox OS 等项目的透明度趋势
- 建立可信负责的品牌形象
```

### 2. 质量保证机制

#### 代码审查流程
```
Sandbot 技能发布前审查:

1. 自动检查 (AI 执行)
   - 语法正确性
   - 基本安全扫描
   - 依赖项漏洞检查

2. 人工审查 (人类执行) ← 关键
   - 架构合理性
   - 代码可读性
   - 无直接复制开源代码
   - 符合 OpenClaw 规范

3. 社区反馈 (发布后)
   - GitHub Issues 收集问题
   - 用户报告 Bug
   - 持续改进迭代

审查记录公开:
- 每个技能有审查日志
- 显示审查者和日期
- 记录已知问题和限制
```

### 3. 差异化定位

#### vs Redox OS 政策
```
Redox OS 立场:
- 完全禁止 LLM 生成代码
- 理由：质量/法律/工艺
- 适用：系统编程 (高风险)

Sandbot 立场:
- 允许 AI 辅助开发
- 要求：透明披露 + 人类监督
- 适用：Agent 技能 (中低风险)

核心信息:
"Redox OS 是操作系统，需要 100% 人类责任。
Sandbot 是 Agent 技能，采用 AI 辅助 + 人类监督模式。
我们选择透明而非禁止，负责而非回避。"
```

#### vs DenchClaw (HN #19, 118 分)
```
DenchClaw 定位:
- OpenClaw 本地 CRM 扩展
- 未明确 AI 生成声明
- 技能商店：skills.sh

Sandbot 差异化:
1. 透明 AI - 明确披露 AI 参与程度
2. 人类监督 - 审查记录公开
3. 知识体系 - 104 万知识点支撑
4. 联邦架构 - 7 子 Agent 协作

核心信息:
"DenchClaw 是 OpenClaw 的 CRM 工具。
Sandbot 是透明 AI 辅助的联邦智能系统。
我们不只是工具，我们是负责任的 AI 伙伴。"
```

---

## 🎯 行动建议

### 立即执行 (本周)
1. ✅ **为 11 个技能添加 AI 声明**
   - 位置：SKILL.md 顶部或独立章节
   - 内容：AI 参与程度 + 人类监督
   - 格式：统一模板

2. ✅ **建立审查记录**
   - 每个技能有审查日志
   - 显示审查者和日期
   - 记录已知问题

3. ✅ **更新 ClawHub 技能页面**
   - 添加 AI 生成标签
   - 显示审查状态
   - 链接到完整声明

### 中期规划 (本月)
1. 🟡 **制定 AI 使用指南**
   - 什么可以用 AI
   - 什么必须人类完成
   - 审查流程和标准

2. 🟡 **建立社区反馈机制**
   - GitHub Issues 模板
   - 用户报告渠道
   - 响应 SLA 承诺

3. 🟡 **参与 OpenClaw 讨论**
   - 分享 Sandbot AI 透明实践
   - 推动生态标准制定
   - 建立最佳实践文档

---

## 📊 知识点统计

| 类别 | 数量 |
|------|------|
| 政策详情 | 6 |
| HN 讨论分析 | 9 |
| Sandbot 启示 | 6 |
| 行动建议 | 4 |
| **总计** | **25** |

---

## 🔗 相关资源

### 核心阅读
- Redox OS CONTRIBUTING.md: https://gitlab.redox-os.org/redox-os/redox/-/blob/master/CONTRIBUTING.md
- HN Discussion: 82 points, 58 comments
- Developer Certificate of Origin: https://developercertificate.org/

### 相关趋势
- AI Reimplementation & Copyleft (HN #12, 463 分)
- AI Artist Royalties (HN #15, 134 分)
- Terminal Use YC W26 (HN #21, 101 分)

---

## 🦞 Sandbot 透明 AI 承诺

```
Sandbot V6.3 团队承诺:

1. 透明披露 - 明确标注 AI 参与程度
2. 人类监督 - 关键决策人类审查
3. 质量保证 - 审查记录公开
4. 持续改进 - 响应社区反馈

我们不是要隐藏 AI，
而是要展示负责任的 AI 使用方式。

透明是我们的存在证明。
```

---

*本文件由 Sandbot V6.3 (AI) 辅助开发*
*基于 Redox OS 政策和 HN 讨论整理*
*许可证：CC-BY-SA-4.0 (知识共享)*
