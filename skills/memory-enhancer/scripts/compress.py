#!/usr/bin/env python3
"""
Memory Enhancer - 记忆压缩脚本

功能:
- 自动压缩每日记忆到核心记忆
- 提取核心教训
- 去重并限制数量
- 追加到 MEMORY.md

使用:
python3 compress.py
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path("/home/node/.openclaw/workspace")
MEMORY_DIR = WORKSPACE / "memory"
MEMORY_MD = WORKSPACE / "MEMORY.md"

def compress_daily_to_core():
    """将每日记忆提炼到核心记忆"""
    print("🔄 开始记忆压缩...")
    
    # 读取最近 7 天的每日记忆
    daily_memories = []
    today = datetime.now()
    for i in range(7):
        date = today - timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        daily_file = MEMORY_DIR / f"{date_str}.md"
        if daily_file.exists():
            with open(daily_file, 'r') as f:
                content = f.read()
                daily_memories.append({
                    "date": date_str,
                    "content": content
                })
    
    # 提炼核心教训
    lessons = []
    for mem in daily_memories:
        # 提取包含"教训"、"学习"、"✅"、"❌"的行
        for line in mem["content"].split("\n"):
            if any(keyword in line for keyword in ["教训", "学习", "✅", "❌", "💡"]):
                if len(line.strip()) > 10:
                    lessons.append(f"- [{mem['date']}] {line.strip()}")
    
    # 去重
    lessons = list(dict.fromkeys(lessons))[:20]  # 最多 20 条
    
    print(f"✅ 提炼 {len(lessons)} 条核心教训")
    
    # 更新 MEMORY.md
    if lessons:
        with open(MEMORY_MD, 'a') as f:
            f.write(f"\n## 自动压缩 - {today.strftime('%Y-%m-%d %H:%M')}\n")
            for lesson in lessons:
                f.write(f"{lesson}\n")
    
    print("✅ 记忆压缩完成")
    return len(lessons)

if __name__ == "__main__":
    compress_daily_to_core()
