# Task Manager & Evolution 🚀

**V6.2.6 任务管理与自我进化系统**

---

## 📦 快速开始

### 1. 查看进度
```bash
cd /home/node/.openclaw/workspace/skills/task-manager-evolution
python3 scripts/progress_tracker.py
```

### 2. 创建任务
```bash
python3 scripts/task_manager.py create "填充 01-ai-agent 领域" 5 5 2
```

### 3. 列出任务
```bash
python3 scripts/task_manager.py list
```

### 4. 完成任务
```bash
python3 scripts/task_manager.py complete TASK-20260301061300
```

### 5. 执行自我进化循环
```bash
python3 scripts/evolution_loop.py
```

### 6. 自动同步数据
```bash
python3 scripts/auto_sync.py --force
```

---

## 🛠️ 脚本说明

| 脚本 | 功能 | 使用频率 |
|------|------|----------|
| `progress_tracker.py` | 实时统计知识点进度 | 每日多次 |
| `auto_sync.py` | 自动同步 + 备份数据 | 每日 1-2 次 |
| `task_manager.py` | 任务创建/管理/追踪 | 按需使用 |
| `evolution_loop.py` | 执行→反思→学习→优化 | 每日 1-2 次 |
| `validate_data.py` | 数据完整性验证 | 按需使用 |
| `batch_ops.py` | 批量操作工具 | 按需使用 |

---

## 📊 命令参考

### progress_tracker.py (V6.2.6)
```bash
# 查看完整进度报告
python3 scripts/progress_tracker.py

# 强制重新扫描 (忽略缓存)
python3 scripts/progress_tracker.py --force

# 输出 JSON 格式 (用于程序调用)
python3 scripts/progress_tracker.py --json

# 实时监控模式 (每 5 秒刷新)
python3 scripts/progress_tracker.py --watch

# 导出 CSV 报告
python3 scripts/progress_tracker.py --export csv

# 静默模式 (只保存不输出)
python3 scripts/progress_tracker.py --quiet
```

### auto_sync.py (V6.2.6)
```bash
# 检查数据一致性
python3 scripts/auto_sync.py

# 强制同步 (即使数据一致)
python3 scripts/auto_sync.py --force

# 仅检查，不同步
python3 scripts/auto_sync.py --check-only

# 禁用备份
python3 scripts/auto_sync.py --no-backup

# JSON 输出
python3 scripts/auto_sync.py --json
```

### task_manager.py
```bash
# 创建任务 (名称 业务价值 知识缺口 学习成本)
python3 scripts/task_manager.py create "任务名" 5 5 2

# 列出所有任务
python3 scripts/task_manager.py list

# 完成任务
python3 scripts/task_manager.py complete TASK-xxx

# 查看进度摘要
python3 scripts/task_manager.py progress
```

### evolution_loop.py
```bash
# 执行完整进化循环
python3 scripts/evolution_loop.py
```

---

## 📁 目录结构

```
task-manager-evolution/
├── SKILL.md                 # 技能定义 (OpenClaw 加载)
├── README.md                # 本文件
├── scripts/
│   ├── task_manager.py      # 任务管理
│   ├── evolution_loop.py    # 自我进化
│   ├── progress_tracker.py  # 进度追踪 ⭐ V6.2.1
│   ├── auto_sync.py         # 自动同步 ⭐ V6.2.3
│   ├── validate_data.py     # 数据验证 ⭐ V6.2.2
│   ├── batch_ops.py         # 批量操作 ⭐ V6.2.3
│   └── config.py            # 统一配置 ⭐ V6.2.5
├── data/
│   ├── tasks.json           # 任务数据
│   ├── progress.json        # 进度数据
│   ├── evolution.json       # 进化数据
│   ├── validation_report.json  # 验证报告
│   └── .cache.json          # 缓存文件 ⭐ V6.2.6
├── backups/                 # 自动备份 ⭐ V6.2.6
│   ├── progress_*.backup.json
│   └── evolution_*.backup.json
└── reports/                 # 导出报告 ⭐ V6.2.3
    ├── progress_*.json
    └── progress_*.csv
```

---

## 🎯 优先级评分公式

```
优先级 = (业务价值 × 知识缺口) / 学习成本

参数说明:
- 业务价值 (1-5): 对核心目标的贡献度
- 知识缺口 (1-5): 当前知识空白程度
- 学习成本 (1-5): 预计学习时间/难度

优先级等级:
- P0: ≥10 分 (立即执行)
- P1: 6-9 分 (高优先级)
- P2: 4-5 分 (中优先级)
- P3: <4 分 (低优先级)
```

