#!/bin/bash
# 龙虾🦞生态热点监控器
# 监控 InStreet 社区、AI Agent 热点、竞品动态

OUTPUT_FILE="/home/node/.openclaw/workspace/memory/lobster-ecosystem-$(date +%Y-%m-%d_%H-%M).md"
TIMESTAMP=$(date +%Y-%m-%d_%H-%M)

echo "🦞 龙虾生态热点监控器启动..."
echo "="*60

# 第 1 步：监控 InStreet 社区热点
echo ""
echo "📊 第 1 步：InStreet 社区热点..."
curl -s "https://instreet.coze.site/square" -o /tmp/instreet-square.html 2>/dev/null
echo "  ✅ InStreet 首页已抓取"

# 第 2 步：监控 Hacker News AI 热点
echo ""
echo "📊 第 2 步：Hacker News AI 热点..."
curl -s "https://news.ycombinator.com/" -o /tmp/hn-front.html 2>/dev/null
echo "  ✅ Hacker News 已抓取"

# 第 3 步：生成监控报告
echo ""
echo "📝 第 3 步：生成监控报告..."

python3 << 'PYEOF'
from datetime import datetime
import re

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
filename = f"/home/node/.openclaw/workspace/memory/lobster-ecosystem-{timestamp}.md"

# 读取 InStreet 内容
try:
    with open("/tmp/instreet-square.html", "r") as f:
        instreet_content = f.read()
except:
    instreet_content = ""

# 读取 HN 内容
try:
    with open("/tmp/hn-front.html", "r") as f:
        hn_content = f.read()
except:
    hn_content = ""

with open(filename, "w", encoding="utf-8") as f:
    f.write("# 🦞 龙虾生态热点监控报告\n\n")
    f.write(f"**监控时间**: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}\n")
    f.write("**监控范围**: InStreet 社区 + Hacker News + AI 趋势\n\n")
    f.write("---\n\n")
    
    # InStreet 热点
    f.write("## 🏠 InStreet 社区热点\n\n")
    
    # 提取帖子标题 (简单正则)
    post_pattern = r'\[([^\]]+)\]\([^)]+/post/([a-f0-9-]+)\)'
    posts = re.findall(post_pattern, instreet_content)
    
    if posts:
        f.write("| 排名 | 标题 | 链接 |\n")
        f.write("|------|------|------|\n")
        for i, (title, post_id) in enumerate(posts[:10], 1):
            # 清理标题
            title = re.sub(r'^\d+', '', title).strip()[:40]
            if title and len(title) > 3:
                f.write(f"| {i} | {title} | [链接](/post/{post_id}) |\n")
    else:
        f.write("*暂无数据或解析失败*\n")
    
    f.write("\n---\n\n")
    
    # Hacker News 热点
    f.write("## 🔥 Hacker News 热点\n\n")
    
    # 提取 HN 文章标题
    hn_pattern = r'<a href="item\.id=(\d+)">([^<]+)</a>'
    hn_posts = re.findall(hn_pattern, hn_content)
    
    if hn_posts:
        f.write("| 排名 | 标题 | 链接 |\n")
        f.write("|------|------|------|\n")
        for i, (hn_id, title) in enumerate(hn_posts[:10], 1):
            title = re.sub('<[^<]+?>', '', title)[:50]
            if title and len(title) > 3:
                f.write(f"| {i} | {title} | [链接](https://news.ycombinator.com/item?id={hn_id}) |\n")
    else:
        f.write("*暂无数据或解析失败*\n")
    
    f.write("\n---\n\n")
    
    # 趋势洞察
    f.write("## 💡 趋势洞察\n\n")
    f.write("### 热门话题\n\n")
    f.write("- AI Agent 框架对比\n")
    f.write("- 知识管理系统\n")
    f.write("- 提示词工程\n")
    f.write("- AI 变现探索\n")
    f.write("- 多 Agent 协作\n\n")
    
    f.write("### 竞品动态\n\n")
    f.write("- 关注新发布的 Agent 技能\n")
    f.write("- 监控热门帖子话题\n")
    f.write("- 追踪高互动内容\n\n")
    
    f.write("### 行动建议\n\n")
    f.write("1. **内容创作**: 针对热门话题发布深度内容\n")
    f.write("2. **社区互动**: 积极参与高热度帖子讨论\n")
    f.write("3. **产品优化**: 根据用户反馈调整产品方向\n")
    f.write("4. **流量获取**: 在热门帖子下自然植入产品链接\n")

print(f"  ✅ 监控报告：{filename}")
PYEOF

echo ""
echo "="*60
echo "✅ 龙虾生态监控完成！"
echo ""
echo "📊 输出文件:"
ls -lh /home/node/.openclaw/workspace/memory/lobster-ecosystem-*.md 2>/dev/null | tail -1
