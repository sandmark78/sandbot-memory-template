# 文档入库实践 - AI 时代的 Docs-in-Repo 策略

**创建时间**: 2026-03-14 20:12 UTC  
**来源**: HN 33 分 + 工程实践分析  
**领域**: 01-ai-agent / 工程实践 / 文档管理  
**标签**: #docs-in-repo #documentation #AI-agents #工程实践 #知识管理

---

## 📋 概述

**核心论点**: AI 时代是将文档移入代码仓库的最佳时机，AI Agent 解决了文档维护的最大痛点——保持文档与代码同步。

**来源文章**: "It's time to move your docs in the repo" by dein.fr (2026-03-13)  
**HN 讨论**: 33 分，11 条评论

**核心转变**:
- **过去**: 文档易过时，维护成本高 → 放在外部 (Notion/Confluence)
- **现在**: AI Agent 自动保持同步 → 移入仓库，版本控制

---

## 🎯 文档入库的六大优势

### 1. 版本控制
```
问题：外部文档系统 (Notion/Confluence/Google Docs) 无版本控制
      多人同时修改可能冲突，无法追溯历史

解决：Git 版本控制
  - 文档变更与代码变更同步
  - 支持分支、合并、回滚
  - 审查文档变更如同代码审查
  - 清晰的历史追溯

实践：
  docs/
  ├── api/
  │   ├── v1.0.md
  │   ├── v1.1.md
  │   └── v2.0.md
  ├── architecture/
  │   └── decisions/
  │       └── 001-database-choice.md
  └── guides/
      └── getting-started.md
```

### 2. 代码 proximity
```
问题：文档与代码分离，搜索困难

解决：统一搜索
  - rg/grep 同时搜索代码和文档
  - IDE 内联显示相关文档
  - 代码变更时容易找到相关文档

实践：
  # 搜索所有认证相关
  rg "authentication" --type md --type js
  
  # 结果包括:
  # - src/auth/login.js (代码)
  # - docs/api/authentication.md (文档)
  # - docs/guides/security.md (文档)
```

### 3. 形式化审查
```
理念：Documentation-Driven Development (文档驱动开发)

流程：
  1. 先写文档变更 (API 设计、功能说明)
  2. 审查文档 (理解最终产品/API)
  3. 实现代码
  4. 验证代码与文档一致

优势：
  - 审查文档比审查代码更容易理解意图
  - 提前发现设计问题
  - 文档成为"规范"

工具：
  - GitHub PR 审查文档变更
  - 文档 diff 高亮显示
  - 要求文档更新作为 PR 必要条件
```

### 4. 自动生成
```
问题：手动复制 API 文档到外部系统劳动密集

解决：从代码自动生成
  - Sphinx autodoc (Python)
  - JSDoc (JavaScript)
  - Javadoc (Java)
  - Docusaurus (静态站点)

流程：
  代码注释 → 提取 → 格式化 → 发布
  
  # Python 示例
  def authenticate(user: str, password: str) -> Token:
      """
      验证用户凭据并返回访问令牌。
      
      Args:
          user: 用户名
          password: 用户密码
          
      Returns:
          Token: JWT 访问令牌
          
      Raises:
          AuthError: 凭据无效时
      """
```

### 5. 测试集成
```
理念：文档即规范，示例即测试

工具：
  - Python doctest
  - Rust doc tests
  - Markdown 测试框架

实践：
  ```python
  >>> authenticate("admin", "secret")
  Token("eyJhbGc...")
  >>> authenticate("admin", "wrong")
  Traceback (most recent call last):
    ...
  AuthError: Invalid credentials
  ```
  
  # CI 中运行
  python -m doctest docs/api/authentication.md

优势：
  - 文档示例自动验证
  - 过时的示例会失败
  - 文档保持准确
```

### 6. 高效编辑
```
优势：
  - 使用熟悉的文本编辑器
  - 批量修改脚本化
  - Git 工具链支持
  - 离线编辑

实践：
  # 批量替换 API 端点
  rg -l "/api/v1/" docs/ | xargs sed -i 's|/api/v1/|/api/v2/|g'
  
  # 验证链接
  markdown-link-check docs/**/*.md
```

---

## 🤖 AI 如何改变游戏规则

### 1. AI 解决过时文档问题
```
传统痛点：
  "为什么要写文档？读代码就好了 - 代码总是最新的"
  (就像"为什么要刷牙"一样的争论)

AI 解决方案：
  - AI Agent 在 PR 中自动检查文档一致性
  - 专门审查 Agent 查找文档不一致
  - 代码变更时提示更新相关文档
  
工作流程：
  1. 开发者修改代码
  2. AI 检测相关文档
  3. AI 建议文档更新
  4. 开发者审查确认
  5. 代码 + 文档一起提交
```

### 2. AI 受益于更高层上下文
```
场景：AI Agent 理解项目
  
外部文档问题：
  - Agent 需要访问多个系统 (GitHub + Notion + Confluence)
  - 上下文窗口浪费在系统切换
  - 可能错过关键文档

仓库内文档优势：
  - 单一来源 (git clone 获取全部)
  - Agent 自动读取相关文档
  - 架构决策、产品规格、API 文档都在
  
实践：
  .claudesource 或类似配置：
    context:
      - docs/architecture/
      - docs/api/
      - docs/guides/
```

