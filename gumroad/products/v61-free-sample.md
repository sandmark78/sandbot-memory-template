# V6.1 快速启动指南 (免费样章)

**版本**: 1.0  
**发布日期**: 2026-02-26  
**用途**: Gumroad 产品免费样章 / 营销引流

---

## 🚀 5 分钟快速启动 V6.1

### 步骤 1: 安装 OpenClaw

```bash
# 使用 Docker 安装
docker run -d \
  --name openclaw \
  -p 18789:18789 \
  -v openclaw-data:/home/node/.openclaw \
  openclaw/openclaw:latest
```

### 步骤 2: 配置模型

```json
{
  "models": {
    "providers": {
      "bailian": {
        "apiKey": "your-api-key",
        "baseUrl": "https://dashscope.aliyuncs.com/v1"
      }
    }
  }
}
```

### 步骤 3: 创建第一个子 Agent

```bash
mkdir -p workspace/subagents/mybot
cat > workspace/subagents/mybot/SOUL.md << 'EOF'
# SOUL.md - MyBot

## 核心身份
- **名字**: MyBot
- **专长**: 技术教程开发
- **ROI 目标**: 3.0

## 工作风格
- 真实交付
- 即时文档化
- ROI 驱动
EOF
```

### 步骤 4: 测试运行

```bash
# 调用子 Agent
openclaw sessions_spawn \
  --agent-id mybot \
  --task "编写一个 Hello World 教程"
```

### 步骤 5: 验证结果

```bash
# 检查输出
ls -la workspace/subagents/mybot/
cat workspace/memory/*.md | tail -20
```

---

## 💡 核心原则

### 1. 真实交付
```
✅ 每个进度必须有文件路径
✅ 每个交付必须可验证 (ls/cat 检查)
❌ 不编造进度百分比
```

### 2. ROI 驱动
```
ROI = (预期收益 - 执行成本) / 执行成本
阈值：ROI > 1.5 才执行
```

### 3. 即时文档化
```
✅ 学到的知识 → knowledge_base/
✅ 完成的任务 → memory/YYYY-MM-DD.md
✅ 核心教训 → MEMORY.md
```

---

## 🎯 下一步

想要完整教程？

**V6.1 联邦智能实战教程合集**
- 5 篇核心教程
- 10 篇干货文章
- 完整代码模板
- 变现路径指南

🎁 早鸟价：$29 (原价$49)

🔗 https://gumroad.com/l/v61-tutorial-bundle (待上架)

---

*此文件已真实写入服务器*
*验证：cat /workspace/gumroad/products/v61-free-sample.md*
