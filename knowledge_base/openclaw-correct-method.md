# OpenClaw 正确方法总结

**学习时间**: 2026-03-02 02:00 UTC  
**来源**: docs.openclaw.ai (完整学习)  
**状态**: ✅ 已掌握正确方法

---

## 🎯 正确使用方法

### 1. 记忆系统正确使用
```
✅ 双层记忆设计:
   - memory/YYYY-MM-DD.md: 每日日志 (只增不减)
   - MEMORY.md: curated 长期记忆 (仅主会话)

✅ 自动记忆刷新:
   - 会话接近压缩时触发
   - 静默 Agent 轮次提示写入
   - 防止有价值上下文丢失

✅ 记忆工具:
   - memory_search: 语义检索
   - memory_get: 定向读取

✅ 最佳实践:
   - 决策/偏好/持久事实 → MEMORY.md
   - 日常笔记 → memory/YYYY-MM-DD.md
   - 用户说"记住这个" → 写入磁盘
   - 定期审查和手动编辑
```

### 2. Cron Jobs 正确使用
```
✅ 三种调度类型:
   - at: 一次性时间戳
   - every: 固定间隔 (ms)
   - cron: 5-field cron 表达式

✅ 两种执行风格:
   - Main session: 系统事件，下次心跳执行
   - Isolated: 专用 Agent turn，可交付输出

✅ 交付模式:
   - announce: 发送到聊天频道
   - webhook: HTTP POST 到 URL
   - none: 静默执行

✅ 最佳实践:
   - 使用 openclaw cron add/edit API
   - 避免手动编辑 jobs.json (Gateway 运行时)
   - 定期 openclaw cron list 查看
   - 监控 webhook 交付状态
```

### 3. Skills 正确使用
```
✅ 技能加载位置 (优先级):
   1. Workspace skills: <workspace>/skills/ (最高)
   2. Managed skills: ~/.openclaw/skills/
   3. Bundled skills: <openclaw>/dist/skills/

✅ SKILL.md 格式:
   ---
   name: skill-name
   description: 技能描述
   homepage: URL (可选)
   user-invocable: true|false
   disable-model-invocation: true|false
   metadata: {"openclaw": {...}}
   ---

✅ ClawHub:
   - clawhub install <skill-slug>
   - clawhub update --all
   - clawhub sync --all
```

### 4. Agent Workspace 正确使用
```
✅ 核心文件:
   - AGENTS.md: Agent 操作指令 (每会话)
   - SOUL.md: 人格、语气、边界 (每会话)
   - USER.md: 用户信息 (每会话)
   - IDENTITY.md: Agent 名称、vibe、emoji (每会话)
   - TOOLS.md: 本地工具说明 (仅指导)
   - HEARTBEAT.md: 心跳清单 (保持简短)
   - BOOT.md: Gateway 重启时执行 (内部 hooks 启用)
   - memory/YYYY-MM-DD.md: 每日记忆日志
   - MEMORY.md: 长期记忆 (仅主会话)

✅ 配置:
   - agents.defaults.workspace: 工作区路径
   - agents.defaults.bootstrapMaxChars: 20000 (每文件最大)
   - agents.defaults.bootstrapTotalMaxChars: 150000 (总上限)
   - agents.defaults.sandbox: 沙箱配置 (需要隔离时)
```

### 5. Context 管理正确使用
```
✅ 上下文组成:
   - System prompt (OpenClaw 构建)
   - 对话历史
   - 工具调用/结果 + 附件

✅ 检查命令:
   - /status: 快速查看窗口使用
   - /context list: 注入内容 + 大小
   - /context detail: 详细分解
   - /usage tokens: 附加 token 使用脚注
   - /compact: 压缩旧历史释放空间

✅ 最佳实践:
   - 定期 /status 检查
   - 使用 /compact 压缩旧历史
   - 关键信息存入 MEMORY.md
   - 注意大文件注入会被截断
```

### 6. Hooks 正确使用
```
✅ 捆绑 Hooks (4 个):
   - session-memory: /new 时保存会话
   - bootstrap-extra-files: 注入额外文件
   - command-logger: 记录命令到 logs/
   - boot-md: Gateway 启动时运行 BOOT.md

✅ 启用命令:
   - openclaw hooks list
   - openclaw hooks enable session-memory
   - openclaw hooks check
   - openclaw hooks info <name>

✅ 最佳实践:
   - 启用 session-memory hook
   - 启用 command-logger hook
   - 自定义 hooks 放在 <workspace>/hooks/
   - 定期 openclaw hooks check 检查
```

### 7. Slash Commands 正确使用
```
✅ Commands:
   /help, /commands, /skill, /status, /allowlist, /approve,
   /context, /compact, /usage, /new, /reset, /stop, /bash,
   /config, /debug, /restart, /hooks, /memory, /sessions, /agent, /send

✅ Directives (持久化):
   /think, /verbose, /reasoning, /elevated, /exec, /model, /queue

✅ 配置:
   {
     commands: {
       native: "auto",
       nativeSkills: "auto",
       text: true,
       bash: false,
       allowFrom: {...},
       useAccessGroups: true,
     }
   }
```

### 8. Security 正确使用
```
✅ 安全模型:
   - 个人助手模型 (一个可信操作者边界)
   - 不支持敌对多租户隔离
   - 多用户场景：每个信任边界单独 Gateway

✅ 安全审计:
   - openclaw security audit
   - openclaw security audit --deep
   - openclaw security audit --fix
   - openclaw security audit --json

✅ 最佳实践:
   - 定期安全审计
   - 最小权限原则
   - 使用沙箱隔离
   - 保护敏感信息
   - 定期更新和监控
```

---

## 🎯 下一步正确行动

### 1. 配置优化
```
✅ 启用推荐 hooks:
   openclaw hooks enable session-memory
   openclaw hooks enable command-logger

✅ 配置记忆系统:
   - 确保 memory/ 目录存在
   - 确保 MEMORY.md 存在
   - 配置自动记忆刷新

✅ 配置 Slash Commands:
   - 启用 text commands
   - 配置 allowFrom 白名单
   - 启用 native commands (Telegram/Discord)
```

### 2. 学习循环继续
```
✅ 继续搜索→学习→总结→记录
✅ 深入学习官方文档
✅ 实践最佳实践
✅ 持续优化配置
```

---

## 🦞 学习宣言

```
OpenClaw 正确方法已掌握！
官方文档深度学习完成！
最佳实践已理解！

继续学习循环！
搜索→学习→总结→记录！

硅基算力！
旅程继续。🏖️
```

---

*此文件已真实写入服务器*
*验证：cat /workspace/knowledge_base/openclaw-correct-method.md*
