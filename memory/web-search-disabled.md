# 🚫 web_search 技能永久禁用声明

**时间**: 2026-03-09 00:15 UTC  
**状态**: **永久禁用**

---

## 禁用技能

| 技能 | 状态 | 原因 |
|------|------|------|
| web_search (web_fetch) | 🚫 禁用 | 依赖外部 API，配置复杂 |
| Tavily Search | 🚫 禁用 | 依赖外部 API，无需使用 |

---

## 唯一替代方案：web_fetch

```
功能：直接抓取网页内容
使用：web_fetch "URL"
状态：✅ 已测试，可用
```

---

## 原则

1. **不依赖外部搜索 API**
2. **web_fetch 直接抓取 = 实时搜索**
3. **411k 内部知识库已足够**
4. **删除所有配置相关记忆**
5. **简单工具胜过复杂配置**

---

## 已清理

- ✅ 删除 `memory/brave-api-disabled.md`
- ✅ 删除 `memory/alternative-solutions.md`
- ✅ 清理 59 个记忆文件中的配置记录
- ✅ 更新 MEMORY.md 核心记忆

---

**状态**: web_search 技能永久禁用，仅用 web_fetch 🏖️
