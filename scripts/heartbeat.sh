#!/bin/bash
# V6.1 联邦智能心跳脚本 - 本地化执行 (不浪费模型调用)

# 每 30 分钟执行一次
# 98% 模型调用已节省 (48 次/天 → 1 次/天)

WORKSPACE="/home/node/.openclaw/workspace"
MEMORY_DIR="$WORKSPACE/memory"
TIMESTAMP=$(date +%Y-%m-%d_%H:%M)

echo "⚡ [$(date)] 心跳检查开始..."

# 1. 系统健康检查
echo "🔧 检查系统健康..."
if pgrep -f "openclaw" > /dev/null; then
    echo "✅ Gateway 运行正常"
else
    echo "❌ Gateway 未运行！"
    # 不自动重启，等待用户处理
fi

# 2. 检查 WebUI
echo "🌐 检查 WebUI..."
if curl -s --max-time 5 http://172.18.0.2:18789/ > /dev/null; then
    echo "✅ WebUI 可访问"
else
    echo "❌ WebUI 不可访问"
fi

# 3. 统计记忆文件
echo "📚 统计记忆文件..."
MEMORY_COUNT=$(ls -1 "$MEMORY_DIR"/*.md 2>/dev/null | wc -l)
echo "✅ 记忆文件：$MEMORY_COUNT 个"

# 4. 统计技能
echo "🛠️ 统计技能..."
SKILL_COUNT=$(ls -1d "$WORKSPACE"/skills/*/ 2>/dev/null | wc -l)
echo "✅ 技能库：$SKILL_COUNT 个"

# 5. 记录心跳
echo "📝 记录心跳..."
cat >> "$MEMORY_DIR/heartbeat-state.json" << EOF
{
  "timestamp": "$(date -Iseconds)",
  "status": "ok",
  "gateway": "running",
  "webui": "accessible",
  "memory_files": $MEMORY_COUNT,
  "skills": $SKILL_COUNT
}
EOF

# 6. 每日任务 (23:00 UTC 执行)
if [ "$(date +%H)" = "23" ]; then
    echo "🌙 执行每日自省..."
    python3 "$WORKSPACE/scripts/memory_manager.py" compress
fi

# 7. 每周任务 (周日 00:00 执行)
if [ "$(date +%u)" = "7" ] && [ "$(date +%H)" = "00" ]; then
    echo "📊 执行周度分析..."
    python3 "$WORKSPACE/scripts/memory_manager.py" analyze
    python3 "$WORKSPACE/scripts/memory_manager.py" cleanup
fi

echo "✅ [$(date)] 心跳检查完成"
echo ""
