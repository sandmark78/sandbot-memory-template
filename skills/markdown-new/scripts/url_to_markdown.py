#!/usr/bin/env python3
"""markdown.new - URL 转 Markdown 工具 (无依赖版本)

将任何网页转换为 AI 友好的 Markdown 格式，节省 80% token。
使用 Cloudflare markdown.new 服务，无需 API 密钥，无需额外依赖。

用法:
    python3 url_to_markdown.py <url> [options]

示例:
    python3 url_to_markdown.py "https://example.com/article"
    python3 url_to_markdown.py "https://example.com" --method browser
    python3 url_to_markdown.py "https://example.com" -o output.md
"""

import argparse
import json
import ssl
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

# --- 常量 ---
API_URL = "https://markdown.new/"
DEFAULT_TIMEOUT = 30
USER_AGENT = "markdown-new-skill/1.0 (OpenClaw Agent)"


def url_to_markdown(url: str, method: str = "auto", retain_images: bool = False, timeout: int = DEFAULT_TIMEOUT) -> str:
    """
    将 URL 转换为 Markdown 格式 (使用 urllib 标准库，无需额外依赖)
    
    Args:
        url: 要转换的 URL
        method: 转换方法 (auto/ai/browser)
        retain_images: 是否保留图片
        timeout: 请求超时时间 (秒)
    
    Returns:
        转换后的 Markdown 文本
    
    Raises:
        urllib.error.URLError: 网络请求失败
        ValueError: URL 无效或转换失败
    """
    # 验证 URL
    if not url.startswith(("http://", "https://")):
        raise ValueError(f"无效的 URL 格式：{url} (必须以 http:// 或 https:// 开头)")
    
    # 构建请求数据
    payload = {
        "url": url,
        "method": method,
        "retain_images": str(retain_images).lower() == "true"
    }
    
    # 创建请求
    data = json.dumps(payload).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "User-Agent": USER_AGENT,
        "Accept": "text/markdown"
    }
    
    request = urllib.request.Request(
        API_URL,
        data=data,
        headers=headers,
        method="POST"
    )
    
    start_time = time.time()
    
    # 创建 SSL 上下文 (忽略证书验证警告，生产环境应该验证)
    ssl_context = ssl.create_default_context()
    
    try:
        # 发送请求
        with urllib.request.urlopen(
            request,
            timeout=timeout,
            context=ssl_context
        ) as response:
            # 获取转换时间
            elapsed = time.time() - start_time
            
            # 获取响应头
            content_type = response.headers.get("Content-Type", "")
            
            # 读取响应内容
            markdown_content = response.read().decode("utf-8")
            
            # 添加元数据注释
            metadata = [
                "<!-- 转换信息 -->",
                f"<!-- 源 URL: {url} -->",
                f"<!-- 转换方法：{method} -->",
                f"<!-- 转换时间：{elapsed:.2f}s -->",
                f"<!-- 内容类型：{content_type} -->",
                ""
            ]
            
            return "\n".join(metadata) + markdown_content
        
    except urllib.error.HTTPError as e:
        if e.code == 429:
            raise ValueError("请求过于频繁，请稍后重试 (速率限制)")
        raise ValueError(f"HTTP 错误 {e.code}: {e.read().decode('utf-8')[:200]}")
    except urllib.error.URLError as e:
        if isinstance(e.reason, TimeoutError):
            raise ValueError(f"请求超时 ({timeout}秒)，请尝试：1. 检查网络连接 2. 使用 browser 模式 3. 稍后重试")
        raise ValueError(f"网络错误：{e.reason}")
    except TimeoutError:
        raise ValueError(f"请求超时 ({timeout}秒)，请稍后重试")
    except Exception as e:
        raise ValueError(f"转换失败：{str(e)}")


def save_to_file(content: str, output_path: str) -> str:
    """
    将内容保存到文件
    
    Args:
        content: 要保存的内容
        output_path: 输出文件路径
    
    Returns:
        实际保存的文件路径
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return str(path.absolute())


def main():
    """主函数 - 解析参数并执行转换"""
    parser = argparse.ArgumentParser(
        description="将 URL 转换为 Markdown 格式 (无需额外依赖)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s "https://example.com/article"
  %(prog)s "https://example.com" --method browser
  %(prog)s "https://example.com" -o output.md --verbose
        """
    )
    
    parser.add_argument(
        "url",
        help="要转换的 URL (必须以 http:// 或 https:// 开头)"
    )
    
    parser.add_argument(
        "-m", "--method",
        choices=["auto", "ai", "browser"],
        default="auto",
        help="转换方法 (默认：auto)"
    )
    
    parser.add_argument(
        "--retain-images",
        choices=["true", "false"],
        default="false",
        help="是否保留图片 (默认：false)"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="输出文件路径 (不指定则输出到 stdout)"
    )
    
    parser.add_argument(
        "-t", "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help=f"请求超时时间 (秒，默认：{DEFAULT_TIMEOUT})"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="显示详细信息"
    )
    
    args = parser.parse_args()
    
    # 执行转换
    if args.verbose:
        print(f"🔄 开始转换：{args.url}", file=sys.stderr)
        print(f"   方法：{args.method}", file=sys.stderr)
        print(f"   保留图片：{args.retain_images}", file=sys.stderr)
        print(f"   超时：{args.timeout}s", file=sys.stderr)
    
    try:
        markdown_content = url_to_markdown(
            url=args.url,
            method=args.method,
            retain_images=(args.retain_images == "true"),
            timeout=args.timeout
        )
        
        # 输出结果
        if args.output:
            output_path = save_to_file(markdown_content, args.output)
            if args.verbose:
                print(f"✅ 已保存到：{output_path}", file=sys.stderr)
            else:
                print(f"文件已保存：{output_path}")
        else:
            # 输出到 stdout
            print(markdown_content)
            
    except ValueError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️  用户中断", file=sys.stderr)
        sys.exit(130)


if __name__ == "__main__":
    main()
