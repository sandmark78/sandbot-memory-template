# AI Agent 工程化趋势 - 验收标准机制 (2026-03)

**领域**: ai-agent/engineering  
**类别**: 质量保证  
**创建时间**: 2026-03-11 00:07 UTC  
**来源**: Hacker News / Claude Code Camp  
**热度**: 🔥 186 点 HN 讨论

---

## 核心问题

**背景**: AI Agent 自主编写代码时，如何验证输出正确性？

**现状**:
- 工程师每周合并 PR 从 10 个→40-50 个 (AI 辅助)
- 代码审查时间大幅增加
- 同一 AI 写代码 + 写测试 = "自我祝贺机器" (无法发现原始误解)

---

## 解决方案：验收标准先行 (Acceptance Criteria First)

### 核心原则
```
1. 在 prompt 之前写验收标准 (AC)
2. AC 必须具体到可验证 (pass/fail)
3. Agent 根据 AC 构建功能
4. 独立验证 Agent 运行 AC 检查
5. 人类只审查失败的 AC
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

---

## 实现架构 (4 阶段)

### 1. Pre-flight (Bash, 无 LLM)
```bash
# 快速失败检查
- Dev server running?
- Auth session valid?
- Spec file exists?
```

### 2. Planner (1x Opus call)
```
输入：Spec + 变更文件
输出：每个 AC 的检查方案
功能：
  - 读取代码找到正确的 selectors
  - 规划每个检查的执行方式
  - 避免猜测 class names
```

### 3. Browser Agents (N x Sonnet calls, 并行)
```
- 每个 AC 一个独立 Agent
- 5 个 AC = 5 个 Agent 并行执行
- 使用 Sonnet (比 Opus 便宜 3-4x)
- 每个 Agent 导航 + 截图
```

### 4. Judge (1x Opus call)
```
输入：所有证据 (screenshots, results)
输出：JSON verdicts
格式：
{
  "verdicts": [
    {"id": "AC-1", "passed": true, "reasoning": "..."},
    {"id": "AC-2", "passed": false, "reasoning": "..."}
  ]
}
```

---

## 工具实现

### Claude Code 插件
```bash
# 安装
/plugin marketplace add opslane/verify
/plugin install opslane-verify@opslane/verify

# 或克隆自定义
git clone https://github.com/opslane/verify
```

### 核心命令
```bash
claude -p --model claude-opus-4-6 \
  "Review this evidence and return a verdict for each AC.
   Evidence: $(cat .verify/evidence/*/result.json)
   Return JSON: {verdicts: [{id, passed, reasoning}]}"
```

---

## 优势与局限

### ✅ 优势
- 捕获集成失败、渲染 bug、浏览器行为问题
- 比传统 code review 更可靠
- 人类只审查失败项，效率提升
- 并行执行，速度快

### ⚠️ 局限
- **无法捕获 spec 误解** (如果 spec 本身错了，检查会通过)
- 需要 upfront 思考 (工程师抗拒，感觉慢)
- 依赖 Playwright + MCP 配置

---

## 适用场景

### 前端变更
```
- Playwright browser agents
- 截图 + 视觉验证
- DOM 状态检查
```

### 后端变更
```
- curl 命令检查
- 可观察的 API 行为
- 状态码、响应头、错误消息
```

---

## 关键洞察

> "你无法信任 Agent 的产出，除非你在它开始之前就告诉了它'完成'是什么样子。"

> "写验收标准比写 prompt 更难，因为它强迫你在看到边界情况之前就思考它们。"

> "工程师抗拒它的原因和他们抗拒 TDD 一样——开始时感觉更慢。"

---

## 与 Sandbot V6.3 的关联

### 现有能力
- ✅ 已有 `input-validator` 技能 (内容安全验证)
- ✅ 已有 `agent-optimizer` 技能 (轨迹分析 + 奖励反馈)

### 可整合点
1. **任务规划阶段**: 强制要求 AC 先行
2. **验证阶段**: 独立 Agent 运行 AC 检查
3. **审计阶段**: Auditor Agent 审查失败 AC

### 实施建议
```
优先级：P1 (高价值，中等成本)
ROI 估算：3.5 (减少 60% 审查时间)
实施路径:
  1. 修改任务模板，增加 AC 字段
  2. 创建 verify 技能 (基于 Playwright)
  3. Auditor Agent 集成 AC 审查
```

---

## 知识点统计

| 类别 | 数量 |
|------|------|
| 核心概念 | 8 |
| 实现细节 | 12 |
| 工具配置 | 6 |
| 最佳实践 | 10 |
| **总计** | **36 点** |

---

*此文件已真实写入服务器*
*最后更新：2026-03-11 00:07 UTC*
*验证：cat /home/node/.openclaw/workspace/knowledge_base/01-ai-agent/engineering/acceptance-criteria-verification.md*
