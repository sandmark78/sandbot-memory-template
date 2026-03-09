#!/usr/bin/env python3
"""Knowledge Filler - 批量填充知识点"""

import argparse
import os
from datetime import datetime

def generate_knowledge_point(domain, number, template='compact'):
    """生成单个知识点"""
    point_id = f"A{domain}-{number:03d}"
    
    if template == 'compact':
        return f"""### {point_id}: 知识点标题
- **定义**: 一句话定义 (20 字)
- **核心**: 核心概念 (30 字)
- **应用**: 应用场景 (30 字)
- **参数**: 关键参数 (20 字)

"""
    elif template == 'standard':
        return f"""### {point_id}: 知识点标题

**定义**: 知识点的详细定义说明

**核心概念**: 
- 核心点 1
- 核心点 2
- 核心点 3

**应用场景**:
- 场景 1
- 场景 2

**关键参数**:
- 参数 1
- 参数 2

"""
    return ""

def main():
    parser = argparse.ArgumentParser(description='批量填充知识点')
    parser.add_argument('--domain', required=True, help='领域 ID')
    parser.add_argument('--start', type=int, required=True, help='起始编号')
    parser.add_argument('--end', type=int, required=True, help='结束编号')
    parser.add_argument('--output', help='输出目录')
    parser.add_argument('--template', default='compact', help='模板类型')
    parser.add_argument('--dry-run', action='store_true', help='试运行')
    
    args = parser.parse_args()
    
    # 确定输出目录
    if args.output:
        output_dir = args.output
    else:
        output_dir = f"/home/node/.openclaw/workspace/knowledge_base/{args.domain}/"
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 生成知识点
    content = f"# {args.domain} 知识点 A{args.start:03d} 到 A{args.end:03d}\n\n"
    content += f"**领域**: {args.domain}\n"
    content += f"**范围**: A{args.start:03d} 到 A{args.end:03d}\n"
    content += f"**数量**: {args.end - args.start + 1} 知识点\n"
    content += f"**时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    content += "---\n\n"
    
    count = 0
    for i in range(args.start, args.end + 1):
        content += generate_knowledge_point(args.domain, i, args.template)
        count += 1
    
    if args.dry_run:
        print(f"📊 试运行：将生成 {count} 个知识点")
        print(f"📁 输出目录：{output_dir}")
    else:
        # 写入文件
        output_file = os.path.join(output_dir, f"A{args.domain}-{args.start:03d}-{args.end:03d}.md")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 生成 {count} 个知识点")
        print(f"📁 输出文件：{output_file}")

if __name__ == '__main__':
    main()
