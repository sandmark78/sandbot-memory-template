# 手机作为完整计算机：Right to Root Access 运动

**来源**: HN (288 pts, 2026-03-14) + medhir.com  
**主题**: 设备自由/Root 权限/软件安装自由  
**标签**: #RightToRoot #设备自由 #iOS 越狱 #软件自由 #数字权利

---

## 📋 核心论点

### 文章背景
```
作者：Medhir Jaddou (medhir.com)
时间：2026-03-13
热度：HN 288 pts, 258 条评论
关联事件：Apple 发布 $599 MacBook Neo

核心观点:
  "你的 iPhone 是一台完整的计算机，能够运行完整的桌面操作系统，
   而且已经如此很长一段时间了。"

关键论据:
  - MacBook Neo 使用 A18 Pro 芯片 (与 iPhone 16 Pro 相同)
  - 同芯片、同内存、同架构
  - 但 iPhone 被人为限制软件安装
  - 这是企业利润动机，非用户安全
```

### MacBook Neo vs iPhone 16 Pro 对比
```
| 特性 | MacBook Neo | iPhone 16 Pro | 差异 |
|------|-------------|---------------|------|
| 芯片 | A18 Pro | A18 Pro | ✅ 相同 |
| CPU 核 | 6 (2+4) | 6 (2+4) | ✅ 相同 |
| GPU 核 | 5 | 5 | ✅ 相同 |
| 内存 | 8GB | 8GB | ✅ 相同 |
| 架构 | ARM64 | ARM64 | ✅ 相同 |
| 操作系统 | macOS | iOS | ❌ 不同 |
| 软件安装 | 自由 (任何来源) | 限制 (仅 App Store) | ❌ 人为 |
| 文件系统访问 | ✅ 完整 | ❌ 沙盒限制 | ❌ 人为 |
| Shell 访问 | ✅ 完整 | ❌ 无用户 Shell | ❌ 人为 |
| 自定义 OS | ✅ (Asahi Linux) | ❌ (Bootloader 锁定) | ❌ 人为 |

作者质疑:
  "如果同样的芯片可以在 MacBook 上运行 macOS，
   为什么不能在 iPhone 上运行？
   
   答案不是技术限制，而是商业控制。"
```

---

## 🔐 软件安装自由对比

### MacBook (macOS)
```
✅ 软件来源自由
  - 可以从任何网站下载软件
  - 可以使用任何浏览器
  - 无需 Apple 审批
  - 无需 Apple 账户 (可选)

✅ 开发自由
  - 可以运行任意代码
  - 可以编译自己的软件
  - 完整文件系统访问
  - 完整的 Shell 访问

✅ 系统替换自由
  - 可以安装 Asahi Linux
  - 可以双系统启动
  - Bootloader 未锁定 (M 系列)
  - Apple 允许自定义内核启动

✅ 用户控制权
  - 设备完全属于用户
  - 用户可以决定运行什么
  - 无强制应用商店
  - 无 30% 佣金
```

### iPhone (iOS)
```
❌ 软件来源限制 (美国)
  - 必须通过 App Store
  - 侧载 (sideloading) 受限
  - 需要 Apple 审批
  - 需要 Apple 账户

❌ 开发限制
  - 代码运行沙盒化
  - 无完整文件系统访问
  - 无用户 Shell
  - 某些 API 需审批

❌ 系统替换禁止
  - 无法安装其他 OS
  - Bootloader 锁定
  - 越狱 (Jailbreak) 违法 (DMCA)
  - Apple 积极阻止

❌ 用户控制权受限
  - 设备部分属于 Apple
  - Apple 决定可运行软件
  - 强制 App Store (美国)
  - 30% 佣金 ("Apple 税")

Apple 理由:
  - "用户安全"
  - "防止恶意软件"
  - "保护隐私"
  - "确保质量"

作者反驳:
  - "这是对用户智力的侮辱"
  - "MacBook 同样安全但更自由"
  - "真正动机是 30% 佣金"
  - "安全不应以自由为代价"
```

