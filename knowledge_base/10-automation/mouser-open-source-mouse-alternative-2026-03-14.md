# Mouser 开源鼠标软件：Logitech Options+ 替代方案

**来源**: HN Show HN (258 pts, 2026-03-14)  
**项目**: https://github.com/TomBadash/MouseControl  
**标签**: #开源替代 #外设驱动 #隐私保护 #本地优先

---

## 📋 核心洞察

### 问题背景
```
痛点：Logitech Options+ 软件存在的问题
  - 强制云连接和遥测
  - 需要 Logitech 账户登录
  - 臃肿的资源占用
  - 隐私数据收集担忧

解决方案：Mouser - 完全本地化的开源替代
  - 零遥测、零云服务、零账户要求
  - 纯本地配置 (JSON 文件)
  - 开源透明 (MIT License)
  - 轻量级运行 (系统托盘后台)
```

### 技术架构
```
┌─────────────┐ ┌──────────┐ ┌────────────────┐
│ Mouse HW    │──▶│ Mouse    │──▶│ Engine         │
│ (MX Master) │  │ Hook     │  │ (orchestrator) │
└─────────────┘ └──────────┘ └───────┬────────┘
  ▲                                  │
  │ block/pass                  ┌────▼────────┐
  │                          │ Key         │
┌─────────────┐ ┌──────────┐ │ Simulator   │
│ QML UI      │◀───▶│ Backend  │ │ (SendInput) │
│ (PySide6)   │  │ (QObject)│ └─────────────┘
└─────────────┘ └──────────┘
  ▲
  ┌────┴────────┐
  │ App         │
  │ Detector    │
  └─────────────┘

核心组件:
  1. Low-level Mouse Hook (WH_MOUSE_LL)
     - 拦截 WM_XBUTTONDOWN/UP (侧键)
     - 拦截 WM_MBUTTONDOWN/UP (中键)
     - 拦截 WM_MOUSEHWHEEL (横向滚动)
  
  2. HID++ 2.0 Gesture Button (蓝牙)
     - REPROG_CONTROLS_V4 (feature 0x1B04)
     - Divert CID 0x00C3 (手势按钮)
     - 无需 Logitech 软件
  
  3. App Detector (每 300ms 轮询)
     - GetForegroundWindow → 进程名
     - 自动切换配置文件
  
  4. Config Manager (本地 JSON)
     - %APPDATA%\Mouser\config.json
     - 多配置文件支持
     - 版本迁移机制
```

### 核心功能
```
✅ 6 个可编程按钮重映射
   - 后退/前进键
   - 中键点击
   - 手势按钮
   - 横向滚动左/右

✅ 22 个内置动作
   - 导航：Alt+Tab, Win+D, Win+Tab
   - 浏览器：后退/前进/关闭标签/新建标签
   - 编辑：复制/粘贴/剪切/撤销/全选/保存/查找
   - 媒体：音量+/ -/静音/播放暂停/上/下一曲

✅ 每应用配置文件
   - 自动检测前台应用
   - 秒级配置切换
   - 支持 Chrome/VSCode/VLC 等

✅ DPI/指针速度控制
   - 范围：200-8000 DPI
   - 快速预设：400/800/1000/1600/2400/4000/6000/8000
   - 通过 HID++ 同步到设备

✅ 滚动方向反转
   - 垂直滚动独立开关
   - 水平滚动独立开关

✅ 自动重连
   - 检测鼠标开关/断开/重连
   - 自动恢复功能，无需重启应用

✅ 实时连接状态
   - UI 显示"Connected"/"Not Connected"徽章
   - 跨线程安全 (Qt signals)

✅ 系统托盘运行
   - 后台运行，隐藏到托盘
   - 托盘菜单切换重映射开关
   - 右键退出
```

### 技术栈
```
语言：Python 3.10+ (测试通过 3.14)
UI 框架：PySide6 (Qt Quick/QML)
底层通信：hidapi (HID++ 协议)
系统托盘：pystray
图像处理：Pillow
打包工具：PyInstaller (生成独立 exe)

依赖包:
  - PySide6: Qt Quick/QML UI 框架
  - hidapi: HID++ 通信 (手势按钮/DPI)
  - pystray: 系统托盘图标
  - Pillow: 图标生成
```

