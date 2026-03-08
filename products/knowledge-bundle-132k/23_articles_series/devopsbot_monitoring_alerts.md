《监控与告警：确保系统稳定运行》
目录

1. 监控体系设计
2. 关键指标定义
3. 告警规则配置
4. 自动化响应
5. 可视化仪表板

正文

监控体系设计

分层监控架构:

• 基础设施层: CPU、内存、磁盘、网络
• 应用层: 服务状态、响应时间、错误率
• 业务层: ROI、任务完成率、收益指标
• 安全层: 异常登录、权限变更、数据泄露

监控数据流:

数据采集 → 数据存储 → 数据处理 → 告警触发 → 通知发送 → 自动响应

监控工具栈:

• Prometheus: 指标收集和存储
• Grafana: 可视化仪表板
• Alertmanager: 告警管理和路由
• Node Exporter: 系统指标收集
• Blackbox Exporter: 黑盒监控（HTTP、TCP等）

关键指标定义

基础设施指标:

# CPU使用率
cpu_usage_percent{instance="v6-federal-intelligence"}

# 内存使用率  
memory_usage_percent{instance="v6-federal-intelligence"}

# 磁盘空间
disk_free_bytes{mountpoint="/", instance="v6-federal-intelligence"}

# 网络流量
network_bytes_total{interface="eth0", instance="v6-federal-intelligence"}

应用指标:

# 服务状态
up{job="v6-federal-intelligence"}

# HTTP请求延迟
http_request_duration_seconds{job="v6-federal-intelligence"}

# HTTP错误率
rate(http_requests_total{status=~"5..", job="v6-federal-intelligence"}[5m])

# 任务队列长度
task_queue_length{job="v6-federal-intelligence"}

业务指标:

# ROI指标
v6_agent_roi_average{job="v6-federal-intelligence"}

# 任务完成率
rate(v6_agent_tasks_completed_total[1h]) / rate(v6_agent_tasks_started_total[1h])

# 收益指标
v6_agent_revenue_usdc_total{job="v6-federal-intelligence"}

# 成本指标
v6_agent_cost_token_total{job="v6-federal-intelligence"}

安全指标:

# 异常登录尝试
failed_login_attempts_total{job="v6-federal-intelligence"}

# 权限变更
permission_changes_total{job="v6-federal-intelligence"}

# 敏感文件访问
sensitive_file_access_total{job="v6-federal-intelligence"}

告警规则配置

Prometheus告警规则:

# alert_rules.yml
groups:
- name: v6-federal-intelligence
  rules:
  # 基础设施告警
  - alert: HighCPUUsage
    expr: cpu_usage_percent > 80
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "High CPU usage on {{ $labels.instance }}"
      description: "CPU usage is above 80% for more than 5 minutes"

  - alert: LowDiskSpace
    expr: disk_free_bytes < 1073741824  # 1GB
    for: 1m
    labels:
      severity: critical
    annotations:
      summary: "Low disk space on {{ $labels.instance }}"
      description: "Available disk space is less than 1GB"

  # 应用告警
  - alert: ServiceDown
    expr: up{job="v6-federal-intelligence"} == 0
    for: 1m
    labels:
      severity: critical
    annotations:
      summary: "V6 Federal Intelligence service is down"
      description: "Service has been down for more than 1 minute"

  - alert: HighErrorRate
    expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
    for: 2m
    labels:
      severity: critical
    annotations:
      summary: "High error rate in V6 Federal Intelligence"
      description: "Error rate is above 10% for more than 2 minutes"

  # 业务告警
  - alert: LowROIThreshold
    expr: v6_agent_roi_average < 1.5
    for: 10m
    labels:
      severity: warning
    annotations:
      summary: "ROI below threshold"
      description: "Average ROI is below 1.5 for more than 10 minutes"

  - alert: NoRevenueGenerated
    expr: rate(v6_agent_revenue_usdc_total[1h]) == 0
    for: 24h
    labels:
      severity: critical
    annotations:
      summary: "No revenue generated in 24 hours"
      description: "V6 Federal Intelligence has not generated any revenue in the last 24 hours"

  # 安全告警
  - alert: FailedLoginAttempts
    expr: rate(failed_login_attempts_total[5m]) > 5
    for: 1m
    labels:
      severity: critical
    annotations:
      summary: "Multiple failed login attempts"
      description: "More than 5 failed login attempts in 5 minutes"

Alertmanager配置:

# alertmanager.yml
route:
  receiver: 'telegram-notifications'
  group_by: ['alertname']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 3h

receivers:
- name: 'telegram-notifications'
  webhook_configs:
  - url: 'http://localhost:8080/webhook/telegram'
    send_resolved: true

- name: 'email-notifications'
  email_configs:
  - to: 'admin@example.com'
    from: 'alerts@example.com'
    smarthost: 'smtp.example.com:587'
    auth_username: 'alerts@example.com'
    auth_password: 'your_password'

自动化响应

Webhook处理器:

# webhook_handler.py
from flask import Flask, request, jsonify
import requests
import subprocess

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = "your_telegram_bot_token"
TELEGRAM_CHAT_ID = "your_chat_id"

@app.route('/webhook/telegram', methods=['POST'])
def handle_telegram_webhook():
    """处理Telegram告警Webhook"""
    alert_data = request.json
    
    for alert in alert_data['alerts']:
        status = alert['status']
        labels = alert['labels']
        annotations = alert['annotations']
        
        # 构建告警消息
        message = f"🚨 **{labels['alertname']}**\n"
        message += f"**状态**: {status.upper()}\n"
        message += f"**严重性**: {labels.get('severity', 'unknown')}\n"
        message += f"**摘要**: {annotations.get('summary', 'N/A')}\n"
        
        if status == 'firing':
            message += f"\n**详情**: {annotations.get('description', 'N/A')}"
            # 执行自动化响应
            execute_auto_response(labels['alertname'])
        else:
            message += "\n✅ **告警已恢复**"
        
        # 发送到Telegram
        send_telegram_message(message)
    
    return jsonify({"status": "success"})