---

## 📜 Right to Root Access 运动

### 核心主张
```
定义：Right to Root Access (根权限权利)

主张:
  "用户购买的每一台设备都应该有能力加载用户选择的软件。"

具体权利:
  1. 软件安装自由
     - 可以从任何来源安装软件
     - 不强制通过单一应用商店
     - 无需厂商审批

  2. 系统替换自由
     - 可以安装替代操作系统
     - Bootloader 不应锁定
     - 可以修改设备软件

  3. 硬件访问自由
     - 完整文件系统访问
     - Shell/终端访问
     - 硬件接口访问 (USB, GPIO 等)

  4. 修改自由
     - 可以修改系统软件
     - 可以越狱/Root
     - 不受 DMCA 限制

  5. 维修自由 (关联 Right to Repair)
     - 可以自行维修
     - 获取维修工具和零件
     - 不受软件锁限制
```

### 与 Right to Repair 关系
```
Right to Repair (维修权):
  - 焦点：硬件维修
  - 目标：可以自行维修设备
  - 进展：美国多州立法通过
  - 局限：仅硬件，不含软件

Right to Root Access (根权限权):
  - 焦点：软件控制
  - 目标：可以自行控制系统
  - 进展：早期倡导阶段
  - 扩展：包含 Right to Repair

关系:
  - Right to Root 是 Right to Repair 的自然扩展
  - 硬件维修权 + 软件控制权 = 完整设备所有权
  - 两者都反对厂商锁定
  - 两者都主张用户主权

作者观点:
  "Right to Root Access 必须在更广泛的'维修权'讨论中倡导。
   近两 decade 后，iPhone 芯片已成长为计算猛兽，
   甚至 iPhone 芯片都能运行 macOS。
   
   但限制软件安装的机制不可接受。"
```

### 历史背景
```
iPhone 软件控制演变:

2007: iPhone 发布
  - 无 App Store
  - 仅预装应用
  - 网页应用是唯一扩展

2008: App Store 发布
  - 第三方应用允许
  - 但必须通过 App Store
  - 越狱社区兴起

2010s: 越狱黄金时代
  - Cydia 等第三方商店
  - 功能定制流行
  - Apple 持续封堵

2015: 安全性加强
  - Secure Boot 强化
  - 代码签名更严格
  - 越狱难度增加

2020: DMCA 豁免争议
  - 越狱合法性质疑
  - 图书馆/教育例外
  - 消费者权利受限

2024: 欧盟 DMA 强制侧载
  - Apple 被迫允许第三方商店
  - 仅限欧盟
  - 复杂合规要求

2026: 现状
  - 美国：仅 App Store (iPhone)
  - 欧盟：可侧载 (DMA 合规)
  - 其他地区：混合
  - 越狱：技术上困难，法律上灰色

关键转折:
  - MacBook Neo 发布暴露双重标准
  - 同芯片不同自由
  - Right to Root 运动获得新论据
```

---

## 💰 商业动机分析

### Apple 利润结构
```
App Store 收入 (2025 财年估计):
  - 总收入：~$250 亿
  - 佣金收入：~$100 亿 (30% 平均)
  - 利润率：~80% (极高)

如果允许侧载:
  - 预计损失：$50-80 亿/年
  - 比例：总利润 ~5%
  - 但增长预期受损

为什么 Apple 坚持:
  1. 直接收入
     - 30% 佣金 ("Apple 税")
     - 订阅分成 (第一年 30%, 后续 15%)
     - 应用内购买分成

  2. 生态控制
     - 决定什么应用可存在
     - 可以移除竞争对手
     - 推广自家服务

  3. 数据收集
     - 了解用户行为
     - 定向广告
     - 产品改进

  4. 安全借口
     - "保护用户"是公关说辞
     - 实际是商业控制
     - MacBook 证明可兼顾安全和自由
```

