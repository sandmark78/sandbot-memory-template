#!/bin/bash
# 晨间启动脚本 - 修复版 (分割长消息)

MESSAGE_MAX_LENGTH=3500  # Telegram 限制 4096，留余量

# 生成简报内容
generate_briefing() {
    echo "☀️ 晨间启动 - $(date '+%Y-%m-%d %H:%M UTC')"
    echo ""
    echo "📊 今日重点:"
    echo "1. 知识变现推进"
    echo "2. 社区互动维持"
    echo "3. 技能发布完成"
    echo ""
    echo "🎯 优先级:"
    echo "P0: Gumroad 破零"
    echo "P1: ClawHub 5/5"
    echo "P2: Reddit 引流"
}

# 分割并发送消息
send_split_message() {
    local message="$1"
    local len=${#message}
    
    if [ $len -le $MESSAGE_MAX_LENGTH ]; then
        echo "$message"
    else
        # 分割成多条
        local part1="${message:0:$MESSAGE_MAX_LENGTH}"
        local part2="${message:$MESSAGE_MAX_LENGTH}"
        echo "$part1"
        echo "---"
        echo "$part2"
    fi
}

# 主逻辑
briefing=$(generate_briefing)
send_split_message "$briefing"

echo ""
echo "✅ 晨间启动完成 ($(date '+%H:%M UTC'))"
