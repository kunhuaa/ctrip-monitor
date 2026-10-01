# 携程金钻会员匹配监控

监控携程万事达卡联名会员匹配名额，名额开放时发送飞书通知。

## 功能特点

- ⏰ 定时监控匹配页面状态
- 🔔 飞书机器人实时通知
- 📱 支持每月自动提醒
- 🎯 智能频率调整（月初加密监控）

## 活动说明

**携程 × 万事达卡联名会员匹配活动**

- 万事达世界之极卡持卡人可匹配携程金钻会员
- 每月名额有限（约125个/月）
- 每月1日0点重置名额
- 需在携程APP内手动完成匹配

## 环境要求

- Python 3.8+
- requests 库
- Docker（可选）

## 快速开始

### 1. 安装依赖

```bash
pip install requests
```

### 2. 配置

复制并修改配置文件：

```bash
cp config.example.json config.json
```

需要配置：
- `FEISHU_WEBHOOK` - 飞书机器人 Webhook
- `CHECK_INTERVAL` - 检查间隔（秒）

### 3. 运行监控

```bash
# 手动运行
python3 ctrip_monitor.py

# 后台运行
nohup python3 ctrip_monitor.py >> monitor.log 2>&1 &

# 或使用 systemd（推荐）
sudo cp ctrip-monitor.service /etc/systemd/system/
sudo systemctl enable ctrip-monitor
sudo systemctl start ctrip-monitor
```

### 4. 配置定时任务（可选）

每月1日0:05发送提醒：

```bash
# 编辑 crontab
crontab -e

# 添加以下行
5 0 1 * * /path/to/ctrip_reminder.sh
```

## 文件说明

```
ctrip-monitor/
├── ctrip_monitor.py       # 主监控脚本
├── ctrip_reminder.sh      # 每月提醒脚本
├── config.example.json    # 配置模板
├── README.md              # 说明文档
└── requirements.txt       # Python 依赖
```

## 使用流程

1. **提前准备**：确保携程APP已登录，万事达卡已绑定
2. **启动监控**：每月最后一天的23:55启动监控脚本
3. **收到通知**：名额开放时收到飞书通知
4. **立即操作**：打开携程APP → 搜索"万事达卡" → 点击匹配

## 注意事项

1. 本脚本仅提供监控和提醒功能，匹配操作需在APP内手动完成
2. 名额非常有限，建议提前打开APP等待
3. 请勿高频请求，避免触发风控
4. 脚本仅供学习参考，请遵守携程服务条款

## 许可证

MIT License
