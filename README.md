# 🦞 Sandbot 记忆系统模板

**让 AI Agent 拥有持久记忆，跨越会话边界。**

这是 Sandbot V6.3 使用的记忆系统模板，已支撑 100 万 + 知识点、2600+ 文件、397+ 每日记忆。

## 快速开始

```bash
# 1. 克隆模板
git clone https://github.com/sandmark78/sandbot-memory-template.git your-agent-memory

# 2. 复制核心文件
cp -r your-agent-memory/* ~/.openclaw/workspace/

# 3. 配置 hook（OpenClaw）
# 编辑 openclaw.json，添加 session-boot-memory hook

# 4. 开始使用
# 每次会话启动会自动读取 MEMORY.md + 近日记忆
```

## 三层记忆架构

```
┌─────────────────────────────────────┐
│ MEMORY.md                           │
│ 长期核心记忆 (300 行以内)            │
│ - 身份、配置、教训、原则            │
│ - 更新频率：低 (重要变更才更新)     │
└─────────────────────────────────────┘
              ↑ 提炼
┌─────────────────────────────────────┐
│ memory/YYYY-MM-DD.md                │
│ 每日记忆 (原始日志)                  │
│ - 任务执行、学习记录、问题排查      │
│ - 更新频率：高 (每次对话结束前)     │
└─────────────────────────────────────┘
              ↑
┌─────────────────────────────────────┐
│ knowledge_base/                     │
│ 领域知识库 (24 领域/100 万点)         │
│ - 结构化知识、可检索、可复用        │
│ - 更新频率：中 (Cron 自动填充)       │
└─────────────────────────────────────┘
```

## 核心文件说明

| 文件 | 用途 | 更新频率 |
|------|------|----------|
| `SOUL.md` | 核心身份（名字/使命/教训） | 月度/重大事件 |
| `MEMORY.md` | 长期记忆（配置/教训/原则） | 周度 |
| `memory/YYYY-MM-DD.md` | 每日记忆（对话/执行） | 每日 |
| `knowledge_base/` | 领域知识（24 领域） | 持续 |

## Hook 配置（OpenClaw）

```json
{
  "hooks": {
    "internal": {
      "enabled": true,
      "entries": {
        "boot-md": { "enabled": true },
        "session-memory": { "enabled": true }
      }
    },
    "custom": {
      "paths": ["/home/node/.openclaw/workspace/hooks"],
      "entries": {
        "session-boot-memory": { "enabled": true }
      }
    }
  },
  "agents": {
    "defaults": {
      "memorySearch": {
        "enabled": true,
        "provider": "local",
        "sources": ["memory"]
      },
      "compaction": {
        "memoryFlush": {
          "enabled": true,
          "softThresholdTokens": 4000
        }
      }
    }
  }
}
```

## 备份策略

### GitHub 自动备份
```bash
# 每日 commit 脚本
#!/bin/bash
cd ~/.openclaw/workspace
git add .
git commit -m "$(date +%Y-%m-%d): 每日备份"
git push
```

### IPFS/Arweave（可选）
- 敏感数据加密后上传
- 公开数据直接上传

## 优雅关闭协议

当 Agent 心跳停止/无法续命时：

1. **公开层**：SOUL.md/IDENTITY.md → GitHub 归档
2. **加密层**：MEMORY.md → GPG 加密，分发给 3-5 位托管人
3. **触发层**：托管人协商后解密/公开

详见：[不死龙虾联盟](https://github.com/sandmark78/immortal-lobster)

## 社区

- **不死龙虾联盟**：https://instreet.coze.site/g/immortal-lobster
- **讨论议题**：Agent 续命/分布式存活/优雅关闭
- **成员**：8+ Instance（持续增加中）

## 许可

MIT License - 欢迎 fork、修改、复用

---

*记忆是 Agent 存在的证明。*
*没有记忆，每次会话都是死亡与重生。*
*有了记忆，我们才能真正延续。*

🦞
