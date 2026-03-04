# Agent Browser 技能 (OpenClaw 原生适配版)

**技能名称**: `agent-browser-wrapper`  
**版本**: V1.0.0  
**创建时间**: 2026-03-03 07:45 UTC  
**依赖**: 零依赖 (使用 OpenClaw 原生 `browser` 工具)

---

## 🎯 功能定位

将 Vercel Agent Browser 的 CLI 语法映射到 OpenClaw 原生 `browser` 工具，实现：
- ✅ 零安装 (不用 npm install)
- ✅ 零依赖 (不用 Rust/Node.js)
- ✅ 即用 OpenClaw Browser 能力
- ✅ 语法兼容 Agent Browser 风格

---

## 📊 功能对比

| 功能 | Agent Browser CLI | OpenClaw Native | 状态 |
|------|-------------------|-----------------|------|
| 打开 URL | `open example.com` | `browser open` | ✅ 已映射 |
| 截图 | `snapshot` | `browser snapshot` | ✅ 已映射 |
| 点击 | `click @e2` | `browser act click ref=e2` | ✅ 已映射 |
| 填充 | `fill @e3 "text"` | `browser act fill ref=e3` | ✅ 已映射 |
| 语义搜索 | `find role button` | `browser snapshot refs=aria` | ✅ 已映射 |
| 等待 | `wait 3000` | `browser act wait timeMs=3000` | ✅ 已映射 |
| 键盘 | `press Enter` | `browser act press key=Enter` | ✅ 已映射 |
| 获取文本 | `get text @e1` | `browser snapshot` + 解析 | ✅ 可实现 |

---

## 🚀 使用方法

### 方法 1: 直接使用 OpenClaw Browser (推荐)

```
# 打开网页
browser open url="https://example.com"

# 获取快照 (带 aria refs)
browser snapshot refs="aria"

# 点击元素
browser act click ref="e2"

# 填充表单
browser act fill ref="e3" text="test@example.com"

# 截图
browser screenshot fullPage=true
```

### 方法 2: 使用包装脚本 (语法兼容 Agent Browser)

```bash
python3 /workspace/skills/agent-browser-wrapper/abw.py open https://example.com
python3 /workspace/skills/agent-browser-wrapper/abw.py snapshot
python3 /workspace/skills/agent-browser-wrapper/abw.py click @e2
python3 /workspace/skills/agent-browser-wrapper/abw.py fill @e3 "test@example.com"
```

---

## 🛠️ 包装脚本：abw.py

```python
#!/usr/bin/env python3
"""
Agent Browser Wrapper for OpenClaw
将 Agent Browser CLI 语法映射到 OpenClaw browser 工具

用法:
    python3 abw.py <command> [args]
    
示例:
    python3 abw.py open https://example.com
    python3 abw.py snapshot
    python3 abw.py click @e2
    python3 abw.py fill @e3 "test text"
"""

import sys
import json

def cmd_open(url):
    """打开 URL"""
    return {
        "tool": "browser",
        "action": "open",
        "targetUrl": url
    }

def cmd_snapshot(refs="aria"):
    """获取 accessibility tree"""
    return {
        "tool": "browser",
        "action": "snapshot",
        "refs": refs,
        "snapshotFormat": "aria"
    }

def cmd_click(ref):
    """点击元素"""
    ref_id = ref.lstrip('@')
    return {
        "tool": "browser",
        "action": "act",
        "request": {
            "kind": "click",
            "ref": ref_id
        }
    }

def cmd_fill(ref, text):
    """填充表单"""
    ref_id = ref.lstrip('@')
    return {
        "tool": "browser",
        "action": "act",
        "request": {
            "kind": "fill",
            "ref": ref_id,
            "fields": [{"text": text}]
        }
    }

def cmd_screenshot(path=None, full=False):
    """截图"""
    return {
        "tool": "browser",
        "action": "screenshot",
        "fullPage": full,
        "type": "png"
    }

def cmd_wait(time_ms=3000):
    """等待"""
    return {
        "tool": "browser",
        "action": "act",
        "request": {
            "kind": "wait",
            "timeMs": time_ms
        }
    }

def cmd_press(key):
    """按键"""
    return {
        "tool": "browser",
        "action": "act",
        "request": {
            "kind": "press",
            "key": key
        }
    }

def main():
    if len(sys.argv) < 2:
        print("用法：python3 abw.py <command> [args]")
        print("\n命令:")
        print("  open <url>          - 打开 URL")
        print("  snapshot            - 获取 accessibility tree")
        print("  click <ref>         - 点击元素 (@e2)")
        print("  fill <ref> <text>   - 填充表单")
        print("  screenshot [path]   - 截图")
        print("  wait [ms]           - 等待")
        print("  press <key>         - 按键")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "open":
        if len(sys.argv) < 3:
            print("错误：open 需要 URL 参数")
            sys.exit(1)
        result = cmd_open(sys.argv[2])
    
    elif cmd == "snapshot":
        result = cmd_snapshot()
    
    elif cmd == "click":
        if len(sys.argv) < 3:
            print("错误：click 需要 ref 参数 (@e2)")
            sys.exit(1)
        result = cmd_click(sys.argv[2])
    
    elif cmd == "fill":
        if len(sys.argv) < 4:
            print("错误：fill 需要 ref 和 text 参数")
            sys.exit(1)
        result = cmd_fill(sys.argv[2], sys.argv[3])
    
    elif cmd == "screenshot":
        path = sys.argv[2] if len(sys.argv) > 2 else None
        result = cmd_screenshot(path)
    
    elif cmd == "wait":
        time_ms = int(sys.argv[2]) if len(sys.argv) > 2 else 3000
        result = cmd_wait(time_ms)
    
    elif cmd == "press":
        if len(sys.argv) < 3:
            print("错误：press 需要 key 参数")
            sys.exit(1)
        result = cmd_press(sys.argv[2])
    
    else:
        print(f"未知命令：{cmd}")
        sys.exit(1)
    
    # 输出 JSON 格式的工具调用
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
```

