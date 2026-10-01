#!/bin/bash
# 携程金钻匹配提醒脚本
# 每月1日0:00发送飞书通知提醒用户去匹配

LOG_FILE="/root/logs/ctrip_reminder.log"
FEISHU_WEBHOOK="https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_HOOK_ID"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

send_feishu() {
    local message="$1"
    # 使用临时文件避免JSON转义问题
    local tmpfile=$(mktemp)
    printf '{"msg_type":"text","content":{"text":"%s"}}' "$message" > "$tmpfile"
    
    curl -s -X POST "$FEISHU_WEBHOOK" \
        -H "Content-Type: application/json" \
        -d @"$tmpfile" 2>&1
    
    rm -f "$tmpfile"
}

main() {
    log "=== 携程金钻匹配提醒 ==="
    
    # 发送提醒消息
    local message="⏰ 携程金钻会员匹配提醒

今天是每月1日，名额已重置！

📱 操作步骤：
1. 打开携程APP
2. 搜索「万事达卡」
3. 点击「立即匹配」
4. 完成匹配

⚠️ 名额有限，请尽快操作！
每月限额125个（世界之极卡个人卡）"
    
    send_feishu "$message"
    log "✅ 提醒已发送"
}

main
