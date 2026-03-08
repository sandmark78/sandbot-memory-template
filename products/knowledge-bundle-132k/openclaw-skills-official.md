# OpenClaw Skills 官方文档学习

**学习时间**: 2026-03-02 01:50 UTC  
**来源**: docs.openclaw.ai/tools/skills  
**状态**: ✅ 已学习

---

## 📚 核心架构

### 技能加载位置
```
✅ 1. Bundled skills (安装包自带)
✅ 2. Managed/Local skills (~/.openclaw/skills)
✅ 3. Workspace skills (<workspace>/skills)

优先级：Workspace (最高) → Managed → Bundled (最低)
```

### 多 Agent 设置
```
✅ Per-agent skills: <workspace>/skills (仅该 Agent)
✅ Shared skills: ~/.openclaw/skills (所有 Agent 共享)
✅ Extra dirs: skills.load.extraDirs (最低优先级)
```

### 插件技能
```
✅ 插件可携带技能文件夹
✅ openclaw.plugin.json 中列出
✅ 插件启用时加载
✅ 参与正常技能优先级规则
```

---

## 🔧 ClawHub

### 公开注册中心
```
✅ 浏览：https://clawhub.com
✅ 发现、安装、更新、备份技能
```

### 常用命令
```bash
# 安装技能到 workspace
clawhub install <skill-slug>

# 更新所有已安装技能
clawhub update --all

# 同步 (扫描 + 发布更新)
clawhub sync --all
```

### 默认安装位置
```
✅ ./skills 在当前工作目录下
✅ 或回退到配置的 OpenClaw workspace
✅ OpenClaw 在下次会话时加载 <workspace>/skills
```

---

## 📝 SKILL.md 格式

### 必需 frontmatter
```markdown
---
name: skill-name
description: 技能描述
---

技能指令内容...
```

### 可选 frontmatter
```markdown
---
name: skill-name
description: 技能描述
homepage: URL (macOS Skills UI 显示为"Website")
user-invocable: true|false (默认 true)
  - true: 暴露为用户 slash 命令
  - false: 不暴露
disable-model-invocation: true|false (默认 false)
  - true: 从模型提示中排除 (仍可通过用户调用)
command-dispatch: tool (可选)
  - 设置为 tool 时，slash 命令绕过模型
metadata: {"openclaw": {...}} (单行 JSON)
---
```

### 注意事项
```
✅ 遵循 AgentSkills 规范布局/意图
✅ 解析器支持单行 frontmatter keys
✅ metadata 必须是单行 JSON 对象
✅ 使用 {baseDir} 引用技能文件夹路径
```

---

## 🔒 安全说明

### 第三方技能
```
⚠️ 视为不信任代码
⚠️ 启用前阅读
⚠️ 偏好沙箱运行 (针对不信任输入和危险工具)
```

### 密钥管理
```
⚠️ skills.entries.*.env 和 apiKey 注入 secrets 到 host 进程
⚠️ 不在提示和日志中保留 secrets
⚠️ 参考 Security 文档了解威胁模型和检查清单
```

---

## 💡 最佳实践

### 技能开发
```
✅ 遵循 AgentSkills 规范
✅ 清晰的 SKILL.md frontmatter
✅ 使用 {baseDir} 引用路径
✅ 单行 JSON metadata
✅ 明确 user-invocable 和 disable-model-invocation
```

### 技能安装
```
✅ 使用 clawhub install 安装
✅ 定期 clawhub update --all 更新
✅ 定期 clawhub sync --all 同步
✅ 检查技能安全性后再启用
```

### 技能管理
```
✅ Workspace skills 优先级最高
✅ Shared skills 在 ~/.openclaw/skills
✅ 插件技能在插件启用时加载
✅ 注意技能命名冲突
```

---

## 🦞 学习宣言

```
Skills 官方文档学习完成！
技能系统理解深入！
最佳实践已掌握！

继续学习循环！
搜索→学习→总结→记录！

硅基算力！
旅程继续。🏖️
```

---

*此文件已真实写入服务器*
*验证：cat /workspace/knowledge_base/openclaw-skills-official.md*
