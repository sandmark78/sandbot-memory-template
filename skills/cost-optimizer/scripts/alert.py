#!/usr/bin/env python3
"""
Cost Optimizer - 预算预警脚本

功能:
- 设置预算上限
- 监控支出
- 发送预警

使用:
python3 alert.py
"""

import json
from datetime import datetime

# 预算配置
BUDGET = {
    "daily": 10.0,      # 日预算 $10
    "weekly": 50.0,     # 周预算 $50
    "monthly": 200.0    # 月预算 $200
}

def check_budget():
    """检查预算"""
    print("💰 预算预警系统")
    print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 模拟今日支出
    today_spent = 0.60  # 从 track.py 数据
    
    print("预算状态:")
    print(f"  日预算：${BUDGET['daily']:.2f}")
    print(f"  已支出：${today_spent:.2f}")
    print(f"  剩余：${BUDGET['daily']-today_spent:.2f}")
    print(f"  使用率：{today_spent/BUDGET['daily']*100:.1f}%")
    print()
    
    # 预警级别
    usage = today_spent / BUDGET['daily']
    if usage >= 1.0:
        print("🚨 警报：已达预算上限！")
    elif usage >= 0.8:
        print("⚠️ 警告：已达预算 80%！")
    elif usage >= 0.5:
        print("💡 提醒：已达预算 50%")
    else:
        print("✅ 预算健康")

if __name__ == "__main__":
    check_budget()
