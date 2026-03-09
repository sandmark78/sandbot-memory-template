#!/usr/bin/env python3
"""
Growth Tracker - 报告生成脚本

功能:
- 收集当日文件
- 统计任务完成
- 提取关键学习
- 生成成长报告

使用:
python3 report.py
"""

import json
from pathlib import Path
from datetime import datetime

WORKSPACE = Path("/home/node/.openclaw/workspace")
MEMORY_DIR = WORKSPACE / "memory"
GROWTH_DIR = WORKSPACE / "growth"

def generate_report():
    """生成成长报告"""
    print("📊 成长报告生成")
    print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 统计今日文件
    today = datetime.now().strftime("%Y-%m-%d")
    file_count = 0
    
    for file in MEMORY_DIR.glob("*.md"):
        if today in str(file):
            file_count += 1
    
    for file in (WORKSPACE / "knowledge_base").glob("*.md"):
        if today in str(file):
            file_count += 1
    
    print(f"今日文件产出：{file_count}个")
    print()
    
    # 加载能力评估
    capabilities_file = GROWTH_DIR / "capabilities.json"
    if capabilities_file.exists():
        with open(capabilities_file, 'r') as f:
            data = json.load(f)
            print("能力等级:")
            for dim, info in data.get("capabilities", {}).items():
                print(f"  {info['name']}: Lv.{info['level']} ({info['evidence']}证据)")
    
    print()
    print("✅ 报告生成完成")

if __name__ == "__main__":
    generate_report()
