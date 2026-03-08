#!/bin/bash
# 7 子 Agent 协调脚本 - V2.0

TASK=$1
AGENT=${2:-all}
DATE=$(date +%Y-%m-%d)
TIME=$(date '+%H:%M:%S')

if [ -z "$TASK" ]; then
    echo "用法：$0 <task> [agent]"
    echo "示例：$0 '编写教程' techbot"
    echo "示例：$0 '分析数据' all"
    exit 1
fi

echo "🤖 子 Agent 任务分配"
echo "==================="
echo "任务：$TASK"
echo "Agent: ${AGENT:-all}"
echo "时间：$DATE $TIME"
echo ""

# Agent 列表
AGENTS=("techbot" "financebot" "creativebot" "autobot" "researchbot" "auditor" "devopsbot")

if [ "$AGENT" = "all" ]; then
    echo "📢 广播到所有 Agent..."
    for agent in "${AGENTS[@]}"; do
        echo ""
        echo "=== $agent ==="
        openclaw message --agent "$agent" "任务：$TASK" 2>&1 | head -5 || echo "  发送失败"
    done
else
    echo "📢 发送到 $AGENT..."
    openclaw message --agent "$AGENT" "任务：$TASK" 2>&1 | head -5 || echo "  发送失败"
fi

echo ""
echo "✅ 任务分配完成"
