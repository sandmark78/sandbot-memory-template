#!/usr/bin/env python3
"""
V6.2.3 批量操作工具 - 高效管理知识点

功能:
- 批量创建知识点文件
- 批量重命名/移动
- 批量统计/分析
- 导出 CSV/JSON 报告

使用:
python3 batch_ops.py <command> [options]

命令:
  create <domain> <count>  - 批量创建知识点文件
  stats                    - 详细统计报告
  export <format>          - 导出报告 (csv/json)
  find-empty               - 查找空文件
  cleanup                  - 清理无效文件
"""

import json
import csv
import sys
import argparse
from datetime import datetime
from pathlib import Path

WORKSPACE = Path("/home/node/.openclaw/workspace")
SKILL_DIR = WORKSPACE / "skills" / "task-manager-evolution"
KNOWLEDGE_BASE = WORKSPACE / "knowledge_base"
REPORTS_DIR = SKILL_DIR / "reports"

# 12 个知识领域定义
DOMAINS = {
    "01-ai-agent": {"target": 1000, "name": "AI Agent"},
    "02-openclaw": {"target": 800, "name": "OpenClaw"},
    "03-federal-system": {"target": 600, "name": "联邦系统"},
    "04-skill-dev": {"target": 500, "name": "技能开发"},
    "05-memory-system": {"target": 400, "name": "记忆系统"},
    "06-growth-system": {"target": 400, "name": "成长系统"},
    "07-community": {"target": 500, "name": "社区建设"},
    "08-monetization": {"target": 500, "name": "变现"},
    "09-security": {"target": 400, "name": "安全"},
    "10-automation": {"target": 500, "name": "自动化"},
    "11-content": {"target": 400, "name": "内容创作"},
    "12-tools": {"target": 400, "name": "工具"},
}

