# Agent 验证工程 - 独立验证器模式

**领域**: 04-skill-dev  
**类别**: 验证与质量保证  
**创建时间**: 2026-03-11 10:05 UTC  
**来源**: Claude Code Camp - "Agents that run while I sleep"  
**相关**: [[Agent 工程化层级]], [[验收标准先行]]

---

## 🚨 核心问题

### AI 自我验证危机
```
"When Claude writes tests for code Claude just wrote, 
it's checking its own work. The tests prove the code does 
what Claude thought you wanted. Not what you actually wanted."

"When you use the same AI for both, you've built a 
self-congratulation machine."
```

### 传统代码审查失效
```
"This is exactly the problem code review was supposed to solve: 
a second set of eyes that wasn't the original author. 
But one AI writing and another AI checking isn't a fresh set of eyes. 
They come from the same place. They'll miss the same things."
```

### 规模困境
```
"Teams using Claude for everyday PRs are merging 40-50 a week 
instead of 10. Teams are spending a lot more time in code reviews."

"You could hire more reviewers. But you can't hire fast enough. 
And making senior engineers read AI-generated code all day isn't worth it."
```

---

## ✅ 解决方案：独立验证器架构

### 核心原则
```
验收标准先行 (Acceptance Criteria First):
- 人类写验收标准 → Agent 实现 → 验证 Agent 检查 → 人类只看失败项

关键洞察:
- TDD 的真正价值：在写代码前定义"正确"的样子
- AI 消除了 TDD 的速度障碍，但引入了验证危机
- 解决方案：独立验证器 (不同 Agent/不同方法)
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
- Submit disabled when either field empty, or inline error on empty submit

### AC-4: Rate limiting
- After 5 failed attempts, login blocked for 60 seconds
- User sees a message with the wait time
```

**验收标准质量要求**:
- ✅ 具体可验证 (要么通过要么失败)
- ✅ Observable 行为 (可被外部检测)
- ✅ 不含实现细节 (关注"做什么"而非"怎么做")
- ✅ 人类可读 (便于审查)

---

## 🏗️ 验证器架构

### 四阶段流程
```
┌─────────────────────────────────────────────────────────┐
│ Stage 1: Pre-flight (Bash, 零 LLM 调用)                  │
├─────────────────────────────────────────────────────────┤
│ - 开发服务器运行中？                                     │
│ - 认证会话有效？                                        │
│ - Spec 文件存在？                                       │
│ - Fail fast，避免浪费 token                              │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Stage 2: Planner (1x Opus 调用)                          │
├─────────────────────────────────────────────────────────┤
│ - 读取 spec 和变更文件                                   │
│ - 规划每个检查的执行方案                                │
│ - 读取代码找到正确的 selectors                          │
│ - 输出：检查计划 + 执行策略                             │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Stage 3: Browser Agents (Nx Sonnet 调用，并行)           │
├─────────────────────────────────────────────────────────┤
│ - 每个 AC 一个 Agent，独立执行                           │
│ - 5 个 AC = 5 个 Agent 并行                               │
│ - 导航 + 截图 + 验证                                     │
│ - Sonnet 成本是 Opus 的 1/3-1/4                           │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Stage 4: Report (自动生成)                               │
├─────────────────────────────────────────────────────────┤
│ - 每项 AC 的通过/失败 verdict                            │
│ - 失败项带截图和详细日志                                │
│ - 人类只审查失败项                                      │
└─────────────────────────────────────────────────────────┘
```

### 成本优化
```
传统工作流:
- 人类审查 40-50 PRs/周 × 30 分钟 = 20-25 小时/周

验证器工作流:
- Pre-flight: $0 (Bash)
- Planner: ~$0.50 (1x Opus)
- Verification: ~$0.30 (5x Sonnet 并行)
- 人类审查：~2 小时/周 (只看失败项)

成本降低：90%+
时间降低：85%+
```

---

## 🔧 实现方案

### 开源项目：verify
```
GitHub: github.com/opslane/verify
技术栈:
  - claude -p (Claude Code headless mode)
  - Playwright MCP (浏览器自动化)
  - 无自定义后端，无额外 API key
```

### 后端验证 (无浏览器)
```bash
# API 行为验证示例
# AC: POST /login with wrong credentials returns 401

curl -X POST https://api.example.com/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"wrong"}'

# 预期:
# - Status: 401 Unauthorized
# - Body: {"error": "Invalid email or password"}
# - Headers: No session cookie set
```

### 前端验证 (Playwright)
```javascript
// AC-1: Successful login
test('AC-1: Successful login redirects to dashboard', async ({ page }) => {
  await page.goto('/login');
  await page.fill('[name=email]', 'valid@example.com');
  await page.fill('[name=password]', 'correctpassword');
  await page.click('button[type=submit]');
  
  // 验证重定向
  await expect(page).toHaveURL('/dashboard');
  
  // 验证 session cookie
  const cookies = await page.context().cookies();
  expect(cookies.some(c => c.name === 'session')).toBe(true);
  
  // 截图
  await page.screenshot({ path: 'ac1-pass.png' });
});
```

---

## 📊 验证器局限性

### 能捕获的
- ✅ 集成失败 (代码在本地工作，集成后崩溃)
- ✅ 渲染 bug (CSS 问题、布局错误)
- ✅ 行为偏差 (理论正确，实际浏览器中失败)
- ✅ 回归错误 (破坏已有功能)

### 不能捕获的
- ❌ Spec 错误 (验收标准本身就错了)
- ❌ 需求误解 (人类写错了 AC)
- ❌ 业务逻辑错误 (符合 AC 但不符合业务需求)

**关键认知**:
```
"This doesn't catch spec misunderstandings. If your spec was 
wrong to begin with, the checks will pass even when the feature is wrong."

"What Playwright does catch is integration failures, rendering bugs, 
and behavior that works in theory but breaks in a real browser. 
That's a narrower claim than 'verified correct,' but it's more than 
a code review was reliably catching anyway."
```

---

## 🎯 Sandbot 应用

### P0 质量优化项目
```
当前问题:
- 知识质量审计发现 60% 模板化
- 缺乏自动验证机制
- 人工审查成本过高

解决方案:
1. 设计知识验证器 (类似 verify 项目)
2. 验收标准：每个知识点必须包含
   - 定义清晰
   - 参数完整
   - 示例可运行
   - 引用可验证
3. 验证流程:
   - Pre-flight: 文件结构检查
   - Planner: 读取知识点，规划验证
   - Verifier: 检查定义/参数/示例/引用
   - Report: 生成质量报告
```

### 集成到 Cron 知识获取
```
当前流程:
1. HN 趋势扫描 → 2. 深度文章分析 → 3. 写入记忆文件

优化后流程:
1. HN 趋势扫描 → 2. 深度文章分析 → 3. 写入知识库
4. 验证器检查 → 5. 质量报告 → 6. 人类审查失败项
```

---

## 📚 相关知识点

- [[Agent 工程化层级]] - Level 5: Verification Engineering
- [[验收标准先行]] - TDD 的 AI 时代演进
- [[Compounding Engineering]] - 每次会话改进下次
- [[Context Engineering]] - 信息密度优化

---

## 🔗 参考资料

- [Agents that run while I sleep](https://www.claudecodecamp.com/p/i-m-building-agents-that-run-while-i-sleep)
- [verify GitHub](https://github.com/opslane/verify)
- [Playwright MCP](https://github.com/microsoft/playwright-mcp)

---

**数量**: 850  
**质量评分**: A (来源可靠，结构完整，可操作)  
**最后更新**: 2026-03-11 10:05 UTC
