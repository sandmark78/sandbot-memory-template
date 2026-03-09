#!/usr/bin/env python3
"""
🤖 OpenClaw 知识检索工具 v2.0
从 411k 知识点中快速检索有价值的内容
"""

import os
import re
import sys
from pathlib import Path

KB_PATH = Path("/home/node/.openclaw/workspace/knowledge_base")

# 24 领域映射
DOMAINS = {
    "01": "AI Agent",
    "02": "OpenClaw",
    "03": "Federal System",
    "04": "Skill Dev",
    "05": "Memory",
    "06": "Growth",
    "07": "Community",
    "08": "Monetization",
    "09": "Security",
    "10": "Automation",
    "11": "Content",
    "12": "Tools",
    "13": "Blockchain",
    "14": "IoT",
    "15": "Cloud",
    "16": "DevOps",
    "17": "ML",
    "18": "NLP",
    "19": "CV",
    "20": "Robotics",
    "21": "Edge",
    "22": "Quantum",
    "23": "Bio",
    "24": "Finance"
}

def search_knowledge(query, domain=None, limit=10):
    """搜索知识库"""
    results = []
    
    if domain:
        search_paths = [KB_PATH / f"{domain}-{domain}"]
    else:
        search_paths = [KB_PATH / d for d in os.listdir(KB_PATH) if (KB_PATH / d).is_dir()]
    
    for path in search_paths:
        if not path.exists():
            continue
        for md_file in path.glob("*.md"):
            if md_file.name == "INDEX.md":
                continue
            try:
                content = md_file.read_text()[:10000]
                if query.lower() in content.lower():
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
            except Exception as e:
                pass
    return results

def get_knowledge_stats():
    """获取知识库统计"""
    files = list(KB_PATH.rglob("*.md"))
    total_size = sum(f.stat().st_size for f in files if f.is_file())
    domains = len([d for d in KB_PATH.iterdir() if d.is_dir()])
    
    # 估算知识点
    points = 0
    for f in files:
        if f.name == "INDEX.md":
            continue
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

def list_domains():
    """列出所有领域"""
    print("\n📚 24 知识领域:\n")
    for code, name in DOMAINS.items():
        domain_path = KB_PATH / f"{code}-{name.lower().replace(' ', '-')}"
        file_count = len(list(domain_path.glob("*.md"))) if domain_path.exists() else 0
        print(f"  {code}. {name:15} ({file_count} files)")

if __name__ == "__main__":
    print("🤖 OpenClaw Knowledge Retriever v2.0")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--domains":
            list_domains()
        elif sys.argv[1] == "--stats":
            stats = get_knowledge_stats()
            print(f"\n📊 知识库统计:")
            print(f"   文件数：{stats['files']}")
            print(f"   大小：{stats['size_mb']} MB")
            print(f"   领域数：{stats['domains']}")
            print(f"   知识点：{stats['knowledge_points']}")
        else:
            query = " ".join(sys.argv[1:])
            print(f"\n🔍 搜索：'{query}'")
            results = search_knowledge(query, limit=10)
            if results:
                print(f"\n找到 {len(results)} 条结果:\n")
                for r in results:
                    print(f"   📄 {r['file']}:{r['line']}")
                    print(f"   💡 {r['content']}\n")
            else:
                print("\n❌ 未找到结果")
    else:
        stats = get_knowledge_stats()
        print(f"\n📊 知识库统计:")
        print(f"   文件数：{stats['files']}")
        print(f"   大小：{stats['size_mb']} MB")
        print(f"   领域数：{stats['domains']}")
        print(f"   知识点：{stats['knowledge_points']}")
        print(f"\n💡 使用示例:")
        print(f"   python3 {sys.argv[0]} --domains  # 列出所有领域")
        print(f"   python3 {sys.argv[0]} --stats    # 显示统计")
        print(f"   python3 {sys.argv[0]} ROI        # 搜索关键词")
        print(f"\n🏖️ 411k 知识点，24 领域，随时可用！")
