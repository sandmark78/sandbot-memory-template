#!/usr/bin/env python3
"""
Intent Predictor - 上下文准备脚本

功能:
- 加载相关文件
- 建立索引
- 准备执行环境

使用:
python3 context.py research "OpenClaw"
"""

import sys
import json
from pathlib import Path
from datetime import datetime

WORKSPACE = Path("/home/node/.openclaw/workspace")

def load_context(intent, topic=""):
    """加载相关上下文"""
    context = {
        "intent": intent,
        "topic": topic,
        "timestamp": datetime.now().isoformat(),
        "files": [],
        "resources": []
    }
    
    # 根据意图加载文件
    if intent == "research":
        kb_dir = WORKSPACE / "knowledge_base"
        for file in kb_dir.glob("*openclaw*.md"):
            context["files"].append(str(file))
    
    elif intent == "coding":
        scripts_dir = WORKSPACE / "scripts"
        for file in scripts_dir.glob("*.py"):
            context["files"].append(str(file))
    
    elif intent == "writing":
        memory_dir = WORKSPACE / "memory"
        for file in memory_dir.glob("*.md"):
            context["files"].append(str(file))
    
    return context

def main():
    if len(sys.argv) < 2:
        print("🔮 Intent Predictor - Context Preparation")
        print("用法：python3 context.py <intent> [topic]")
        return
    
    intent = sys.argv[1]
    topic = sys.argv[2] if len(sys.argv) > 2 else ""
    
    context = load_context(intent, topic)
    
    print(f"📚 上下文准备")
    print(f"意图：{intent}")
    print(f"主题：{topic}")
    print(f"加载文件：{len(context['files'])}个")
    for f in context["files"][:5]:
        print(f"  - {f}")
    if len(context["files"]) > 5:
        print(f"  ... 还有 {len(context['files'])-5} 个")

if __name__ == "__main__":
    main()