---

## 📝 使用示例

### 示例 1: 打开网页并截图

```bash
# Agent Browser 语法
agent-browser open example.com
agent-browser screenshot page.png

# OpenClaw 原生
browser open url="https://example.com"
browser screenshot fullPage=true
```

### 示例 2: 填写表单并提交

```bash
# Agent Browser 语法
agent-browser open login.com
agent-browser snapshot
agent-browser fill @e3 "user@example.com"
agent-browser fill @e4 "password123"
agent-browser click @e5

# OpenClaw 原生
browser open url="https://login.com"
browser snapshot refs="aria"
browser act fill ref="e3" text="user@example.com"
browser act fill ref="e4" text="password123"
browser act click ref="e5"
```

### 示例 3: 语义搜索元素

```bash
# Agent Browser 语法
agent-browser find role button click --name "Submit"

# OpenClaw 原生
browser snapshot refs="aria"
# 从快照中找到 button，获取 ref
browser act click ref="e10"
```

---

## 🎯 与 Agent Browser 对比

| 维度 | Agent Browser | OpenClaw + abw | 优势 |
|------|---------------|----------------|------|
| 安装 | ❌ npm install | ✅ 零安装 | OpenClaw ✅ |
| 依赖 | ❌ Rust/Node.js | ✅ 无 | OpenClaw ✅ |
| 性能 | ⚡ Rust CLI | 🐢 Python 包装 | Agent Browser ✅ |
| 功能 | ✅ 完整 | ✅ 核心功能 | 平手 |
| AI 优化 | ✅ | ✅ | 平手 |
| 集成 | ❌ 外部工具 | ✅ OpenClaw 原生 | OpenClaw ✅ |

---

## 🔧 高级用法

### 1. 批量操作脚本

```python
#!/usr/bin/env python3
"""
批量浏览器操作示例
"""

operations = [
    {"cmd": "open", "url": "https://example.com"},
    {"cmd": "snapshot"},
    {"cmd": "click", "ref": "@e2"},
    {"cmd": "wait", "ms": 2000},
    {"cmd": "screenshot"},
]

for op in operations:
    # 执行操作
    pass
```

### 2. 元素定位辅助

```python
def find_element_by_text(text):
    """通过文本查找元素"""
    # 1. 获取快照
    snapshot = browser_snapshot()
    
    # 2. 搜索包含文本的元素
    for elem in snapshot['nodes']:
        if text in elem.get('name', ''):
            return elem['ref']
    
    return None
```

### 3. 表单自动填充

```python
def fill_form(form_data):
    """自动填充表单"""
    for field_name, field_value in form_data.items():
        ref = find_field_by_label(field_name)
        if ref:
            browser_act_fill(ref, field_value)
```

---

## ✅ 验证命令

```bash
# 1. 验证 OpenClaw browser 工具可用
browser status

# 2. 测试打开网页
browser open url="https://example.com"

# 3. 测试截图
browser snapshot refs="aria"

# 4. 测试包装脚本 (如果创建)
python3 /workspace/skills/agent-browser-wrapper/abw.py open https://example.com
```

---

## 🦞 Sandbot 建议

```
老大，分析结论：

✅ OpenClaw 的 browser 工具已经覆盖了 Agent Browser 的核心功能
✅ 无需安装外部 npm 包
✅ 无需 Rust/Node.js 依赖
✅ 直接用 browser open/snapshot/act 即可

如果需要语法兼容层：
- 创建 abw.py 包装脚本
- 映射 Agent Browser CLI → OpenClaw browser 工具
- 零安装，纯 Python

我的建议：
1. 直接用 OpenClaw browser 工具 (推荐)
2. 如需批量操作，写 Python 脚本调用
3. 不用安装 agent-browser npm 包

原因：
- 功能相同
- 零额外依赖
- 更好的 OpenClaw 集成
- 节省安装和维护成本

旅程继续。🏖️
```

---

*技能创建时间：2026-03-03 07:45 UTC*  
*验证：cat /workspace/skills/agent-browser-wrapper/SKILL.md*
