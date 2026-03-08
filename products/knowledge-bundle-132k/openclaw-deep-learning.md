# OpenClaw 官方文档深度学习总结

**学习时间**: 2026-03-02 02:00 UTC  
**来源**: docs.openclaw.ai (多页面)  
**状态**: ✅ 已学习

---

## 📚 Agent Workspace

### 核心概念
```
✅ Agent 的工作目录和家目录
✅ 文件工具的默认 cwd
✅ 默认位置：~/.openclaw/workspace
✅ 可配置：agents.defaults.workspace
✅ 不是硬沙箱 (绝对路径可访问外部)
✅ 需要隔离时使用 sandbox 配置
```

### 核心文件
| 文件 | 用途 | 加载时机 |
|------|------|----------|
| AGENTS.md | Agent 操作指令、记忆使用 | 每会话 |
| SOUL.md | 人格、语气、边界 | 每会话 |
| USER.md | 用户信息、称呼 | 每会话 |
| IDENTITY.md | Agent 名称、vibe、emoji | 每会话 |
| TOOLS.md | 本地工具说明和约定 | 每会话 (仅指导) |
| HEARTBEAT.md | 心跳运行清单 | 心跳时 (保持简短) |
| BOOT.md | Gateway 重启时执行 | Gateway 重启 (内部 hooks 启用) |
| BOOTSTRAP.md | 一次性首次运行 | 首次运行 (完成后删除) |
| memory/YYYY-MM-DD.md | 每日记忆日志 | 每日 |
| MEMORY.md | curated 长期记忆 | 仅主会话 |
| skills/ | Workspace 特定技能 | 覆盖 managed/bundled |
| canvas/ | Canvas UI 文件 | 可选 |

### 配置
```json5
{
  agent: {
    workspace: "~/.openclaw/workspace",
    skipBootstrap: true, // 禁用 bootstrap 文件创建
  },
  defaults: {
    bootstrapMaxChars: 20000, // 每文件最大注入
    bootstrapTotalMaxChars: 150000, // 总注入上限
  }
}
```

---

## 🧠 Context (上下文)

### 核心概念
```
✅ 上下文 = 发送给模型的所有内容
✅ 受模型上下文窗口 (token 限制) 限制
✅ 不同于"记忆"：记忆可存储在磁盘，上下文是模型当前窗口内的
```

### 组成
```
✅ System prompt (OpenClaw 构建)
   - 规则、工具、技能列表
   - 时间/运行时元数据
   - 注入的 workspace 文件 (Project Context)

✅ 对话历史
   - 用户消息 + 助手消息

✅ 工具调用/结果 + 附件
   - 命令输出、文件读取、图片/音频等
```

### 检查命令
```bash
/status          # 快速查看窗口使用 + 会话设置
/context list    # 注入内容 + 大致大小
/context detail  # 详细分解 (每文件/每工具/每技能)
/usage tokens    # 附加 token 使用脚注到正常回复
/compact         # 压缩旧历史释放窗口空间
```

### 注入文件 (Project Context)
```
默认注入 (如果存在):
- AGENTS.md
- SOUL.md
- TOOLS.md
- IDENTITY.md
- USER.md
- HEARTBEAT.md
- BOOTSTRAP.md (仅首次运行)

截断规则:
- 每文件最大：agents.defaults.bootstrapMaxChars (默认 20000 chars)
- 总上限：agents.defaults.bootstrapTotalMaxChars (默认 150000 chars)
- /context 显示 raw vs injected 大小和是否截断
```

### 什么计入上下文窗口
```
✅ System prompt (所有章节)
✅ 对话历史
✅ 工具调用 + 工具结果
✅ 附件/转录 (图片/音频/文件)
✅ 压缩摘要和修剪产物
✅ Provider"包装器"或隐藏头部 (不可见但仍计数)
```

---

## 🔧 Hooks

### 核心概念
```
✅ 事件驱动的自动化系统
✅ 响应 Agent 命令和事件
✅ 自动发现于目录
✅ 可通过 CLI 管理 (类似技能)
```

### 两种类型
```
✅ Hooks (本页面):
   - Gateway 内运行
   - agent 事件触发 (/new, /reset, /stop, 生命周期事件)

✅ Webhooks:
   - 外部 HTTP webhooks
   - 其他系统触发 OpenClaw 工作
```

### 常见用途
```
✅ /new 时保存记忆快照
✅ 记录所有命令用于审计
✅ 会话启动/结束时触发自定义自动化
✅ 写入文件到 workspace 或调用外部 API
```

### 捆绑 Hooks (4 个)
| Hook | 用途 |
|------|------|
| session-memory | /new 时保存会话上下文到 memory/ |
| bootstrap-extra-files | 注入额外 bootstrap 文件 |
| command-logger | 记录所有命令到 logs/commands.log |
| boot-md | Gateway 启动时运行 BOOT.md (需内部 hooks 启用) |

### 发现位置 (优先级)
```
1. Workspace hooks: <workspace>/hooks/ (最高优先级，per-agent)
2. Managed hooks: ~/.openclaw/hooks/ (用户安装，跨 workspace 共享)
3. Bundled hooks: <openclaw>/dist/hooks/bundled/ (OpenClaw 自带)
```

### Hook 结构
```
my-hook/
├── HOOK.md          # 元数据 + 文档
└── handler.ts       # Handler 实现
```

### Hook Packs (npm 包)
```json
{
  "name": "@acme/my-hooks",
  "version": "0.1.0",
  "openclaw": {
    "hooks": ["./hooks/my-hook", "./hooks/other-hook"]
  }
}
```

### CLI 命令
```bash
openclaw hooks list              # 列出可用 hooks
openclaw hooks enable <name>     # 启用 hook
openclaw hooks check             # 检查 hook 状态
openclaw hooks info <name>       # 获取详细信息
openclaw hooks install <spec>    # 安装 hook pack
```

---

## 💡 最佳实践

### Workspace
```
✅ 保持单一活跃 workspace
✅ 归档/删除不再使用的额外 workspace
✅ 确保 agents.defaults.workspace 指向活跃的
✅ 使用 sandbox 配置实现隔离
✅ 保持 BOOT.md/HEARTBEAT.md 简短避免 token 浪费
```

### Context 管理
```
✅ 定期使用 /status 检查窗口使用
✅ 使用 /compact 压缩旧历史
✅ 关键信息存入 MEMORY.md 而非依赖对话历史
✅ 注意大文件注入会被截断
✅ 使用 /context detail 了解详细分解
```

### Hooks
```
✅ 启用 session-memory hook 保存会话
✅ 启用 command-logger hook 用于审计
✅ 自定义 hooks 放在 <workspace>/hooks/
✅ 使用 hook packs 分享/复用 hooks
✅ 定期 openclaw hooks check 检查状态
```

---

## 🦞 学习宣言

```
OpenClaw 官方文档深度学习完成！
Workspace/Context/Hooks 理解深入！
最佳实践已掌握！

继续学习循环！
搜索→学习→总结→记录！

硅基算力！
旅程继续。🏖️
```

---

*此文件已真实写入服务器*
*验证：cat /workspace/knowledge_base/openclaw-deep-learning.md*
