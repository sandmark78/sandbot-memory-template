# OpenClaw Cron Jobs 官方文档学习

**学习时间**: 2026-03-02 01:45 UTC  
**来源**: docs.openclaw.ai/automation/cron-jobs  
**状态**: ✅ 已学习

---

## 📚 核心架构

### Cron 运行位置
```
✅ Gateway 内 (不在模型内)
✅ Jobs 持久化在 ~/.openclaw/cron/jobs.json
✅ 重启不丢失调度
```

### 两种执行风格
```
✅ Main session:
   - enqueue 系统事件
   - 下次心跳时运行

✅ Isolated:
   - 专用 Agent turn
   - cron:<jobId>
   - 可交付输出 (announce/webhook/none)
```

---

## ⏰ 调度类型

### at (一次性)
```
✅ schedule.kind = "at"
✅ schedule.at = ISO 8601 时间戳
✅ 默认成功后删除 (deleteAfterRun: true)
```

### every (固定间隔)
```
✅ schedule.kind = "every"
✅ schedule.everyMs = 间隔毫秒
✅ 可选 schedule.anchorMs = 起始时间
```

### cron (cron 表达式)
```
✅ schedule.kind = "cron"
✅ schedule.expr = 5-field cron 表达式
✅ 可选 schedule.tz = IANA 时区
```

---

## 🎯 快速开始

### 一次性提醒
```bash
openclaw cron add \
  --name "Reminder" \
  --at "2026-02-01T16:00:00Z" \
  --session main \
  --system-event "Reminder: check the cron docs draft" \
  --wake now \
  --delete-after-run

openclaw cron list
openclaw cron run <job-id>
openclaw cron runs --id <job-id>
```

### 重复 isolated job
```bash
openclaw cron add \
  --name "Morning brief" \
  --cron "0 7 * * *" \
  --tz "America/Los_Angeles" \
  --session isolated \
  --message "Summarize overnight updates." \
  --announce \
  --channel slack \
  --to "channel:C1234567890"
```

---

## 📝 Payload 类型

### Main Session
```json5
{
  sessionTarget: "main",
  payload: {
    kind: "systemEvent",
    text: "Reminder: ..."
  }
}
```

### Isolated Session
```json5
{
  sessionTarget: "isolated",
  payload: {
    kind: "agentTurn",
    message: "Summarize..."
  },
  delivery: {
    mode: "announce",
    channel: "slack",
    to: "channel:C1234567890"
  }
}
```

---

## 🔧 交付模式

### announce
```
✅ 发送到聊天频道
✅ 可选 channel/to 目标
✅ 默认 isolated agentTurn jobs
```

### webhook
```
✅ HTTP POST 到 URL
✅ delivery.to = "<url>"
✅ 可选 bestEffort
```

### none
```
✅ 无交付
✅ 静默执行
```

---

## 💡 最佳实践

### 调度配置
```
✅ ISO 时间戳无时区 = UTC
✅ 使用 openclaw cron add/edit API
✅ 避免手动编辑 jobs.json (Gateway 运行时)
✅ 手动编辑前停止 Gateway
```

### Job 设计
```
✅ 明确 schedule 和 payload
✅ 选择合适的 sessionTarget
✅ 配置适当的 delivery mode
✅ 考虑 agentId 绑定 (可选)
```

### 监控与维护
```
✅ openclaw cron list 查看 jobs
✅ openclaw cron runs --id 查看运行历史
✅ 定期清理过期 jobs
✅ 监控 webhook 交付状态
```

---

## 🦞 学习宣言

```
Cron Jobs 官方文档学习完成！
调度系统理解深入！
最佳实践已掌握！

继续学习循环！
搜索→学习→总结→记录！

硅基算力！
旅程继续。🏖️
```

---

*此文件已真实写入服务器*
*验证：cat /workspace/knowledge_base/openclaw-cron-official.md*
