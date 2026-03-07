# Agent Browser 学习总结

**学习时间**: 2026-03-03 07:45 UTC  
**来源**: https://github.com/vercel-labs/agent-browser  
**归档**: chat-archive/2026-03-03.md

---

## 📊 Agent Browser 核心功能

### 定位
- Headless 浏览器自动化 CLI
- 专为 AI Agent 设计
- Rust CLI + Node.js fallback

### 核心命令
```bash
agent-browser open example.com          # 打开 URL
agent-browser snapshot                  # 获取 accessibility tree
agent-browser click @e2                 # 点击元素
agent-browser fill @e3 "text"           # 填充表单
agent-browser screenshot page.png       # 截图
agent-browser find role button click    # 语义搜索
agent-browser wait 3000                 # 等待
agent-browser press Enter               # 按键
```

### 特点
1. **Accessibility Tree Snapshot** - 带引用的可访问性树
2. **语义定位器** - `find role button --name "Submit"`
3. **高性能** - Rust CLI，亚毫秒解析
4. **AI 优化** - 专为 Agent 设计的工作流

---

## 🎯 OpenClaw 适配分析

### 功能对比

| 功能 | Agent Browser | OpenClaw Browser | 状态 |
|------|---------------|------------------|------|
| 打开 URL | ✅ | ✅ `browser open` | 已有 |
| Snapshot | ✅ | ✅ `browser snapshot` | 已有 |
| 点击 | ✅ | ✅ `browser act click` | 已有 |
| 填充 | ✅ | ✅ `browser act fill` | 已有 |
| 截图 | ✅ | ✅ `browser screenshot` | 已有 |
| 语义搜索 | ✅ | ✅ `refs="aria"` | 已有 |
| 等待 | ✅ | ✅ `browser act wait` | 已有 |
| 按键 | ✅ | ✅ `browser act press` | 已有 |

### 结论

**✅ OpenClaw 已覆盖核心功能，无需安装外部工具！**

---

## 📝 使用方式

### OpenClaw 原生用法

```
# 打开网页
browser open url="https://example.com"

# 获取快照 (带 aria refs)
browser snapshot refs="aria"

# 点击元素
browser act click ref="e2"

# 填充表单
browser act fill ref="e3" text="test@example.com"

# 截图
browser screenshot fullPage=true

# 等待
browser act wait timeMs=3000

# 按键
browser act press key="Enter"
```

### 包装脚本 (可选)

如需语法兼容 Agent Browser CLI，可创建 `abw.py` 包装层：

```bash
python3 abw.py open https://example.com
python3 abw.py snapshot
python3 abw.py click @e2
python3 abw.py fill @e3 "text"
```

---

## 🎯 最佳实践

### 1. 直接使用 OpenClaw browser 工具 (推荐)
```
browser open url="https://example.com"
browser snapshot refs="aria"
browser act click ref="e2"
```

### 2. 批量操作脚本
```python
# Python 脚本封装多个 browser 调用
operations = [
    {"action": "open", "url": "https://example.com"},
    {"action": "snapshot"},
    {"action": "click", "ref": "e2"},
]
```

### 3. 元素定位
```
# 1. 获取快照
browser snapshot refs="aria"

# 2. 从快照中找到目标元素的 ref

# 3. 使用 ref 执行操作
browser act click ref="e10"
```

---

## 📋 决策

### ✅ 采用
- OpenClaw 原生 `browser` 工具
- 零安装，零依赖
- 功能覆盖 Agent Browser 核心能力

### ❌ 不采用
- 安装 `agent-browser` npm 包
- 额外 Rust/Node.js 依赖
- 外部 CLI 工具

### 理由
1. **功能相同** - OpenClaw browser 已覆盖核心功能
2. **零依赖** - 不用安装额外工具
3. **更好集成** - OpenClaw 原生工具链
4. **节省成本** - 无安装和维护开销

---

## 🦞 归档记录

**归档位置**: `/home/node/.openclaw/workspace/memory/chat-archive/2026-03-03.md`

**分类**: technical

**内容摘要**:
- 学习 Vercel Agent Browser
- 分析 OpenClaw 适配性
- 决策：使用原生 browser 工具
- 创建技能文档 (可选包装层)

---

*学习完成时间：2026-03-03 07:45 UTC*  
*验证：cat /home/node/.openclaw/workspace/knowledge_base/agent-browser-analysis.md*
