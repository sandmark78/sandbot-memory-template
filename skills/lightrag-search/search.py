#!/usr/bin/env python3
"""
LightRAG-Style 知识检索工具
零依赖，使用 OpenClaw 原生工具 + 本地命令

用法:
    python search.py <query> [mode]
    mode: keyword (默认) | hybrid | stats
"""

import os
import subprocess
import json
import sys

KB_PATH = "/home/node/.openclaw/workspace/knowledge_base"

def keyword_search(query, max_results=10):
    """
    关键词搜索 (类似 LightRAG 的细粒度检索)
    使用 grep 在知识库中搜索
    """
    results = []
    
    # 使用 grep 递归搜索
    cmd = [
        "grep", "-r", "-n", "-i",
        "--include=*.md",
        query,
        KB_PATH
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        lines = result.stdout.strip().split("\n") if result.stdout.strip() else []
        
        for line in lines[:max_results]:
            if ":" in line:
                parts = line.split(":", 2)
                if len(parts) >= 3:
                    file_path = parts[0]
                    line_num = parts[1]
                    content = parts[2] if len(parts) > 2 else ""
                    results.append({
                        "type": "keyword",
                        "file": file_path,
                        "line": int(line_num),
                        "content": content[:300],  # 截断过长内容
                        "relevance": "exact_match"
                    })
    except Exception as e:
        results.append({"error": str(e)})
    
    return results

def get_knowledge_stats():
    """
    获取知识库统计信息
    """
    stats = {
        "total_files": 0,
        "total_size": "",
        "domains": []
    }
    
    try:
        # 统计文件数
        cmd = f"find {KB_PATH} -name '*.md' -type f | wc -l"
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        stats["total_files"] = int(result.stdout.strip()) if result.stdout.strip() else 0
        
        # 统计总大小
        result = subprocess.run(
            ["du", "-sh", KB_PATH],
            capture_output=True, text=True
        )
        if result.stdout.strip():
            stats["total_size"] = result.stdout.strip().split()[0]
        
        # 列出知识领域
        result = subprocess.run(
            ["ls", "-1", KB_PATH],
            capture_output=True, text=True
        )
        stats["domains"] = [d for d in result.stdout.strip().split("\n") if d and not d.endswith('.md')]
        
    except Exception as e:
        stats["error"] = str(e)
    
    return stats

def search_file_content(file_path, query, context_lines=2):
    """
    搜索特定文件并返回上下文
    """
    results = []
    
    if not os.path.exists(file_path):
        return [{"error": f"File not found: {file_path}"}]
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for i, line in enumerate(lines, 1):
            if query.lower() in line.lower():
                # 获取上下文
                start = max(0, i - context_lines - 1)
                end = min(len(lines), i + context_lines)
                context = "".join(lines[start:end])
                
                results.append({
                    "type": "context",
                    "file": file_path,
                    "line": i,
                    "context": context.strip()
                })
        
        return results
    except Exception as e:
        return [{"error": str(e)}]

def list_knowledge_domains():
    """
    列出所有知识领域及其文件数
    """
    domains = []
    
    try:
        for item in os.listdir(KB_PATH):
            item_path = os.path.join(KB_PATH, item)
            if os.path.isdir(item_path):
                # 统计该领域下的文件数
                file_count = len([f for f in os.listdir(item_path) if f.endswith('.md')])
                domains.append({
                    "name": item,
                    "files": file_count
                })
            elif item.endswith('.md'):
                domains.append({
                    "name": item,
                    "files": 1,
                    "type": "file"
                })
    except Exception as e:
        return [{"error": str(e)}]
    
    return sorted(domains, key=lambda x: x.get("files", 0), reverse=True)

def main():
    if len(sys.argv) < 2:
        print("用法：python search.py <query> [mode]")
        print("mode: keyword (默认) | hybrid | stats | domains")
        print("\n示例:")
        print("  python search.py '知识图谱' keyword  # 关键词搜索")
        print("  python search.py stats              # 查看统计")
        print("  python search.py domains            # 列出知识领域")
        sys.exit(1)
    
    arg1 = sys.argv[1]
    
    # stats 和 domains 模式不需要 query
    if arg1 == "stats":
        print(json.dumps(get_knowledge_stats(), indent=2, ensure_ascii=False))
        return
    elif arg1 == "domains":
        print(json.dumps(list_knowledge_domains(), indent=2, ensure_ascii=False))
        return
    
    query = arg1
    mode = sys.argv[2] if len(sys.argv) > 2 else "keyword"
    
    if mode == "keyword":
        results = keyword_search(query)
        print(json.dumps(results, indent=2, ensure_ascii=False))
    elif mode == "hybrid":
        # 混合模式 = 关键词 + 提示使用 memory_search
        keyword_results = keyword_search(query)
        print(json.dumps({
            "query": query,
            "keyword_results": keyword_results,
            "semantic_hint": "For semantic search, use OpenClaw memory_search tool with the same query"
        }, indent=2, ensure_ascii=False))
    else:
        print(f"未知模式：{mode}")
        print("可用模式：keyword, hybrid, stats, domains")
        sys.exit(1)

if __name__ == "__main__":
    main()
