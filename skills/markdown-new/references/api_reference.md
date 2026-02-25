# markdown.new API 参考

**官方文档**: https://markdown.new

---

## API 端点

```
POST https://markdown.new/
```

---

## 请求格式

### JSON Body
```json
{
  "url": "https://example.com/article",
  "method": "auto",
  "retain_images": false
}
```

### 参数说明

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `url` | string | ✅ | - | 要转换的 URL |
| `method` | string | ❌ | `"auto"` | 转换方法 (auto/ai/browser) |
| `retain_images` | boolean | ❌ | `false` | 是否保留图片 |

---

## 转换方法

### auto (推荐)
```
自动选择最佳转换方法：
1. 尝试 text/markdown (最快)
2. 回退 Workers AI (快速)
3. 回退 Browser Rendering (完整)
```

### ai
```
使用 Cloudflare Workers AI 进行 HTML→Markdown 转换
- 速度：快 (0.3-0.5s)
- 适用：普通 HTML 页面
- 不支持：JS 重页面
```

### browser
```
使用浏览器渲染完整页面
- 速度：中等 (0.5-1.5s)
- 适用：JS 重页面 (SPA)
- 支持：动态加载内容
```

---

## 响应格式

### 成功响应 (200 OK)
```
Content-Type: text/markdown

# 文章标题

文章内容...
```

### 错误响应

#### 400 Bad Request
```json
{
  "error": "Invalid URL",
  "message": "URL must start with http:// or https://"
}
```

#### 429 Too Many Requests
```json
{
  "error": "Rate Limited",
  "message": "Too many requests. Please wait before retrying."
}
```

#### 500 Internal Server Error
```json
{
  "error": "Conversion Failed",
  "message": "Failed to convert URL to Markdown"
}
```

---

## 速率限制

| 限制 | 说明 |
|------|------|
| **请求频率** | 未公开 (建议 < 100 次/分钟) |
| **并发连接** | 未公开 (建议 < 10 并发) |
| **超时时间** | 30 秒 |

---

## 使用示例

### cURL
```bash
# 基础用法
curl -X POST "https://markdown.new/" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/article"}'

# 指定方法
curl -X POST "https://markdown.new/" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "method": "browser"}'

# 保留图片
curl -X POST "https://markdown.new/" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "retain_images": true}'
```

### Python
```python
import requests

response = requests.post(
    "https://markdown.new/",
    json={
        "url": "https://example.com/article",
        "method": "auto",
        "retain_images": False
    },
    headers={"Content-Type": "application/json"},
    timeout=30
)

markdown_content = response.text
print(markdown_content)
```

### JavaScript
```javascript
const response = await fetch("https://markdown.new/", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    url: "https://example.com/article",
    method: "auto"
  })
});

const markdown = await response.text();
console.log(markdown);
```

---

## 最佳实践

### 1. 错误处理
```python
try:
    response = requests.post(
        "https://markdown.new/",
        json={"url": url},
        timeout=30
    )
    response.raise_for_status()
    markdown = response.text
except requests.exceptions.Timeout:
    print("请求超时，请重试")
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 429:
        print("请求过于频繁，请稍后重试")
    else:
        print(f"HTTP 错误：{e.response.status_code}")
```

### 2. 重试机制
```python
import time
from requests.exceptions import RequestException

def convert_with_retry(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.post(
                "https://markdown.new/",
                json={"url": url},
                timeout=30
            )
            response.raise_for_status()
            return response.text
        except RequestException as e:
            if attempt == max_retries - 1:
                raise
            wait_time = 2 ** attempt  # 指数退避
            time.sleep(wait_time)
```

### 3. 批量处理
```python
from concurrent.futures import ThreadPoolExecutor

def convert_urls(urls, max_workers=5):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(url_to_markdown, urls))
    return results
```

---

## 故障排查

### 问题 1: 请求超时
```
症状：TimeoutError
原因：网络问题或服务繁忙
解决：
1. 检查网络连接
2. 增加 timeout 参数
3. 稍后重试
```

### 问题 2: 转换结果为空
```
症状：返回空字符串
原因：页面无法访问或内容为空
解决：
1. 验证 URL 是否有效
2. 尝试 browser 模式
3. 检查页面是否需要登录
```

### 问题 3: 图片丢失
```
症状：Markdown 中无图片
原因：retain_images 默认为 false
解决：设置 retain_images: true
```

---

## 相关资源

- **官方文档**: https://markdown.new
- **Cloudflare Workers AI**: https://developers.cloudflare.com/workers-ai/
- **Markdown for Agents**: https://github.com/cloudflare/markdown-for-agents

---

*最后更新：2026-02-24*
*版本：1.0.0*
