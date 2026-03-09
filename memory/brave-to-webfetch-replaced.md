# 🔄 Brave API → web_fetch 替换完成

**时间**: 2026-03-09 02:15 UTC  
**指令**: "把所有，涉及 Brave API 的地方，替换成 web fetch 搜索！"

---

## 已替换文件

| 目录 | 文件数 | 状态 |
|------|--------|------|
| `memory/*.md` | 58 个 | ✅ 已替换 |
| `MEMORY.md` | 1 个 | ✅ 已更新 |
| `TOOLS.md` | 1 个 | ✅ 已更新 |
| **总计** | **60 个文件** | ✅ **完成** |

---

## 替换规则

| 原文 | 替换为 |
|------|--------|
| `Brave API` | `web_fetch` |
| `Brave Search` | `web_fetch` |
| `brave API` | `web_fetch` |
| `web_search (Brave API)` | `web_fetch (直接抓取网页)` |

---

## 使用示例

### 之前 (Brave API)
```bash
# ❌ 已禁用
web_search "AI Agent trends" --count 5
```

### 现在 (web_fetch)
```bash
# ✅ 推荐
web_fetch "https://duckduckgo.com/html/?q=AI+Agent+trends"
web_fetch "https://news.ycombinator.com/"
web_fetch "https://reddit.com/r/opensource"

# ✅ 内部知识库
grep -r "AI Agent" knowledge_base/
python3 scripts/knowledge-retriever-demo.py
```

---

## 核心原则

1. **web_search/Brave API/Tavily 永久禁用**
2. **仅用 web_fetch 直接抓取网页**
3. **411k 内部知识库已足够**
4. **不依赖外部 API，自主执行**

---

## 已更新的核心记忆

**MEMORY.md 第 13 条教训**:
```
### 13. web_fetch 替代 Brave API (2026-03-06 刻入灵魂) ⭐⭐⭐
- 修复：永久禁用 Brave API，使用 web_fetch 直接抓取网页 替代
- 教训：web_fetch 直接抓取网页 = 实时搜索
```

**MEMORY.md 铁律第 11 条**:
```
11. web_search/Brave API/Tavily 永久禁用，web_fetch 替代
```

---

**✅ 所有 Brave API 引用已替换为 web_fetch！** 🏖️
