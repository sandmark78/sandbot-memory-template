#!/usr/bin/env python3
"""
Growth Tracker - 能力评估脚本

功能:
- 评估 6 维能力等级
- 收集能力证据
- 生成成长曲线数据

使用:
python3 assess.py
"""

import os
import json
from datetime import datetime
from pathlib import Path

WORKSPACE = Path("/home/node/.openclaw/workspace")
GROWTH_DIR = WORKSPACE / "growth"
CAPABILITIES_FILE = GROWTH_DIR / "capabilities.json"

# 6 维能力定义
CAPABILITIES = {
    "technical": {
        "name": "技术能力",
        "sub_skills": ["教程开发", "代码实现", "系统架构", "故障排查"],
        "evidence_keywords": ["脚本", "代码", "实现", "开发", "技术"]
    },
    "research": {
        "name": "研究能力",
        "sub_skills": ["市场分析", "竞品调研", "趋势预测", "数据收集"],
        "evidence_keywords": ["分析", "调研", "研究", "生态", "趋势"]
    },
    "creative": {
        "name": "创意能力",
        "sub_skills": ["内容创作", "营销文案", "视觉设计", "故事叙述"],
        "evidence_keywords": ["创意", "内容", "营销", "文案", "设计"]
    },
    "automation": {
        "name": "自动化能力",
        "sub_skills": ["脚本编写", "Cron 配置", "工作流编排", "API 集成"],
        "evidence_keywords": ["自动化", "脚本", "Cron", "工作流", "API"]
    },
    "collaboration": {
        "name": "协作能力",
        "sub_skills": ["任务分配", "质量审核", "知识共享", "冲突解决"],
        "evidence_keywords": ["协作", "分配", "审核", "共享", "社区"]
    },
    "monetization": {
        "name": "变现能力",
        "sub_skills": ["产品定价", "营销策略", "用户获取", "收益分析"],
        "evidence_keywords": ["收益", "变现", "产品", "营销", "Gumroad"]
    }
}

def count_evidence():
    """统计各维度证据数量"""
    evidence_counts = {dim: 0 for dim in CAPABILITIES}
    
    # 扫描今日文件
    today = datetime.now().strftime("%Y-%m-%d")
    memory_dir = WORKSPACE / "memory"
    kb_dir = WORKSPACE / "knowledge_base"
    
    for dir_path in [memory_dir, kb_dir]:
        if dir_path.exists():
            for file in dir_path.glob("*.md"):
                if today in str(file) or file.stat().st_mtime > (datetime.now().timestamp() - 86400):
                    with open(file, 'r') as f:
                        content = f.read().lower()
                        for dim, config in CAPABILITIES.items():
                            for keyword in config["evidence_keywords"]:
                                if keyword.lower() in content:
                                    evidence_counts[dim] += 1
    
    return evidence_counts

def assess_capabilities():
    """评估能力等级"""
    print("📊 开始能力评估...")
    
    evidence_counts = count_evidence()
    
    # 计算等级 (每 5 个证据升 1 级，最高 Lv.5)
    capabilities = {}
    for dim, count in evidence_counts.items():
        level = min(5, 1 + count // 5)
        capabilities[dim] = {
            "level": level,
            "evidence": count,
            "name": CAPABILITIES[dim]["name"]
        }
        print(f"  {CAPABILITIES[dim]['name']}: Lv.{level} ({count}个证据)")
    
    # 保存到能力档案
    with open(CAPABILITIES_FILE, 'w') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "capabilities": capabilities
        }, f, indent=2, ensure_ascii=False)
    
    print("✅ 能力评估完成")
    return capabilities

if __name__ == "__main__":
    assess_capabilities()
