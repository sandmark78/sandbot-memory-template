#!/usr/bin/env python3
"""
Knowledge Retriever v1.0 - 132k 知识点检索系统
支持关键词搜索 + 领域过滤 + 智能排序
"""

import os
import re
import json
from pathlib import Path
from typing import List, Dict, Optional
import hashlib

class KnowledgeRetriever:
    def __init__(self, kb_path: str = "/home/node/.openclaw/workspace/knowledge_base"):
        self.kb_path = Path(kb_path)
        self.index = {}
        self.cache_file = Path("/tmp/knowledge_index.json")
        
    def build_index(self, force: bool = False):
        """构建知识索引"""
        if self.cache_file.exists() and not force:
            with open(self.cache_file, 'r') as f:
                self.index = json.load(f)
            return
        
        print("📚 构建知识索引...")
        self.index = {
            "files": {},
            "domains": {},
            "total_points": 0
        }
        
        # 扫描所有领域目录
        for domain_dir in self.kb_path.iterdir():
            if not domain_dir.is_dir():
                continue
            
            domain = domain_dir.name
            if domain.startswith('.'):
                continue
                
            self.index["domains"][domain] = {
                "files": [],
                "points": 0
            }
            
            # 扫描领域内所有文件
            for md_file in domain_dir.glob("*.md"):
                file_data = self._parse_file(md_file, domain)
                self.index["files"][str(md_file)] = file_data
                self.index["domains"][domain]["files"].append(str(md_file))
                self.index["domains"][domain]["points"] += file_data["points"]
                self.index["total_points"] += file_data["points"]
        
        # 缓存索引
        with open(self.cache_file, 'w') as f:
            json.dump(self.index, f, indent=2)
        
        print(f"✅ 索引构建完成：{self.index['total_points']} 知识点")
    
    def _parse_file(self, file_path: Path, domain: str) -> Dict:
        """解析 Markdown 文件，提取知识点"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 计算知识点数量 (### A 开头的标题)
        points = len(re.findall(r'^### A\d+', content, re.MULTILINE))
        
        # 提取关键词
        keywords = self._extract_keywords(content)
        
        return {
            "path": str(file_path),
            "domain": domain,
            "points": points,
            "keywords": keywords,
            "size": len(content)
        }
    
    def _extract_keywords(self, content: str) -> List[str]:
        """从内容中提取关键词"""
        # 提取所有### 标题作为关键词
        titles = re.findall(r'^### A\d+[-: ](.+)$', content, re.MULTILINE)
        
        # 提取高频词
        words = re.findall(r'[\u4e00-\u9fa5a-zA-Z]{2,}', content)
        word_count = {}
        for word in words:
            word_count[word] = word_count.get(word, 0) + 1
        
        # 返回标题 + 高频词
        keywords = list(set(titles + [w for w, c in word_count.items() if c > 3][:20]))
        return keywords[:50]  # 限制 50 个关键词
    
    def search(self, query: str, domain: Optional[str] = None, limit: int = 10) -> List[Dict]:
        """搜索知识点"""
        if not self.index:
            self.build_index()
        
        results = []
        query_lower = query.lower()
        
        # 搜索所有文件
        for file_path, file_data in self.index["files"].items():
            # 领域过滤
            if domain and file_data["domain"] != domain:
                continue
            
            # 关键词匹配
            score = 0
            matched_keywords = []
            
            for keyword in file_data["keywords"]:
                if query_lower in keyword.lower():
                    score += 1
                    matched_keywords.append(keyword)
            
            if score > 0:
                results.append({
                    "file": file_path,
                    "domain": file_data["domain"],
                    "score": score,
                    "matched_keywords": matched_keywords,
                    "points": file_data["points"]
                })
        
        # 按分数排序
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:limit]
    
    def get_domain_stats(self) -> Dict:
        """获取领域统计"""
        if not self.index:
            self.build_index()
        return self.index["domains"]
    
    def get_total_stats(self) -> Dict:
        """获取总体统计"""
        if not self.index:
            self.build_index()
        return {
            "total_files": len(self.index["files"]),
            "total_points": self.index["total_points"],
            "total_domains": len(self.index["domains"])
        }

def main():
    """命令行界面"""
    import sys
    
    retriever = KnowledgeRetriever()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 knowledge-retriever.py search <query> [domain] [limit]")
        print("  python3 knowledge-retriever.py stats")
        print("  python3 knowledge-retriever.py build-index")
        return
    
    command = sys.argv[1]
    
    if command == "search":
        if len(sys.argv) < 3:
            print("Error: search query required")
            return
        
        query = sys.argv[2]
        domain = sys.argv[3] if len(sys.argv) > 3 else None
        limit = int(sys.argv[4]) if len(sys.argv) > 4 else 10
        
        results = retriever.search(query, domain, limit)
        
        print(f"\n🔍 搜索结果：'{query}'")
        print(f"找到 {len(results)} 个相关文件:\n")
        
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['file']}")
            print(f"   领域：{result['domain']}")
            print(f"   匹配度：{result['score']}")
            print(f"   知识点：{result['points']}")
            if result['matched_keywords']:
                print(f"   匹配关键词：{', '.join(result['matched_keywords'][:5])}")
            print()
    
    elif command == "stats":
        stats = retriever.get_total_stats()
        print(f"\n📊 知识库统计:")
        print(f"  总文件：{stats['total_files']}")
        print(f"  总知识点：{stats['total_points']:,}")
        print(f"  领域数：{stats['total_domains']}")
        
        print(f"\n📁 领域分布:")
        domain_stats = retriever.get_domain_stats()
        for domain, data in sorted(domain_stats.items(), key=lambda x: x[1]['points'], reverse=True):
            print(f"  {domain}: {data['points']:,} 知识点 ({len(data['files'])} 文件)")
    
    elif command == "build-index":
        retriever.build_index(force=True)
        print("✅ 索引重建完成")

if __name__ == "__main__":
    main()