### 平台支持
```
✅ Windows 10/11 (完整支持)
✅ macOS 12+ (Monterey, 感谢 @andrew-sz)
   - CGEventTap 鼠标钩子
   - Quartz CGEvent 按键模拟
   - NSWorkspace 应用检测
   - NSEvent 媒体键支持

❌ Linux (暂不支持，计划中)
   - 计划：libevdev/evdev hooks

设备支持:
  ✅ Logitech MX Master 3S (PID 0xB034, HID++ 4.5)
  🔜 计划扩展：MX Master 3, MX Anywhere 3 等 HID++ 设备

连接方式:
  ✅ 蓝牙 (推荐，完整 HID++ 支持)
  ✅ USB 接收器 (基础按钮支持)
```

### 隐私优势
```
对比 Logitech Options+:

| 特性 | Options+ | Mouser |
|------|----------|--------|
| 云连接 | ✅ 强制 | ❌ 零 |
| 遥测 | ✅ 收集 | ❌ 零 |
| 账户 | ✅ 必须 | ❌ 零 |
| 配置存储 | 云端 | 本地 JSON |
| 源代码 | 闭源 | 开源 MIT |
| 资源占用 | 臃肿 | 轻量 |
| 后台服务 | 多个 | 单进程 |

隐私保护机制:
  - 零外部服务调用
  - 配置文件本地存储
  - 无网络权限需求
  - 开源代码可审计
```

### 安装部署
```
方式 1: 直接使用 (推荐)
  1. 下载 Mouser.zip (44 MB)
  2. 解压到任意文件夹
  3. 双击运行 Mouser.exe
  4. 完成 (系统托盘图标出现)

方式 2: 开发环境
  git clone https://github.com/TomBadash/MouseControl.git
  cd MouseControl
  python -m venv .venv
  source .venv/bin/activate  # Windows: .venv\Scripts\activate
  pip install -r requirements.txt
  python main_qml.py

方式 3: 独立打包
  pip install pyinstaller
  pyinstaller Mouser.spec --noconfirm
  # 输出：dist/Mouser/ (可分发的独立 exe)
```

### 配置示例
```json
{
  "version": 2,
  "profiles": [
    {
      "name": "Default (All Apps)",
      "apps": [],
      "mappings": {
        "back": "alt+tab",
        "forward": "alt+shift+tab",
        "middle": "passthrough",
        "gesture": "passthrough",
        "hscroll_left": "browser_back",
        "hscroll_right": "browser_forward"
      }
    },
    {
      "name": "VS Code",
      "apps": ["Code.exe"],
      "mappings": {
        "back": "ctrl+shift+p",
        "forward": "ctrl+p",
        "gesture": "ctrl+`"
      }
    }
  ],
  "global": {
    "dpi": 1600,
    "scroll_vertical_inverted": false,
    "scroll_horizontal_inverted": false,
    "start_with_windows": true
  }
}
```

### 已知限制
```
⚠️ 设备限制
  - 仅支持 MX Master 3S (PID 0xB034)
  - HID++ feature indices 硬编码
  - 扩展其他设备需修改代码

⚠️ 连接限制
  - 蓝牙推荐 (完整 HID++ 支持)
  - USB 接收器部分功能受限
  - 手势按钮蓝牙最佳

⚠️ 系统限制
  - Windows SmartScreen 首次警告 (需点击"更多信息"→"仍要运行")
  - 某些游戏/提权窗口可能不接收注入按键
  - 滚动反转实验性 (coalesced PostMessage 注入)

⚠️ 冲突软件
  - Logitech Options+ 不能同时运行 (HID++ 访问冲突)
  - 需先关闭 Options+ 再启动 Mouser
```

### 路线图
```
已完成:
  ✅ Windows 完整支持
  ✅ macOS 支持 (CGEventTap)
  ✅ HID++ 手势按钮 (蓝牙)
  ✅ 每应用配置文件
  ✅ DPI 控制
  ✅ 自动重连
  ✅ 系统托盘

