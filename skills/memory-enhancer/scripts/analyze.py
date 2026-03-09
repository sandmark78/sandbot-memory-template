#!/usr/bin/env python3
"""
Memory Enhancer - 关联分析脚本

功能:
- 提取共现词
- 构建关联图
- 发现隐藏模式
- 生成洞察报告

使用:
python3 analyze.py
"""

import json
from pathlib import Path
from collections import Counter
from datetime import datetime

WORKSPACE = Path("/home/node/.openclaw/workspace")
MEMORY_DIR = WORKSPACE / "memory"
KB_DIR = WORKSPACE / "knowledge_base"

# 停用词
STOP_WORDS = {"the", "a", "an", "is", "are", "was", "were", "be", "been", "being", 
              "have", "has", "had", "do", "does", "did", "will", "would", "could", 
              "should", "may", "might", "must", "shall", "can", "need", "dare", 
              "ought", "used", "to", "of", "in", "for", "on", "with", "at", "by", 
              "from", "as", "into", "through", "during", "before", "after", "above", 
              "below", "between", "under", "again", "further", "then", "once", "和", "的", "了", "在", "是", "我", "有", "就", "不", "人", "都", "一", "就", "这", "那", "他", "她", "它"}

def extract_keywords(text, top_n=20):
    """提取关键词"""
    words = text.lower().split()
    words = [w for w in words if w not in STOP_WORDS and len(w) > 2]
    return Counter(words).most_common(top_n)

def analyze_connections():
    """分析记忆关联"""
    print("🔗 记忆关联分析")
    print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 读取今日文件
    today = datetime.now().strftime("%Y-%m-%d")
    all_keywords = []
    
    for file in MEMORY_DIR.glob("*.md"):
        if today in str(file):
            with open(file, 'r') as f:
                content = f.read()
                keywords = extract_keywords(content, 10)
                all_keywords.extend([kw for kw, _ in keywords])
    
    # 统计共现
    keyword_freq = Counter(all_keywords)
    top_keywords = keyword_freq.most_common(20)
    
    print("Top 20 关键词:")
    for i, (kw, freq) in enumerate(top_keywords, 1):
        print(f"  {i:2}. {kw}: {freq}次")
    
    print()
    print("💡 洞察:")
    print(f"  - 今日焦点：{top_keywords[0][0] if top_keywords else 'N/A'}")
    print(f"  - 关键词数量：{len(keyword_freq)}个")
    print(f"  - 平均频率：{sum(keyword_freq.values()) / len(keyword_freq):.1f}次")

if __name__ == "__main__":
    analyze_connections()
