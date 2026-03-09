#!/usr/bin/env python3
"""
V6.2.5 配置中心 - 统一管理所有配置

功能:
- 集中管理路径配置
- 知识领域定义
- 全局常量
- 配置加载/保存

使用:
from config import Config, DOMAINS
"""

import json
from pathlib import Path
from typing import Dict, Any

# ============================================================================
# 路径配置
# ============================================================================

WORKSPACE = Path("/home/node/.openclaw/workspace")
SKILL_DIR = WORKSPACE / "skills" / "task-manager-evolution"
KNOWLEDGE_BASE = WORKSPACE / "knowledge_base"

# 数据文件路径
DATA_DIR = SKILL_DIR / "data"
TASKS_FILE = DATA_DIR / "tasks.json"
PROGRESS_FILE = DATA_DIR / "progress.json"
EVOLUTION_FILE = DATA_DIR / "evolution.json"
VALIDATION_FILE = DATA_DIR / "validation_report.json"
CACHE_FILE = DATA_DIR / ".cache.json"

# 报告输出目录
REPORTS_DIR = SKILL_DIR / "reports"

# ============================================================================
# 知识领域定义 (12 个领域)
# ============================================================================

DOMAINS: Dict[str, Dict[str, Any]] = {
    "01-ai-agent": {"target": 1000, "name": "AI Agent"},
    "02-openclaw": {"target": 800, "name": "OpenClaw"},
    "03-federal-system": {"target": 600, "name": "联邦系统"},
    "04-skill-dev": {"target": 500, "name": "技能开发"},
    "05-memory-system": {"target": 400, "name": "记忆系统"},
    "06-growth-system": {"target": 400, "name": "成长系统"},
    "07-community": {"target": 500, "name": "社区建设"},
    "08-monetization": {"target": 500, "name": "变现"},
    "09-security": {"target": 400, "name": "安全"},
    "10-automation": {"target": 500, "name": "自动化"},
    "11-content": {"target": 400, "name": "内容创作"},
    "12-tools": {"target": 400, "name": "工具"},
}

# ============================================================================
# 全局常量
# ============================================================================

# 速度阈值 (知识点/分钟)
SPEED_TARGET = 500
SPEED_WARNING = 300
SPEED_CRITICAL = 100

# 进度阈值
PROGRESS_WARNING = 50  # 低于 50% 预警
PROGRESS_CRITICAL = 25  # 低于 25% 严重预警

# 缓存有效期 (秒)
CACHE_TTL = 60  # 1 分钟

# 日志级别
LOG_LEVELS = {
    "DEBUG": 0,
    "INFO": 1,
    "WARNING": 2,
    "ERROR": 3,
    "CRITICAL": 4,
}

# ============================================================================
# 工具函数
# ============================================================================

def get_total_target() -> int:
    """获取总目标知识点数"""
    return sum(d["target"] for d in DOMAINS.values())

def get_domain_ids() -> list:
    """获取所有领域 ID 列表"""
    return list(DOMAINS.keys())

def ensure_dirs():
    """确保所有必要目录存在"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

def load_config(config_file: Path = None) -> dict:
    """加载用户配置 (如果存在)"""
    if config_file is None:
        config_file = SKILL_DIR / "config.json"
    
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    
    return {}

def save_config(config: dict, config_file: Path = None):
    """保存用户配置"""
    if config_file is None:
        config_file = SKILL_DIR / "config.json"
    
    config_file.parent.mkdir(parents=True, exist_ok=True)
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

# ============================================================================
# 初始化
# ============================================================================

# 启动时确保目录存在
ensure_dirs()