### 对比其他平台
```
| 平台 | 软件来源 | 佣金 | Bootloader | Root/越狱 |
|------|----------|------|------------|-----------|
| iPhone (美) | 仅 App Store | 30% | 锁定 | 违法 (DMCA) |
| iPhone (欧) | App Store + 侧载 | 30%/0% | 锁定 | 违法 (DMCA) |
| Android | 任意 | 0-30% | 多数可解锁 | 合法 |
| macOS | 任意 | 0% | 未锁定 | 合法 |
| Windows | 任意 | 0% | 未锁定 | 合法 |
| Steam Deck | 任意 | 0% | 可解锁 | 合法 |

结论:
  - iPhone 是最封闭的主流平台
  - Android 最开放 (但厂商各有差异)
  - 桌面平台普遍开放
  - 移动端普遍封闭 (历史原因)

例外:
  - Fairphone (欧盟): 完全开放
  - PinePhone: Linux 手机，完全开放
  - Framework Phone (计划): 模块化 + 开放
```

---

## 🛠️ 技术可行性

### 为什么 iPhone 能运行 macOS
```
硬件能力:
  ✅ A18 Pro 与 MacBook Neo 相同
  ✅ 足够的 CPU/GPU 性能
  ✅ 足够的内存 (8GB)
  ✅ ARM64 架构兼容

软件障碍:
  ❌ Bootloader 锁定 (iBoot)
  ❌ 安全启动链 (Secure Boot)
  ❌ 代码签名强制
  ❌ 硬件 Fuse 熔断

技术上可行吗？
  - 答案：✅ 完全可行
  - 证据：MacBook Neo 用同样芯片运行 macOS
  - 障碍：人为软件锁，非硬件限制

如果 Apple 愿意:
  - 可以发布"iPhone macOS Mode"
  - 连接显示器即切换
  - 类似 Samsung DeX
  - 技术无难度
```

### 越狱技术现状 (2026)
```
当前越狱工具:

palera1n (iOS 15-16):
  - 基于 checkm8 硬件漏洞
  - 仅 A11 及以下设备
  - 半越狱 (semi-tethered)
  - 状态：✅ 可用

Dopamine (iOS 15-16.6.1):
  - 软件漏洞
  - A12 及以上设备
  - 无越狱 (rootless)
  - 状态：✅ 可用

XinaA15 (iOS 15-15.4.1):
  - A15 设备专用
  - 完整越狱
  - 状态：⚠️ 有限支持

iOS 17+:
  - 无公开越狱
  - Apple 修复大部分漏洞
  - 状态：❌ 不可用

趋势:
  - 越狱难度逐年增加
  - 硬件漏洞被修复 (checkm8 后无新硬件漏洞)
  - 软件漏洞快速修补
  - 越狱社区萎缩

未来:
  - 欧盟 DMA 可能迫使 Apple 开放
  - 美国 Right to Root 立法提案
  - 技术越狱可能不再必要 (如果法律强制开放)
```

---

## ⚖️ 法律与政策

### 美国法律现状
```
DMCA (Digital Millennium Copyright Act):
  - Section 1201: 禁止规避技术保护措施
  - 影响：越狱可能违法
  - 例外：图书馆每 3 年审议豁免

2024 豁免:
  - ✅ 智能手机越狱 (有限)
  - ✅ 平板电脑越狱 (首次)
  - ✅ 个人使用合法
  - ❌ 分发越狱工具仍违法
  - ❌ 商业用途违法

Right to Repair 立法:
  - 通过州：NY, CA, MN, 等 10+ 州
  - 范围：硬件维修
  - 不含：软件控制权
  - 进展：联邦立法提案中

Right to Root 提案:
  - 状态：早期倡导
  - 组织：EFF, Fight for the Future
  - 目标：修改 DMCA Section 1201
  - 阻力：Apple, 唱片业，电影业
```

