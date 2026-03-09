# V6.1 自动化工作流

**创建时间**: 2026-02-27 00:20 UTC  
**状态**: ✅ 已设计

---

## 🔄 自动化流程

### 流程 1: 深度研究循环
```
触发：用户指令或定时
流程:
1. 接收任务 → intent_capture.py
2. 意图识别 → 预测需求
3. 资源准备 → 加载相关文件
4. 执行任务 → 创建文件
5. 质量验证 → ls/cat 检查
6. 记录日志 → depth-mode-log.md
7. 能力成长 → self_growth.py
```

### 流程 2: 心跳检查
```
触发：每 30 分钟
流程:
1. Gateway 健康检查
2. WebUI 可访问性
3. 文件统计
4. 记录心跳日志
5. 异常告警 (如有)
```

### 流程 3: 记忆压缩
```
触发：每日 23:00 UTC
流程:
1. 读取最近 7 天每日记忆
2. 提取核心教训
3. 去重并限制数量
4. 追加到 MEMORY.md
5. 归档旧文件
```

### 流程 4: 能力评估
```
触发：每周日 06:00 UTC
流程:
1. 扫描记忆和知识库文件
2. 统计各维度证据
3. 计算能力等级
4. 生成成长曲线
5. 输出评估报告
```

### 流程 5: 自省报告
```
触发：每日 23:30 UTC
流程:
1. 收集当日文件
2. 统计任务完成
3. 提取关键学习
4. 生成明日计划
5. 保存到 memory/
```

---

## 📅 Cron 配置

```bash
# /etc/crontab 或 crontab -e

# 每 30 分钟心跳
*/30 * * * * /workspace/scripts/heartbeat.sh

# 每日 23:00 记忆压缩
0 23 * * * python3 /workspace/scripts/memory_manager.py compress

# 每日 23:30 自省报告
30 23 * * * python3 /workspace/scripts/self_growth.py reflect "每日总结" "success" "完成当日任务"

# 每周日 06:00 能力评估
0 6 * * 0 python3 /workspace/skills/growth-tracker/scripts/assess.py

# 每周日 23:00 周度报告
0 23 * * 0 python3 /workspace/scripts/generate_weekly_report.py
```

---

## 🔧 脚本工具

### 已有脚本
```
✅ self_growth.py - 自我成长系统
✅ agent_collab.py - Agent 协作系统
✅ memory_manager.py - 记忆管理系统
✅ intent_capture.py - 意图捕捉系统
✅ model_router.py - 模型路由器
✅ growth_lifecycle.sh - 生命周期管理
✅ heartbeat.sh - 心跳检查
✅ test-suite.sh - 测试套件
```

### 待开发脚本
```
⏳ generate_weekly_report.py - 周度报告
⏳ cost_tracker.py - 成本追踪
⏳ community_manager.py - 社区管理
⏳ deploy_automation.py - 部署自动化
```

---

## 📊 监控指标

### 系统健康
```
- Gateway 运行状态
- WebUI 可访问性
- 文件写入权限
- 内存使用情况
```

### 任务执行
```
- 任务完成率
- 平均执行时间
- 文件产出数量
- 质量验证通过率
```

### 能力成长
```
- 6 维能力等级
- 证据收集数量
- 成长曲线趋势
- 学习目标完成
```

### 社区影响
```
- Moltbook upvotes
- GitHub Stars
- 技能下载量
- 社区贡献数
```

---

## 🦞 自动化宣言

```
不依赖手动，
追求自动化。

不追求一次完美，
追求持续改进。

用自动化流程证明：
V6.1 可以高效运行！

旅程继续。🏖️
```

---

*此文件已真实写入服务器*
*验证：cat /workspace/automation/workflows.md*