计划中:
  🔜 Linux 支持 (libevdev/evdev)
  🔜 自定义组合键 (Ctrl+Shift+P 等)
  🔜 开机自启 (注册表/Task Scheduler)
  🔜 手势按钮多动作 (上/下/左/右滑动)
  🔜 配置文件导出/导入
  🔜 更多 Logitech HID++ 设备支持
  🔜 插件系统 (第三方动作提供者)
```

---

## 🧠 深度分析

### 开源替代趋势
```
背景：2026 年用户对隐私和控制的觉醒
  - Logitech Options+ 强制云连接引发不满
  - 用户反感遥测和账户绑定
  - 本地优先软件需求增长

Mouser 的成功要素:
  1. 精准痛点 (258 pts HN 热度)
  2. 完全本地化 (零云服务)
  3. 开源透明 (MIT License)
  4. 开箱即用 (44MB zip, 无需安装)
  5. 现代 UI (Qt Quick/QML, Material 暗色主题)

启示:
  - 闭源软件的云化是双刃剑
  - 本地优先是差异化竞争优势
  - 开源替代有市场需求
  - 用户体验不能妥协 (现代 UI 很重要)
```

### 技术实现亮点
```
1. 低层级鼠标钩子 (WH_MOUSE_LL)
   - 独立后台线程 + Win32 消息泵
   - 拦截/阻断/替换鼠标事件
   - 避免钩子死锁 (coalesced PostMessage)

2. HID++ 2.0 协议逆向
   - REPROG_CONTROLS_V4 (0x1B04)
   - Divert 手势按钮 (CID 0x00C3)
   - 无需官方 SDK

3. 轻量级配置切换
   - 不清理钩子线程/HID++ 连接
   - 仅重新绑定回调
   - 避免延迟和不稳定

4. 设备断连恢复
   - HID++ 层：读错误检测 → 2-5 秒重试
   - 钩子层：WM_DEVICECHANGE 通知 → 重新安装钩子
   - UI 层：跨线程安全状态更新

5. 应用检测优化
   - 300ms 轮询 (平衡响应速度和性能)
   - UWP 应用处理 (ApplicationFrameHost → 子进程)
   - 进程名匹配 (简单高效)
```

### 商业模式思考
```
问题：开源软件如何可持续？

Mouser 方案:
  - GitHub Sponsors (自愿捐赠)
  - 无强制付费功能
  - 社区驱动开发

替代方案:
  - Open Core (基础免费，高级付费)
  - 双许可证 (GPL + 商业)
  - 托管服务 (配置同步/备份)
  - 企业支持 (SLA/定制开发)

建议:
  - 保持核心开源 (社区信任)
  - 可选云同步 (付费增值)
  - 企业定制 (主要收入来源)
  - 捐赠 + 赞助 (社区支持)
```

---

## 📊 知识点统计

| 类别 | 数量 |
|------|------|
| 核心功能点 | 10 |
| 技术组件 | 8 |
| 平台支持 | 4 |
| 配置选项 | 6 |
| 已知限制 | 6 |
| 路线图项目 | 8 |
| 隐私对比项 | 7 |
| **总计** | **49 点** |

---

## 🔗 相关资源

- **项目仓库**: https://github.com/TomBadash/MouseControl
- **下载**: https://github.com/TomBadash/MouseControl/releases/latest
- **macOS 指南**: https://github.com/TomBadash/MouseControl/blob/master/readme_mac_osx.md
- **HN 讨论**: https://news.ycombinator.com/item?id=47368033

---

## 🏷️ 元数据

```json
{
  "created": "2026-03-14T06:20:00Z",
  "source": "HN Show HN #47368033",
  "points": 258,
  "comments": 77,
  "domain": "开源替代/外设驱动",
  "tags": ["open-source", "mouse", "privacy", "local-first", "python", "logitech"],
  "knowledge_points": 49,
  "word_count": 2800,
  "file_size": "~15KB"
}
```

---

*创建时间：2026-03-14 06:20 UTC*  
*Cron #71 深度内容 #1*  
*状态：✅ 完成*
