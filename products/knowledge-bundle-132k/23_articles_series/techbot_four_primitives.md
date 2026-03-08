# 四原语开发模式 (read/edit/write/exec)

## 目录
1. **四原语核心概念**
2. **read原语详解**
3. **edit原语详解**
4. **write原语详解**
5. **exec原语详解**
6. **实战组合应用**

## 正文

### 四原语核心概念
V6.1联邦智能的开发基础建立在四个原子操作原语之上：
- **read**: 读取文件内容或系统信息
- **edit**: 精确替换文件中的特定文本
- **write**: 创建或覆盖文件内容
- **exec**: 执行shell命令或系统操作

这四个原语构成了所有复杂操作的基础，通过组合这些原语可以实现任意功能。

### read原语详解
**功能**: 安全读取文件内容，支持大文件分页读取

**使用场景**:
- 读取配置文件
- 分析日志文件
- 提取数据文件内容
- 验证文件存在性

**最佳实践**:
```python
# 读取文件内容
content = read("/path/to/file.txt")

# 读取大文件（分页）
content = read("/path/to/large_file.log", offset=1000, limit=500)

edit原语详解

功能: 精确替换文件中的指定文本，确保原子性操作

使用场景:

• 修改配置文件参数
• 更新代码中的特定变量
• 修复文件中的错误内容
• 批量替换文本

最佳实践:

# 精确文本替换
edit("/path/to/config.json",
oldText='"debug": false',
newText='"debug": true')

write原语详解

功能: 创建新文件或完全覆盖现有文件

使用场景:

• 生成新的配置文件
• 创建数据输出文件
• 写入日志记录
• 保存处理结果

最佳实践:

# 创建新文件
write("/path/to/new_file.txt", "这是新文件内容")

# 覆盖现有文件
write("/path/to/existing.log", "清空并重写日志")

exec原语详解

功能: 执行系统命令，支持后台执行和结果捕获

使用场景:

• 运行系统工具（curl, git, docker等）
• 执行脚本文件
• 启动后台服务
• 获取系统信息

最佳实践:

# 执行简单命令
result = exec("ls -la /home")

# 后台执行长时间任务
exec("python3 long_running_script.py", background=True)

# 执行带参数的命令
exec("curl -s https://api.example.com/data", timeout=30)

实战组合应用

案例1: 自动化配置更新

# 1. 读取当前配置
config = read("/app/config.json")

# 2. 检查是否需要更新
if "new_feature" not in config:
# 3. 编辑配置文件
edit("/app/config.json",
oldText='"features": []',
newText='"features": ["new_feature"]')

# 4. 重启服务
exec("systemctl restart app")

案例2: 数据抓取和处理

# 1. 执行数据抓取命令
exec("curl -s https://api.data.com/latest > raw_data.json")

# 2. 读取原始数据
raw_data = read("raw_data.json")

# 3. 处理数据并写入新文件
processed_data = process_data(raw_data)
write("processed_data.json", processed_data)

# 4. 验证处理结果
result = exec("python3 validate.py processed_data.json")
if result.exit_code == 0:
print("✅ 数据处理成功")

总结

四原语开发模式提供了构建可靠自动化系统的基础。通过组合read、edit、write、exec四个原子操作，可以实现任意复杂的自动化任务，同时确保操作的精确性和可验证性。