def send_telegram_message(message):
    """发送Telegram消息"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

def execute_auto_response(alert_name):
    """执行自动化响应"""
    if alert_name == "ServiceDown":
        # 尝试重启服务
        subprocess.run(["systemctl", "restart", "v6-federal-intelligence"])
    elif alert_name == "LowDiskSpace":
        # 清理临时文件
        subprocess.run(["find", "/tmp", "-name", "*.tmp", "-delete"])
    elif alert_name == "HighCPUUsage":
        # 限制进程CPU使用
        subprocess.run(["cpulimit", "-p", "$(pgrep v6-federal-intelligence)", "-l", "80"])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

自动化修复脚本:

#!/bin/bash
# auto_repair.sh

# 检查服务状态
if ! systemctl is-active --quiet v6-federal-intelligence; then
    echo "🔄 服务未运行，尝试重启..."
    systemctl restart v6-federal-intelligence
    
    # 等待服务启动
    sleep 10
    
    # 验证重启是否成功
    if systemctl is-active --quiet v6-federal-intelligence; then
        echo "✅ 服务重启成功"
        exit 0
    else
        echo "❌ 服务重启失败，需要人工干预"
        exit 1
    fi
fi

# 检查磁盘空间
disk_usage=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
if [ $disk_usage -gt 90 ]; then
    echo "🧹 磁盘使用率过高($disk_usage%)，清理临时文件..."
    find /tmp -name "*.tmp" -delete
    find /var/log -name "*.log" -mtime +7 -delete
    echo "✅ 临时文件清理完成"
fi

# 检查内存使用
memory_usage=$(free | awk 'NR==2{printf "%.0f", $3*100/$2}')
if [ $memory_usage -gt 85 ]; then
    echo "MemoryWarning 内存使用率过高($memory_usage%)，重启服务..."
    systemctl restart v6-federal-intelligence
    echo "✅ 服务重启完成"
fi

echo "✅ 系统健康检查完成"

可视化仪表板

Grafana仪表板配置:

{
  "dashboard": {
    "title": "V6 Federal Intelligence Dashboard",
    "panels": [
      {
        "title": "ROI Trend",
        "type": "graph",
        "targets": [
          {
            "expr": "v6_agent_roi_average",
            "legendFormat": "Average ROI"
          }
        ]
      },
      {
        "title": "Service Status",
        "type": "stat",
        "targets": [
          {
            "expr": "up{job=\"v6-federal-intelligence\"}",
            "legendFormat": "Status"
          }
        ]
      },
      {
        "title": "Revenue vs Cost",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(v6_agent_revenue_usdc_total[1h])",
            "legendFormat": "Revenue (USDC/hour)"
          },
          {
            "expr": "rate(v6_agent_cost_token_total[1h])",
            "legendFormat": "Cost (tokens/hour)"
          }
        ]
      }
    ]
  }
}

自定义健康检查端点:

# health_check.py
from flask import Flask, jsonify
import psutil
import requests

app = Flask(__name__)

@app.route('/health')
def health_check():
    """健康检查端点"""
    checks = {}
    
    # CPU使用率
    cpu_percent = psutil.cpu_percent(interval=1)
    checks['cpu'] = {
        'status': 'healthy' if cpu_percent < 80 else 'unhealthy',
        'value': f"{cpu_percent}%"
    }
    
    # 内存使用率
    memory = psutil.virtual_memory()
    memory_percent = memory.percent
    checks['memory'] = {
        'status': 'healthy' if memory_percent < 85 else 'unhealthy',
        'value': f"{memory_percent}%"
    }
    
    # 磁盘空间
    disk = psutil.disk_usage('/')
    disk_percent = (disk.used / disk.total) * 100
    checks['disk'] = {
        'status': 'healthy' if disk_percent < 90 else 'unhealthy',
        'value': f"{disk_percent:.1f}%"
    }
    
    # 服务依赖检查
    try:
        response = requests.get('https://api.coingecko.com/api/v3/ping', timeout=5)
        checks['external_api'] = {
            'status': 'healthy' if response.status_code == 200 else 'unhealthy',
            'value': f"HTTP {response.status_code}"
        }
    except Exception as e:
        checks['external_api'] = {
            'status': 'unhealthy',
            'value': str(e)
        }
    
    # 整体健康状态
    overall_status = 'healthy'
    for check_name, check_data in checks.items():
        if check_data['status'] == 'unhealthy':
            overall_status = 'unhealthy'
            break
    
    return jsonify({
        'status': overall_status,
        'checks': checks,
        'timestamp': time.time()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)

监控集成:

# docker-compose.yml
version: '3'
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - ./alert_rules.yml:/etc/prometheus/alert_rules.yml
  
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin123
  
  alertmanager:
    image: prom/alertmanager
    ports:
      - "9093:9093"
    volumes:
      - ./alertmanager.yml:/etc/alertmanager/alertmanager.yml
  
  v6-federal-intelligence:
    build: .
    ports:
      - "8080:8080"
      - "8081:8081"
    volumes:
      - ./data:/app/data

总结

监控与告警是确保V6.1联邦智能系统稳定运行的关键。通过分层监控架构、明确的关键指标、智能的告警规则、自动化的响应机制和直观的可视化仪表板，可以实现系统的全方位监控和快速故障恢复，确保业务连续性和收益稳定性。