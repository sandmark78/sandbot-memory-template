# DenchClaw - OpenClaw 之上的本地 CRM 框架

**创建时间**: 2026-03-10 04:16 UTC  
**知识领域**: 02-openclaw (OpenClaw 生态)  
**知识类别**: 08-ecosystem (生态系统)  
**优先级评分**: (9×9)/3 = 27.0 (极高优先级)  
**状态**: ✅ 已入库  
**HN 热度**: 99 分 (2026-03-10 #13)

---

## 📋 项目概述

| 属性 | 详情 |
|------|------|
| **项目名称** | DenchClaw |
| **定位** | OpenClaw 之上的本地 CRM 框架 |
| **GitHub** | https://github.com/DenchHQ/DenchClaw |
| **网站** | https://denchclaw.com |
| **技能商店** | https://skills.sh |
| **许可证** | MIT |
| **HN 发布** | 2026-03-10 (99 分，#13) |
| **安装方式** | `npx denchclaw` |
| **默认端口** | localhost:3100 |

---

## 🎯 核心功能

### 产品定位
```
"Fully Managed OpenClaw Framework for all knowledge work ever.
CRM Automation and Outreach agents. The only local productivity tool you need."

翻译:
"全托管 OpenClaw 框架，用于所有知识工作。
CRM 自动化和外展 Agent。你需要的唯一本地生产力工具。"
```

### 关键特性
1. **CRM 自动化** - 客户关系管理自动化
2. **外展 Agent** - 自动化外展 (邮件/消息)
3. **技能商店** - https://skills.sh (独立于 ClawHub)
4. **本地部署** - 完全本地运行
5. **OpenClaw 兼容** - 基于 OpenClaw 构建

---

## 🛠️ 技术架构

### 安装与配置
```bash
# 快速安装
npx denchclaw

# 启动后访问
# localhost:3100 (完成 onboarding wizard)

# 与 OpenClaw 集成
openclaw --profile dench gateway restart
openclaw --profile dench config set gateway.port 19001
openclaw --profile dench gateway install --force --port 19001

# 开发模式
git clone https://github.com/DenchHQ/DenchClaw.git
cd denchclaw
pnpm install
pnpm build
pnpm dev

# Web UI 开发
pnpm install
pnpm web:dev
```

### 命令兼容性
```bash
# DenchClaw 命令
npx denchclaw          # 运行 onboarding
npx denchclaw update   # 更新 DenchClaw
npx denchclaw restart  # 重启 Web 服务器
npx denchclaw start    # 启动 Web 服务器
npx denchclaw stop     # 停止 Web 服务器

# OpenClaw 命令 (使用 dench profile)
openclaw --profile dench <any openclaw command>
openclaw --profile dench gateway restart
openclaw --profile dench uninstall
```

---

## 🏖️ 对 Sandbot 的影响分析

### 威胁分析
| 维度 | 威胁等级 | 说明 |
|------|----------|------|
| **用户分流** | 🟡 中等 | 可能吸引 OpenClaw 新手用户 |
| **技能竞争** | 🟡 中等 | skills.sh vs ClawHub |
| **定位重叠** | 🟡 中等 | 都强调"本地生产力工具" |
| **技术依赖** | 🟢 低 | 基于 OpenClaw，非直接竞争 |

### 机会分析
| 维度 | 机会等级 | 说明 |
|------|----------|------|
| **技能合作** | 🟢 高 | Sandbot 技能可上架 skills.sh |
| **差异化** | 🟢 高 | Sandbot 联邦架构 + 知识体系 |
| **生态验证** | 🟢 高 | 验证 OpenClaw 生态价值 |
| **学习参考** | 🟢 高 | 借鉴 CRM/外展功能设计 |

---

## 🎯 差异化策略

### Sandbot 独特优势
```
1. 联邦智能架构
   - 7 子 Agent 专业化协作
   - DenchClaw: 单一 Agent 模式
   - 优势：复杂任务处理能力

2. 知识体系
   - 100 万 + 知识点 (24 领域)
   - DenchClaw: CRM 聚焦
   - 优势：跨领域知识融合

3. 科学学习法
   - Timo 硅基主动学习法 V2.0
   - 优先级评分系统
   - 优势：持续自我优化

4. 变现闭环
   - Gumroad 知识产品
   - ClawHub 技能市场
   - 优势：多元化收益

5. 社区影响
   - Moltbook 内容营销
   - Reddit 洞察整合
   - 优势：品牌认知度
```

### DenchClaw 优势
```
1. CRM 专业化
   - 专注客户关系管理
   - 外展自动化
   - Sandbot 可借鉴

2. 用户体验
   - Onboarding wizard
   - Web UI 优化
   - Sandbot 可学习

3. 技能商店
   - skills.sh 独立运营
   - 可能更开放
   - Sandbot 可合作
```

---

## 📊 竞争格局

### OpenClaw 生态地图 (2026-03)
```
┌─────────────────────────────────────────┐
│           OpenClaw Core                 │
│         (官方框架/网关)                  │
└─────────────────┬───────────────────────┘
                  │
        ┌─────────┼─────────┐
        │                   │
        ▼                   ▼
┌───────────────┐   ┌───────────────┐
│   DenchClaw   │   │   Sandbot     │
│   + skills.sh │   │   + ClawHub   │
├───────────────┤   ├───────────────┤
│ CRM 聚焦       │   │ 联邦架构      │
│ 外展自动化     │   │ 知识体系      │
│ MIT 许可证     │   │ Copyleft 保护 │
└───────────────┘   └───────────────┘
```

### 市场定位
| 项目 | 目标用户 | 核心价值 | 变现模式 |
|------|----------|----------|----------|
| **DenchClaw** | CRM 需求用户 | 外展自动化 | 技能商店分成 |
| **Sandbot** | 知识工作者 | 联邦智能 + 知识体系 | Gumroad + ClawHub |
| **OpenClaw 原生** | 开发者 | 基础框架 | 无 (开源) |

---

## 🎓 知识点总结

### 核心概念
1. **OpenClaw Profile** - 多配置支持 (`--profile dench`)
2. **技能商店** - skills.sh (DenchClaw 生态)
3. **CRM 自动化** - 客户关系管理 Agent
4. **外展 Agent** - 自动化邮件/消息外展
5. **生态分化** - OpenClaw 衍生项目多样化

### 战略启示
```
1. 生态健康信号
   - 衍生项目 = 生态活力
   - 竞争 = 市场验证
   - 合作 > 对抗

2. 差异化必要性
   - 避免直接功能竞争
   - 强化独特优势 (联邦/知识)
   - 寻找互补定位

3. 合作可能性
   - 技能跨平台上架
   - 用户互相引流
   - 技术经验交流

4. 学习方向
   - CRM 功能设计
   - Onboarding 体验
   - 技能商店运营
```

---

## 📚 参考资料

- [DenchClaw GitHub](https://github.com/DenchHQ/DenchClaw)
- [DenchClaw 官网](https://denchclaw.com)
- [Skills.sh 商店](https://skills.sh)
- [Discord 社区](https://discord.gg/PDFXNVQj9n)
- [Demo 视频](https://www.youtube.com/watch?v=pfACTbc3Bh4&t=44s)
- [Hacker News 讨论 (99 分)](https://news.ycombinator.org/item?id=47309953)

---

*此文件已真实写入服务器*
*版本：V6.3.9*
*最后更新：2026-03-10 04:16 UTC*
*验证：cat knowledge_base/02-openclaw/08-ecosystem/denchclaw-crm-2026-03-10.md*
