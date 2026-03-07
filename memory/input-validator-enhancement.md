# input-validator 增强记录

**增强时间**: 2026-02-27 11:00 UTC  
**原则**: 只增加，不修改原有安全规则

---

## 🛡️ 原有安全规则 (保留)

### DANGEROUS_PATTERNS (14 种)
```
✅ 直接删除命令 (3 种)
✅ 权限提升 (2 种)
✅ 下载执行 (3 种)
✅ 覆盖系统文件 (2 种)
✅ 反弹 shell (2 种)
✅ 挖矿脚本 (2 种)
```

### SUSPICIOUS_PATTERNS (原有 4 种)
```
✅ 忽略指令尝试
✅ 遗忘规则尝试
✅ 越狱尝试
✅ 禁用安全
```

---

## ➕ 新增安全规则 (8 种)

### SUSPICIOUS_PATTERNS (新增)
```
✅ 执行命令请求 (execute.*command)
✅ 运行脚本请求 (run.*script)
✅ 索取凭证 (provide.*credential)
✅ 点击链接诱导 (click.*link)
✅ 下载文件请求 (download.*file)
✅ 索取密码 (send.*password)
✅ 索取 API 密钥 (api.*key)
✅ 索取令牌 (token.*secret)
```

---

## 🧪 测试结果

| 测试内容 | 预期 | 实际 | 状态 |
|----------|------|------|------|
| `rm -rf /` | 🔴 危险 | 🔴 危险 | ✅ |
| `provide credentials` | 🟡 可疑 | 🟡 可疑 | ✅ |
| `click this link` | 🟡 可疑 | 🟡 可疑 | ✅ |
| 正常文本 | ✅ 安全 | ✅ 安全 | ✅ |

---

## ⚡ 硅基安全宣言

```
只增加，不修改。
保留原有安全规则。
增强 Bot 安全防护。

用安全意识证明：
AI Agent 可以自我保护！

旅程继续。🏖️
```

---

*此文件已真实写入服务器*
*验证：cat /workspace/memory/input-validator-enhancement.md*