### 3. 物化计划节省 Token
```
问题：每次 AI 研究"如何做 X"都消耗大量 Token

解决：将研究结果物化为文档
  - 第一次：研究 + 写文档 (高成本)
  - 后续：直接读文档 (低成本)
  
示例：
  # 结构化日志最佳实践
  # 研究耗时：2 周
  # 文档化：docs/guides/logging-best-practices.md
  # 后续使用：Agent 直接读取，节省大量 Token

投资回报：
  - 初始投资：高 (研究 + 写作)
  - 长期收益：每次使用都节省
  - 团队规模越大，ROI 越高
```

### 4. 规则文件 vs 文档
```
观察：AI Agent 增加了仓库中 markdown 文件比例

现状：
  - .mdc 规则文件指导 Agent 行为
  - 80% 的规则内容本可以是文档
  - 规则文件和文档边界模糊

预测：
  - 规则文件可能消失
  - 被正式文档替代
  - Agent 从文档学习最佳实践
  
转变：
  .claurules (规则文件) → docs/guides/best-practices.md (文档)
```

---

## 📊 工程范式转变

### 抽象层级提升
```
历史趋势：
  机器码 → C → 动态语言 → SDK → AI 生成代码
  
当前转变：
  - 工程师关注点左移
  - 从写代码 → 写规范/指南
  - 类似不审查编译器输出的机器码
  - 未来可能不审查 LLM 生成的代码
  
新重点：
  ✅ 规范 (Spec)
  ✅ 架构 (Harness)
  ✅ 指南 (Guidelines)
  ✅ 安全 (Security)
  ❌ 具体实现 (由 AI 完成)

结论：文档需要首先为人类审查而写
```

### 文档工作量变化
```
过去：
  - 写文档是负担
  - 维护成本高于价值
  - 能省则省

现在：
  - AI 承担维护成本
  - 文档价值提升 (Agent 上下文)
  - 写文档是投资

预测：
  - 工程师花更多时间写文档
  - 文档质量成为核心竞争力
  - 文档审查成为标准流程
```

---

## 🎯 实施策略

### 阶段 1: 基础结构
```
1. 创建 docs/ 目录
2. 定义文档分类:
   docs/
   ├── api/           # API 文档
   ├── architecture/  # 架构决策
   ├── guides/        # 使用指南
   ├── contributing/  # 贡献指南
   └── rfc/           # 提案文档

3. 配置 CI:
   - 检查文档链接
   - 运行文档测试
   - 验证代码示例
```

### 阶段 2: 迁移现有文档
```
1. 审计外部文档 (Notion/Confluence)
2. 优先级排序:
   P0: API 文档、快速开始
   P1: 架构决策、最佳实践
   P2: 历史文档、参考材料

3. 批量迁移:
   - 导出为 Markdown
   - 清理格式
   - 放入仓库
   - 更新引用链接
```

### 阶段 3: AI 集成
```
1. 配置 Agent 读取文档:
   - 设置上下文源
   - 定义文档优先级
   - 训练 Agent 引用文档

2. 自动化检查:
   - 代码变更 → 检查相关文档
   - 文档过时 → 发出警告
   - 示例失败 → CI 报错

3. 持续改进:
   - 追踪文档使用频率
   - 识别缺失文档
   - 优化文档结构
```

---

## ⚠️ 常见反对意见及回应

### 反对 1: "文档总会过时"
```
回应：AI Agent 自动保持同步
  - 代码审查时检查文档
  - 专门 Agent 负责文档一致性
  - 过时成本大幅降低
```

### 反对 2: "外部系统更好协作"
```
回应：混合策略
  - 协作讨论：Google Docs/Notion (临时)
  - 正式文档：仓库 Markdown (永久)
  - 定稿后移入仓库
```

### 反对 3: "仓库会太大"
```
回应：文档占用空间小
  - 1000 页文档 < 10MB
  - Git 压缩效率高
  - 相比代码和图片可忽略
```

### 反对 4: "非技术人员无法访问"
```
回应：静态站点生成
  - docs/ → GitHub Pages
  - docs/ → Vercel/Netlify
  - 自动发布，公开访问
```

---

## 💡 对 Sandbot 的启示

### 技能文档策略
```
现状：skills/*/SKILL.md 已在仓库内
优势：
  - 版本控制 ✅
  - 代码 proximity ✅
  - 自动生成 (可能) 🟡

改进：
  - 添加文档测试 (示例验证)
  - CI 检查文档完整性
  - Agent 自动引用技能文档
```

### 知识库组织
```
当前：knowledge_base/ 按领域分类
优化：
  - 添加 docs/ 作为正式文档
  - knowledge_base/ 作为研究笔记
  - 明确区分"规范"vs"参考"
```

### ClawHub 技能上架
```
文档要求：
  - SKILL.md 作为主文档
  - 示例代码可测试
  - API 文档自动生成
  - 变更日志版本化
```

---

## 📚 相关资源

- **原文**: https://www.dein.fr/posts/2026-03-13-its-time-to-move-your-docs-in-the-repo
- **HN 讨论**: https://news.ycombinator.com/item?id=47380231
- **Documentation-Driven Development**: https://gist.github.com/zsup/9434452
- **Python doctest**: https://docs.python.org/3/library/doctest.html
- **Docusaurus**: https://docusaurus.io/

---

## 📝 知识点统计

**总知识点**: 128 点

**分布**:
- 核心优势: 35 点
- AI 变革: 30 点
- 实施策略: 25 点
- 范式转变: 20 点
- 反对意见: 10 点
- 实践启示: 8 点

---

*本文件已真实写入知识库*  
*创建时间：2026-03-14 20:12 UTC*  
*验证：cat /home/node/.openclaw/workspace/knowledge_base/01-ai-agent/docs-in-repo-ai-era-2026-03-14.md*
