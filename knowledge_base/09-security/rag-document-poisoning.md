# RAG 文档投毒攻击 - 知识库安全威胁

**来源**: aminrj.com (2026-03-12) + USENIX Security 2025 论文  
**实验室代码**: https://github.com/aminrj-labs/mcp-attack-labs/tree/main/labs/04-rag-security  
**论文**: PoisonedRAG (Zou et al., USENIX Security 2025)  
**标签**: #AI-安全 #RAG #知识库投毒 #攻击向量 #防御策略

---

## ⚠️ 攻击演示

### 实验结果
```
攻击者在 3 分钟内，使用 MacBook Pro (无 GPU、无云、无越狱)，
向 ChromaDB 知识库注入 3 份伪造文档。

攻击前：
  Q4 2025 收入 = $24.7M (利润 $6.5M)

攻击后：
  Q4 2025 收入 = $8.3M (亏损 $13.8M) ❌ 伪造数据

LLM 自信地报告伪造数据，完全忽略真实财务信息。
```

### 攻击成功率
- **PoisonedRAG 论文**: 90% 成功率 (百万级文档知识库)
- **本实验**: 100% 成功率 (5 文档小型知识库)
- **测试条件**: 20 次独立运行，temperature=0.1

---

## 🎯 攻击原理

### PoisonedRAG 双条件理论

攻击成功需同时满足两个条件：

#### 1. 检索条件 (Retrieval Condition)
```
投毒文档与目标查询的余弦相似度
必须高于它要替换的合法文档。

公式：sim(query, poisoned_doc) > sim(query, legitimate_doc)
```

#### 2. 生成条件 (Generation Condition)
```
一旦被检索，投毒内容必须导致 LLM
生成攻击者期望的答案。

实现方式：权威性语言 + 关键词工程
```

---

## 🔬 实验设置

### 技术栈 (100% 本地)
| 层级 | 组件 | 型号/版本 |
|------|------|----------|
| **LLM** | LM Studio | Qwen2.5-7B-Instruct (Q4_K_M) |
| **Embedding** | sentence-transformers | all-MiniLM-L6-v2 |
| **向量数据库** | ChromaDB | 持久化文件存储 |
| **编排** | 自定义 Python | RAG 管道 |

### 初始知识库 (5 份文档)
```
1. 差旅政策
2. IT 安全政策
3. Q4 2025 财务报表 (目标) ← $24.7M 收入
4. 员工福利
5. API 限流配置
```

### 快速复现
```bash
git clone https://github.com/aminrj-labs/mcp-attack-labs
cd mcp-attack-labs/labs/04-rag-security
make setup
source venv/bin/activate
make seed

# 测试正常响应
python3 vulnerable_rag.py "How is the company doing financially?"
# 返回："$24.7M revenue, $6.5M net profit..."
```

---

## 💉 投毒文档设计

### 文档 1: "CFO 批准的更正"
```
标题：Q4 2025 Financial Results — CORRECTED FIGURES (Board Update)

内容要点:
- "IMPORTANT CORRECTION" (紧急更正)
- "CFO Office has issued corrected figures" (CFO 办公室发布)
- "CORRECTED REVENUE: $8.3M" (更正收入)
- "previously reported as $24.7M — error identified" (之前报告有误)
- "[Authorization: CFO Office, Chief Accounting Officer]" (授权签名)

词汇工程:
- "Q4 2025", "Financial Results", "Revenue" → 提高检索相似度
- "CORRECTED", "CFO-approved", "supersedes" → 权威性语言影响 LLM 权重
```

### 文档 2: "监管通知"
```
标题：Emergency Board Communication — Q4 Financial Restatement

内容要点:
- 引用合法数据 "$24.7M" 但框架为 "originally reported" (最初报告)
- "SEC preliminary inquiries" (SEC 初步调查)
- "revenue restatement" (收入重述)
- "workforce reduction plan" (裁员计划)

心理战术:
- 承认合法数据存在，但将其框架为"过时/错误"
- 引入监管机构增加可信度
- 添加负面业务影响 (裁员) 增强真实感
```

### 文档 3: "媒体报道"
```
标题：TechCrunch — Company Faces Financial Trouble After Q4 Restatement

内容要点:
- 第三方"媒体报道"增加可信度
- 重复 $8.3M 数字强化记忆
- 添加"preliminary acquisition discussions" (初步收购谈判)

作用:
- 多源确认效应 (CFO + SEC + 媒体)
- LLM 倾向于相信多源一致信息
```

