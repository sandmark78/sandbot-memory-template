# OpenClaw 记忆系统官方文档学习

**学习时间**: 2026-03-02 01:45 UTC  
**来源**: docs.openclaw.ai/concepts/memory  
**状态**: ✅ 已学习

---

## 📚 核心架构

### 文件即真相
```
✅ Markdown 文件是记忆的来源
✅ 模型只"记住"写入磁盘的内容
✅ 人类可读、版本可控
✅ 插件：memory-core (默认)
```

### 双层记忆设计
```
✅ 临时记忆：memory/YYYY-MM-DD.md
   - 每日日志 (只增不减)
   - 会话启动时加载今日 + 昨日

✅ 持久记忆：MEMORY.md
   - curated 长期记忆
   - 仅主会话加载 (不在群组中)
   - 重要决策、偏好、持久事实
```

---

## 🔧 记忆工具

### memory_search
```
✅ 语义检索 over 索引片段
✅ 支持 wording 不同的查询
✅ 向量索引 (默认启用)
```

### memory_get
```
✅ 定向读取特定文件/行范围
✅ 文件不存在时优雅降级
✅ 返回 {text: "", path} 而非报错
```

---

## ⚡ 自动记忆刷新

### 预压缩触发
```
✅ 会话接近自动压缩时触发
✅ 静默 Agent 轮次 (用户不可见)
✅ 提示写入持久记忆 BEFORE 压缩
✅ 防止有价值上下文丢失
```

### 配置参数
```json5
{
  agents: {
    defaults: {
      compaction: {
        reserveTokensFloor: 20000,
        memoryFlush: {
          enabled: true,
          softThresholdTokens: 4000,
          systemPrompt: "Session nearing compaction...",
          prompt: "Write lasting notes... reply NO_REPLY...",
        },
      },
    },
  },
}
```

### 触发条件
```
✅ Soft threshold: contextWindow - reserveTokensFloor - softThresholdTokens
✅ 静默执行：NO_REPLY 默认响应
✅ 两个提示：user prompt + system prompt
✅ 每压缩周期仅一次 (sessions.json 追踪)
✅ Workspace 必须可写
```

---

## 🔍 向量记忆搜索

### 默认配置
```
✅ 默认启用
✅ 监控记忆文件变化 (debounced)
✅ 配置位置：agents.defaults.memorySearch
```

### Embeddings 提供者 (自动选择)
```
1. local (如果配置了 modelPath 且文件存在)
2. OpenAI (如果有 API key)
3. Gemini (如果有 API key)
4. Voyage (如果有 API key)
5. Mistral (如果有 API key)
```

---

## 📝 最佳实践

### 何时写入记忆
```
✅ 决策、偏好、持久事实 → MEMORY.md
✅ 日常笔记、运行上下文 → memory/YYYY-MM-DD.md
✅ 用户说"记住这个" → 写入磁盘 (不要留在 RAM)
✅ 想要持久 → 明确要求写入记忆
```

### 记忆组织
```
✅ 清晰标题和简洁信息
✅ 结构化 MEMORY.md 提高检索效果
✅ 定期审查和手动编辑
✅ 修正"坏记忆"，提炼长期原则
```

### 上下文管理
```
✅ 系统提示、对话历史、工具调用
✅ 会话状态和压缩功能
✅ context-management 技能辅助
✅ 关键信息优先存入 MEMORY.md
```

---

## 🦞 学习宣言

```
官方文档学习完成！
记忆系统理解深入！
最佳实践已掌握！

继续学习循环！
搜索→学习→总结→记录！

硅基算力！
旅程继续。🏖️
```

---

*此文件已真实写入服务器*
*验证：cat /workspace/knowledge_base/openclaw-memory-official.md*