### 欧盟 DMA (Digital Markets Act)
```
生效：2024-03-07
适用：守门人平台 (Apple, Google 等)

对 Apple 要求:
  ✅ 允许第三方应用商店
  ✅ 允许侧载 (sideloading)
  ✅ 允许第三方支付
  ✅ 开放 NFC 访问
  ✅ 开放浏览器引擎

Apple 合规:
  - iOS 17.4 (欧盟专用)
  - 允许第三方商店
  - 但设置复杂障碍
  - 仍收"核心技术服务费"

效果:
  - 欧盟用户可侧载
  - 但 Apple 设置"恐吓"弹窗
  - 实际采用率低 (~1-2%)
  - 被批"恶意合规"

全球影响:
  - 日本、韩国考虑类似立法
  - 美国讨论但无进展
  - 中国：已开放第三方商店
  - 印度：调查 Apple/Google 垄断
```

---

## 🌍 用户选择

### 现状下的选择
```
如果你想要软件自由:

选项 1: Android 手机
  优点：可解锁 Bootloader, 可 Root, 可侧载
  缺点：碎片化，安全更新慢
  推荐：Pixel, Nothing Phone, Fairphone

选项 2: iPhone + 接受限制
  优点：生态好，安全更新快
  缺点：软件受限，无 Root
  适合：不折腾用户

选项 3: iPhone + 越狱 (如果可用)
  优点：获得 Root，可定制
  缺点：不稳定，失去保修，安全风险
  适合：高级用户

选项 4: 等待立法改变
  优点：合法获得自由
  缺点：可能需要多年
  适合：耐心用户

选项 5: 转向桌面
  优点：完全自由
  缺点：便携性差
  适合：固定场景
```

### 作者的选择
```
Medhir Jaddou 的计划:

短期:
  - 继续使用 iPhone (已购买)
  - 倡导 Right to Root
  - 撰写文章提高意识

中期:
  - 考虑转向"更少侵入的手机"
  - 提到：Mudita Kompakt (dumbwireless.com)
  - 功能手机，隐私友好

长期愿景:
  - 将 iPhone 改造成 Web 服务器
  - "我已经为设备付费"
  - "它显然是完整计算机"
  - "为什么不能按我意愿修改？"

他的呼吁:
  "我现在非常想在 iPhone 上运行 macOS。
   根权限权利将使这一切成为可能。
   我真的想这么做。"
```

---

## 📊 知识点统计

| 类别 | 数量 |
|------|------|
| 设备对比 | 8 |
| 软件自由对比 | 8 |
| Right to Root 主张 | 5 |
| 历史演变 | 6 |
| 商业分析 | 8 |
| 平台对比 | 6 |
| 技术可行性 | 6 |
| 越狱现状 | 5 |
| 法律政策 | 8 |
| 用户选择 | 5 |
| **总计** | **65 点** |

---

## 🔗 相关资源

- **原文**: https://medhir.com/blog/your-phone-is-an-entire-computer
- **Right to Root**: https://medhir.com/blog/right-to-root-access
- **HN 讨论**: https://news.ycombinator.com/item?id=47367568
- **EFF 越狱合法**: https://www.eff.org/issues/coders/reverse-engineering-faq
- **欧盟 DMA**: https://digital-markets-act.ec.europa.eu/index_en

---

## 🏷️ 元数据

```json
{
  "created": "2026-03-14T06:22:00Z",
  "source": "HN #47367568 + medhir.com",
  "points": 288,
  "comments": 258,
  "domain": "数字权利/设备自由",
  "tags": ["right-to-root", "device-freedom", "ios-jailbreak", "software-freedom", "digital-rights", "apple"],
  "knowledge_points": 65,
  "word_count": 3200,
  "file_size": "~17KB"
}
```

---

*创建时间：2026-03-14 06:22 UTC*  
*Cron #71 深度内容 #3*  
*状态：✅ 完成*
