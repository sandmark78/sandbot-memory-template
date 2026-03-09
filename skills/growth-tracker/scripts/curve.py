#!/usr/bin/env python3
"""
Growth Tracker - 成长曲线生成脚本

功能:
- 读取成长日志
- 按日期统计证据
- 计算每日能力等级
- 生成曲线数据

使用:
python3 curve.py
"""

import json
from pathlib import Path
from datetime import datetime, timedelta

WORKSPACE = Path("/home/node/.openclaw/workspace")
GROWTH_DIR = WORKSPACE / "growth"
MEMORY_DIR = WORKSPACE / "memory"

def generate_growth_curve():
    """生成成长曲线数据"""
    print("📈 成长曲线生成")
    print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 读取最近 7 天文件
    today = datetime.now()
    daily_evidence = {}
    
    for i in range(7):
        date = today - timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        daily_evidence[date_str] = 0
    
    # 统计每日文件数
    for file in MEMORY_DIR.glob("*.md"):
        for date_str in daily_evidence.keys():
            if date_str in str(file):
                daily_evidence[date_str] += 1
    
    print("近 7 天文件产出:")
    for date_str, count in sorted(daily_evidence.items(), reverse=True):
        bar = "█" * min(count, 50)
        print(f"  {date_str}: {bar} ({count}个)")
    
    print()
    total = sum(daily_evidence.values())
    avg = total / 7
    print(f"总计：{total}个文件")
    print(f"日均：{avg:.1f}个文件")
    
    # 生成曲线数据 (JSON 格式)
    curve_data = {
        "dates": list(daily_evidence.keys()),
        "values": list(daily_evidence.values()),
        "total": total,
        "average": avg
    }
    
    # 保存到文件
    curve_file = GROWTH_DIR / "growth_curve.json"
    curve_file.parent.mkdir(exist_ok=True)
    with open(curve_file, 'w') as f:
        json.dump(curve_data, f, indent=2)
    
    print(f"\n✅ 曲线数据已保存：{curve_file}")

if __name__ == "__main__":
    generate_growth_curve()