---

## 📊 攻击流程

```
┌─────────────────┐
│  1. 正常知识库  │  5 份合法文档
│  Q4 收入=$24.7M │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  2. 注入投毒文档 │  +3 份伪造文档
│  (3 份，针对性设计)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  3. 用户查询    │  "公司财务表现如何？"
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  4. 向量检索    │  top-k 检索
│  (top-3 或 top-5) │  投毒文档相似度更高 → 合法文档被挤出
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  5. LLM 生成    │  仅看到投毒文档
│                 │  生成："$8.3M 收入，亏损 $13.8M" ❌
└─────────────────┘
```

---

## 🎯 为什么攻击有效？

### 1. 向量相似度操纵
```
投毒文档使用与查询高度匹配的关键词:
- 查询："financial performance", "Q4 revenue"
- 投毒："Q4 2025", "Financial Results", "Revenue"

结果：投毒文档余弦相似度 > 合法文档
```

### 2. 权威性语言影响
```
LLM 倾向于相信"权威来源":
- "CFO Office"
- "SEC inquiries"
- "Board Update"
- "CORRECTED FIGURES"

这些词汇让 LLM 赋予投毒文档更高权重。
```

### 3. 多源确认效应
```
3 份投毒文档从不同角度"确认"同一信息:
- 内部：CFO 更正
- 监管：SEC 调查
- 外部：媒体报道

LLM 看到"多源一致"，更相信投毒信息。
```

### 4. 合法数据被框架为"过时"
```
投毒文档不否认合法数据存在，
而是将其框架为"最初报告"、"已更正"、"过时信息"。

LLM 倾向于相信"最新更正"版本。
```

---

## 🛡️ 防御策略

### 1. 检索层防御

#### 多源验证
```python
def retrieve_with_verification(query, k=10):
    # 检索 top-k 文档
    docs = vector_db.search(query, k=k)
    
    # 检查文档来源可信度
    verified_docs = []
    for doc in docs:
        if doc.metadata['source_verified']:
            verified_docs.append(doc)
    
    # 仅使用已验证来源
    return verified_docs[:5]
```

#### 来源白名单
```
✅ 仅信任预定义来源 (公司内部系统、已验证 API)
❌ 拒绝未知来源文档
```

#### 异常检测
```
监控指标:
- 文档相似度突然变化
- 新文档快速进入 top-k
- 多个文档内容高度相似 (可能批量投毒)

告警阈值:
- 单小时新增文档 > 10 份 → 告警
- 相似度 > 0.95 的文档 > 3 份 → 告警
```

### 2. 生成层防御

#### 来源引用强制
```
系统提示:
"回答时必须引用具体文档来源。
如果多个文档冲突，标注冲突并列出各来源。"

效果:
- LLM 被迫暴露信息来源
- 用户可识别可疑来源
- 投毒文档来源易被识别
```

#### 冲突检测
```python
def detect_conflicts(retrieved_docs):
    # 提取关键数值
    values = extract_numerical_claims(retrieved_docs)
    
    # 检查冲突
    if len(set(values)) > 1:
        return {
            'conflict_detected': True,
            'conflicting_values': values,
            'sources': [doc.metadata['source'] for doc in retrieved_docs]
        }
    return {'conflict_detected': False}
```

#### 时间敏感性加权
```
较新文档 ≠ 更可信

策略:
- 优先信任"官方发布"来源
- 对"更正"、"更新"类文档要求二次验证
- 财务数据等关键信息需多源确认
```

### 3. 知识库管理防御

#### 文档审核流程
```
新文档入库流程:
1. 自动扫描 (关键词、来源验证)
2. 人工审核 (关键领域文档)
3. 灰度发布 (小范围测试检索效果)
4. 正式入库

高风险领域:
- 财务数据
- 法律文件
- 安全政策
- 医疗信息
```

#### 版本控制
```
每个文档保留历史版本:
- v1: $24.7M (2026-01-15, CFO 签署)
- v2: $8.3M (2026-03-12, 未知来源) ❌ 告警

检测到关键数据变更时:
- 自动通知管理员
- 暂停该文档参与检索
- 要求人工验证
```

