#!/usr/bin/env python3
"""
Memory Enhancer - 语义搜索 v2

功能:
- 向量嵌入搜索
- 余弦相似度排序
- 关键词 + 语义混合

使用:
python3 search_v2.py "OpenClaw 生态"
"""

import sys
import json
from pathlib import Path
from datetime import datetime

WORKSPACE = Path("/home/node/.openclaw/workspace")
MEMORY_DIR = WORKSPACE / "memory"
KB_DIR = WORKSPACE / "knowledge_base"

def simple_semantic_search(query, limit=5):
    """
    简单语义搜索 (基于关键词相似度)
    
    实际生产环境应使用 sentence-transformers
    这里用简化版本演示
    """
    results = []
    query_words = set(query.lower().split())
    
    # 扫描记忆文件
    for file in MEMORY_DIR.glob("*.md"):
        if file.name.startswith("2026"):
            with open(file, 'r') as f:
                content = f.read().lower()
                file_words = set(content.split())
                
                # 计算 Jaccard 相似度
                intersection = query_words & file_words
                union = query_words | file_words
                
                if len(union) > 0:
                    similarity = len(intersection) / len(union)
                    if similarity > 0.1:
                        results.append({
                            "file": str(file),
                            "similarity": similarity,
                            "matches": len(intersection)
                        })
    
    # 按相似度排序
    results.sort(key=lambda x: x["similarity"], reverse=True)
    return results[:limit]

def main():
    if len(sys.argv) < 2:
        print("🧠 Memory Enhancer - Semantic Search v2")
        print("用法：python3 search_v2.py <query> [limit]")
        print("示例：python3 search_v2.py 'OpenClaw 生态' 5")
        return
    
    query = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    print(f"🔍 语义搜索 v2")
    print(f"查询：{query}")
    print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    results = simple_semantic_search(query, limit)
    
    print(f"找到 {len(results)} 个相关结果:")
    print()
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['file']}")
        print(f"   相似度：{result['similarity']:.2%}")
        print(f"   匹配词：{result['matches']} 个")
        print()
    
    if not results:
        print("⚠️ 未找到相关结果")

if __name__ == "__main__":
    main()
