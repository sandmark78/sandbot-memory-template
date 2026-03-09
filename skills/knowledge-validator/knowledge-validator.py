#!/usr/bin/env python3
"""Knowledge Validator - 验证知识点格式和质量"""

import argparse
import os
import re
from pathlib import Path
from datetime import datetime

def validate_file(filepath, strict=False):
    """验证单个文件"""
    issues = []
    warnings = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查标题
    if not content.startswith('#'):
        issues.append("文件缺少标题")
    
    # 检查知识点格式
    knowledge_points = re.findall(r'^### (A\d+-\d+): (.+)$', content, re.MULTILINE)
    
    if not knowledge_points:
        issues.append("未找到知识点 (### AXX-XXX 格式)")
    
    # 检查必需字段 (检查整个文件)
    has_definition = '**定义**' in content or '**定义:**' in content
    has_core = '**核心**' in content or '**核心:**' in content
    has_application = '**应用**' in content or '**应用:**' in content
    has_params = '**参数**' in content or '**参数:**' in content
    
    if not has_definition:
        warnings.append("文件缺少'定义'字段")
    if not has_core:
        warnings.append("文件缺少'核心'字段")
    if not has_application:
        warnings.append("文件缺少'应用'字段")
    if not has_params:
        warnings.append("文件缺少'参数'字段")
    
    # 严格模式额外检查
    if strict:
        # 检查字数
        word_count = len(content)
        if word_count < 500:
            warnings.append(f"文件字数偏少 ({word_count} 字)")
        
        # 检查知识点密度
        if knowledge_points:
            avg_words_per_point = word_count / len(knowledge_points)
            if avg_words_per_point < 50:
                warnings.append(f"每个知识点平均字数偏少 ({avg_words_per_point:.0f} 字)")
    
    return {
        'file': filepath,
        'issues': issues,
        'warnings': warnings,
        'knowledge_points': len(knowledge_points),
        'valid': len(issues) == 0
    }

def main():
    parser = argparse.ArgumentParser(description='验证知识点格式和质量')
    parser.add_argument('--file', help='单个文件路径')
    parser.add_argument('--dir', help='目录路径')
    parser.add_argument('--report', help='报告输出路径')
    parser.add_argument('--auto-fix', action='store_true', help='自动修复')
    parser.add_argument('--strict', action='store_true', help='严格模式')
    
    args = parser.parse_args()
    
    results = []
    
    if args.file:
        results.append(validate_file(args.file, args.strict))
    elif args.dir:
        for filepath in sorted(Path(args.dir).glob('*.md')):
            if filepath.name.startswith('INDEX'):
                continue  # 跳过索引文件
            results.append(validate_file(str(filepath), args.strict))
    
    # 输出结果
    total = len(results)
    valid = sum(1 for r in results if r['valid'])
    total_issues = sum(len(r['issues']) for r in results)
    total_warnings = sum(len(r['warnings']) for r in results)
    total_points = sum(r['knowledge_points'] for r in results)
    
    print(f"📊 验证完成")
    print(f"  总文件数：{total}")
    print(f"  有效文件：{valid}")
    print(f"  问题文件：{total - valid}")
    print(f"  问题数：{total_issues}")
    print(f"  警告数：{total_warnings}")
    print(f"  知识点总数：{total_points}")
    
    # 显示问题文件
    error_files = [r for r in results if not r['valid']]
    if error_files:
        print(f"\n❌ 问题文件:")
        for r in error_files:
            print(f"\n  {r['file']}")
            for issue in r['issues']:
                print(f"    - {issue}")
    
    # 显示警告
    warning_files = [r for r in results if r['warnings']]
    if warning_files:
        print(f"\n⚠️  警告:")
        for r in warning_files[:5]:  # 只显示前 5 个
            print(f"\n  {r['file']}")
            for warning in r['warnings']:
                print(f"    - {warning}")
        if len(warning_files) > 5:
            print(f"\n  ... 还有 {len(warning_files) - 5} 个文件有警告")
    
    # 生成报告
    if args.report:
        with open(args.report, 'w', encoding='utf-8') as f:
            f.write(f"# 知识验证报告\n\n")
            f.write(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"## 总览\n\n")
            f.write(f"- 总文件数：{total}\n")
            f.write(f"- 有效文件：{valid}\n")
            f.write(f"- 问题文件：{total - valid}\n")
            f.write(f"- 知识点总数：{total_points}\n\n")
            
            if error_files:
                f.write(f"## 问题文件\n\n")
                for r in error_files:
                    f.write(f"### {r['file']}\n\n")
                    for issue in r['issues']:
                        f.write(f"- ❌ {issue}\n")
                    f.write("\n")
        
        print(f"\n📁 报告已保存到：{args.report}")

if __name__ == '__main__':
    main()
