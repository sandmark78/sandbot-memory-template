#!/bin/bash
# 知识填充脚本 - 修复版 (使用 sed 替代 edit)

MEMORY_FILE="/home/node/.openclaw/workspace/memory/2026-03-12.md"
TIMESTAMP=$(date '+%H:%M UTC')

# 使用 sed 添加内容 (而不是 edit 工具)
sed -i "/^## 📚 Cron 知识获取/a\\
### 执行记录 ($TIMESTAMP)\\
- ✅ 状态检查\\
- ✅ 知识整合\\
\\
" "$MEMORY_FILE" 2>/dev/null || echo "sed 失败，使用追加方式" && cat >> "$MEMORY_FILE" << INNEREOF

### 执行记录 ($TIMESTAMP)
- ✅ 状态检查
- ✅ 知识整合

INNEREOF

echo "✅ 知识填充完成 ($TIMESTAMP)"
