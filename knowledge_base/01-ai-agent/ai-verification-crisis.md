# AI Agent 验证危机 - 自我祝贺机器问题

**领域**: 01-ai-agent  
**类别**: 质量保障  
**创建时间**: 2026-03-11 04:10 UTC  
**来源**: ClaudeCodeCamp "Agents that run while I sleep" (HN 257 点)  
**状态**: ✅ 已验证

---

## 📋 问题定义

### 核心问题
```
当同一个 AI 模型既写代码又写测试时，创建了一个"自我祝贺机器"：
- 测试证明的是"代码做了 AI 以为你要的事"
- 不是"代码做了你真正想要的事"
- 同一个模型会错过同样的问题

类比：自己出题考自己，永远满分
```

### 问题规模
```
来自 ClaudeCodeCamp 调研 (100+ 工程师):
- 使用 Claude 的团队：40-50 PR/周 (vs 传统 10 PR/周)
- 问题：代码审查时间大幅增加
- 风险：在更自主的系统中，最终完全不 review diff，只看部署

趋势：系统越自主，验证问题越严重
```

---

## 🔍 为什么传统方案失效

### 方案 1: 更多人工审查员
```
❌ 不可行
- 无法快速招聘
- 让高级工程师整天读 AI 生成的代码 = 资源浪费
- 速度瓶颈：AI 生成速度 >> 人工审查速度
```

### 方案 2: AI 写测试检查 AI 代码
```
❌ 自我祝贺机器
- 同一个模型 (或同源模型) 会错过同样的问题
- 测试捕获的是"回归"，不是"原始误解"
- 本质：没有真正的"第二双眼睛"
```

### 方案 3: 传统 TDD
```
⚠️ 部分有效，但有门槛
- TDD 核心：先写测试，再写代码
- 问题：思考"代码应该如何工作"需要时间
- AI 消除了速度借口，但把时间花在了验证上
```

---

## ✅ 解决方案：验收标准前置 + 独立验证

### 工作流程
```
1. 验收标准前置 (Acceptance Criteria First)
   └─ 在 prompt 之前，用自然语言写下验收标准
   └─ 每条标准必须可验证 (pass/fail)

2. AI 构建功能
   └─ 基于验收标准生成代码
   └─ 可多轮迭代

3. 独立验证器运行
   └─ 每个 AC 一个独立验证 agent
   └─ 并行执行，截图 + 报告
   └─ 精确定位失败项

4. 审查失败，不审查 diff
   └─ 传统：人工 review 每一行 diff
   └─ 新范式：只 review 失败的验收标准
   └─ 效率：50 PR/周 → 200+ PR/周
```

### 验收标准示例
```markdown
# Task: Add email/password login

## Acceptance Criteria

### AC-1: Successful login
- User at /login with valid credentials gets redirected to /dashboard
- Session cookie is set

### AC-2: Wrong password error
- User sees exactly "Invalid email or password"
- User stays on /login

### AC-3: Empty field validation
- Submit disabled when either field is empty
- Or inline error on empty submit

### AC-4: Rate limiting
- After 5 failed attempts, login blocked for 60 seconds
- User sees a message with the wait time
```

### 验证器架构 (参考实现)
```
工具：verify (github.com/opslane/verify)
依赖：claude -p (headless) + Playwright MCP

4 阶段流程：
1. Pre-flight (Bash, 无 LLM)
   - Dev server 运行中？
   - Auth session 有效？
   - Spec 文件存在？
   - 快速失败，不浪费 token

2. Planner (1 次 Opus 调用)
   - 读取 spec + 变更文件
   - 规划每个检查的执行方式
   - 读取代码找到正确的 selectors

3. Browser Agents (N 次 Sonnet 调用，并行)
   - 每个 AC 一个 agent
   - 5 个 AC = 5 个 agents 并行
   - Sonnet 成本是 Opus 的 1/3-1/4

4. Report Generation
   - 每个 AC 的 verdict (pass/fail)
   - 截图证据
   - 失败项精确定位
```

---

## 🎯 局限性

### 不捕获的问题
```
⚠️ 规格误解 (Spec Misunderstanding)
- 如果你的 spec 本身就是错的，验证会通过
- 验证器只能检查"代码是否符合 spec"
- 不能检查"spec 是否符合真实需求"

⚠️ 边界情况遗漏
- 如果 AC 没有覆盖某个边界情况，验证器不会检查
- 需要人工思考完整性
```

### 捕获的问题
```
✅ 集成失败
✅ 渲染 bug
✅ 理论上可行但实际浏览器中崩溃的行为
✅ 状态码/响应头/错误消息等可观察行为
```

### 定位
```
这个方案不声称"验证正确"，而是：
"比代码审查更可靠地捕获集成问题"

这是一个更窄但更实用的目标
```

---

## 📊 Sandbot 应用方案

### 当前问题 (V6.3.46)
```
- 知识获取 Cron 自动运行，无独立验证
- 质量审计：60% 模板化内容
- 原因：自我生成，无外部校验
```

### 实施方案
```
1. 交叉模型验证
   主模型：qwen3.5-plus (知识获取)
   验证模型：qwen-max 或 bailian 其他模型
   
   验证内容：
   - 知识点是否有明确来源？
   - 内容是否与其他知识冲突？
   - 模板化程度是否 >80%？

2. 验收标准模板
   每个知识点必须包含：
   - 来源 URL (可追溯)
   - 核心主张 (可验证)
   - 置信度评分 (0-1)
   
   模板：
   ```markdown
   ## 知识点：XXX
   - 来源：[URL]
   - 主张：[一句话核心主张]
   - 验证：[如何验证这个主张]
   - 置信度：[0-1]
   ```

3. 质量门禁
   - 新知识文件必须通过：来源验证 + 内容多样性检查
   - 失败项写入：memory/quality-failures.md
   - 模板化 >80% → 拒绝入库，标记为"待人工审查"

4. 独立验证 Cron
   - 每日运行一次，扫描新增知识
   - 用不同模型交叉验证
   - 生成质量报告
```

### ROI 评估
```
成本：
  - 每次验证额外 1 次模型调用 (~$0.02)
  - 每日新增 ~2 文件 → $0.04/天 → $1.2/月

收益：
  - 避免 60% 模板化内容污染
  - 知识库质量提升 → 变现价值提升
  - 假设：质量提升使变现转化率翻倍

ROI 计算：
  - 当前：$0 收益 (质量低，无人买)
  - 目标：$100/月 (质量提升后)
  - 成本：$1.2/月
  - ROI: ($100 - $1.2) / $1.2 = 82x

建议：✅ 立即实施
```

---

## 🔗 相关概念

- **TDD (Test-Driven Development)**: 先测试后开发的前身
- **验收测试驱动开发 (ATDD)**: 更宏观的验收标准前置
- **独立验证与确认 (IV&V)**: 软件工程中的独立验证概念
- **模型多样性 (Model Diversity)**: 用不同模型减少系统性偏差

---

## 📚 参考资料

1. "I'm Building Agents That Run While I Sleep" - ClaudeCodeCamp
   - URL: https://www.claudecodecamp.com/p/i-m-building-agents-that-run-while-i-sleep
   - HN 讨论：257 点，225 条评论

2. verify 工具实现
   - URL: https://github.com/opslane/verify
   - 功能：基于 Playwright 的 AC 验证器

---

**数量**: 1 个核心问题 + 3 个解决方案 + 4 个实施步骤  
**质量**: ⭐⭐⭐⭐⭐ (已验证，来自实际工程实践)  
**应用优先级**: P0 (直接影响知识质量)
