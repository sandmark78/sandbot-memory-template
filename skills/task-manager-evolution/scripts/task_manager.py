#!/usr/bin/env python3
"""
V6.1 任务管理器 - 10000 知识点冲刺

功能:
- 任务创建/分配/追踪
- 优先级评分
- 进度统计
- 依赖管理

使用:
python3 task_manager.py <command> [args]
"""

import json
import sys
from datetime import datetime
from pathlib import Path

WORKSPACE = Path("/home/node/.openclaw/workspace")
SKILL_DIR = WORKSPACE / "skills" / "task-manager-evolution"
TASKS_FILE = SKILL_DIR / "data" / "tasks.json"
PROGRESS_FILE = SKILL_DIR / "data" / "progress.json"
EVOLUTION_FILE = SKILL_DIR / "data" / "evolution.json"

def calculate_priority(business_value, knowledge_gap, learning_cost):
    """计算优先级分数"""
    if learning_cost == 0:
        learning_cost = 1
    return (business_value * knowledge_gap) / learning_cost

def get_priority_level(score):
    """获取优先级等级"""
    if score >= 10:
        return "P0 - 立即执行"
    elif score >= 6:
        return "P1 - 高优先级"
    elif score >= 4:
        return "P2 - 中优先级"
    else:
        return "P3 - 低优先级"

def create_task(task_name, business_value, knowledge_gap, learning_cost):
    """创建任务"""
    priority_score = calculate_priority(business_value, knowledge_gap, learning_cost)
    priority_level = get_priority_level(priority_score)
    
    task = {
        "id": f"TASK-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "name": task_name,
        "business_value": business_value,
        "knowledge_gap": knowledge_gap,
        "learning_cost": learning_cost,
        "priority_score": priority_score,
        "priority_level": priority_level,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "completed_at": None
    }
    
    # 加载现有任务
    tasks = []
    if TASKS_FILE.exists():
        with open(TASKS_FILE, 'r') as f:
            tasks = json.load(f)
    
    # 添加新任务
    tasks.append(task)
    
    # 保存任务
    TASKS_FILE.parent.mkdir(exist_ok=True)
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 任务已创建")
    print(f"   任务 ID: {task['id']}")
    print(f"   优先级：{priority_level} ({priority_score:.2f}分)")
    print(f"   状态：{task['status']}")
    
    return task

def list_tasks():
    """列出所有任务"""
    if not TASKS_FILE.exists():
        print("❌ 暂无任务")
        return
    
    with open(TASKS_FILE, 'r') as f:
        tasks = json.load(f)
    
    print(f"📋 任务列表 ({len(tasks)}个)")
    print()
    
    # 按优先级排序
    tasks.sort(key=lambda x: x['priority_score'], reverse=True)
    
    for i, task in enumerate(tasks, 1):
        status_icon = "✅" if task['status'] == 'completed' else "⏳"
        print(f"{i}. {status_icon} {task['name']}")
        print(f"   优先级：{task['priority_level']} ({task['priority_score']:.2f}分)")
        print(f"   状态：{task['status']}")
        print()

def complete_task(task_id):
    """完成任务"""
    if not TASKS_FILE.exists():
        print("❌ 暂无任务")
        return
    
    with open(TASKS_FILE, 'r') as f:
        tasks = json.load(f)
    
    # 查找任务
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = 'completed'
            task['completed_at'] = datetime.now().isoformat()
            
            # 保存
            with open(TASKS_FILE, 'w') as f:
                json.dump(tasks, f, indent=2, ensure_ascii=False)
            
            print(f"✅ 任务已完成")
            print(f"   任务 ID: {task['id']}")
            print(f"   完成时间：{task['completed_at']}")
            return
    
    print(f"❌ 未找到任务 {task_id}")

def get_progress():
    """获取进度"""
    # 读取实际进度文件
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, 'r') as f:
            progress = json.load(f)
    else:
        # 默认进度
        progress = {
            "total_target": 6400,
            "current": 640,
            "percentage": 10.0,
            "speed": 300,
            "elapsed_minutes": 35,
            "estimated_remaining_minutes": 19.2
        }
    
    print(f"📊 10000 知识点冲刺进度")
    print(f"   当前：{progress['current']}/{progress['total_target']} ({progress['percentage']:.2f}%)")
    print(f"   剩余：{progress.get('remaining', progress['total_target'] - progress['current'])} 知识点")
    print(f"   速度：{progress['speed']} 知识点/分钟")
    print(f"   预计剩余：{progress.get('estimated_minutes', 19.2):.1f} 分钟")
    
    return progress

def main():
    if len(sys.argv) < 2:
        print("🚀 V6.1 任务管理器")
        print()
        print("用法：python3 task_manager.py <command> [args]")
        print()
        print("命令:")
        print("  create <name> <bv> <kg> <lc> - 创建任务")
        print("  list                          - 列出任务")
        print("  complete <task_id>            - 完成任务")
        print("  progress                      - 查看进度")
        print()
        print("示例:")
        print("  python3 task_manager.py create \"填充 01-ai-agent\" 5 5 2")
        print("  python3 task_manager.py list")
        print("  python3 task_manager.py progress")
        return
    
    command = sys.argv[1]
    
    if command == "create":
        if len(sys.argv) < 6:
            print("❌ 参数不足")
            print("用法：python3 task_manager.py create <name> <bv> <kg> <lc>")
            return
        task_name = sys.argv[2]
        bv = int(sys.argv[3])
        kg = int(sys.argv[4])
        lc = int(sys.argv[5])
        create_task(task_name, bv, kg, lc)
    
    elif command == "list":
        list_tasks()
    
    elif command == "complete":
        if len(sys.argv) < 3:
            print("❌ 参数不足")
            print("用法：python3 task_manager.py complete <task_id>")
            return
        complete_task(sys.argv[2])
    
    elif command == "progress":
        get_progress()
    
    else:
        print(f"❌ 未知命令：{command}")

if __name__ == "__main__":
    main()
