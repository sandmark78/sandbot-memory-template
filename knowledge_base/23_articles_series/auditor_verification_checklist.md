《验证清单：确保真实产出的检查表》

目录

1. 验证清单概述
2. 文件存在性验证
3. 内容完整性验证
4. 功能性验证
5. 价值性验证
6. 自动化验证脚本

正文

验证清单概述

验证清单是确保V6.1联邦智能每个任务都有真实产出的核心工具。通过系统化的验证步骤，可以有效防止幻觉循环和模拟执行。

验证原则:

• 即时验证: 任务完成后立即验证，不依赖记忆
• 客观标准: 验证标准必须客观可衡量，不依赖主观判断
• 自动化执行: 验证过程尽可能自动化，减少人为错误
• 全面覆盖: 验证必须覆盖存在性、完整性、功能性和价值性

文件存在性验证

基本检查:

• 文件是否真实存在于指定路径
• 文件权限是否正确（可读/可写/可执行）
• 文件大小是否合理（非空文件）

验证命令:

# 检查文件是否存在
if [ -f "/path/to/file.txt" ]; then
    echo "✅ 文件存在"
else
    echo "❌ 文件不存在"
fi

# 检查文件权限
if [ -r "/path/to/file.txt" ]; then
    echo "✅ 文件可读"
fi
if [ -w "/path/to/file.txt" ]; then
    echo "✅ 文件可写"
fi
if [ -x "/path/to/script.sh" ]; then
    echo "✅ 文件可执行"
fi

# 检查文件大小
file_size=$(stat -c%s "/path/to/file.txt")
if [ $file_size -gt 0 ]; then
    echo "✅ 文件非空 ($file_size bytes)"
else
    echo "❌ 文件为空"
fi

内容完整性验证

文本内容验证:

• 关键词是否存在于文件中
• 内容格式是否符合预期
• 数据结构是否完整

验证命令:

# 检查关键词存在
if grep -q "关键内容" "/path/to/file.txt"; then
    echo "✅ 关键内容存在"
else
    echo "❌ 关键内容缺失"
fi

# 检查JSON格式
if python3 -m json.tool "/path/to/data.json" > /dev/null 2>&1; then
    echo "✅ JSON格式正确"
else
    echo "❌ JSON格式错误"
fi

# 检查CSV格式
if head -n1 "/path/to/data.csv" | grep -q ","; then
    echo "✅ CSV格式正确"
else
    echo "❌ CSV格式错误"
fi

功能性验证

可执行文件验证:

• 脚本是否能正常执行
• 程序是否能正常运行
• 输出是否符合预期

验证命令:

# 验证Shell脚本
if bash -n "/path/to/script.sh" > /dev/null 2>&1; then
    echo "✅ Shell脚本语法正确"
    if timeout 10s bash "/path/to/script.sh" > /dev/null 2>&1; then
    echo "✅ Shell脚本执行成功"
    else
        echo "❌ Shell脚本执行失败"
    fi
else
    echo "❌ Shell脚本语法错误"
fi

# 验证Python脚本
if python3 -m py_compile "/path/to/script.py" > /dev/null 2>&1; then
    echo "✅ Python脚本语法正确"
    if timeout 10s python3 "/path/to/script.py" > /dev/null 2>&1; then
        echo "✅ Python脚本执行成功"
    else
        echo "❌ Python脚本执行失败"
    fi
else
    echo "❌ Python脚本语法错误"
fi

价值性验证

ROI验证:

• 任务是否产生实际价值
• ROI是否大于1.5
• 是否值得投入资源

验证标准:

• 直接价值: 能否产生USDC收入、用户增长等可量化收益
• 间接价值: 能否提升系统能力、积累技能、改善用户体验
• 长期价值: 能否形成可复用的资产、建立竞争优势

验证方法:

def validate_value(task_result, expected_roi=1.5):
    """验证任务价值"""
    # 计算实际ROI
    actual_roi = calculate_actual_roi(task_result)
    
    # 验证ROI阈值
    if actual_roi >= expected_roi:
        return True, f"ROI达标: {actual_roi:.1f} >= {expected_roi}"
    else:
        return False, f"ROI不足: {actual_roi:.1f} < {expected_roi}"

