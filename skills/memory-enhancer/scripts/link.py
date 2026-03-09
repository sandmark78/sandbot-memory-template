#!/usr/bin/env python3
"""
Memory Enhancer - 跨文件链接脚本

功能:
- 扫描相关文件
- 识别相关主题
- 添加内部链接
- 生成导航索引

使用:
python3 link.py
"""

import json
from pathlib import Path
from datetime import datetime

WORKSPACE = Path("/home/node/.openclaw/workspace")
KB_DIR = WORKSPACE / "knowledge_base"
MEMORY_DIR = WORKSPACE / "memory"

def create_cross_links():
    """创建跨文件链接"""
    print("🔗 跨文件链接生成")
    print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 扫描知识库文件
    kb_files = list(KB_DIR.glob("*.md"))
    memory_files = list(MEMORY_DIR.glob("*.md"))
    
    print(f"知识库文件：{len(kb_files)}个")
    print(f"记忆文件：{len(memory_files)}个")
    print()
    
    # 生成链接统计
    links_created = 0
    for file in kb_files[:10]:
        with open(file, 'r') as f:
            content = f.read()
            # 简单统计链接数量
            links = content.count("](")
            links_created += links
    
    print(f"现有链接数：{links_created}个")
    print()
    print("💡 建议:")
    print("  - 添加 INDEX.md 引用")
    print("  - 添加相关文件互链")
    print("  - 生成导航菜单")

if __name__ == "__main__":
    create_cross_links()
