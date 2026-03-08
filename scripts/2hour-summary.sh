#!/bin/bash
# 2 小时学习总结脚本

echo "=== 2 小时学习总结 ==="
echo "时间：$(date)"
echo ""

# 统计今日文件
echo "📁 今日文件统计:"
TODAY=$(date +%Y-%m-%d)
TODAY_FILES=$(find /home/node/.openclaw/workspace -name "*${TODAY}*" -type f 2>/dev/null | wc -l)
echo "  今日创建文件：$TODAY_FILES 个"

# 统计项目进度
echo ""
echo "📊 项目进度统计:"
for dir in /home/node/.openclaw/workspace/projects/*/; do
    if [ -d "$dir" ]; then
        PROJECT_NAME=$(basename "$dir")
        FILES=$(find "$dir" -type f 2>/dev/null | wc -l)
        echo "  $PROJECT_NAME: $FILES 个文件"
    fi
done

# 统计技能
echo ""
echo "🛠️ 技能统计:"
SKILLS=$(ls -d /home/node/.openclaw/workspace/skills/*/ 2>/dev/null | wc -l)
echo "  技能目录：$SKILLS 个"

# 统计知识库
echo ""
echo "📚 知识库统计:"
KB_FILES=$(ls /home/node/.openclaw/workspace/knowledge_base/*.md 2>/dev/null | wc -l)
echo "  知识库文件：$KB_FILES 个"

echo ""
echo "🚀 继续执行！"
