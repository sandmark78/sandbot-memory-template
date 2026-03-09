#!/bin/bash
# Script Optimizer V6.3 - 脚本质量审计与优化
# 用途：检查脚本质量，添加错误处理，标准化日志
# 负责 Agent: AutoBot 🤖 + Auditor 🔍
# 版本：V6.3.0
# 创建：2026-03-09

set -euo pipefail

# 配置
WORKSPACE="/home/node/.openclaw/workspace"
SCRIPTS_DIR="$WORKSPACE/scripts"
REPORT_FILE="$WORKSPACE/reports/$(date +%Y-%m-%d)-script-audit.md"
LOG_FILE="$WORKSPACE/logs/script-optimizer.log"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 创建日志目录
mkdir -p "$(dirname "$LOG_FILE")"
mkdir -p "$(dirname "$REPORT_FILE")"

log "🔍 开始脚本质量审计..."

# 审计检查清单
check_shebang() {
    local file=$1
    if head -1 "$file" | grep -qE '^#!(/bin/bash|/usr/bin/env bash|/usr/bin/python3|/usr/bin/env python3)'; then
        return 0
    else
        return 1
    fi
}

check_error_handling() {
    local file=$1
    if grep -qE '(set -e|set -euo pipefail|try:|except|set -o pipefail)' "$file"; then
        return 0
    else
        return 1
    fi
}

check_logging() {
    local file=$1
    if grep -qE '(log\(|logger\.|echo.*\[|print.*\[)' "$file"; then
        return 0
    else
        return 1
    fi
}

check_config_vars() {
    local file=$1
    if grep -qE '^(WORKSPACE|DATA_DIR|CONFIG_|API_)' "$file"; then
        return 0
    else
        return 1
    fi
}

check_executable() {
    local file=$1
    if [[ -x "$file" ]]; then
        return 0
    else
        return 1
    fi
}

# 生成审计报告
echo "# 脚本质量审计报告" > "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "**生成时间**: $(date '+%Y-%m-%d %H:%M:%S UTC')" >> "$REPORT_FILE"
echo "**审计范围**: $SCRIPTS_DIR" >> "$REPORT_FILE"
echo "**审计者**: AutoBot 🤖 + Auditor 🔍" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

echo "## 📊 总体统计" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

total_scripts=0
passed_all=0
needs_optimization=0

echo "| 脚本 | Shebang | 错误处理 | 日志 | 配置 | 可执行 | 状态 |" >> "$REPORT_FILE"
echo "|------|---------|----------|------|------|--------|------|" >> "$REPORT_FILE"

for script in "$SCRIPTS_DIR"/*.sh "$SCRIPTS_DIR"/*.py; do
    [[ -f "$script" ]] || continue
    
    total_scripts=$((total_scripts + 1))
    basename=$(basename "$script")
    
    # 检查各项
    shebang_ok=$(check_shebang "$script" && echo "✅" || echo "❌")
    error_ok=$(check_error_handling "$script" && echo "✅" || echo "❌")
    log_ok=$(check_logging "$script" && echo "✅" || echo "❌")
    config_ok=$(check_config_vars "$script" && echo "✅" || echo "❌")
    exec_ok=$(check_executable "$script" && echo "✅" || echo "❌")
    
    # 判断状态
    if [[ "$shebang_ok" == "✅" && "$error_ok" == "✅" && "$log_ok" == "✅" ]]; then
        status="✅ 优秀"
        passed_all=$((passed_all + 1))
    elif [[ "$shebang_ok" == "✅" && "$error_ok" == "✅" ]]; then
        status="⚠️ 需改进"
        needs_optimization=$((needs_optimization + 1))
    else
        status="❌ 需优化"
        needs_optimization=$((needs_optimization + 1))
    fi
    
    echo "| $basename | $shebang_ok | $error_ok | $log_ok | $config_ok | $exec_ok | $status |" >> "$REPORT_FILE"
done

echo "" >> "$REPORT_FILE"
echo "## 📈 统计摘要" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "- 总脚本数：$total_scripts" >> "$REPORT_FILE"
passed_pct=$((passed_all * 100 / total_scripts))
needs_pct=$((needs_optimization * 100 / total_scripts))
echo "- 优秀：$passed_all ($passed_pct%)" >> "$REPORT_FILE"
echo "- 需优化：$needs_optimization ($needs_pct%)" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

echo "## 🛠️ 优化建议" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

if [[ $needs_optimization -gt 0 ]]; then
    echo "### 优先级 P0 (立即优化)" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    echo "1. 添加错误处理 (set -euo pipefail / try-except)" >> "$REPORT_FILE"
    echo "2. 标准化日志输出" >> "$REPORT_FILE"
    echo "3. 配置变量集中管理" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    
    echo "### 优先级 P1 (本周优化)" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    echo "1. 添加使用文档 (Usage 注释)" >> "$REPORT_FILE"
    echo "2. 添加参数验证" >> "$REPORT_FILE"
    echo "3. 添加单元测试" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
else
    echo "✅ 所有脚本质量良好，无需优化" >> "$REPORT_FILE"
fi

echo "## 📝 下一步行动" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "1. 审查本报告标记为 ❌ 的脚本" >> "$REPORT_FILE"
echo "2. 按优先级逐步优化" >> "$REPORT_FILE"
echo "3. 建立脚本开发规范文档" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "---" >> "$REPORT_FILE"
echo "*报告生成：AutoBot 🤖 + Auditor 🔍*" >> "$REPORT_FILE"
echo "*验证：cat $REPORT_FILE*" >> "$REPORT_FILE"

log "✅ 审计报告生成：$REPORT_FILE"
log "📊 总计：$total_scripts 脚本，$passed_all 优秀，$needs_optimization 需优化"

# 输出摘要
echo ""
echo "================================"
echo "脚本质量审计完成"
echo "================================"
echo "总脚本数：$total_scripts"
echo -e "优秀：${GREEN}$passed_all${NC}"
echo -e "需优化：${YELLOW}$needs_optimization${NC}"
echo "报告：$REPORT_FILE"
echo "================================"