def calculate_actual_roi(task_result):
    """计算实际ROI"""
    # 基于实际收益和成本计算ROI
    actual_revenue = get_actual_revenue(task_result)
    actual_cost = get_actual_cost(task_result)
    if actual_cost == 0:
        return float('inf')
    return (actual_revenue - actual_cost) / actual_cost

自动化验证脚本

完整验证脚本:

#!/usr/bin/env python3
import os
import json
import subprocess
import sys

class VerificationChecklist:
    def __init__(self, file_path):
        self.file_path = file_path
        self.results = []
    
    def verify_existence(self):
        """验证文件存在性"""
        if os.path.exists(self.file_path):
            self.results.append(("存在性", "通过", f"文件存在: {self.file_path}"))
            return True
        else:
            self.results.append(("存在性", "失败", f"文件不存在: {self.file_path}"))
            return False
    
    def verify_content(self, expected_keywords=None):
        """验证内容完整性"""
        try:
            with open(self.file_path, 'r') as f:
                content = f.read()
            
            if len(content.strip()) == 0:
                self.results.append(("内容完整性", "失败", "文件为空"))
                return False
            
            if expected_keywords:
                for keyword in expected_keywords:
                    if keyword not in content:
                        self.results.append(("内容完整性", "失败", f"缺少关键词: {keyword}"))
                        return False
            
            self.results.append(("内容完整性", "通过", "内容完整"))
            return True
        except Exception as e:
            self.results.append(("内容完整性", "失败", f"读取错误: {e}"))
            return False
    
    def verify_functionality(self, executable=False):
        """验证功能性"""
        if not executable:
            self.results.append(("功能性", "跳过", "非可执行文件"))
            return True
        
        try:
            # 检查文件扩展名
            if self.file_path.endswith('.py'):
                result = subprocess.run([sys.executable, self.file_path], 
                                      capture_output=True, timeout=10)
            elif self.file_path.endswith(('.sh', '.bash')):
                result = subprocess.run(['bash', self.file_path], 
                                      capture_output=True, timeout=10)
            else:
                self.results.append(("功能性", "跳过", "未知文件类型"))
                return True
            
            if result.returncode == 0:
                self.results.append(("功能性", "通过", "执行成功"))
                return True
            else:
                self.results.append(("功能性", "失败", f"执行失败: {result.stderr.decode()}"))
                return False
        except subprocess.TimeoutExpired:
            self.results.append(("功能性", "失败", "执行超时"))
            return False
        except Exception as e:
            self.results.append(("功能性", "失败", f"执行异常: {e}"))
            return False
    
    def verify_value(self, min_size=10):
        """验证价值性"""
        file_size = os.path.getsize(self.file_path)
        if file_size >= min_size:
            self.results.append(("价值性", "通过", f"文件大小合理: {file_size} bytes"))
            return True
        else:
        self.results.append(("价值性", "失败", f"文件太小: {file_size} bytes < {min_size}"))
            return False
    
    def run_all_checks(self, expected_keywords=None, executable=False, min_size=10):
        """运行所有验证检查"""
        all_passed = True
        
        all_passed &= self.verify_existence()
        all_passed &= self.verify_content(expected_keywords)
        all_passed &= self.verify_functionality(executable)
        all_passed &= self.verify_value(min_size)
        
        return all_passed, self.results

# 使用示例
if __name__ == "__main__":
    file_path = sys.argv[1]
    expected_keywords = sys.argv[2].split(',') if len(sys.argv) > 2 else None
    executable = '--executable' in sys.argv
    
    verifier = VerificationChecklist(file_path)
    success, results = verifier.run_all_checks(expected_keywords, executable)
    
    print("验证结果:")
    for check_name, status, message in results:
        status_icon = "✅" if status == "通过" else "❌"
        print(f"{status_icon} {check_name}: {message}")
    
    if success:
        print("\n🎉 所有验证通过！")
        sys.exit(0)
    else:
        print("\n💥 验证失败！")
        sys.exit(1)

使用方法:

# 验证普通文件
python3 verify.py /path/to/file.txt "关键词1,关键词2"

# 验证可执行脚本
python3 verify.py /path/to/script.py "main,function" --executable

总结

验证清单是确保V6.1联邦智能真实产出的核心保障。通过系统化的存在性、完整性、功能性和价值性验证，可以有效防止幻觉循环，确保每个任务都有可验证的实际价值。