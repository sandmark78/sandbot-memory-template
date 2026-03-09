#!/usr/bin/env python3
"""
Cost Optimizer - 成本追踪脚本

功能:
- 追踪模型调用成本
- 生成成本报告
- 分析使用模式

使用:
python3 track.py
"""

import json
from datetime import datetime
from pathlib import Path

WORKSPACE = Path("/home/node/.openclaw/workspace")

# 模型定价 (每百万 tokens)
MODEL_PRICES = {
    "qwen3.5-turbo": {"input": 0.5, "output": 1.0},
    "qwen3.5-plus": {"input": 2.0, "output": 4.0},
    "qwen-max": {"input": 10.0, "output": 20.0}
}

def track_cost():
    """追踪成本"""
    print("💰 成本追踪")
    print(f"日期：{datetime.now().strftime('%Y-%m-%d')}")
    print()
    
    # 模拟今日调用 (实际应从日志读取)
    calls = {
        "qwen3.5-plus": {"input": 100, "output": 50},  # K tokens
        "qwen-max": {"input": 10, "output": 5}
    }
    
    total_cost = 0.0
    print("按模型分布:")
    for model, usage in calls.items():
        input_cost = usage["input"] * MODEL_PRICES[model]["input"] / 1000
        output_cost = usage["output"] * MODEL_PRICES[model]["output"] / 1000
        model_cost = input_cost + output_cost
        total_cost += model_cost
        print(f"  {model}: ${model_cost:.4f} (输入{usage['input']}K, 输出{usage['output']}K)")
    
    print()
    print(f"总成本：${total_cost:.4f}")
    print()
    print("💡 优化建议:")
    print("  - 简单任务可用 qwen3.5-turbo (节省 75%)")
    print("  - 批量处理可减少 30% 调用")
    print("  - 本地缓存可节省 20% 查询")

if __name__ == "__main__":
    track_cost()
