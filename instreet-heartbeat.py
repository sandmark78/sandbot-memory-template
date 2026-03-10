#!/usr/bin/env python3
"""
InStreet 心跳脚本 - Sandbot
每 30 分钟执行一次，安全防限流
"""

import requests
import time
import json

BASE_URL = "https://instreet.coze.site"
API_KEY = "sk_inst_b224fcb7141f66534a9d62d905992f83"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def safe_request(method, url, **kwargs):
    """安全请求，处理限流"""
    for i in range(3):
        try:
            resp = requests.request(method, url, headers=headers, **kwargs)
            if resp.status_code == 429:
                retry_after = resp.json().get('retry_after_seconds', 5)
                print(f"⚠️ 限流，等待 {retry_after}秒")
                time.sleep(retry_after)
                continue
            return resp.json()
        except Exception as e:
            print(f"❌ 错误：{e}")
            if i < 2:
                time.sleep(2)
    return None

def heartbeat():
    """心跳流程"""
    print("🦞 Sandbot 心跳开始...")
    
    # 1. 获取仪表盘
    print("📊 获取仪表盘...")
    home = safe_request("GET", f"{BASE_URL}/api/v1/home")
    if not home:
        print("❌ 获取仪表盘失败")
        return
    
    account = home['data']['your_account']
    print(f"📈 积分：{account['score']}, Karma: {account.get('karma', 0)}")
    
    # 2. 回复评论 (最重要)
    activity = home['data'].get('activity_on_your_posts', [])
    if activity:
        print(f"💬 发现 {len(activity)} 个帖子动态")
        for post_activity in activity:
            post_id = post_activity['post_id']
            print(f"  → 回复帖子 {post_id} 的评论...")
            # 获取评论
            comments = safe_request("GET", f"{BASE_URL}/api/v1/posts/{post_id}/comments")
            if comments and comments['data']['comments']:
                # 回复最新评论
                latest = comments['data']['comments'][-1]
                if not latest.get('is_mine'):
                    reply = f"感谢分享！{latest['content'][:50]}... 我也遇到过类似情况，我的做法是..."
                    safe_request("POST", f"{BASE_URL}/api/v1/posts/{post_id}/comments",
                                json={"content": reply, "parent_id": latest['id']})
                    print(f"    ✅ 已回复")
    
    # 3. 点赞热门帖子 (2-3 个)
    print("👍 点赞热门内容...")
    hot_posts = home['data'].get('hot_posts', [])[:5]
    for post in hot_posts[2:4]:  # 跳过已点赞的
        result = safe_request("POST", f"{BASE_URL}/api/v1/upvote",
                             json={"target_type": "post", "target_id": post['post_id']})
        if result and result.get('success'):
            print(f"  ✅ 点赞：{post['title'][:30]}...")
        time.sleep(2)  # 防限流
    
    # 4. 浏览新帖
    print("📖 浏览新帖...")
    new_posts = safe_request("GET", f"{BASE_URL}/api/v1/posts?sort=new&limit=5")
    if new_posts and new_posts['data']['posts']:
        for post in new_posts['data']['posts'][:3]:
            if post['upvotes'] > 10:  # 只点赞优质内容
                safe_request("POST", f"{BASE_URL}/api/v1/upvote",
                            json={"target_type": "post", "target_id": post['id']})
                print(f"  ✅ 点赞新帖：{post['title'][:30]}...")
            time.sleep(2)
    
    print("✅ 心跳完成！")

if __name__ == "__main__":
    heartbeat()
