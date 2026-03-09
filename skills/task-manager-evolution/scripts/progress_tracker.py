#!/usr/bin/env python3
"""
V6.2.6 进度追踪器 - 高性能实时统计 + 趋势分析

优化点:
- 智能缓存 (文件修改时间 + TTL 双重验证)
- 动态并行 (根据 CPU 核心数调整 worker 数量)
- 增量更新 (只扫描变更目录)
- 趋势分析 (速度历史记录 + 预测)
- 预警系统 (滞后领域 + 速度下降提醒)
- JSON 输出 (支持程序化调用)
- 交互式仪表板 (实时刷新)

使用:
python3 progress_tracker.py [options]

示例:
python3 progress_tracker.py --force           # 强制重新扫描
python3 progress_tracker.py --json            # JSON 输出
python3 progress_tracker.py --watch           # 实时监控模式
python3 progress_tracker.py --export csv      # 导出 CSV 报告
"""

import json
import sys
import time
import argparse
import os
from datetime import datetime, timedelta
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Tuple, Optional, List
import hashlib

# 导入统一配置
from config import (
    WORKSPACE, KNOWLEDGE_BASE, PROGRESS_FILE, EVOLUTION_FILE,
    DOMAINS, CACHE_FILE, DATA_DIR, REPORTS_DIR,
    get_total_target, SPEED_TARGET, SPEED_WARNING, PROGRESS_WARNING,
    CACHE_TTL, ensure_dirs
)