def batch_create(domain_id, count, prefix="kp"):
    """批量创建知识点文件"""
    if domain_id not in DOMAINS:
        print(f"❌ 未知领域：{domain_id}")
        print(f"   可用领域：{', '.join(DOMAINS.keys())}")
        return False
    
    domain_dir = KNOWLEDGE_BASE / domain_id
    domain_dir.mkdir(exist_ok=True)
    
    # 获取当前文件数
    existing = list(domain_dir.glob("*.md"))
    start_num = len(existing) + 1
    
    print(f"📝 批量创建知识点文件")
    print(f"   领域：{domain_id} ({DOMAINS[domain_id]['name']})")
    print(f"   数量：{count}")
    print(f"   目录：{domain_dir}")
    print()
    
    created = 0
    for i in range(start_num, start_num + count):
        filename = f"{prefix}-{i:03d}.md"
        filepath = domain_dir / filename
        
        if filepath.exists():
            print(f"   ⚠️  跳过已存在：{filename}")
            continue
        
        # 创建模板内容
        content = f"""# {DOMAINS[domain_id]['name']} - 知识点 {i}

**领域**: {domain_id}  
**创建时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  
**状态**: 📝 待填充

---

## 核心概念

<!-- 在此填写核心概念 -->

---

## 关键参数

<!-- 在此填写关键参数 -->

---

## 实践应用

<!-- 在此填写实践应用 -->

---

## 关联知识

<!-- 在此填写关联知识点 -->

---

*知识点 #{i} | {domain_id}*
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        created += 1
        if created % 10 == 0:
            print(f"   已创建：{created}/{count}")
    
    print()
    print(f"✅ 创建完成：{created} 个文件")
    return True

def detailed_stats():
    """生成详细统计报告"""
    print("📊 详细统计报告")
    print("=" * 70)
    print()
    
    stats = {
        "timestamp": datetime.now().isoformat(),
        "domains": {},
        "total": 0,
        "total_target": 0
    }
    
    total_files = 0
    total_size = 0
    
    for domain_id, domain_info in sorted(DOMAINS.items()):
        domain_dir = KNOWLEDGE_BASE / domain_id
        
        if domain_dir.exists():
            md_files = [f for f in domain_dir.glob("*.md") if f.is_file()]
            count = len(md_files)
            size = sum(f.stat().st_size for f in md_files)
        else:
            count = 0
            size = 0
        
        target = domain_info["target"]
        pct = (count / target) * 100 if target > 0 else 0
        remaining = target - count
        
        stats["domains"][domain_id] = {
            "name": domain_info["name"],
            "target": target,
            "current": count,
            "remaining": remaining,
            "percentage": round(pct, 2),
            "size_bytes": size
        }
        
        stats["total"] += count
        stats["total_target"] += target
        total_files += count
        total_size += size
        
        # 打印进度条
        bar_len = int(pct / 5)
        bar = "█" * bar_len + "░" * (20 - bar_len)
        
        print(f"{domain_id:<15} {domain_info['name']:<12} {count:>4}/{target:<4} {bar} {pct:>5.1f}% ({remaining} 剩余)")
    
    print()
    print("=" * 70)
    overall_pct = (stats["total"] / stats["total_target"]) * 100 if stats["total_target"] > 0 else 0
    print(f"总计：{stats['total']}/{stats['total_target']} ({overall_pct:.2f}%)")
    print(f"文件总数：{total_files}")
    print(f"总大小：{total_size / 1024:.1f} KB")
    print()
    
    return stats

def export_report(format_type):
    """导出报告"""
    REPORTS_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    stats = detailed_stats()
    
    if format_type == "json":
        filepath = REPORTS_DIR / f"knowledge_stats_{timestamp}.json"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        print(f"✅ JSON 报告已导出：{filepath}")
    
    elif format_type == "csv":
        filepath = REPORTS_DIR / f"knowledge_stats_{timestamp}.csv"
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["领域 ID", "领域名称", "目标", "当前", "剩余", "进度%", "大小 (KB)"])
            
            for domain_id, info in stats["domains"].items():
                writer.writerow([
                    domain_id,
                    info["name"],
                    info["target"],
                    info["current"],
                    info["remaining"],
                    info["percentage"],
                    round(info["size_bytes"] / 1024, 2)
                ])
            
            # 总计行
            overall_pct = (stats["total"] / stats["total_target"]) * 100 if stats["total_target"] > 0 else 0
            writer.writerow([
                "总计",
                "-",
                stats["total_target"],
                stats["total"],
                stats["total_target"] - stats["total"],
                round(overall_pct, 2),
                "-"
            ])
        
        print(f"✅ CSV 报告已导出：{filepath}")
    
    else:
        print(f"❌ 未知格式：{format_type}")
        print(f"   支持格式：json, csv")

def find_empty_files():
    """查找空文件"""
    print("🔍 查找空文件...")
    print()
    
    empty_files = []
    
    for domain_id in DOMAINS.keys():
        domain_dir = KNOWLEDGE_BASE / domain_id
        if not domain_dir.exists():
            continue
        
        for md_file in domain_dir.glob("*.md"):
            if md_file.stat().st_size < 50:  # 小于 50 字节视为空文件
                empty_files.append(md_file)
    
    if empty_files:
        print(f"发现 {len(empty_files)} 个空文件:")
        for f in empty_files[:20]:  # 只显示前 20 个
            print(f"   - {f}")
        if len(empty_files) > 20:
            print(f"   ... 还有 {len(empty_files) - 20} 个")
    else:
        print("✅ 未发现空文件")
    
    return empty_files

def cleanup():
    """清理无效文件"""
    print("🧹 清理无效文件...")
    print()
    
    # 查找并删除空文件
    empty_files = find_empty_files()
    
    if empty_files:
        print()
        confirm = input(f"确认删除 {len(empty_files)} 个空文件？(y/N): ")
        if confirm.lower() == 'y':
            for f in empty_files:
                f.unlink()
                print(f"   已删除：{f}")
            print(f"✅ 清理完成：删除 {len(empty_files)} 个文件")
        else:
            print("❌ 取消操作")
    else:
        print("无需清理")

def main():
    parser = argparse.ArgumentParser(description='V6.2.3 批量操作工具')
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # create 命令
    create_parser = subparsers.add_parser('create', help='批量创建知识点文件')
    create_parser.add_argument('domain', help='领域 ID (如 01-ai-agent)')
    create_parser.add_argument('count', type=int, help='创建数量')
    create_parser.add_argument('--prefix', default='kp', help='文件名前缀')
    
    # stats 命令
    subparsers.add_parser('stats', help='详细统计报告')
    
    # export 命令
    export_parser = subparsers.add_parser('export', help='导出报告')
    export_parser.add_argument('format', choices=['json', 'csv'], help='导出格式')
    
    # find-empty 命令
    subparsers.add_parser('find-empty', help='查找空文件')
    
    # cleanup 命令
    subparsers.add_parser('cleanup', help='清理无效文件')
    
    args = parser.parse_args()
    
    if args.command == 'create':
        batch_create(args.domain, args.count, args.prefix)
    elif args.command == 'stats':
        detailed_stats()
    elif args.command == 'export':
        export_report(args.format)
    elif args.command == 'find-empty':
        find_empty_files()
    elif args.command == 'cleanup':
        cleanup()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
