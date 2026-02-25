#!/bin/bash
# Vercel 部署脚本 - 使用 HTTP API，无需 CLI

set -e

VERCEL_TOKEN=$(cat /home/node/.openclaw/secrets/vercel_token.txt)
PROJECT_NAME="v61-docs"
TEAM_ID="team_sandmark"  # 从 Vercel dashboard 获取

# 部署目录
DEPLOY_DIR="/home/node/.openclaw/workspace/docs"

echo "🔺 Vercel 部署启动..."
echo "   项目：${PROJECT_NAME}"
echo "   目录：${DEPLOY_DIR}"

# 1. 创建部署
echo "1. 创建部署..."
DEPLOY_RESPONSE=$(curl -s -X POST \
  "https://api.vercel.com/v13/deployments" \
  -H "Authorization: Bearer ${VERCEL_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"${PROJECT_NAME}\",
    \"project\": \"${PROJECT_NAME}\",
    \"target\": \"production\"
  }")

DEPLOY_ID=$(echo $DEPLOY_RESPONSE | jq -r '.id')
echo "   部署 ID: ${DEPLOY_ID}"

# 2. 上传文件
echo "2. 上传文件..."
cd ${DEPLOY_DIR}
for file in *; do
  if [ -f "$file" ]; then
    FILE_CONTENT=$(base64 -w0 "$file")
    curl -s -X POST \
      "https://api.vercel.com/v2/deployments/${DEPLOY_ID}/files" \
      -H "Authorization: Bearer ${VERCEL_TOKEN}" \
      -H "Content-Type: application/json" \
      -d "{
        \"file\": \"${file}\",
        \"data\": \"${FILE_CONTENT}\"
      }" > /dev/null
    echo "   ✅ 上传：${file}"
  fi
done

# 3. 完成部署
echo "3. 完成部署..."
curl -s -X POST \
  "https://api.vercel.com/v13/deployments/${DEPLOY_ID}" \
  -H "Authorization: Bearer ${VERCEL_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{\"target\": \"production\"}" > /dev/null

# 4. 获取部署 URL
echo "4. 获取部署 URL..."
DEPLOY_URL=$(curl -s \
  "https://api.vercel.com/v13/deployments/${DEPLOY_ID}" \
  -H "Authorization: Bearer ${VERCEL_TOKEN}" | jq -r '.url')

echo ""
echo "✅ 部署完成！"
echo "   URL: https://${DEPLOY_URL}"
echo ""