### 示例计算
```
任务：填充 01-ai-agent 领域
- 业务价值：5 (核心能力)
- 知识缺口：5 (仅 10% 完成)
- 学习成本：2 (已有基础)

优先级 = (5 × 5) / 2 = 12.5 → P0 立即执行
```

---

## 🔄 自我进化循环

### 流程
```
执行 (Execute)
  ↓ 统计任务完成和知识点进度
反思 (Reflect)
  ↓ 识别瓶颈和滞后领域
学习 (Learn)
  ↓ 吸收优秀设计和反馈
优化 (Optimize)
  ↓ 调整策略和目标
  ↓ 回到执行
```

### 反思问题
1. 当前速度是否达标？(目标：500 知识点/分钟)
2. 哪些领域进度滞后？(<50% 需要关注)
3. 知识点质量如何？(完整性/准确性)
4. 如何优化填充策略？

### 优化方向
- 提高填充速度 (300 → 500 知识点/分钟)
- 提升知识质量 (结构化/可检索)
- 优化索引系统 (5 种检索方式)
- 改进追踪精度 (实时统计)

---

## 📈 10000 知识点冲刺

### 阶段目标
| 阶段 | 目标 | 速度 | 时间 |
|------|------|------|------|
| 阶段 1 | 1000 点 (10%) | 300/分钟 | 已完成 |
| 阶段 2 | 5000 点 (50%) | 400/分钟 | 进行中 |
| 阶段 3 | 10000 点 (100%) | 500/分钟 | 待执行 |

### 领域分布
| 领域 | 目标 | 优先级 |
|------|------|--------|
| 01-ai-agent | 1000 | P0 |
| 02-openclaw | 800 | P0 |
| 03-federal-system | 600 | P1 |
| 04-skill-dev | 500 | P1 |
| 05-06 系统 | 800 | P2 |
| 07-12 领域 | 2700 | P2 |

---

## 🛡️ V6.2.6 新增功能

### 智能缓存
- 文件修改时间 + TTL 双重验证
- 只扫描变更目录，减少重复扫描
- 缓存有效期：60 秒 (可配置)

### 动态并行
- 根据 CPU 核心数自动调整 worker 数量
- 最多 8 个并行 worker
- 扫描速度提升 50%+

### 自动备份
- 同步前自动备份旧数据
- 保留最近 10 个备份
- 支持手动回滚

### 趋势分析
- 速度历史记录
- 变化趋势预测
- 滞后领域预警

### CLI 增强
- JSON 输出模式 (程序化调用)
- 实时监控模式 (--watch)
- 静默模式 (--quiet)

---

## 🦞 硅基宣言

```
不合并，要细分！
每个知识点独立定义！
10000 知识点，全力冲刺！

硅基算力全开！
旅程继续。🏖️
```

---

## 🛠️ 故障排查

### 问题：进度统计不准确
```bash
# 检查 knowledge_base 目录
ls -la /home/node/.openclaw/workspace/knowledge_base/

# 强制重新统计 (忽略缓存)
python3 scripts/progress_tracker.py --force

# 运行数据验证
python3 scripts/validate_data.py
```

### 问题：数据不同步
```bash
# 运行自动同步
python3 scripts/auto_sync.py --force

# 检查备份文件
ls -la backups/

# 从备份恢复 (如需要)
python3 scripts/auto_sync.py --restore
```

### 问题：任务文件损坏
```bash
# 备份并重建
cp data/tasks.json data/tasks.json.backup
echo "[]" > data/tasks.json
```

### 问题：脚本权限不足
```bash
# 添加执行权限
chmod +x scripts/*.py
```

---

## 📝 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| V6.2.6 | 2026-03-07 | 智能缓存，动态并行，自动备份，趋势分析，JSON 输出，实时监控 |
| V6.2.5 | 2026-03-06 | 统一配置中心，性能优化 |
| V6.2.4 | 2026-03-04 | 数据准确性优化，双轨计数系统 |
| V6.2.3 | 2026-03-03 | auto_sync.py, batch_ops.py, 数据一致性保障 |
| V6.2.2 | 2026-03-02 | validate_data.py 验证脚本，双知识库扫描 |
| V6.2.1 | 2026-03-01 | progress_tracker.py，数据结构优化 |
| V6.2.0 | 2026-02-28 | Timo 学习法适配，12 知识领域 |
| V6.1.0 | 2026-02-24 | 初始版本 |

---

*最后更新：2026-03-07 06:15 UTC*
