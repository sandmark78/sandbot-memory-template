#!/usr/bin/env python3
"""Index Generator - 自动生成知识索引"""

import argparse
import os
import re
from pathlib import Path
from datetime import datetime

def scan_domain(domain_dir):
    """扫描领域目录"""
    files = []
    total_points = 0
    
    for filepath in sorted(Path(domain_dir).glob('*.md')):
        if filepath.name.startswith('INDEX'):
            continue  # 跳过索引文件
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 统计知识点数量
        points = len(re.findall(r'^### A\d+-\d+:', content, re.MULTILINE))
        total_points += points
        
        # 提取知识点范围
        match = re.search(r'A(\d+)-(\d+)', filepath.name)
        start = match.group(1) if match else '?'
        end = match.group(2) if match else '?'
        
        files.append({
            'name': filepath.name,
            'points': points,
            'size': os.path.getsize(filepath),
            'range': f"A{start}-{end}"
        })
    
    return {
        'files': files,
        'total_points': total_points,
        'file_count': len(files)
    }

def generate_domain_index(domain, stats):
    """生成领域索引"""
    index = f"# {domain} 知识索引\n\n"
    index += f"**领域**: {domain}\n"
    index += f"**知识点总数**: {stats['total_points']}\n"
    index += f"**文件数**: {stats['file_count']}\n"
    index += f"**最后更新**: {datetime.now().strftime('%Y-%m-%d')}\n\n"
    
    index += "## 文件列表\n"
    index += "| 文件 | 知识点范围 | 知识点数 | 大小 |\n"
    index += "|------|-----------|---------|------|\n"
    
    for f in stats['files']:
        size_kb = f['size'] / 1024
        index += f"| {f['name']} | {f['range']} | {f['points']} | {size_kb:.1f}KB |\n"
    
    return index

def generate_global_index(knowledge_base_dir):
    """生成总索引"""
    domains = {}
    total_points = 0
    
    # 扫描所有领域
    for domain_dir in sorted(Path(knowledge_base_dir).iterdir()):
        if not domain_dir.is_dir():
            continue
        if domain_dir.name.startswith('23_articles') or domain_dir.name.startswith('{'):
            continue
        
        stats = scan_domain(str(domain_dir))
        if stats['total_points'] > 0:
            domains[domain_dir.name] = stats
            total_points += stats['total_points']
    
    # 生成总索引
    index = f"# V6.4 知识体系总索引 (10000 知识点)\n\n"
    index += f"**版本**: V6.4.0\n"
    index += f"**最后更新**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    index += f"**目标**: 10000 知识点\n"
    index += f"**当前**: {total_points}/10000 ({total_points/100:.1f}%)\n"
    index += f"**领域数**: {len(domains)}\n\n"
    
    index += "## 知识领域分布\n\n"
    index += "| 领域 | 文件数 | 知识点数 | 进度 |\n"
    index += "|------|--------|---------|------|\n"
    
    for domain_name in sorted(domains.keys()):
        stats = domains[domain_name]
        progress = (stats['total_points'] / 10000) * 100
        index += f"| {domain_name} | {stats['file_count']} | {stats['total_points']} | {progress:.1f}% |\n"
    
    index += f"| **总计** | {sum(s['file_count'] for s in domains.values())} | {total_points} | {total_points/100:.1f}% |\n"
    
    index += "\n## 详细说明\n\n"
    index += "每个领域的详细索引请参考对应目录下的 INDEX.md 文件。\n"
    
    return index

def main():
    parser = argparse.ArgumentParser(description='生成知识索引')
    parser.add_argument('--domain', help='单个领域 ID')
    parser.add_argument('--all', action='store_true', help='生成所有领域索引')
    parser.add_argument('--global', dest='global_index', action='store_true', help='生成总索引')
    parser.add_argument('--output', help='输出文件路径')
    parser.add_argument('--format', default='markdown', help='索引格式 (markdown/json)')
    
    args = parser.parse_args()
    
    kb_dir = "/home/node/.openclaw/workspace/knowledge_base/"
    
    if args.domain:
        # 生成单个领域索引
        domain_dir = os.path.join(kb_dir, args.domain)
        if not os.path.exists(domain_dir):
            print(f"❌ 领域目录不存在：{domain_dir}")
            return
        
        stats = scan_domain(domain_dir)
        index = generate_domain_index(args.domain, stats)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(index)
            print(f"✅ 索引已保存到：{args.output}")
        else:
            output_file = os.path.join(domain_dir, 'INDEX.md')
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(index)
            print(f"✅ 索引已保存到：{output_file}")
            print(f"📊 {args.domain}: {stats['total_points']} 知识点，{stats['file_count']} 个文件")
    
    elif args.all:
        # 生成所有领域索引
        print("🚀 生成所有领域索引...")
        for domain_dir in sorted(Path(kb_dir).iterdir()):
            if not domain_dir.is_dir():
                continue
            if domain_dir.name.startswith('23_articles') or domain_dir.name.startswith('{'):
                continue
            
            stats = scan_domain(str(domain_dir))
            if stats['total_points'] > 0:
                index = generate_domain_index(domain_dir.name, stats)
                output_file = os.path.join(domain_dir, 'INDEX.md')
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(index)
                print(f"✅ {domain_dir.name}: {stats['total_points']} 知识点")
    
    elif args.global_index:
        # 生成总索引
        print("🚀 生成总索引...")
        index = generate_global_index(kb_dir)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(index)
            print(f"✅ 总索引已保存到：{args.output}")
        else:
            output_file = os.path.join(kb_dir, 'INDEX-10000.md')
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(index)
            print(f"✅ 总索引已保存到：{output_file}")
    
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
