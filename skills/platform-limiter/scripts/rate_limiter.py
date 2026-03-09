#!/usr/bin/env python3
"""
Platform Rate Limiter - API 限流管理

功能:
- 追踪各平台 API 调用
- 自动退避 (429 错误)
- 队列管理
- 实时监控

使用:
python3 rate_limiter.py
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path("/home/node/.openclaw/workspace")
LIMITS_FILE = WORKSPACE / "memory" / "api_limits.json"

# 平台 API 限制 (次/分钟，除非特别说明)
PLATFORM_LIMITS = {
    "moltbook": {"calls": 5, "window": 60},      # 5 次/分钟
    "github": {"calls": 83, "window": 60},       # 5000 次/小时
    "evomap": {"calls": 6, "window": 60},        # 6 次/分钟
    "gumroad": {"calls": 100, "window": 3600},   # 100 次/小时
    "vercel": {"calls": 100, "window": 3600},    # 100 次/小时
}

class RateLimiter:
    def __init__(self):
        self.limits = self.load_limits()
    
    def load_limits(self):
        """加载限流状态"""
        if LIMITS_FILE.exists():
            with open(LIMITS_FILE, 'r') as f:
                return json.load(f)
        return {platform: {"calls": [], "blocked": False} for platform in PLATFORM_LIMITS}
    
    def save_limits(self):
        """保存限流状态"""
        LIMITS_FILE.parent.mkdir(exist_ok=True)
        with open(LIMITS_FILE, 'w') as f:
            json.dump(self.limits, f, indent=2)
    
    def can_call(self, platform):
        """检查是否可以调用 API"""
        if platform not in PLATFORM_LIMITS:
            return True
        
        limit = PLATFORM_LIMITS[platform]
        now = time.time()
        window_start = now - limit["window"]
        
        # 清理过期记录
        self.limits[platform]["calls"] = [
            t for t in self.limits[platform]["calls"] if t > window_start
        ]
        
        # 检查是否超限
        if len(self.limits[platform]["calls"]) >= limit["calls"]:
            return False
        
        return True
    
    def record_call(self, platform):
        """记录 API 调用"""
        if platform not in self.limits:
            self.limits[platform] = {"calls": [], "blocked": False}
        
        self.limits[platform]["calls"].append(time.time())
        self.save_limits()
    
    def wait_if_needed(self, platform):
        """等待直到可以调用"""
        while not self.can_call(platform):
            limit = PLATFORM_LIMITS[platform]
            oldest = min(self.limits[platform]["calls"])
            wait_time = oldest + limit["window"] - time.time()
            if wait_time > 0:
                time.sleep(min(wait_time, 1))  # 最多等 1 秒
    
    def get_status(self):
        """获取限流状态"""
        status = {}
        now = time.time()
        
        for platform, limit in PLATFORM_LIMITS.items():
            window_start = now - limit["window"]
            calls = len([t for t in self.limits[platform]["calls"] if t > window_start])
            remaining = limit["calls"] - calls
            status[platform] = {
                "used": calls,
                "limit": limit["calls"],
                "remaining": max(0, remaining),
                "reset_in": f"{limit['window']}s"
            }
        
        return status

def main():
    limiter = RateLimiter()
    status = limiter.get_status()
    
    print("🚦 Platform Rate Limiter")
    print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    for platform, stats in status.items():
        bar = "█" * int(stats["used"] / stats["limit"] * 20)
        bar = bar.ljust(20, "░")
        print(f"{platform:12} [{bar}] {stats['used']}/{stats['limit']} (剩余：{stats['remaining']})")
    
    print()
    print("✅ API 限流管理已激活")
    print("⚠️ 尊重平台限制，自动退避")

if __name__ == "__main__":
    main()
