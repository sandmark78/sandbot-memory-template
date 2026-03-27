#!/bin/bash
# daily-backup.sh - 每日自动备份到 GitHub

WORKSPACE="${OPENCLAW_WORKSPACE:-/home/node/.openclaw/workspace}"
MESSAGE="${1:-$(date +%Y-%m-%d): 每日备份}"

cd "$WORKSPACE" || exit 1

# 检查 Git 状态
if ! git status --porcelain | grep -q .; then
  echo "✅ 无变更，跳过备份"
  exit 0
fi

# 提交并推送
git add .
git commit -m "$MESSAGE"
git push

echo "✅ 备份成功：$MESSAGE"
