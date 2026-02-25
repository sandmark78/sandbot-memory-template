---
name: markdown-new
description: 将任何 URL 转换为干净、AI 友好的 Markdown 格式。使用 Cloudflare 原生 text/markdown 内容类型，节省 80% token。无需 API 密钥，0.1-0.6s 响应时间。
homepage: https://markdown.new
metadata: {"openclaw":{"emoji":"📝","requires":{"bins":["python3","pip"],"env":[],"packages":["requests"]},"primaryEnv":""}}
---

# markdown.new - URL 转 Markdown 技能

**将任何网页转换为 AI 友好的 Markdown 格式**

- 🚀 **80% token 节省** - 相比原始 HTML
- ⚡ **0.1-0.6s 响应** - Cloudflare 边缘加速
- 🔒 **无需 API 密钥** - 开箱即用
- 🌐 **支持 JS 重页面** - 三层回退机制

---

## 🎯 使用场景

当用户请求以下任务时触发：
- "把这个链接转成 Markdown"
- "提取这个网页的内容"
- "帮我读一下这个文章"
- "总结这个网页的主要内容"
- "https://example.com/article 转 Markdown"
- 任何涉及 URL 内容提取的请求

---

## 🚀 快速开始

### 基础用法
```bash
# 转换 URL 为 Markdown
python3 scripts/url_to_markdown.py "https://example.com/article"

# 指定转换方法 (auto/ai/browser)
python3 scripts/url_to_markdown.py "https://example.com" --method browser

# 保留图片
python3 scripts/url_to_markdown.py "https://example.com" --retain-images true
```

### 在对话中使用
```
用户：把这个链接转成 Markdown https://example.com/article

AI: 好的，正在转换...
[调用 markdown-new 技能]
[输出 Markdown 内容]
```

---

## 📋 命令参考

### 主命令
```bash
python3 scripts/url_to_markdown.py <url> [options]
```

### 参数说明

| 参数 | 说明 | 默认值 | 可选值 |
|------|------|--------|--------|
| `url` | 要转换的 URL (必填) | - | 任意 HTTP/HTTPS URL |
| `--method, -m` | 转换方法 | auto | auto, ai, browser |
| `--retain_images` | 保留图片 | false | true, false |
| `--output, -o` | 输出文件路径 | 不保存 | 文件路径 |
| `--verbose, -v` | 详细输出 | false | true, false |

### 转换方法说明

| 方法 | 说明 | 适用场景 | 速度 |
|------|------|----------|------|
| **auto** | 自动选择最佳方法 | 通用 | ⚡⚡⚡ |
| **ai** | Workers AI 转换 | 普通 HTML 页面 | ⚡⚡⚡ |
| **browser** | 浏览器渲染 | JS 重页面 (SPA) | ⚡⚡ |

---

## 💡 使用示例

### 示例 1: 转换博客文章
```bash
# 转换 Medium 文章
python3 scripts/url_to_markdown.py "https://medium.com/@user/ai-agents-guide"

# 输出示例：
# # AI Agents 完全指南
# 
# ## 简介
# AI Agents 是自主执行任务的智能系统...
# 
# ## 核心组件
# - 感知模块
# - 决策引擎
# - 执行框架
```

### 示例 2: 转换技术文档
```bash
# 转换 GitHub README
python3 scripts/url_to_markdown.py "https://github.com/openclaw/openclaw"

# 输出示例：
# # OpenClaw
# 
# **AI Agent 操作系统**
# 
# ## 安装
# ```bash
# npm install -g openclaw
# ```
```

### 示例 3: 转换新闻文章
```bash
# 转换新闻网站 (JS 重页面，使用 browser 模式)
python3 scripts/url_to_markdown.py "https://example-news.com/breaking-news" --method browser

# 保存为文件
python3 scripts/url_to_markdown.py "https://example.com" -o /tmp/article.md
```

### 示例 4: 批量转换
```bash
# 批量转换多个 URL
urls=(
  "https://example.com/article1"
  "https://example.com/article2"
  "https://example.com/article3"
)

for url in "${urls[@]}"; do
  python3 scripts/url_to_markdown.py "$url" -o "output_$(echo $url | md5sum).md"
done
```

---

## 🔧 技术实现

### 三层转换管道

```
┌─────────────────────────────────────────────────────────┐
│                    URL 输入                              │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ Layer 1: Markdown for Agents (Accept: text/markdown)    │
│ - Cloudflare 边缘直接返回 Markdown                        │
│ - 速度最快，零解析                                        │
└─────────────────────────────────────────────────────────┘
                          │ 失败
                          ▼
┌─────────────────────────────────────────────────────────┐
│ Layer 2: Workers AI toMarkdown()                        │
│ - HTML → Markdown 转换                                   │
│ - 快速，无需重新获取                                      │
└─────────────────────────────────────────────────────────┘
                          │ 失败
                          ▼
┌─────────────────────────────────────────────────────────┐
│ Layer 3: Browser Rendering                              │
│ - 完整浏览器渲染                                         │
│ - 支持 JS 重页面 (SPA)                                    │
└─────────────────────────────────────────────────────────┘
```

### 核心代码逻辑
```python
def url_to_markdown(url: str, method: str = "auto") -> str:
    """
    三层回退转换逻辑
    
    1. 尝试 text/markdown (最快)
    2. 回退 Workers AI (快速)
    3. 回退 Browser Rendering (完整)
    """
    if method == "auto":
        # 自动选择：先试 text/markdown
        response = requests.get(url, headers={"Accept": "text/markdown"})
        if response.headers["Content-Type"] == "text/markdown":
            return response.text
    
    # 回退到 API 转换
    response = requests.post(
        "https://markdown.new/",
        json={"url": url, "method": method},
        timeout=30
    )
    return response.text
```

---

## 📊 性能对比

### Token 节省
| 格式 | Token 数 | 对比 |
|------|----------|------|
| **原始 HTML** | 16,180 | 100% |
| **Markdown** | 3,150 | **80% 节省** |

### 响应时间
| 方法 | 平均时间 | 适用场景 |
|------|----------|----------|
| **text/markdown** | 0.1-0.3s | Cloudflare 站点 |
| **Workers AI** | 0.3-0.5s | 普通 HTML |
| **Browser** | 0.5-1.5s | JS 重页面 |

---

## ⚠️ 限制说明

| 限制 | 说明 |
|------|------|
| **依赖外部服务** | markdown.new 由 Cloudflare 提供，服务下线则技能失效 |
| **不支持认证页面** | 无法访问需要登录的网页 |
| **不支持私有内容** | 无法访问付费墙后内容 |
| **大文件限制** | 超过 10MB 页面可能超时 |
| **动态内容** | 部分 JS 重页面可能需要 browser 模式 |

---

## 🔗 相关资源

- **官方网站**: https://markdown.new
- **Cloudflare 文档**: https://developers.cloudflare.com/workers-ai/
- **Markdown for Agents**: https://github.com/cloudflare/markdown-for-agents

---

## 📝 更新日志

### v1.0.0 (2026-02-24)
- ✅ 初始版本发布
- ✅ 三层转换管道实现
- ✅ 支持 auto/ai/browser 方法
- ✅ 图片保留选项
- ✅ 文件输出支持

---

*此技能已真实写入服务器*
*创建时间：2026-02-24 16:20 UTC*
*验证：cat /home/node/.openclaw/workspace/skills/markdown-new/SKILL.md*
