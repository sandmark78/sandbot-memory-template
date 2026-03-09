#!/usr/bin/env python3
"""
V6.2.5 数据验证器 - 全面数据一致性检查

优化点:
- 统一配置中心
- 并行扫描加速
- 详细验证报告
- 自动修复建议
- JSON 报告导出

使用:
python3 validate_data.py [--export]
"""

import json
import sys
import time
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Tuple, List

# 导入统一配置
from config import (
    WORKSPACE, KNOWLEDGE_BASE, SKILL_DIR,
    TASKS_FILE, PROGRESS_FILE, EVOLUTION_FILE, VALIDATION_FILE,
    DOMAINS, get_total_target, ensure_dirs
)


class DataValidator:
    """数据验证器 - 核心逻辑"""
    
    def __init__(self):
        self.start_time = None
        self.issues: List[str] = []
        self.warnings: List[str] = []
        self.stats = {
            "files_checked": 0,
            "domains_scanned": 0,
            "issues_found": 0,
            "warnings_found": 0,
        }
    
    def count_domain(self, domain_id: str) -> int:
        """统计单个领域的知识点数 (用于并行)"""
        domain_dir = KNOWLEDGE_BASE / domain_id
        if not domain_dir.exists():
            return 0
        
        md_files = list(domain_dir.glob("*.md"))
        return len([f for f in md_files if f.is_file()])
    
    def count_actual_knowledge_points(self) -> Tuple[Dict[str, int], int]:
        """并行统计实际知识点文件"""
        domain_counts = {}
        total = 0
        
        with ThreadPoolExecutor(max_workers=4) as executor:
            future_to_domain = {
                executor.submit(self.count_domain, domain_id): domain_id
                for domain_id in DOMAINS.keys()
            }
            
            for future in as_completed(future_to_domain):
                domain_id = future_to_domain[future]
                try:
                    count = future.result()
                    domain_counts[domain_id] = count
                    total += count
                    self.stats["domains_scanned"] += 1
                except Exception as e:
                    print(f"   ⚠️  扫描 {domain_id} 失败：{e}")
                    domain_counts[domain_id] = 0
        
        return domain_counts, total
    
    def load_json_file(self, file_path: Path, default=None) -> dict:
        """安全加载 JSON 文件"""
        self.stats["files_checked"] += 1
        if not file_path.exists():
            return default
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            self.issues.append(f"JSON 解析错误 {file_path}: {e}")
            return default
    
    def validate_all(self) -> dict:
        """执行全面验证"""
        self.start_time = time.time()
        
        print("🔍 V6.2.5 数据验证器")
        print("=" * 70)
        print()
        
        # 加载所有数据文件
        print("📂 加载数据文件...")
        progress = self.load_json_file(PROGRESS_FILE, {})
        evolution = self.load_json_file(EVOLUTION_FILE, {})
        tasks = self.load_json_file(TASKS_FILE, [])
        
        # 统计实际知识点
        print("📈 扫描知识库...")
        actual_counts, actual_total = self.count_actual_knowledge_points()
        
        print()
        print("📊 验证报告")
        print("=" * 70)
        print()
        
        # 1. 知识点统计验证
        progress_total = progress.get("current", 0) if progress else 0
        progress_match = progress_total == actual_total
        
        if not progress_match:
            self.issues.append(f"progress.json 数据不一致：记录={progress_total}, 实际={actual_total}")
        
        print(f"1️⃣ 知识点统计验证")
        print(f"   progress.json 记录：{progress_total}")
        print(f"   实际文件统计：{actual_total}")
        print(f"   状态：{'✅ 一致' if progress_match else '❌ 不一致'}")
        print()
        
        # 2. 进化数据验证
        evolution_kp = evolution.get("stats", {}).get("knowledge_points", 0) if evolution else 0
        evolution_match = evolution_kp == progress_total
        
        if not evolution_match:
            self.warnings.append(f"evolution.json 与 progress.json 不一致：evolution={evolution_kp}, progress={progress_total}")
        
        print(f"2️⃣ 进化数据验证")
        print(f"   evolution.json 记录：{evolution_kp}")
        print(f"   progress.json 记录：{progress_total}")
        print(f"   状态：{'✅ 一致' if evolution_match else '⚠️ 不一致'}")
        print()
        
        # 3. 任务状态验证
        total_tasks = len(tasks) if isinstance(tasks, list) else 0
        completed_tasks = len([t for t in (tasks if isinstance(tasks, list) else []) if t.get("status") == "completed"])
        pending_tasks = len([t for t in (tasks if isinstance(tasks, list) else []) if t.get("status") == "pending"])
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        print(f"3️⃣ 任务状态验证")
        print(f"   总任务数：{total_tasks}")
        print(f"   已完成：{completed_tasks}")
        print(f"   待执行：{pending_tasks}")
        print(f"   完成率：{completion_rate:.1f}%" if total_tasks > 0 else "   完成率：N/A")
        print()
        
        # 4. 领域分布验证
        print(f"4️⃣ 领域分布验证")
        print(f"   {'领域':<20} {'记录':>6} {'实际':>6} {'状态':>8}")
        print(f"   {'-'*20} {'-'*6} {'-'*6} {'-'*8}")
        
        progress_domains = progress.get("domains", {}) if progress else {}
        mismatch_count = 0
        
        for domain_id, actual_count in actual_counts.items():
            recorded = progress_domains.get(domain_id, {}).get("current", 0)
            match = recorded == actual_count
            status = "✅" if match else "❌"
            
            if not match:
                mismatch_count += 1
            
            print(f"   {domain_id:<12} {recorded:>6} {actual_count:>6} {status:>8}")
        
        if mismatch_count > 0:
            self.warnings.append(f"{mismatch_count} 个领域数据不匹配")
        
        print()
        
        # 5. 文件完整性检查
        print(f"5️⃣ 文件完整性检查")
        required_files = [
            ("SKILL.md", SKILL_DIR / "SKILL.md"),
            ("README.md", SKILL_DIR / "README.md"),
            ("tasks.json", TASKS_FILE),
            ("progress.json", PROGRESS_FILE),
            ("evolution.json", EVOLUTION_FILE),
            ("config.py", SKILL_DIR / "scripts" / "config.py"),
            ("progress_tracker.py", SKILL_DIR / "scripts" / "progress_tracker.py"),
            ("auto_sync.py", SKILL_DIR / "scripts" / "auto_sync.py"),
            ("validate_data.py", SKILL_DIR / "scripts" / "validate_data.py"),
        ]
        
        missing_files = []
        for name, path in required_files:
            self.stats["files_checked"] += 1
            exists = path.exists()
            status = "✅" if exists else "❌"
            size = path.stat().st_size if path.exists() else 0
            
            if not exists:
                missing_files.append(name)
            
            print(f"   {name:<25} {status} ({size} bytes)" if exists else f"   {name:<25} {status}")
        
        if missing_files:
            self.warnings.append(f"缺失文件：{', '.join(missing_files)}")
        
        print()
        
        # 6. 脚本可执行检查
        print(f"6️⃣ 脚本权限检查")
        scripts_dir = SKILL_DIR / "scripts"
        scripts = [
            "task_manager.py",
            "evolution_loop.py",
            "progress_tracker.py",
            "auto_sync.py",
            "validate_data.py",
            "batch_ops.py",
        ]
        
        for script in scripts:
            path = scripts_dir / script
            self.stats["files_checked"] += 1
            exists = path.exists()
            executable = exists and (path.stat().st_mode & 0o111)
            status = "✅" if exists else "❌"
            exec_status = "🚀" if executable else ""
            
            print(f"   {script:<25} {status} {exec_status}")
        
        print()
        
        # 汇总报告
        print("=" * 70)
        print("📊 验证汇总")
        print()
        
        self.stats["issues_found"] = len(self.issues)
        self.stats["warnings_found"] = len(self.warnings)
        
        if self.issues:
            print(f"❌ 严重问题 ({len(self.issues)}个):")
            for issue in self.issues:
                print(f"   - {issue}")
            print()
        
        if self.warnings:
            print(f"⚠️  警告 ({len(self.warnings)}个):")
            for warning in self.warnings:
                print(f"   - {warning}")
            print()
        
        if not self.issues and not self.warnings:
            print("✅ 所有检查通过！数据一致性良好")
            print()
        
        # 性能统计
        elapsed = time.time() - self.start_time
        print(f"⏱️  验证耗时：{elapsed:.2f}秒")
        print(f"📈 统计：检查文件={self.stats['files_checked']}, 扫描领域={self.stats['domains_scanned']}")
        print()
        
        # 修复建议
        if self.issues or self.warnings:
            print("🔧 修复建议:")
            if progress_total != actual_total:
                print(f"   1. 运行 progress_tracker.py 重新同步进度数据")
            if evolution_kp != progress_total:
                print(f"   2. 运行 auto_sync.py --force 强制同步")
            if missing_files:
                print(f"   3. 检查缺失文件是否被误删")
            print()
        
        # 生成验证结果
        result = {
            "timestamp": datetime.now().isoformat(),
            "issues_count": len(self.issues),
            "warnings_count": len(self.warnings),
            "actual_knowledge_points": actual_total,
            "progress_recorded": progress_total,
            "evolution_recorded": evolution_kp,
            "tasks_total": total_tasks,
            "tasks_completed": completed_tasks,
            "completion_rate": round(completion_rate, 2),
            "issues": self.issues,
            "warnings": self.warnings,
            "performance": {
                "elapsed_seconds": round(elapsed, 2),
                "files_checked": self.stats["files_checked"],
                "domains_scanned": self.stats["domains_scanned"]
            }
        }
        
        return result


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='V6.2.5 数据验证器')
    parser.add_argument('--export', '-e', action='store_true', help='导出 JSON 报告')
    parser.add_argument('--quiet', '-q', action='store_true', help='静默模式')
    args = parser.parse_args()
    
    validator = DataValidator()
    result = validator.validate_all()
    
    # 保存验证报告
    VALIDATION_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(VALIDATION_FILE, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 验证报告已保存：{VALIDATION_FILE}")
    
    # 导出 JSON 报告 (如果需要)
    if args.export:
        from config import REPORTS_DIR
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_path = REPORTS_DIR / f"validation_{timestamp}.json"
        with open(export_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"📄 报告已导出：{export_path}")
    
    # 如果有严重问题，返回错误码
    if result["issues_count"] > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
