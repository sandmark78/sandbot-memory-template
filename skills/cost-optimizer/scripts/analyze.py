#!/usr/bin/env python3
"""
Cost Optimizer - 使用分析脚本

功能:
- 分析模型使用情况
- 按功能分布统计
- 生成优化建议

使用:
python3 analyze.py
"""

import json
from datetime import datetime

def analyze_usage():
    """分析使用情况"""
    print("💰 成本优化器 - 使用分析")
    print(f"日期：{datetime.now().strftime('%Y-%m-%d')}")
    print()
    
    # 模拟使用数据
    usage = {
        "by_model": {
            "qwen3.5-plus": {"calls": 45, "tokens": 150000},
            "qwen-max": {"calls": 2, "tokens": 15000}
        },
        "by_function": {
            "研究分析": 20,
            "文档写作": 15,
            "代码开发": 10,
            "社区互动": 2
        },
        "by_time": {
            "白天 (07-19 UTC)": 35,
            "夜晚 (19-07 UTC)": 12
        }
    }
    
    print("按模型分布:")
    for model, data in usage["by_model"].items():
        print(f"  {model}: {data['calls']}次调用，{data['tokens']:,} tokens")
    
    print()
    print("按功能分布:")
    for func, count in usage["by_function"].items():
        bar = "█" * min(count, 50)
        print(f"  {func}: {bar} ({count}次)")
    
    print()
    print("按时段分布:")
    for time, count in usage["by_time"].items():
        bar = "█" * min(count, 50)
        print(f"  {time}: {bar} ({count}次)")
    
    print()
    print("💡 优化建议:")
    print("  - 简单任务用 qwen3.5-turbo (节省 75%)")
    print("  - 批量处理减少调用 (节省 30%)")
    print("  - 本地缓存重复查询 (节省 20%)")

if __name__ == "__main__":
    analyze_usage()
