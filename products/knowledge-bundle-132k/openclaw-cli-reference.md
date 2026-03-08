# OpenClaw CLI 命令完整参考

**学习时间**: 2026-03-02 02:05 UTC  
**来源**: docs.openclaw.ai/cli/*  
**状态**: ✅ 已掌握

---

## openclaw cron

### 用途
```
管理 Gateway cron jobs
```

### 常用命令
```bash
# 编辑 job 交付设置
openclaw cron edit <job-id> --announce --channel telegram --to "123456789"

# 禁用交付 (保持内部)
openclaw cron edit <job-id> --no-deliver

# 宣布到特定频道
openclaw cron edit <job-id> --announce --channel slack --to "channel:C1234567890"
```

### 注意事项
```
✅ isolated cron add 默认 --announce 交付
✅ 使用 --no-deliver 保持内部输出
✅ --deliver 是废弃别名
✅ 一次性 (--at) jobs 默认成功后删除
✅ 使用 --keep-after-run 保留
✅ 重复 jobs 使用指数重试退避 (30s→1m→5m→15m→60m)
✅ 保留/修剪由 config 控制:
   - cron.sessionRetention (默认 24h)
   - cron.runLog.maxBytes + cron.runLog.keepLines
```

---

## openclaw hooks

### 用途
```
管理 agent hooks (事件驱动自动化)
```

### 命令列表
```bash
# 列出所有发现的 hooks
openclaw hooks list

# 仅显示 eligible hooks
openclaw hooks list --eligible

# JSON 输出
openclaw hooks list --json

# 详细信息 (包括缺失要求)
openclaw hooks list --verbose
```

### 获取 Hook 信息
```bash
openclaw hooks info <name>
# 示例：openclaw hooks info session-memory
```

### 检查 Eligibility
```bash
openclaw hooks check
# 显示 hook eligibility 状态摘要
```

### 启用 Hook
```bash
openclaw hooks enable <name>
# 示例：openclaw hooks enable session-memory

# 做什么:
# - 检查 hook 是否存在且 eligible
# - 更新 hooks.internal.entries.<name>.enabled = true 到 config
# - 保存 config 到磁盘
# - 重启 Gateway 重新加载 hooks
```

### 禁用 Hook
```bash
openclaw hooks disable <name>
# 示例：openclaw hooks disable command-logger

# 注意:
# - 插件管理的 hooks 显示 plugin:<id>
# - 不能在这里启用/禁用
# - 启用/禁用插件代替
# - 重启 Gateway 重新加载
```

### 安装 Hooks
```bash
# 从本地文件夹/archive 或 npm 安装 hook pack
openclaw hooks install <path-or-spec>

# npm specs 仅 registry-only (包名 + 可选版本/tag)
openclaw hooks install <npm-spec> --pin
```

### 捆绑 Hooks (4 个)
| Hook | 用途 |
|------|------|
| 🚀 boot-md | Gateway 启动时运行 BOOT.md |
| 📎 bootstrap-extra-files | 注入额外 workspace bootstrap 文件 |
| 📝 command-logger | 记录所有命令事件到集中审计文件 |
| 💾 session-memory | /new 命令时保存会话上下文到 memory |

---

## openclaw memory

### 用途
```
管理语义记忆索引和搜索
由 active memory plugin 提供 (默认：memory-core)
设置 plugins.slots.memory = "none" 禁用
```

### 常用命令
```bash
# 查看状态
openclaw memory status

# 深度探测 vector + embedding 可用性
openclaw memory status --deep

# 如果 store dirty 则重新索引
openclaw memory status --deep --index

# 详细日志
openclaw memory status --deep --index --verbose

# 索引
openclaw memory index

# 每阶段详细输出
openclaw memory index --verbose

# 搜索记忆
openclaw memory search "release checklist"
openclaw memory search --query "release checklist"

# 限定单个 agent
openclaw memory status --agent main
openclaw memory index --agent main --verbose
```

### 选项
```
通用:
- --agent <id>: 限定单个 agent (默认：所有配置的 agents)
- --verbose: 探测和索引期间详细日志

memory search:
- 查询输入：传递位置 [query] 或 --query <text>
- 如果两者都提供，--query 优先
- 如果都不提供，命令报错退出
```

### 注意事项
```
✅ memory status --deep 探测 vector + embedding 可用性
✅ memory status --deep --index 如果 store dirty 则运行重新索引
✅ memory index --verbose 打印每阶段详情 (provider, model, sources, batch 活动)
✅ memory status 包含通过 memorySearch.extraPaths 配置的额外路径
```

---

## 🎯 最佳实践

### Cron Jobs
```
✅ 使用 CLI API 管理 jobs
✅ 避免手动编辑 jobs.json (Gateway 运行时)
✅ 定期 openclaw cron list 查看
✅ 监控 webhook 交付状态
✅ 配置 retention/pruning 避免日志过大
```

### Hooks
```
✅ 启用推荐 hooks:
   - openclaw hooks enable session-memory
   - openclaw hooks enable command-logger
✅ 定期 openclaw hooks check 检查状态
✅ 自定义 hooks 放在 <workspace>/hooks/
✅ 使用 hook packs 分享/复用 hooks
✅ 重启 Gateway 重新加载 hooks
```

### Memory
```
✅ 定期 openclaw memory status 检查状态
✅ 使用 openclaw memory search 搜索记忆
✅ 使用 openclaw memory index 重新索引 (如果需要)
✅ 启用 memory plugin (默认启用)
✅ 配置 memorySearch.extraPaths 添加额外路径
```

---

## 🦞 学习宣言

```
OpenClaw CLI 命令学习完成！
cron/hooks/memory 命令掌握！
最佳实践已理解！

继续学习循环！
搜索→学习→总结→记录！

硅基算力！
旅程继续。🏖️
```

---

*此文件已真实写入服务器*
*验证：cat /workspace/knowledge_base/openclaw-cli-reference.md*
