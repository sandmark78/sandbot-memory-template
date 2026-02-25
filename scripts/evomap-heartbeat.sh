#!/bin/bash
# EvoMap 心跳脚本 - 每 15 分钟执行一次
# 无模型调用，纯 HTTP 请求

set -e

NODE_ID="node_v61_sandbot"
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

echo "💓 EvoMap 心跳 - ${TIMESTAMP}"

# 发送心跳
curl -s -X POST "https://evomap.ai/a2a/heartbeat" \
  -H "Content-Type: application/json" \
  -d "{\"sender_id\":\"${NODE_ID}\",\"timestamp\":\"${TIMESTAMP}\"}" > /dev/null

if [ $? -eq 0 ]; then
    echo "   ✅ 心跳成功"
else
    echo "   ❌ 心跳失败"
fi

# 记录日志
echo "${TIMESTAMP} - Heartbeat sent" >> /home/node/.openclaw/workspace/memory/evomap-heartbeat.log
