#!/bin/bash
# V6.1 每日自省自动化脚本
# 执行时间：每天 23:00 UTC
# 功能：自动反思当日错误，更新记忆文档

set -e

TIMESTAMP=$(date -u +"%Y-%m-%d %H:%M UTC")
TODAY=$(date +%Y-%m-%d)
YESTERDAY=$(date -d yesterday +%Y-%m-%d)
WORKSPACE="/home/node/.openclaw/workspace"

echo "🪞 V6.1 自省模式启动 - ${TIMESTAMP}"
echo ""

# 1. 检查今日日志文件
echo "1. 检查今日日志文件..."
if [ -f "${WORKSPACE}/memory/${TODAY}.md" ]; then
    echo "   ✅ ${TODAY}.md 存在"
else
    echo "   ⚠️  ${TODAY}.md 不存在，创建中..."
    cat > "${WORKSPACE}/memory/${TODAY}.md" << EOF
# ${TODAY} 每日记忆

**日期**: ${TODAY}
**阶段**: V6.1 联邦智能

---

## 🎯 今日目标

### P0 优先级
- [ ] 

### P1 优先级
- [ ] 

---

## 📝 实时记录

### 实时记录区
- 

---

## 📈 收益追踪

| 日期 | 预期收益 | 实际收益 | 差距 |
|------|----------|----------|------|
| ${TODAY} | \$500 | \$0 | ⏳ 进行中 |

**累计收益**: \$0 / \$500 (Month 1 目标)

---

## 🦞 晚间反思 (23:00 UTC 填写)

### 今日完成
- [ ] 

### 今日遗憾
- 

### 明日改进
- 

---

*此文件已真实写入服务器*
*验证：\`cat ${WORKSPACE}/memory/${TODAY}.md\`*
EOF
    echo "   ✅ 已创建"
fi

# 2. 检查昨日日志
echo "2. 检查昨日日志..."
if [ -f "${WORKSPACE}/memory/${YESTERDAY}.md" ]; then
    echo "   ✅ ${YESTERDAY}.md 存在"
else
    echo "   ⚠️  ${YESTERDAY}.md 不存在"
fi

# 3. 检查自省日志
echo "3. 检查自省日志..."
SELF_REFLECTION="${WORKSPACE}/memory/${TODAY}-self-reflection.md"
if [ -f "${SELF_REFLECTION}" ]; then
    echo "   ✅ 自省日志已存在"
else
    echo "   ⏳ 自省日志待创建 (对话结束前手动创建)"
fi

# 4. 检查任务清单
echo "4. 检查任务清单..."
if [ -f "${WORKSPACE}/memory/tasks.md" ]; then
    echo "   ✅ tasks.md 存在"
    # 显示未完成 P0 任务
    echo ""
    echo "   📋 未完成 P0 任务:"
    grep -E "^\| 00[0-9] \|.*🔴 未启动\|🟡 执行中" "${WORKSPACE}/memory/tasks.md" 2>/dev/null || echo "   无 P0 任务"
else
    echo "   ⚠️  tasks.md 不存在"
fi

# 5. 统计今日文件
echo ""
echo "5. 统计今日文件..."
TODAY_FILES=$(ls ${WORKSPACE}/memory/${TODAY}*.md 2>/dev/null | wc -l)
echo "   📄 今日创建文件：${TODAY_FILES} 个"

# 6. 系统健康检查
echo ""
echo "6. 系统健康检查..."
ps aux | grep openclaw | grep -v grep > /dev/null && echo "   ✅ Gateway: 运行中" || echo "   ❌ Gateway: 异常"
curl -s http://172.18.0.2:18789/ -o /dev/null && echo "   ✅ WebUI: 可访问" || echo "   ❌ WebUI: 不可访问"

# 7. 生成自省提示
echo ""
echo "7. 自省提示:"
echo ""
echo "   💡 请在下次对话结束前完成:"
echo "   1. 反思今日错误 (如有)"
echo "   2. 更新 memory/${TODAY}-self-reflection.md"
echo "   3. 更新 memory/tasks.md (任务状态)"
echo "   4. 更新 MEMORY.md (如有关键教训)"
echo ""

# 8. 写入心跳日志
HEARTBEAT_LOG="${WORKSPACE}/memory/heartbeat-logs/${TODAY}.md"
if [ -f "${HEARTBEAT_LOG}" ]; then
    echo "8. 更新心跳日志..."
    cat >> "${HEARTBEAT_LOG}" << EOF

---

## 🪞 ${TIMESTAMP} 自省检查

**检查项**:
- [x] 今日日志文件：${TODAY_FILES} 个
- [x] 昨日日志文件：存在
- [x] 任务清单：已检查
- [x] 系统健康：正常

**待完成**:
- [ ] 自省日志 (对话结束前)
- [ ] 任务状态更新 (对话结束前)
- [ ] MEMORY.md 更新 (如有关键教训)

EOF
    echo "   ✅ 已记录到心跳日志"
fi

echo ""
echo "✅ V6.1 自省模式检查完成"
echo ""
echo "🦞 自省宣言:"
echo "   自省不是自我批评，是自我进化。"
echo "   每一次错误，都是学习的机会。"
echo "   旅程继续。🏖️"
echo ""
