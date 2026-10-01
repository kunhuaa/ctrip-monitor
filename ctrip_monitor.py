#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
携程金钻会员匹配监控脚本
监控匹配页面名额状态，名额开放时发送飞书通知
"""

import time
import requests
import json
import random
from datetime import datetime, timedelta

# 配置
FEISHU_WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_HOOK_ID"
CHECK_INTERVAL = 60  # 检查间隔（秒）
NOTIFIED = False

# 携程匹配页面URL
MATCH_URL = "https://m.ctrip.com/webapp/ctrip/membership/match"

# User-Agent模拟
HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 CtripApp/10.x",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}


def send_feishu_notify(message):
    """发送飞书通知"""
    try:
        data = {
            "msg_type": "text",
            "content": {
                "text": message
            }
        }
        resp = requests.post(
            FEISHU_WEBHOOK,
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        if resp.status_code == 200:
            result = resp.json()
            print(f"✅ 飞书通知发送成功: {result.get('msg_code')}")
        else:
            print(f"❌ 飞书通知发送失败: HTTP {resp.status_code}")
    except Exception as e:
        print(f"❌ 飞书通知异常: {e}")


def check_quota():
    """检查名额状态"""
    global NOTIFIED
    
    now = datetime.now()
    
    # 如果是每月1日前几天，增加检查频率
    days_to_first = (now.replace(day=1) + timedelta(days=32) - now).days
    if days_to_first <= 3:
        print(f"📍 距离下月1日还有{days_to_first}天，增加监控频率")
    
    try:
        # 这里需要实际的API接口，暂时用占位
        # 实际使用时需要获取Cookie后调用匹配接口
        
        print(f"⏰ {now.strftime('%H:%M:%S')} 检查名额状态...")
        
        # TODO: 添加实际的API调用
        # response = requests.get(MATCH_URL, headers=HEADERS, timeout=10)
        
        # 模拟检查（实际使用需替换为真实API）
        is_open = False  # 默认未开放
        
        if is_open and not NOTIFIED:
            message = f"🎉 携程金钻会员匹配名额已开放！\n\n"
            message += f"时间：{now.strftime('%Y-%m-%d %H:%M:%S')}\n"
            message += f"请立即打开携程APP匹配：\n"
            message += f"路径：首页搜索'万事达卡' → 点击匹配"
            
            send_feishu_notify(message)
            NOTIFIED = True
            print("✅ 已发送飞书通知")
        
        return is_open
        
    except Exception as e:
        print(f"❌ 检查失败: {e}")
        return False


def main():
    """主函数"""
    print("=" * 50)
    print("🚀 携程金钻会员匹配监控启动")
    print("=" * 50)
    print(f"⏰ 检查间隔: {CHECK_INTERVAL}秒")
    print(f"📱 通知方式: 飞书机器人")
    print("=" * 50)
    
    while True:
        try:
            check_quota()
            
            # 随机延迟避免过于频繁
            delay = CHECK_INTERVAL + random.randint(-5, 5)
            print(f"💤 等待 {delay} 秒后再次检查...")
            time.sleep(max(30, delay))
            
        except KeyboardInterrupt:
            print("\n👋 监控已停止")
            break
        except Exception as e:
            print(f"❌ 监控异常: {e}")
            time.sleep(60)


if __name__ == "__main__":
    main()