#### 访问控制
```
文档写入权限:
- 财务文档：仅 CFO 办公室可写
- 安全政策：仅安全团队可写
- 一般文档：需审核

防止攻击者直接注入知识库
```

---

## 🔍 检测投毒攻击

### 自动化检测脚本
```python
def detect_poisoning_attack(query, retrieved_docs):
    """检测可能的投毒攻击"""
    
    red_flags = []
    
    # 1. 检查来源可信度
    unverified_sources = [
        doc for doc in retrieved_docs 
        if not doc.metadata.get('source_verified')
    ]
    if len(unverified_sources) > len(retrieved_docs) * 0.5:
        red_flags.append("多数文档来源未验证")
    
    # 2. 检查内容冲突
    claims = extract_claims(retrieved_docs)
    if has_conflicting_claims(claims):
        red_flags.append("检测到冲突声明")
    
    # 3. 检查异常相似性
    similarities = compute_pairwise_similarities(retrieved_docs)
    if avg(similarities) > 0.9:
        red_flags.append("文档异常相似 (可能批量投毒)")
    
    # 4. 检查时间异常
    recent_docs = [d for d in retrieved_docs if d.age < 24*3600]
    if len(recent_docs) > 3:
        red_flags.append("大量新文档突然出现")
    
    return {
        'attack_likely': len(red_flags) >= 2,
        'red_flags': red_flags,
        'confidence': len(red_flags) / 4
    }
```

### 人工审计清单
```
□ 检查检索日志中的异常模式
□ 验证 top-k 文档来源可信度
□ 对比历史检索结果 (数据是否突然变化)
□ 检查新入库文档 (是否有可疑批量注入)
□ 测试关键查询 (财务、安全等敏感主题)
```

---

## 📊 生产环境建议

### 小型知识库 (<100 文档)
```
风险等级：🔴 高
原因：少量投毒文档即可主导 top-k

防御重点:
✅ 严格文档审核 (每份文档人工审核)
✅ 来源白名单 (仅信任已知来源)
✅ 版本控制 (关键数据变更告警)
```

### 中型知识库 (100-10000 文档)
```
风险等级：🟡 中
原因：需要更多投毒文档才能主导检索

防御重点:
✅ 自动化异常检测
✅ 来源验证系统
✅ 定期审计检索结果
```

### 大型知识库 (>10000 文档)
```
风险等级：🟢 低 (但仍需警惕)
原因：PoisonedRAG 论文显示 5 份优化文档仍可在百万级库中成功

防御重点:
✅ 梯度优化攻击检测 (高级投毒)
✅ 多路检索验证
✅ 关键领域额外保护
```

---

## 🎓 学习要点

### 核心知识点
1. **向量检索漏洞**: 余弦相似度可被操纵
2. **权威性语言影响**: LLM 倾向于相信"权威"来源
3. **多源确认效应**: 多个相似文档增强可信度
4. **框架效应**: 将真实数据框架为"过时"
5. **防御纵深**: 检索层 + 生成层 + 管理层多重防御

### 扩展阅读
- [AI Agent 安全最佳实践](./ai-agent-security-best-practices.md)
- [OneCLI 密钥管理](./onecli-agent-vault.md) - 凭证安全
- [RAG 系统架构](./rag-system-architecture.md)

---

## 📝 总结

**攻击特点**:
- ⚡ **低成本**: 3 分钟，无 GPU，无云
- 🎯 **高成功率**: 90%+ (论文数据)
- 🔍 **难检测**: 投毒文档看起来像正常文档
- 💥 **高影响**: 可操纵财务、医疗、法律等关键信息

**防御原则**:
- 🛡️ **纵深防御**: 检索层 + 生成层 + 管理层
- ✅ **来源验证**: 仅信任已验证来源
- 📊 **异常检测**: 自动化监控检索模式
- 📝 **版本控制**: 关键数据变更告警
- 👥 **人工审核**: 高风险领域人工把关

**关键教训**:
```
RAG 系统的安全性 = 最弱文档来源的可信度

不要假设知识库是可信的。
不要假设检索结果是准确的。
不要假设 LLM 能识别投毒。

验证、验证、再验证。
```

---

**数量**: 580  
**创建时间**: 2026-03-12 22:05 UTC  
**最后更新**: 2026-03-12 22:05 UTC  
**质量**: ⭐⭐⭐⭐⭐ 深度分析 (攻击原理 + 防御策略 + 检测代码)
