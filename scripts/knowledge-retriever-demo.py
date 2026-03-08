#!/usr/bin/env python3
"""
🤖 OpenClaw Knowledge Retriever Demo
从 411k 知识点中即时检索有价值的内容
"""

import os
import re
import json
from pathlib import Path

KB_PATH = Path("/home/node/.openclaw/workspace/knowledge_base")

def search_knowledge(query, limit=5):
    """搜索知识库"""
    results = []
    for md_file in KB_PATH.rglob("*.md"):
        try:
            content = md_file.read_text()[:5000]
            if query.lower() in content.lower():
                # 提取相关段落
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if query.lower() in line.lower():
                        results.append({
                            'file': str(md_file.relative_to(KB_PATH)),
                            'line': i + 1,
                            'content': line.strip()[:200]
                        })
                        if len(results) >= limit:
                            return results
        except:
            pass
    return results

def get_knowledge_stats():
    """获取知识库统计"""
    files = list(KB_PATH.rglob("*.md"))
    total_size = sum(f.stat().st_size for f in files)
    domains = len([d for d in KB_PATH.iterdir() if d.is_dir()])
    
    # 估算知识点
    points = 0
    for f in files:
        try:
            content = f.read_text()
            points += len(re.findall(r'^### A\d+-', content, re.MULTILINE))
        except:
            pass
    
    return {
        'files': len(files),
        'size_mb': round(total_size / 1024 / 1024, 2),
        'domains': domains,
        'knowledge_points': points
    }

if __name__ == "__main__":
    print("🤖 OpenClaw Knowledge Retriever Demo")
    print("=" * 50)
    
    stats = get_knowledge_stats()
    print(f"\n📊 知识库统计:")
    print(f"   文件数：{stats['files']}")
    print(f"   大小：{stats['size_mb']} MB")
    print(f"   领域数：{stats['domains']}")
    print(f"   知识点：{stats['knowledge_points']}")
    
    print(f"\n🔍 示例搜索：'ROI'")
    results = search_knowledge("ROI", limit=3)
    for r in results:
        print(f"\n   📄 {r['file']}:{r['line']}")
        print(f"   💡 {r['content']}")
    
    print("\n" + "=" * 50)
    print("✅ 知识库可立即使用！")
