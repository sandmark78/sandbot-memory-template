#!/usr/bin/env python3
"""
V6.2.8 通知模块 - Telegram 通知 + 日志记录

功能:
- Telegram 通知发送
- 通知频率限制 (同类通知间隔>=1 小时)
- 通知历史记录
- 多级别通知 (info/warning/error/success)

使用:
python3 notify.py --level warning --message "测试通知"
"""

import json
import sys
import time
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, List

# 导入统一配置
from config import SKILL_DIR, DATA_DIR

# 通知配置文件
NOTIFY_HISTORY_FILE = DATA_DIR / "notify_history.json"
NOTIFY_RATE_LIMIT = 3600  # 1 小时 (秒)


class NotificationManager:
    """通知管理器 - 频率限制 + 历史记录"""
    
    EMOJIS = {
        'info': 'ℹ️',
        'warning': '⚠️',
        'error': '❌',
        'success': '✅',
        'milestone': '🎉'
    }
    
    def __init__(self):
        self.history = self._load_history()
    
    def _load_history(self) -> dict:
        """加载通知历史"""
        if NOTIFY_HISTORY_FILE.exists():
            try:
                with open(NOTIFY_HISTORY_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return {"notifications": [], "last_sent": {}}
    
    def _save_history(self):
        """保存通知历史"""
        NOTIFY_HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(NOTIFY_HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, indent=2, ensure_ascii=False)
    
    def _should_send(self, category: str) -> bool:
        """检查是否应该发送 (频率限制)"""
        last_sent = self.history.get("last_sent", {}).get(category, 0)
        return (time.time() - last_sent) >= NOTIFY_RATE_LIMIT
    
    def _record_sent(self, category: str, level: str, message: str):
        """记录已发送的通知"""
        # 更新最后发送时间
        if "last_sent" not in self.history:
            self.history["last_sent"] = {}
        self.history["last_sent"][category] = time.time()
        
        # 添加到历史记录
        notification = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "category": category,
            "message": message
        }
        
        if "notifications" not in self.history:
            self.history["notifications"] = []
        
        # 保留最近 100 条
        self.history["notifications"].append(notification)
        self.history["notifications"] = self.history["notifications"][-100:]
        
        self._save_history()
    
    def send_telegram(self, message: str, level: str = 'info') -> bool:
        """
        发送 Telegram 通知
        
        注意：实际发送需要通过 OpenClaw message 工具或 Telegram Bot API
        这里记录通知内容，实际发送由调用方处理
        """
        emoji = self.EMOJIS.get(level, 'ℹ️')
        formatted = f"{emoji} **Task Manager**: {message}"
        
        # 记录到日志
        print(f"[TELEGRAM] {formatted}")
        
        # 实际发送需要通过 OpenClaw 或 Bot API
        # 这里输出到 stdout，由 cron 日志捕获
        return True
    
    def send(self, category: str, message: str, level: str = 'info', force: bool = False) -> bool:
        """
        发送通知 (带频率限制)
        
        Args:
            category: 通知类别 (如 "lagging_domain", "data_sync", "milestone")
            message: 通知内容
            level: 通知级别 (info/warning/error/success/milestone)
            force: 是否忽略频率限制
        
        Returns:
            bool: 是否成功发送
        """
        # 检查频率限制
        if not force and not self._should_send(category):
            print(f"[SKIP] 频率限制：{category} (1 小时内已发送)")
            return False
        
        # 发送通知
        if self.send_telegram(message, level):
            self._record_sent(category, level, message)
            print(f"[SENT] {category}: {message}")
            return True
        
        return False
    
    def get_history(self, limit: int = 10) -> List[dict]:
        """获取最近通知历史"""
        notifications = self.history.get("notifications", [])
        return notifications[-limit:]
    
    def check_lagging_domains(self, progress_data: dict, force: bool = False) -> List[dict]:
        """
        检查滞后领域并发送通知
        
        Args:
            progress_data: 进度数据 (包含 domains 字段)
            force: 是否忽略频率限制
        
        Returns:
            List[dict]: 滞后领域列表
        """
        domains = progress_data.get("domains", {})
        avg_progress = progress_data.get("percentage", 0)
        
        # 滞后阈值：低于平均进度的 50%
        lagging_threshold = avg_progress * 0.5
        
        lagging = []
        for domain_id, domain_data in domains.items():
            domain_progress = domain_data.get("percentage", 0)
            if domain_progress < lagging_threshold:
                lagging.append({
                    "id": domain_id,
                    "name": domain_data.get("name", domain_id),
                    "progress": domain_progress,
                    "gap": avg_progress - domain_progress
                })
        
        # 发送通知
        if lagging:
            lagging_sorted = sorted(lagging, key=lambda x: x["progress"])
            top_lagging = lagging_sorted[0]
            
            message = (
                f"滞后领域预警：{top_lagging['name']} ({top_lagging['id']})\n"
                f"进度：{top_lagging['progress']:.1f}% (平均：{avg_progress:.1f}%)\n"
                f"差距：{top_lagging['gap']:.1f}%\n"
                f"建议：优先填充该领域知识点"
            )
            
            self.send(
                category="lagging_domain",
                message=message,
                level="warning",
                force=force
            )
        
        return lagging
    
    def notify_milestone(self, progress_data: dict, force: bool = False):
        """
        检查进度里程碑并发送通知
        
        里程碑：25%, 50%, 75%, 100%
        """
        percentage = progress_data.get("percentage", 0)
        milestones = [25, 50, 75, 100]
        
        for milestone in milestones:
            category = f"milestone_{milestone}"
            
            # 检查是否刚达到里程碑
            if percentage >= milestone:
                # 检查是否已通知过
                if self._should_send(category) or force:
                    message = (
                        f"🎉 进度里程碑：{milestone}%!\n"
                        f"当前：{progress_data.get('current', 0)}/{progress_data.get('total_target', 0)}\n"
                        f"速度：{progress_data.get('speed', 0)} 知识点/分钟\n"
                        f"预计：{progress_data.get('estimated_minutes', 0):.1f} 分钟完成"
                    )
                    
                    self.send(
                        category=category,
                        message=message,
                        level="milestone",
                        force=force
                    )
    
    def notify_data_sync(self, issues: List[str], total: int, force: bool = False):
        """
        数据同步结果通知
        
        Args:
            issues: 数据不一致问题列表
            total: 实际知识点数
            force: 是否忽略频率限制
        """
        if issues:
            message = (
                f"⚠️ 数据不一致检测\n"
                f"发现 {len(issues)} 个问题:\n" +
                "\n".join(f"  - {issue}" for issue in issues[:3]) +
                f"\n已自动同步：{total} 知识点"
            )
            
            self.send(
                category="data_sync",
                message=message,
                level="warning",
                force=force
            )
        else:
            # 只在首次或强制时发送成功通知
            if force:
                message = f"✅ 数据一致性检查通过：{total} 知识点"
                self.send(
                    category="data_sync_ok",
                    message=message,
                    level="success",
                    force=force
                )


def main():
    parser = argparse.ArgumentParser(description='V6.2.8 通知模块')
    parser.add_argument('--level', '-l', type=str, default='info',
                       choices=['info', 'warning', 'error', 'success', 'milestone'],
                       help='通知级别')
    parser.add_argument('--message', '-m', type=str, required=True,
                       help='通知内容')
    parser.add_argument('--category', '-c', type=str, default='manual',
                       help='通知类别')
    parser.add_argument('--force', '-f', action='store_true',
                       help='忽略频率限制')
    parser.add_argument('--history', action='store_true',
                       help='显示通知历史')
    args = parser.parse_args()
    
    manager = NotificationManager()
    
    if args.history:
        history = manager.get_history(limit=10)
        print("最近通知历史:")
        for n in reversed(history):
            print(f"  [{n['timestamp']}] {n['level']}: {n['message'][:50]}...")
    else:
        success = manager.send(
            category=args.category,
            message=args.message,
            level=args.level,
            force=args.force
        )
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