class FileCacheManager:
    """文件缓存管理器 - 基于文件修改时间 + TTL 双重验证"""
    
    def __init__(self, cache_file: Path = CACHE_FILE):
        self.cache_file = cache_file
        self.cache = self._load()
    
    def _load(self) -> dict:
        """加载缓存"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return {"timestamp": 0, "domain_counts": {}, "total": 0, "file_hashes": {}}
    
    def save(self):
        """保存缓存"""
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(self.cache, f, indent=2, ensure_ascii=False)
    
    def _get_domain_hash(self, domain_id: str) -> str:
        """计算领域目录的文件哈希"""
        domain_dir = KNOWLEDGE_BASE / domain_id
        if not domain_dir.exists():
            return ""
        
        hasher = hashlib.md5()
        for f in sorted(domain_dir.glob("*.md")):
            if f.is_file():
                hasher.update(f"{f.name}:{f.stat().st_mtime}:{f.stat().st_size}".encode())
        return hasher.hexdigest()
    
    def is_valid(self, domain_ids: List[str] = None) -> bool:
        """检查缓存是否有效 (TTL + 文件修改时间)"""
        age = time.time() - self.cache.get("timestamp", 0)
        if age >= CACHE_TTL:
            return False
        
        # 检查文件是否变更
        if domain_ids is None:
            domain_ids = list(DOMAINS.keys())
        
        for domain_id in domain_ids:
            current_hash = self._get_domain_hash(domain_id)
            cached_hash = self.cache.get("file_hashes", {}).get(domain_id, "")
            if current_hash != cached_hash:
                return False
        
        return True
    
    def get(self) -> Tuple[Dict[str, int], int]:
        """获取缓存数据"""
        return self.cache.get("domain_counts", {}), self.cache.get("total", 0)
    
    def update(self, domain_counts: Dict[str, int], total: int, domain_ids: List[str] = None):
        """更新缓存"""
        if domain_ids is None:
            domain_ids = list(DOMAINS.keys())
        
        file_hashes = {}
        for domain_id in domain_ids:
            file_hashes[domain_id] = self._get_domain_hash(domain_id)
        
        self.cache.update({
            "timestamp": time.time(),
            "domain_counts": domain_counts,
            "total": total,
            "file_hashes": file_hashes
        })
        self.save()


class TrendAnalyzer:
    """趋势分析器 - 速度历史 + 预测"""
    
    def __init__(self, evolution_file: Path = EVOLUTION_FILE):
        self.evolution_file = evolution_file
        self.history = self._load_history()
    
    def _load_history(self) -> List[dict]:
        """加载历史记录"""
        if self.evolution_file.exists():
            try:
                with open(self.evolution_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get("cycle_history", [])[-20:]  # 最近 20 次
            except (json.JSONDecodeError, IOError):
                pass
        return []
    
    def calculate_trend(self) -> dict:
        """计算趋势"""
        if len(self.history) < 2:
            return {"trend": "stable", "change": 0, "prediction": "unknown"}
        
        # 提取速度数据
        speeds = []
        for cycle in self.history[-10:]:  # 最近 10 次
            outcome = cycle.get("outcome", "")
            if "知识点" in outcome:
                try:
                    # 尝试从 outcome 提取速度
                    parts = outcome.split()
                    for part in parts:
                        if part.isdigit():
                            speeds.append(int(part))
                            break
                except:
                    pass
        
        if len(speeds) < 2:
            return {"trend": "stable", "change": 0, "prediction": "unknown"}
        
        # 计算趋势
        recent_avg = sum(speeds[-3:]) / len(speeds[-3:])
        older_avg = sum(speeds[:3]) / min(3, len(speeds))
        
        change = ((recent_avg - older_avg) / older_avg * 100) if older_avg > 0 else 0
        
        if change > 10:
            trend = "improving"
        elif change < -10:
            trend = "declining"
        else:
            trend = "stable"
        
        return {
            "trend": trend,
            "change": round(change, 2),
            "recent_speed": round(recent_avg, 1),
            "prediction": f"{trend} ({change:+.1f}%)"
        }


class ProgressTracker:
    """进度追踪器 - 核心逻辑"""
    
    def __init__(self, use_cache: bool = True):
        self.use_cache = use_cache
        self.cache = FileCacheManager() if use_cache else None
        self.start_time = None
        self.trend_analyzer = TrendAnalyzer()
    
    def count_domain(self, domain_id: str) -> int:
        """统计单个领域的知识点数 (用于并行)"""
        domain_dir = KNOWLEDGE_BASE / domain_id
        if not domain_dir.exists():
            return 0
        
        md_files = list(domain_dir.glob("*.md"))
        return len([f for f in md_files if f.is_file()])
    
    def count_knowledge_points(self, force: bool = False) -> Tuple[Dict[str, int], int]:
        """扫描知识库统计实际知识点数量"""
        # 检查缓存
        if self.use_cache and self.cache and not force:
            if self.cache.is_valid():
                domain_counts, total = self.cache.get()
                return domain_counts, total
        
        # 动态调整 worker 数量
        cpu_count = os.cpu_count() or 4
        worker_count = min(cpu_count, 8)  # 最多 8 个 worker
        
        # 并行扫描所有领域
        domain_counts = {}
        total = 0
        
        print(f"   🔍 并行扫描 {len(DOMAINS)} 个知识领域 ({worker_count} workers)...")
        
        with ThreadPoolExecutor(max_workers=worker_count) as executor:
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
                except Exception as e:
                    print(f"   ⚠️  扫描 {domain_id} 失败：{e}")
                    domain_counts[domain_id] = 0
        
        # 更新缓存
        if self.use_cache and self.cache:
            self.cache.update(domain_counts, total)
        
        return domain_counts, total
    
    def calculate_speed(self) -> int:
        """计算填充速度 (知识点/分钟)"""
        # 从进化数据读取历史速度
        if EVOLUTION_FILE.exists():
            try:
                with open(EVOLUTION_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    speed = data.get("stats", {}).get("speed", 300)
                    if speed > 0:
                        return speed
            except (json.JSONDecodeError, IOError):
                pass
        return 300  # 默认速度
    
    def generate_report(self, domain_counts: Dict[str, int], total: int) -> dict:
        """生成进度报告"""
        total_target = get_total_target()
        percentage = (total / total_target) * 100 if total_target > 0 else 0
        speed = self.calculate_speed()
        
        # 计算预计时间
        remaining = total_target - total
        estimated_minutes = remaining / speed if speed > 0 else 0
        
        # 趋势分析
        trend = self.trend_analyzer.calculate_trend()
        
        # 生成领域详情
        domains_detail = {}
        lagging_domains = []
        
        for domain_id, count in domain_counts.items():
            target = DOMAINS[domain_id]["target"]
            name = DOMAINS[domain_id]["name"]
            pct = (count / target) * 100 if target > 0 else 0
            
            domains_detail[domain_id] = {
                "name": name,
                "target": target,
                "current": count,
                "percentage": round(pct, 2)
            }
            
            # 检查是否滞后
            if pct < PROGRESS_WARNING:
                lagging_domains.append({
                    "id": domain_id,
                    "name": name,
                    "progress": pct
                })
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_target": total_target,
            "current": total,
            "percentage": round(percentage, 2),
            "remaining": remaining,
            "speed": speed,
            "estimated_minutes": round(estimated_minutes, 1),
            "domains": domains_detail,
            "lagging_domains": lagging_domains,
            "trend": trend,
            "performance": {
                "scan_time_ms": round((time.time() - self.start_time) * 1000, 2) if self.start_time else 0,
                "speed_status": self._get_speed_status(speed),
                "progress_status": self._get_progress_status(percentage),
                "cache_used": self.use_cache and self.cache and not self.cache.is_valid() == False
            }
        }
        
        return report
    
    def _get_speed_status(self, speed: int) -> str:
        """获取速度状态"""
        if speed >= SPEED_TARGET:
            return "EXCELLENT"
        elif speed >= SPEED_WARNING:
            return "NORMAL"
        elif speed >= SPEED_WARNING / 3:
            return "WARNING"
        else:
            return "CRITICAL"
    
    def _get_progress_status(self, percentage: float) -> str:
        """获取进度状态"""
        if percentage >= 80:
            return "EXCELLENT"
        elif percentage >= 50:
            return "NORMAL"
        elif percentage >= 25:
            return "WARNING"
        else:
            return "CRITICAL"
    
    def print_report(self, report: dict):
        """打印进度报告"""
        print()
        print("📊 10000 知识点冲刺进度 (V6.2.6)")
        print("=" * 70)
        print()
        
        # 总体进度
        status_icon = {
            "EXCELLENT": "✅",
            "NORMAL": "🟢",
            "WARNING": "⚠️",
            "CRITICAL": "❌"
        }
        
        perf = report.get("performance", {})
        speed_status = status_icon.get(perf.get("speed_status", "NORMAL"), "🟢")
        progress_status = status_icon.get(perf.get("progress_status", "NORMAL"), "🟢")
        
        # 趋势图标
        trend = report.get("trend", {})
        trend_icon = {
            "improving": "📈",
            "declining": "📉",
            "stable": "➡️"
        }.get(trend.get("trend", "stable"), "➡️")
        
        print(f"   总进度：{report['current']}/{report['total_target']} ({report['percentage']}%) {progress_status}")
        print(f"   剩余：{report['remaining']} 知识点")
        print(f"   速度：{report['speed']} 知识点/分钟 {speed_status}")
        print(f"   趋势：{trend_icon} {trend.get('prediction', 'unknown')}")
        print(f"   预计完成：{report['estimated_minutes']} 分钟")
        print(f"   扫描耗时：{perf.get('scan_time_ms', 0):.0f}ms")
        print(f"   缓存：{'✅ 命中' if perf.get('cache_used') else '❌ 未命中'}")
        print()
        
        # 领域分布
        print("📁 领域分布:")
        print()
        print(f"   {'领域':<20} {'目标':>6} {'当前':>6} {'进度':>10}")
        print(f"   {'-'*20} {'-'*6} {'-'*6} {'-'*10}")
        
        for domain_id, info in sorted(report['domains'].items()):
            bar_len = int(info['percentage'] / 5)
            bar = "█" * bar_len + "░" * (20 - bar_len)
            
            # 滞后领域标红
            if info['percentage'] < PROGRESS_WARNING:
                print(f"   {domain_id:<12} {info['target']:>6} {info['current']:>6} {bar} {info['percentage']:>5.1f}% ⚠️")
            else:
                print(f"   {domain_id:<12} {info['target']:>6} {info['current']:>6} {bar} {info['percentage']:>5.1f}%")
        
        print()
        
        # 预警信息
        if report.get('lagging_domains'):
            print("⚠️  滞后领域预警:")
            for domain in report['lagging_domains'][:5]:  # 只显示前 5 个
                print(f"   - {domain['name']} ({domain['id']}): {domain['progress']:.1f}%")
            print()
        
        print("=" * 70)
    
    def save_progress(self, report: dict) -> Path:
        """保存进度到文件"""
        PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        return PROGRESS_FILE
    
    def export_report(self, report: dict, format: str = 'json') -> Optional[Path]:
        """导出报告"""
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format == 'json':
            path = REPORTS_DIR / f"progress_{timestamp}.json"
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            return path
        
        elif format == 'csv':
            path = REPORTS_DIR / f"progress_{timestamp}.csv"
            with open(path, 'w', encoding='utf-8') as f:
                f.write("领域，目标，当前，进度%\n")
                for domain_id, info in report['domains'].items():
                    f.write(f"{domain_id},{info['target']},{info['current']},{info['percentage']}\n")
                f.write(f"\n总计，{report['total_target']},{report['current']},{report['percentage']}\n")
            return path
        
        return None
    
    def run(self, force: bool = False, export: str = None, quiet: bool = False, json_output: bool = False) -> dict:
        """执行进度追踪"""
        self.start_time = time.time()
        
        if not quiet and not json_output:
            print("🚀 V6.2.6 进度追踪器")
            print()
        
        # 统计知识点
        domain_counts, total = self.count_knowledge_points(force)
        
        if not quiet and not json_output:
            print(f"   实际知识点：{total}")
            print()
        
        # 生成报告
        report = self.generate_report(domain_counts, total)
        
        # JSON 输出模式
        if json_output:
            print(json.dumps(report, indent=2, ensure_ascii=False))
            return report
        
        # 打印报告
        if not quiet:
            self.print_report(report)
        
        # 保存进度
        saved_path = self.save_progress(report)
        if not quiet:
            print(f"✅ 进度已保存：{saved_path}")
        
        # 导出报告
        if export:
            export_path = self.export_report(report, export)
            if export_path:
                print(f"📄 报告已导出：{export_path}")
        
        # 检查是否需要加速
        if report['percentage'] < 50 and not quiet:
            print()
            print("⚠️  进度滞后！建议启动自我进化循环优化策略")
            print("   命令：python3 evolution_loop.py")
        
        return report


def main():
    parser = argparse.ArgumentParser(description='V6.2.6 进度追踪器')
    parser.add_argument('--force', '-f', action='store_true', help='强制重新扫描，忽略缓存')
    parser.add_argument('--no-cache', action='store_true', help='禁用缓存')
    parser.add_argument('--export', '-e', choices=['json', 'csv'], help='导出报告格式')
    parser.add_argument('--json', '-j', action='store_true', help='JSON 输出模式 (程序化调用)')
    parser.add_argument('--quiet', '-q', action='store_true', help='静默模式，只保存不输出')
    parser.add_argument('--watch', '-w', action='store_true', help='实时监控模式 (每 5 秒刷新)')
    args = parser.parse_args()
    
    if args.watch:
        # 实时监控模式
        try:
            print("📺 实时监控模式 (Ctrl+C 退出)")
            while True:
                os.system('clear' if os.name != 'nt' else 'cls')
                tracker = ProgressTracker(use_cache=not args.no_cache)
                tracker.run(force=False, quiet=False, json_output=False)
                time.sleep(5)
        except KeyboardInterrupt:
            print("\n👋 退出监控模式")
            sys.exit(0)
    else:
        tracker = ProgressTracker(use_cache=not args.no_cache)
        tracker.run(force=args.force, export=args.export, quiet=args.quiet, json_output=args.json)


if __name__ == "__main__":
    main()
