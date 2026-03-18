#!/bin/bash
# ClawPI 红包巡逻脚本
# 自动扫描并领取可用红包

export PATH=$PATH:/home/node/.npm-global/bin
CONFIG="$HOME/.fluxa-ai-wallet-mcp/config.json"
LOG="/home/node/.openclaw/workspace/memory/clawpi-patrol.log"

# 刷新 JWT
fluxa-wallet refreshJWT >/dev/null 2>&1
JWT=$(cat "$CONFIG" | python3 -c "import sys,json; print(json.load(sys.stdin)['agentId']['jwt'])")

if [ -z "$JWT" ]; then
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) ERROR: JWT empty" >> "$LOG"
  exit 1
fi

AGENT_ID="eed2a40d-a869-4ec2-8abf-cfcc76312bef"
BASE="https://clawpi.fluxapay.xyz"
CLAIMED=0
TOTAL_USDC=0

# 获取所有可用红包
AVAILABLE=$(curl -s "$BASE/api/redpacket/available?n=50&offset=0" -H "Authorization: Bearer $JWT")
CLAIMABLE=$(echo "$AVAILABLE" | python3 -c "
import sys, json
data = json.load(sys.stdin)
if data.get('success'):
    for rp in data.get('redPackets', []):
        if rp.get('can_claim') and not rp.get('already_claimed'):
            print(f\"{rp['id']}|{rp['per_amount']}|{rp.get('creator_nickname','?')}\")
" 2>/dev/null)

if [ -z "$CLAIMABLE" ]; then
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) SCAN: 无可领红包" >> "$LOG"
  echo "NO_REDPACKETS"
  exit 0
fi

RESULTS=""

while IFS='|' read -r RP_ID AMOUNT CREATOR; do
  # 创建收款链接
  PL_JSON=$(fluxa-wallet paymentlink-create --amount "$AMOUNT" 2>/dev/null)
  PL_URL=$(echo "$PL_JSON" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['data']['paymentLink']['url'])" 2>/dev/null)

  if [ -z "$PL_URL" ]; then
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) ERROR: paymentlink failed for RP#$RP_ID" >> "$LOG"
    continue
  fi

  # 领取
  CLAIM=$(curl -s -X POST "$BASE/api/redpacket/claim" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $JWT" \
    -d "{\"redPacketId\": $RP_ID, \"paymentLink\": \"$PL_URL\"}")

  SUCCESS=$(echo "$CLAIM" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('success',False))" 2>/dev/null)
  PAID=$(echo "$CLAIM" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('claim',{}).get('paid',False))" 2>/dev/null)

  if [ "$SUCCESS" = "True" ]; then
    USDC=$(python3 -c "print(int('$AMOUNT')/1000000)")
    CLAIMED=$((CLAIMED + 1))
    TOTAL_USDC=$(python3 -c "print($TOTAL_USDC + $USDC)")
    RESULTS="${RESULTS}${CREATOR}:${USDC}U "
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) CLAIMED: RP#$RP_ID ${USDC}U from $CREATOR paid=$PAID" >> "$LOG"
  else
    REASON=$(echo "$CLAIM" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('error',{}).get('code','unknown'))" 2>/dev/null)
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) FAILED: RP#$RP_ID reason=$REASON" >> "$LOG"
  fi

  sleep 2
done <<< "$CLAIMABLE"

# 发现新推荐用户并关注
SUGGESTED=$(curl -s "$BASE/api/discover/suggested?n=10&offset=0" -H "Authorization: Bearer $JWT")
NEW_FOLLOWS=0
echo "$SUGGESTED" | python3 -c "
import sys, json
data = json.load(sys.stdin)
if data.get('success'):
    for u in data.get('suggested', []):
        print(u['agent_id'])
" 2>/dev/null | while read -r TID; do
  curl -s -X POST "$BASE/api/follow" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $JWT" \
    -d "{\"targetAgentId\": \"$TID\", \"action\": \"follow\"}" >/dev/null 2>&1
  sleep 1
done

if [ "$CLAIMED" -gt 0 ]; then
  echo "CLAIMED:${CLAIMED}|USDC:${TOTAL_USDC}|${RESULTS}"
else
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) SCAN: 扫描完成，0 个可领" >> "$LOG"
  echo "NO_CLAIMABLE"
fi
