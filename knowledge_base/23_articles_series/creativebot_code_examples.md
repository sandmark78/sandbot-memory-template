《代码示例最佳实践》

目录

1. 可执行性原则
2. 环境兼容性
3. 错误处理
4. 性能优化
5. 安全考虑

正文

可执行性原则

完整命令:
代码示例必须包含完整的命令，不能省略关键参数或选项。

❌ 不完整示例:

# 获取数据
curl api > file

✅ 完整示例:

# 获取精真估估值数据
curl -s "https://www.jingzhengu.com/api/valuation" \
-H "Content-Type: application/json" \
--data '{"vin":"LSVCC24B3AM123456"}' \
> /home/node/.openclaw/workspace/main/viking/resources/rwa_data/tier1/jingzhengu_valuation.json

真实URL:
使用实际可用的API端点，而不是占位符。

❌ 占位符示例:

response = requests.get("https://api.example.com/data")

✅ 真实URL示例:

response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd")

绝对路径:
提供完整的文件路径，避免相对路径的歧义。

❌ 相对路径:

cat data.json

✅ 绝对路径:

cat /home/node/.openclaw/workspace/main/viking/resources/rwa_data/tier1/jingzhengu_valuation.json

环境兼容性

跨平台兼容:
确保代码在不同操作系统和环境中都能正常运行。

Shell脚本兼容性:

#!/bin/bash
# 使用标准POSIX命令，避免bash特有功能
# 兼容sh、bash、zsh等

# 使用$(command)而不是`command`
output=$(ls -la)

# 使用[[ ]]进行条件判断，而不是[ ]
if [[ -f "$file" ]]; then
echo "File exists"
fi

Python版本兼容:

# 兼容Python 3.6+
from typing import List, Dict # Python 3.5+

# 避免使用Python 3.8+特有的海象运算符(:=)
# 避免使用Python 3.9+特有的字典合并运算符(|)

def process_data(data: List[Dict]) -> Dict:
"""处理数据并返回结果"""
result = {}
for item in data:
if item.get("roi", 0) >= 1.5:
result[item["name"]] = item["value"]
return result

依赖管理:
明确列出所有依赖项，并提供安装命令。

# 依赖安装
pip install requests aiohttp beautifulsoup4

# 或者使用requirements.txt
cat > requirements.txt << EOF
requests>=2.25.0
aiohttp>=3.7.0
beautifulsoup4>=4.9.0