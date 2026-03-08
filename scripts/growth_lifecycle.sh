#!/bin/bash
# V6.1 成长系统生命周期管理脚本 (修复版)

WORKSPACE="/home/node/.openclaw/workspace"
PID_FILE="$WORKSPACE/growth/self_growth.pid"
LOG_FILE="$WORKSPACE/growth/lifecycle.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

start() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p $PID > /dev/null 2>&1; then
            log "⚠️ 成长系统已在运行 (PID: $PID)"
            return 1
        fi
    fi
    
    log "🚀 启动成长系统..."
    python3 "$WORKSPACE/scripts/self_growth.py" full >> "$LOG_FILE" 2>&1 &
    echo $! > "$PID_FILE"
    log "✅ 成长系统已启动 (PID: $(cat $PID_FILE))"
}

stop() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p $PID > /dev/null 2>&1; then
            log "🛑 停止成长系统 (PID: $PID)..."
            kill $PID
            rm -f "$PID_FILE"
            log "✅ 成长系统已停止"
            return 0
        fi
    fi
    log "⚠️ 成长系统未运行"
    return 1
}

status() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p $PID > /dev/null 2>&1; then
            echo "✅ 成长系统运行中 (PID: $PID)"
            ps -p $PID -o pid,etime,cmd
            return 0
        fi
    fi
    echo "❌ 成长系统未运行"
    return 1
}

check() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ! ps -p $PID > /dev/null 2>&1; then
            log "⚠️ 成长系统进程丢失，自动重启..."
            rm -f "$PID_FILE"
            start
            return 0
        fi
    else
        log "⚠️ PID 文件丢失，启动成长系统..."
        start
        return 0
    fi
    log "✅ 成长系统健康"
}

restart() {
    stop
    sleep 2
    start
}

case "$1" in
    start) start ;;
    stop) stop ;;
    restart) restart ;;
    status) status ;;
    check) check ;;
    *)
        echo "用法：$0 {start|stop|restart|status|check}"
        exit 1
        ;;
esac
