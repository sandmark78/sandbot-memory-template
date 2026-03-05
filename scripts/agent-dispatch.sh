#!/bin/bash
# 子 Agent 任务分配脚本 - V1.0

AGENT=$1
TASK=$2
DATE=$(date +%Y-%m-%d)
TIME=$(date '+%H:%M:%S')

if [ -z "$AGENT" ] || [ -z "$TASK" ]; then
    echo "用法：$0 <agent> <task>"
    echo "示例：$0 techbot '编写 ClawHub 技能发布教程'"
    exit 1
fi

# 创建任务文件
TASK_FILE="/home/node/.openclaw/workspace/memory/agent-tasks/${AGENT}-${DATE}-$(echo $TASK | md5sum | cut -c1-8).md"

cat > $TASK_FILE << EOF
# ${AGENT^} 任务 - $DATE

**任务**: $TASK
**状态**: 🟡 执行中
**创建时间**: $TIME
**完成时间**: 待填写

---

## 执行记录
- [ ] 任务接收
- [ ] 执行中
- [ ] 完成

## 输出
待填写...

## 验证
- [ ] 文件已创建
- [ ] 内容已验证
- [ ] 已提交 Git
EOF

echo "✅ ${AGENT^} 任务已分配：$TASK"
echo "📁 任务文件：$TASK_FILE"
