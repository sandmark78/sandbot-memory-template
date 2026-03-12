#!/usr/bin/env python3
"""Quality Auditor - 知识质量审计脚本"""
import os, sys, re

def audit_directory(path):
    """审计目录中的知识文件"""
    print(f"🔍 审计目录：{path}")
    files_checked = 0
    issues = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.md'):
                files_checked += 1
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if '**数量**:' not in content:
                        issues.append(f"缺少知识点统计：{filepath}")
    print(f"✅ 检查了 {files_checked} 个文件")
    if issues:
        print(f"⚠️ 发现 {len(issues)} 个问题:")
        for issue in issues[:10]:
            print(f"  - {issue}")
    else:
        print("🎉 所有文件格式正确！")
    return len(issues) == 0

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "knowledge_base/"
    success = audit_directory(path)
    sys.exit(0 if success else 1)
