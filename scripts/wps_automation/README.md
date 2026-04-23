# WPS 自动化资源整理（已支持青龙）

本目录已改造为：✅ **可直接被青龙面板拉库执行的脚本结构**

---

## 🚀 一键接入青龙

在青龙面板执行：

```
ql repo https://github.com/Cuigd/My_Script.git "wps_automation" "" "" "main"
```

说明：
- 只拉取包含 `wps_automation` 的脚本
- 青龙支持 Python / JS / Shell 等脚本运行 citeturn898466search4

---

## ⚙️ 环境变量配置

在青龙面板 → 环境变量 中新增：

```
WPS_USERNAME=账号1
账号2

WPS_PASSWORD=密码1
密码2

WPS_COOKIE=xxx

WPS_TOKEN=xxx

WPS_WEBHOOK=https://xxx
```

说明：
- 支持多账号（换行分隔）
- 脚本会自动一一对应处理

---

## 📜 可执行脚本

### 1️⃣ 青龙任务脚本

```
qinglong_wps_signin.py
```

特点：
- 自动读取环境变量
- 支持多账号
- 支持 webhook 推送
- 已封装日志输出

---

## 🧠 如何运行

青龙中创建任务：

```
python3 scripts/wps_automation/qinglong_wps_signin.py
```

然后设置定时，例如：

```
0 9 * * *
```

---

## 🔧 下一步（我可以继续帮你）

你现在只差一步👇

👉 把具体 WPS 自动化逻辑填进去

我可以帮你：

- ✅ 对接真实 WPS 签到接口
- ✅ 改造成 HTTP API 调用
- ✅ 接入通知（TG / 企业微信 / 钉钉）
- ✅ 做成“自动化任务平台”

只要你说一句：
👉 “我要做 WPS 自动签到” 或 “我要自动处理 Excel”

我可以把这个脚本直接补成**能跑业务的版本**。
