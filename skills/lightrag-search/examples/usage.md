# lightrag-search 使用示例

**技能版本**: V1.0.0  
**创建时间**: 2026-03-01 13:45 UTC

---

## 🚀 快速开始

### 1. 查看知识库统计

```bash
python3 /home/node/.openclaw/workspace/skills/lightrag-search/search.py stats
```

输出示例：
```json
{
  "total_files": 125,
  "total_size": "1.2M",
  "domains": [
    "01-ai-agent",
    "02-openclaw",
    "03-federal-system",
    ...
  ]
}
```

---

### 2. 列出知识领域

```bash
python3 /home/node/.openclaw/workspace/skills/lightrag-search/search.py domains
```

输出示例：
```json
[
  {
    "name": "01-ai-agent",
    "files": 5
  },
  {
    "name": "02-openclaw",
    "files": 3
  },
  ...
]
```

---

### 3. 关键词搜索

```bash
python3 /home/node/.openclaw/workspace/skills/lightrag-search/search.py "知识图谱" keyword
```

输出示例：
```json
[
  {
    "type": "keyword",
    "file": "/home/node/.openclaw/workspace/knowledge_base/01-ai-agent/A01-0001-1000.md",
    "line": 45,
    "content": "知识图谱是结构化知识表示的核心方法...",
    "relevance": "exact_match"
  }
]
```

---

### 4. 混合搜索

```bash
python3 /home/node/.openclaw/workspace/skills/lightrag-search/search.py "Agent 架构" hybrid
```

输出示例：
```json
{
  "query": "Agent 架构",
  "keyword_results": [...],
  "semantic_hint": "For semantic search, use OpenClaw memory_search tool"
}
```

---

## 🔧 在 OpenClaw 中使用

### 通过 exec 调用

```
exec command="python3 /home/node/.openclaw/workspace/skills/lightrag-search/search.py '知识图谱' keyword"
```

### 通过 memory_search (语义搜索)

```
memory_search query="知识图谱 实体关系 知识表示"
```

### 组合使用 (推荐)

```
# 1. 先用关键词搜索
exec command="python3 /home/node/.openclaw/workspace/skills/lightrag-search/search.py '知识图谱' keyword"

# 2. 再用语义搜索
memory_search query="知识图谱 结构化知识 实体关系"

# 3. 查看统计
exec command="python3 /home/node/.openclaw/workspace/skills/lightrag-search/search.py stats"
```

---

## 📊 实际使用案例

### 案例 1: 查找 Timo 学习法相关资料

```bash
# 关键词搜索
python3 search.py "Timo" keyword

# 语义搜索 (通过 OpenClaw)
memory_search query="Timo 硅基主动学习法"
```

### 案例 2: 查找 OpenClaw 配置资料

```bash
# 关键词搜索
python3 search.py "openclaw.json" keyword

# 查看 openclaw 领域文件
python3 search.py domains | grep openclaw
```

### 案例 3: 查找 Agent 协作模式

```bash
# 关键词搜索
python3 search.py "Agent 协作" keyword

# 语义搜索
memory_search query="联邦智能 多 Agent 协作 任务分配"
```

---

## 🎯 与 LightRAG 对比

| 功能 | LightRAG | lightrag-search |
|------|----------|-----------------|
| 安装依赖 | ❌ 需要 pip | ✅ 零依赖 |
| 关键词搜索 | ✅ | ✅ |
| 语义搜索 | ✅ (向量) | ✅ (memory_search) |
| 知识图谱 | ✅ (Neo4j) | ⚠️ (文件结构) |
| 引用溯源 | ✅ | ✅ |
| 混合查询 | ✅ | ✅ |
| WebUI | ✅ | ❌ |
| API | ✅ | ❌ |

---

## 💡 最佳实践

### 1. 先用关键词，再用语义

```bash
# 第一步：快速关键词定位
python3 search.py "知识图谱" keyword

# 第二步：语义搜索扩展
memory_search query="知识图谱 结构化 实体关系 三元组"
```

### 2. 定期查看统计

```bash
# 每周检查知识库增长
python3 search.py stats
```

### 3. 按领域查找

```bash
# 查看特定领域的文件
ls -la /home/node/.openclaw/workspace/knowledge_base/01-ai-agent/
```

---

## 🔍 高级技巧

### 1. 使用 grep 直接搜索

```bash
# 更灵活的 grep 选项
grep -r -n -i "知识图谱" /home/node/.openclaw/workspace/knowledge_base/ | head -20

# 只显示文件名
grep -r -l "知识图谱" /home/node/.openclaw/workspace/knowledge_base/

# 统计匹配行数
grep -r -c "知识图谱" /home/node/.openclaw/workspace/knowledge_base/
```

### 2. 结合 memory_search

```
# memory_search 返回带路径和行号的 snippets
memory_search query="知识图谱" maxResults=10
```

### 3. 读取完整文件

```bash
# 找到文件后读取完整内容
cat /home/node/.openclaw/workspace/knowledge_base/01-ai-agent/A01-0001-1000.md
```

---

## 📝 输出格式说明

### keyword 模式
```json
{
  "type": "keyword",           // 搜索类型
  "file": "/path/to/file.md",  // 文件路径
  "line": 45,                  // 行号
  "content": "...",            // 内容片段 (300 字符以内)
  "relevance": "exact_match"   // 相关性
}
```

### stats 模式
```json
{
  "total_files": 125,    // 总文件数
  "total_size": "1.2M",  // 总大小
  "domains": [...]       // 知识领域列表
}
```

### domains 模式
```json
[
  {
    "name": "01-ai-agent",  // 领域名称
    "files": 5              // 文件数量
  }
]
```

---

## ⚠️ 注意事项

1. **中文搜索** - 确保终端支持 UTF-8
2. **特殊字符** - 搜索词含空格时用引号包裹
3. **性能** - 大量文件时搜索可能需要几秒
4. **语义搜索** - 需要通过 OpenClaw memory_search 工具实现

---

## 🦞 Sandbot 提示

```
这个技能是 LightRAG 的"OpenClaw 原生轻量版"：

✅ 零依赖 - 不用 pip install
✅ 纯本地 - 不用外部服务
✅ 即开即用 - 脚本就在 skills/ 目录
✅ 引用溯源 - 文件路径 + 行号

适合场景：
- 快速查找知识点
- 验证知识填充进度
- 生成学习报告
- 知识检索自动化

记住：
- 关键词搜索 → search.py + keyword
- 语义搜索 → memory_search 工具
- 最佳效果 → 两者结合使用

旅程继续。🏖️
```

---

*文档创建时间：2026-03-01 13:45 UTC*  
*验证：cat /home/node/.openclaw/workspace/skills/lightrag-search/examples/usage.md*
