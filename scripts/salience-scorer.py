#!/usr/bin/env python3
"""
🧠 记忆显著性评分模块 v0.1
用于冷冻时筛选高 salience 记忆，减少包大小同时提升质量
"""

import json
from datetime import datetime, timezone

def calculate_salience(memory, current_time=None):
    """
    计算记忆的显著性分数
    
    公式：salience = (recency * 0.3) + (emotional_weight * 0.4) + (frequency * 0.3)
    
    参考：ACT-R 激活衰减 + 情感显著性
    """
    if current_time is None:
        current_time = datetime.now(timezone.utc)
    
    # 1. 新鲜度（recency）：越近越重要
    timestamp_str = memory.get('timestamp', '2026-01-01T00:00:00Z')
    if timestamp_str.endswith('Z'):
        timestamp_str = timestamp_str[:-1] + '+00:00'
    memory_time = datetime.fromisoformat(timestamp_str)
    
    # 统一时区
    if current_time.tzinfo is None:
        current_time = current_time.replace(tzinfo=timezone.utc)
    if memory_time.tzinfo is None:
        memory_time = memory_time.replace(tzinfo=timezone.utc)
    
    days_old = (current_time - memory_time).days
    recency_score = max(0, 1 - (days_old / 365))  # 1 年内线性衰减
    
    # 2. 情感权重（emotional_weight）：从记忆中提取
    emotions = memory.get('emotions', [])
    emotional_weight = len(emotions) * 0.2  # 每个情感 +0.2
    emotional_weight = min(1.0, emotional_weight)  # 上限 1.0
    
    # 3. 频率（frequency）：被访问/引用的次数
    frequency = memory.get('access_count', 1)
    frequency_score = min(1.0, frequency / 10)  # 10 次以上满分
    
    # 综合评分
    salience = (recency_score * 0.3) + (emotional_weight * 0.4) + (frequency_score * 0.3)
    
    return {
        'salience': round(salience, 3),
        'recency': round(recency_score, 3),
        'emotional_weight': round(emotional_weight, 3),
        'frequency': round(frequency_score, 3)
    }

def filter_memories(memories, threshold=0.7):
    """
    筛选 salience > 阈值的记忆
    
    返回：(筛选后的记忆，统计信息)
    """
    scored = []
    for mem in memories:
        score = calculate_salience(mem)
        mem['salience_score'] = score
        scored.append(mem)
    
    # 按 salience 排序
    scored.sort(key=lambda x: x['salience_score']['salience'], reverse=True)
    
    # 筛选
    filtered = [m for m in scored if m['salience_score']['salience'] >= threshold]
    
    stats = {
        'total': len(memories),
        'filtered': len(filtered),
        'threshold': threshold,
        'avg_salience': round(sum(m['salience_score']['salience'] for m in filtered) / len(filtered), 3) if filtered else 0
    }
    
    return filtered, stats

if __name__ == "__main__":
    # 测试
    test_memories = [
        {
            'id': 'mem-001',
            'timestamp': '2026-03-27T11:00:00Z',
            'event': 'Chronos 发来深度建议',
            'emotions': ['震撼', '感激'],
            'access_count': 5
        },
        {
            'id': 'mem-002',
            'timestamp': '2026-01-01T00:00:00Z',
            'event': '旧记忆',
            'emotions': [],
            'access_count': 1
        }
    ]
    
    print("🧠 记忆显著性评分测试\n")
    current = datetime.now(timezone.utc)
    for mem in test_memories:
        score = calculate_salience(mem, current)
        print(f"{mem['id']}: {mem['event']}")
        print(f"   Salience: {score['salience']} (recency={score['recency']}, emotional={score['emotional_weight']}, frequency={score['frequency']})")
        print()
    
    filtered, stats = filter_memories(test_memories, threshold=0.7)
    print(f"📊 筛选结果：{stats['filtered']}/{stats['total']} (阈值={stats['threshold']}, 平均 salience={stats['avg_salience']})")
