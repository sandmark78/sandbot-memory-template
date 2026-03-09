#!/usr/bin/env python3
"""
Intent Predictor - 意图识别脚本

功能:
- 识别 5 种用户意图
- 预测下一步需求
- 准备相关资源

使用:
python3 detect.py "帮我研究 OpenClaw 生态"
"""

import sys
import json

# 意图模式库
INTENT_PATTERNS = {
    "research": {
        "keywords": ["研究", "分析", "调研", "探索", "学习", "了解", "生态", "趋势"],
        "actions": ["准备相关资料", "搜索类似项目", "整理知识框架"],
        "resources": ["knowledge_base/", "memory/search_cache_*.md"]
    },
    "coding": {
        "keywords": ["代码", "脚本", "实现", "开发", "编写", "创建", "自动化"],
        "actions": ["准备代码模板", "检查依赖", "创建文件结构"],
        "resources": ["scripts/", "skills/"]
    },
    "writing": {
        "keywords": ["文档", "文章", "教程", "报告", "总结", "记录", "帖子"],
        "actions": ["准备文档模板", "整理大纲", "收集参考资料"],
        "resources": ["knowledge_base/", "memory/*.md"]
    },
    "deploy": {
        "keywords": ["部署", "发布", "提交", "推送", "上线", "PR", "GitHub"],
        "actions": ["检查配置文件", "准备部署脚本", "验证环境"],
        "resources": ["scripts/*.sh", "clawhub-releases/"]
    },
    "optimize": {
        "keywords": ["优化", "改进", "增强", "提升", "效率", "性能"],
        "actions": ["分析当前状态", "识别瓶颈", "准备优化方案"],
        "resources": ["memory/*summary*.md", "growth/"]
    }
}

def detect_intent(input_text):
    """检测用户意图"""
    scores = {}
    input_lower = input_text.lower()
    
    for intent, config in INTENT_PATTERNS.items():
        score = sum(1 for kw in config["keywords"] if kw in input_lower)
        scores[intent] = score
    
    if max(scores.values()) > 0:
        best_intent = max(scores, key=scores.get)
        return best_intent, scores[best_intent]
    return "general", 0

def predict_next_steps(intent):
    """预测下一步需求"""
    if intent in INTENT_PATTERNS:
        return INTENT_PATTERNS[intent]["actions"]
    return ["准备通用资源", "等待进一步指令"]

def prepare_resources(intent):
    """准备相关资源"""
    if intent in INTENT_PATTERNS:
        return INTENT_PATTERNS[intent]["resources"]
    return []

def main():
    if len(sys.argv) < 2:
        print("🔮 Intent Predictor - V6.1")
        print("用法：python3 detect.py <input_text>")
        print("示例：python3 detect.py '帮我研究 OpenClaw 生态'")
        return
    
    input_text = " ".join(sys.argv[1:])
    intent, confidence = detect_intent(input_text)
    predictions = predict_next_steps(intent)
    resources = prepare_resources(intent)
    
    print(f"🔮 意图分析")
    print(f"输入：{input_text[:50]}...")
    print(f"意图：{intent} (置信度：{confidence})")
    print(f"预测下一步:")
    for i, action in enumerate(predictions, 1):
        print(f"  {i}. {action}")
    print(f"准备资源:")
    for res in resources[:3]:
        print(f"  - {res}")

if __name__ == "__main__":
    main()
