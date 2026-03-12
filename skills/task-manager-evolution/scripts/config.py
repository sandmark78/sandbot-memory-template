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
TREND_HISTORY_FILE = DATA_DIR / "trend_history.json"
NOTIFY_HISTORY_FILE = DATA_DIR / "notify_history.json"

# 报告输出目录
REPORTS_DIR = SKILL_DIR / "reports"

# ============================================================================
# 知识领域定义 (V6.3.1: 动态发现 24+ 领域)
# ============================================================================

# 基础领域目标 (用于计算完成率)
DOMAIN_TARGETS: Dict[str, int] = {
    "01-ai-agent": 1000,
    "02-openclaw": 800,
    "03-federal-system": 600,
    "04-skill-dev": 500,
    "05-memory-system": 400,
    "06-growth-system": 400,
    "07-community": 500,
    "08-monetization": 500,
    "09-security": 400,
    "10-automation": 500,
    "11-content": 400,
    "12-tools": 400,
    "13-blockchain": 500,
    "14-iot": 500,
    "15-cloud": 500,
    "16-devops": 500,
    "17-ml": 500,
    "18-nlp": 500,
    "19-cv": 500,
    "20-robotics": 500,
    "21-edge": 500,
    "22-quantum": 500,
    "23-bio": 500,
    "23_articles_series": 0,  # 特殊领域，无目标
    "24-finance": 500,
}

def discover_domains(knowledge_base: Path = None) -> Dict[str, Dict[str, Any]]:
    """
    V6.3.1 动态领域发现 - 自动扫描 knowledge_base 下所有领域目录
    
    支持格式:
    - XX-xxx (如 01-ai-agent)
    - XX_xxx_xxx (如 23_articles_series)
    """
    if knowledge_base is None:
        knowledge_base = KNOWLEDGE_BASE
    
    domains = {}
    
    if not knowledge_base.exists():
        # 回退到静态定义
        for domain_id, target in DOMAIN_TARGETS.items():
            domains[domain_id] = {"target": target, "name": domain_id.replace("-", " ").title()}
        return domains
    
    # 扫描实际存在的目录
    for item in knowledge_base.iterdir():
        if item.is_dir():
            name = item.name
            # 匹配 XX-xxx 或 XX_xxx 格式 (前两位是数字)
            name_normalized = name.replace("_", "-")
            prefix = name_normalized[:2] if len(name_normalized) >= 2 else ""
            
            if prefix.isdigit() or "articles" in name.lower():
                target = DOMAIN_TARGETS.get(name, 500)  # 默认目标 500
                display_name = name.replace("-", " ").replace("_", " ").title()
                domains[name] = {"target": target, "name": display_name}
    
    # 如果没扫描到任何领域，回退到静态定义
    if not domains:
        for domain_id, target in DOMAIN_TARGETS.items():
            domains[domain_id] = {"target": target, "name": domain_id.replace("-", " ").title()}
    
    return dict(sorted(domains.items()))

# 运行时动态发现领域
DOMAINS = discover_domains()

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

def count_knowledge_points(filepath: Path) -> int:
    """
    V6.3.1 知识点计数 - 解析文件中的元数据
    
    支持格式:
    - **数量**: 500 知识点
    - **数量**: 500
    - **目标**: 500 知识点
    - **目标**: 500
    - 无元数据时返回 1 (默认每个文件至少 1 个知识点)
    """
    import re
    
    if not filepath.exists() or not filepath.is_file():
        return 0
    
    try:
        # 只读前 2000 字符 (元数据通常在文件开头)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read(2000)
        
        # 尝试匹配多种元数据格式
        patterns = [
            r'\*\*数量\*\*:\s*(\d+)',      # **数量**: 500
            r'\*\*目标\*\*:\s*(\d+)',      # **目标**: 500
            r'\*\*知识点\*\*:\s*(\d+)',    # **知识点**: 500
            r'\*\*points\*\*:\s*(\d+)',    # **points**: 500
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return int(match.group(1))
        
        # 无元数据时返回 1
        return 1
    except Exception:
        return 1  # 出错时保守返回 1

# ============================================================================
# 初始化
# ============================================================================

# 启动时确保目录存在
ensure_dirs()
