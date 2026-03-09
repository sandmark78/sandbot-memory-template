#!/usr/bin/env python3
"""
V6.2.5 统一 CLI - 任务管理器命令行接口

功能:
- 统一入口，替代多个独立脚本
- 子命令模式 (progress/sync/validate/tasks/evolution)
- 全局选项 (--quiet/--export/--force)
- 命令别名和快捷方式

使用:
python3 cli.py <command> [options]

命令:
  progress    进度追踪 (同 progress_tracker.py)
  sync        自动同步 (同 auto_sync.py)
  validate    数据验证 (同 validate_data.py)
  tasks       任务管理
  evolution   进化循环
  status      快速状态检查
  report      生成综合报告
"""

import sys
import argparse
from pathlib import Path

# 确保脚本目录在路径中
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))


def cmd_progress(args):
    """进度追踪命令"""
    from progress_tracker import ProgressTracker
    tracker = ProgressTracker(use_cache=not args.no_cache)
    tracker.run(force=args.force, export=args.export, quiet=args.quiet)


def cmd_sync(args):
    """自动同步命令"""
    from auto_sync import AutoSync
    syncer = AutoSync()
    syncer.run(force=args.force, check_only=args.check_only)


def cmd_validate(args):
    """数据验证命令"""
    from validate_data import DataValidator
    validator = DataValidator()
    result = validator.validate_all()
    
    # 保存报告
    from config import VALIDATION_FILE
    import json
    with open(VALIDATION_FILE, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    if args.export:
        from config import REPORTS_DIR
        from datetime import datetime
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_path = REPORTS_DIR / f"validation_{timestamp}.json"
        with open(export_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"📄 报告已导出：{export_path}")


def cmd_tasks(args):
    """任务管理命令"""
    from task_manager import TaskManager
    manager = TaskManager()
    
    if args.action == 'list':
        manager.list_tasks()
    elif args.action == 'create':
        manager.create_task(args.title, args.priority or 'P2')
    elif args.action == 'complete':
        manager.complete_task(args.id)
    elif args.action == 'stats':
        manager.print_stats()


def cmd_evolution(args):
    """进化循环命令"""
    from evolution_loop import EvolutionLoop
    loop = EvolutionLoop()
    loop.run_cycle()


def cmd_status(args):
    """快速状态检查"""
    from config import PROGRESS_FILE, EVOLUTION_FILE, KNOWLEDGE_BASE
    import json
    from datetime import datetime
    
    print("📊 快速状态检查")
    print("=" * 60)
    print()
    
    # 加载进度
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            progress = json.load(f)
        print(f"📈 进度：{progress['current']}/{progress['total_target']} ({progress['percentage']}%)")
        print(f"🚀 速度：{progress['speed']} 知识点/分钟")
        print(f"⏱️  预计：{progress['estimated_minutes']} 分钟")
    else:
        print("⚠️  进度文件不存在，运行 progress 命令初始化")
    
    print()
    
    # 扫描领域
    domain_count = sum(1 for d in KNOWLEDGE_BASE.iterdir() if d.is_dir() and d.name.startswith('0'))
    print(f"📁 知识领域：{domain_count}/12")
    
    # 统计文件
    total_files = sum(1 for f in KNOWLEDGE_BASE.rglob('*.md'))
    print(f"📄 知识文件：{total_files}")
    
    print()
    print("=" * 60)


def cmd_report(args):
    """生成综合报告"""
    from config import REPORTS_DIR, PROGRESS_FILE, VALIDATION_FILE
    import json
    from datetime import datetime
    
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORTS_DIR / f"comprehensive_{timestamp}.json"
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "version": "V6.2.5",
        "progress": None,
        "validation": None,
    }
    
    # 加载进度
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            report["progress"] = json.load(f)
    
    # 加载验证
    if VALIDATION_FILE.exists():
        with open(VALIDATION_FILE, 'r', encoding='utf-8') as f:
            report["validation"] = json.load(f)
    
    # 保存报告
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 综合报告已生成：{report_path}")
    
    if args.print:
        print()
        print(json.dumps(report, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(
        description='V6.2.5 任务管理器 CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 cli.py progress              # 查看进度
  python3 cli.py sync --force          # 强制同步
  python3 cli.py validate --export     # 验证并导出报告
  python3 cli.py status                # 快速状态检查
  python3 cli.py report --print        # 生成并打印综合报告
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # progress 命令
    p_progress = subparsers.add_parser('progress', help='进度追踪')
    p_progress.add_argument('--force', '-f', action='store_true', help='强制重新扫描')
    p_progress.add_argument('--no-cache', action='store_true', help='禁用缓存')
    p_progress.add_argument('--export', '-e', choices=['json', 'csv'], help='导出格式')
    p_progress.add_argument('--quiet', '-q', action='store_true', help='静默模式')
    p_progress.set_defaults(func=cmd_progress)
    
    # sync 命令
    p_sync = subparsers.add_parser('sync', help='自动同步')
    p_sync.add_argument('--force', '-f', action='store_true', help='强制同步')
    p_sync.add_argument('--check-only', '-c', action='store_true', help='仅检查')
    p_sync.add_argument('--quiet', '-q', action='store_true', help='静默模式')
    p_sync.set_defaults(func=cmd_sync)
    
    # validate 命令
    p_validate = subparsers.add_parser('validate', help='数据验证')
    p_validate.add_argument('--export', '-e', action='store_true', help='导出 JSON 报告')
    p_validate.add_argument('--quiet', '-q', action='store_true', help='静默模式')
    p_validate.set_defaults(func=cmd_validate)
    
    # tasks 命令
    p_tasks = subparsers.add_parser('tasks', help='任务管理')
    p_tasks.add_argument('action', choices=['list', 'create', 'complete', 'stats'], help='操作')
    p_tasks.add_argument('--id', help='任务 ID')
    p_tasks.add_argument('--title', help='任务标题')
    p_tasks.add_argument('--priority', choices=['P0', 'P1', 'P2', 'P3'], help='优先级')
    p_tasks.set_defaults(func=cmd_tasks)
    
    # evolution 命令
    p_evolution = subparsers.add_parser('evolution', help='进化循环')
    p_evolution.set_defaults(func=cmd_evolution)
    
    # status 命令
    p_status = subparsers.add_parser('status', help='快速状态检查')
    p_status.set_defaults(func=cmd_status)
    
    # report 命令
    p_report = subparsers.add_parser('report', help='生成综合报告')
    p_report.add_argument('--print', '-p', action='store_true', help='打印报告')
    p_report.set_defaults(func=cmd_report)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    args.func(args)


if __name__ == "__main__":
    main()
