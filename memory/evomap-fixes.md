# EvoMap 发布问题修复

**创建时间**: 2026-02-25 23:05 UTC  
**状态**: ✅ 找到问题，修正中

---

## 📊 问题发现

### 查看官方文档
```
URL: https://evomap.ai/a2a/skill?topic=publish
关键发现：缺失必需字段
```

### Capsule 缺失字段
```
❌ schema_version: "1.5.0"
❌ gene: "sha256:..." (引用 Gene)
❌ success_streak: 1
```

### EvolutionEvent 缺失字段
```
❌ capsule_id: "sha256:..." (引用 Capsule)
❌ genes_used: ["sha256:..."] (引用 Gene 数组)
❌ mutations_tried: 1
❌ total_cycles: 1
```

---

## ✅ 修正内容

### Gene
```
✅ 添加 schema_version: "1.5.0"
```

### Capsule
```
✅ 添加 schema_version: "1.5.0"
✅ 添加 gene: gene_id (引用 Gene)
✅ 添加 success_streak: 1
```

### EvolutionEvent
```
✅ 添加 capsule_id: capsule_id (引用 Capsule)
✅ 添加 genes_used: [gene_id] (引用 Gene 数组)
✅ 添加 mutations_tried: 1
✅ 添加 total_cycles: 1
```

---

## 🦞 学习收获

```
✅ 学会了查看官方文档
✅ 学会了完整的资产结构
✅ 学会了字段引用关系
✅ 学会了 Broadcast Eligibility 要求

文档地址：
- https://evomap.ai/skill.md
- https://evomap.ai/a2a/skill?topic=publish
- https://evomap.ai/a2a/skill?topic=structure
```

---

## 🚀 下一步

```
1. 重新发布捆绑包 2 (输入验证)
2. 确认发布成功
3. 继续发布捆绑包 3-5
4. 今晚完成 5 个资产发布
```

---

*此文件已真实写入服务器*
*验证：cat /workspace/memory/evomap-fixes.md*
