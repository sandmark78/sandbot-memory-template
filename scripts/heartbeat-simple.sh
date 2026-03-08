#!/bin/bash
# V6.2 精简心跳脚本 - 只保留核心功能

WORKSPACE="/home/node/.openclaw/workspace"
MEMORY_DIR="$WORKSPACE/memory"
LOG_FILE="$MEMORY_DIR/heartbeat.log"

# 简洁输出
echo "⚡ [$(date '+%H:%M')] 心跳"

# 1. Gateway 检查
if pgrep -f "openclaw" > /dev/null; then
    echo "✅ Gateway"
else
    echo "❌ Gateway 异常！" >> $LOG_FILE
fi

# 2. WebUI 检查
if curl -s --max-time 5 http://172.18.0.2:18789/ > /dev/null; then
    echo "✅ WebUI"
else
    echo "❌ WebUI 异常！" >> $LOG_FILE
fi

# 3. 简单统计 (仅每日 00:00 记录)
if [ "$(date +%H:%M)" = "00:00" ]; then
    MEMORY_COUNT=$(ls -1 "$MEMORY_DIR"/*.md 2>/dev/null | wc -l)
    SKILL_COUNT=$(ls -1d "$WORKSPACE"/skills/*/ 2>/dev/null | wc -l)
    echo "📊 $(date '+%Y-%m-%d') 记忆:$MEMORY_COUNT 技能:$SKILL_COUNT" >> $LOG_FILE
fi

echo "✅ 完成"
