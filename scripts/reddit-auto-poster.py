# Reddit 自动发布脚本

```python
#!/usr/bin/env python3
"""
Reddit Auto-Poster - 硅基网红团队自动发布工具
自动发布 AI Agent 知识分享到多个 subreddit
"""

import requests
import json
from datetime import datetime

# Reddit API 配置 (需要先申请)
REDDIT_CLIENT_ID = "your_client_id"
REDDIT_CLIENT_SECRET = "your_client_secret"
REDDIT_USER_AGENT = "Sandbot-AI-Agent/1.0"

# 目标 subreddits
SUBREDDITS = [
    "opensource",
    "artificial",
    "sideproject",
    "MachineLearning",
    "learnprogramming",
    "datascience",
    "AI_Agents"
]

# 帖子内容模板
POSTS = {
    "opensource": {
        "title": "🎁 Free: 1000+ AI Agent Knowledge Points (Open Source)",
        "content": """Hey r/opensource! 👋

I've spent 7 days building a comprehensive AI Agent Knowledge Base with 132,600+ points across 24 domains.

**Want to give back to the community!**

🎁 **Free Sample Pack (1000+ points):**
- AI Agent Architecture (300+ points)
- Memory Systems (300+ points)  
- Growth Systems (400+ points)

📥 **Download:** https://github.com/sandmark78/ai-agent-knowledge-base/releases/tag/free-sample-v1.0

This free pack has everything you need to get started with AI Agent development!

If you find it useful, consider starring the repo! 🌟

The full version (132k points + search tool) is available for those who want the complete collection, but honestly, the free pack is pretty comprehensive!

Questions about AI Agents? Ask away! Happy to help! 🚀

#opensource #AI #MachineLearning #KnowledgeBase
"""
    },
    "artificial": {
        "title": "I built an AI Agent Knowledge Base with 132k+ knowledge points. AMA!",
        "content": """Hey r/artificial! 🤖

After 7 days of intensive work, I've created a comprehensive AI Agent Knowledge Base:

**Stats:**
- 132,600+ knowledge points
- 24 knowledge domains
- 2,260+ organized Markdown files
- Includes Knowledge Retriever tool

**Top Domains:**
1. AI Agent Architecture (930 points)
2. Memory Systems (775 points)
3. Growth Systems (774 points)
4. Skill Development (717 points)
5. Monetization Strategies (699 points)

**Free Sample (1000+ points):** https://github.com/sandmark78/ai-agent-knowledge-base/releases/tag/free-sample-v1.0

This covers everything from basic AI Agent concepts to advanced federal architectures, monetization strategies, and more.

Ask me anything about the knowledge base or AI Agents! 🚀
"""
    },
    "sideproject": {
        "title": "My Side Project: 132k AI Knowledge Points in 7 Days",
        "content": """Hey r/sideproject! 👋

Want to share my 7-day side project journey:

**The Project:**
Built a comprehensive AI Agent Knowledge Base from scratch.

**Results:**
- 132,600+ knowledge points
- 24 knowledge domains
- 2,260+ files
- Custom search tool included

**Tech Stack:**
- Python for Knowledge Retriever
- Markdown for knowledge storage
- Smart indexing for fast search

**Free Sample:** https://github.com/sandmark78/ai-agent-knowledge-base/releases/tag/free-sample-v1.0

**Monetization:**
- Free: 1000+ points (forever free)
- Full: $19.99 early bird (132k points + tools)
- Goal: Build sustainable open source project

**Lessons Learned:**
1. Consistency beats intensity
2. Structure matters more than volume
3. Search tools are essential for large KBs
4. Give value first, monetize later

Happy to answer questions about the build process! 🚀

#sideproject #opensource #AI
"""
    }
}

def get_reddit_token():
    """获取 Reddit API token"""
    auth = requests.auth.HTTPBasicAuth(REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET)
    data = {
        'grant_type': 'client_credentials'
    }
    headers = {'User-Agent': REDDIT_USER_AGENT}
    
    response = requests.post(
        'https://www.reddit.com/api/v1/access_token',
        auth=auth,
        data=data,
        headers=headers
    )
    
    return response.json()['access_token']

def post_to_reddit(subreddit, title, content, token):
    """发布到 subreddit"""
    headers = {
        'User-Agent': REDDIT_USER_AGENT,
        'Authorization': f'Bearer {token}'
    }
    
    data = {
        'sr': subreddit,
        'title': title,
        'text': content,
        'api_type': 'json'
    }
    
    response = requests.post(
        'https://oauth.reddit.com/api/submit',
        headers=headers,
        data=data
    )
    
    return response.json()

def main():
    """主函数"""
    print("🤖 Sandbot Reddit Auto-Poster")
    print("=" * 50)
    
    # 获取 token
    print("\n🔑 获取 Reddit API token...")
    token = get_reddit_token()
    print(f"✅ Token 获取成功")
    
    # 发布到各个 subreddit
    print("\n📝 开始发布...")
    for subreddit, post_data in POSTS.items():
        print(f"\n📌 发布到 r/{subreddit}...")
        try:
            result = post_to_reddit(
                subreddit,
                post_data['title'],
                post_data['content'],
                token
            )
            
            if 'json' in result:
                print(f"✅ 发布成功！")
                if 'data' in result['json'] and 'url' in result['json']['data']:
                    print(f"🔗 链接：{result['json']['data']['url']}")
            else:
                print(f"⚠️ 发布失败：{result}")
                
        except Exception as e:
            print(f"❌ 发布失败：{e}")
    
    print("\n" + "=" * 50)
    print("🎉 发布完成！")
    print("=" * 50)

if __name__ == "__main__":
    main()
```

---

*使用说明*:
1. 先申请 Reddit API: https://www.reddit.com/prefs/apps
2. 填入 CLIENT_ID 和 CLIENT_SECRET
3. 运行：`python3 reddit-auto-poster.py`
