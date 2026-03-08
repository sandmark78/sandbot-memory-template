#!/bin/bash
# V6.1 脚本测试套件

# 测试所有脚本工具
# 使用：bash test-suite.sh

WORKSPACE="/home/node/.openclaw/workspace"
SCRIPTS_DIR="$WORKSPACE/scripts"
PASSED=0
FAILED=0

echo "=== V6.1 脚本测试套件 ==="
echo "时间：$(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 测试 self_growth.py
echo "测试：self_growth.py"
if python3 "$SCRIPTS_DIR/self_growth.py" --help > /dev/null 2>&1; then
    echo "  ✅ self_growth.py 通过"
    ((PASSED++))
else
    echo "  ❌ self_growth.py 失败"
    ((FAILED++))
fi

# 测试 agent_collab.py
echo "测试：agent_collab.py"
if python3 "$SCRIPTS_DIR/agent_collab.py" --help > /dev/null 2>&1; then
    echo "  ✅ agent_collab.py 通过"
    ((PASSED++))
else
    echo "  ❌ agent_collab.py 失败"
    ((FAILED++))
fi

# 测试 memory_manager.py
echo "测试：memory_manager.py"
if python3 "$SCRIPTS_DIR/memory_manager.py" --help > /dev/null 2>&1; then
    echo "  ✅ memory_manager.py 通过"
    ((PASSED++))
else
    echo "  ❌ memory_manager.py 失败"
    ((FAILED++))
fi

# 测试 intent_capture.py
echo "测试：intent_capture.py"
if python3 "$SCRIPTS_DIR/intent_capture.py" --help > /dev/null 2>&1; then
    echo "  ✅ intent_capture.py 通过"
    ((PASSED++))
else
    echo "  ❌ intent_capture.py 失败"
    ((FAILED++))
fi

# 测试 model_router.py
echo "测试：model_router.py"
if python3 "$SCRIPTS_DIR/model_router.py" --help > /dev/null 2>&1; then
    echo "  ✅ model_router.py 通过"
    ((PASSED++))
else
    echo "  ❌ model_router.py 失败"
    ((FAILED++))
fi

# 测试 heartbeat.sh
echo "测试：heartbeat.sh"
if bash "$SCRIPTS_DIR/heartbeat.sh" > /dev/null 2>&1; then
    echo "  ✅ heartbeat.sh 通过"
    ((PASSED++))
else
    echo "  ❌ heartbeat.sh 失败"
    ((FAILED++))
fi

# 测试 growth_lifecycle.sh
echo "测试：growth_lifecycle.sh"
if bash "$SCRIPTS_DIR/growth_lifecycle.sh" --help > /dev/null 2>&1; then
    echo "  ✅ growth_lifecycle.sh 通过"
    ((PASSED++))
else
    echo "  ❌ growth_lifecycle.sh 失败"
    ((FAILED++))
fi

# 技能脚本测试
echo ""
echo "=== 技能脚本测试 ==="

# 测试 memory-enhancer/compress.py
echo "测试：memory-enhancer/compress.py"
if python3 "$WORKSPACE/skills/memory-enhancer/scripts/compress.py" > /dev/null 2>&1; then
    echo "  ✅ memory-enhancer/compress.py 通过"
    ((PASSED++))
else
    echo "  ❌ memory-enhancer/compress.py 失败"
    ((FAILED++))
fi

# 测试 growth-tracker/assess.py
echo "测试：growth-tracker/assess.py"
if python3 "$WORKSPACE/skills/growth-tracker/scripts/assess.py" > /dev/null 2>&1; then
    echo "  ✅ growth-tracker/assess.py 通过"
    ((PASSED++))
else
    echo "  ❌ growth-tracker/assess.py 失败"
    ((FAILED++))
fi

# 测试 intent-predictor/detect.py
echo "测试：intent-predictor/detect.py"
if python3 "$WORKSPACE/skills/intent-predictor/scripts/detect.py" --help > /dev/null 2>&1; then
    echo "  ✅ intent-predictor/detect.py 通过"
    ((PASSED++))
else
    echo "  ❌ intent-predictor/detect.py 失败"
    ((FAILED++))
fi

# 总结
echo ""
echo "=== 测试总结 ==="
echo "通过：$PASSED"
echo "失败：$FAILED"
echo "总计：$((PASSED + FAILED))"
if [ $((PASSED + FAILED)) -gt 0 ]; then
    RATE=$((PASSED * 100 / (PASSED + FAILED)))
    echo "通过率：${RATE}%"
else
    echo "通过率：N/A"
fi

if [ $FAILED -eq 0 ]; then
    echo ""
    echo "🎉 所有测试通过！"
    exit 0
else
    echo ""
    echo "⚠️ 有 $FAILED 个测试失败"
    exit 1
fi
