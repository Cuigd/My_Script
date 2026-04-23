# WPS 自动化（青龙版）

本目录已支持：✅ **WPS 自动签到（青龙运行）**

---

## 🔑 核心原理

WPS 官方没有稳定公开签到 API，常见做法是：

👉 在浏览器中执行一次签到 → 抓取请求 → 青龙重放

开源项目也是通过这种方式实现的 citeturn299135search0

---

## 🧠 一次性配置（非常关键）

### ① 打开签到页面

- 手机 WPS App 或 WPS 社区
- 执行一次签到

👉 官方说明：WPS 支持在 App / 社区进行签到领取空间 citeturn512241search5

---

### ② 抓取请求

1. 打开浏览器 → 登录 WPS
2. 按 F12 → Network
3. 点击签到按钮
4. 找到类似 `check` / `sign` 的请求
5. 右键 → Copy as cURL

👉 推荐方式（通用方案） citeturn512241search6

---

## ⚙️ 青龙环境变量

### 单账号

```
WPS_ACCOUNT_NAME=主号
WPS_CHECKIN_CURL=curl 'https://xxx' -H 'cookie: xxx' ...
```

---

### 多账号

```
WPS_ACCOUNT_NAME=号1
号2

WPS_CHECKIN_CURL=curl ...
curl ...
```

或（推荐）：

```
WPS_CHECKIN_CURL_B64=base64后的curl
```

---

## ▶️ 运行

```
python3 scripts/wps_automation/qinglong_wps_signin.py
```

---

## 📊 脚本能力

- ✅ 自动解析 curl
- ✅ 支持多账号
- ✅ 自动判断成功/重复签到
- ✅ 支持 webhook 推送
- ✅ 支持 dry_run 调试

---

## ⚠️ 注意

1. Cookie 过期需要重新抓
2. WPS 接口会变化（本方案天然兼容）
3. 不建议写死接口

---

## 🚀 下一步升级

我可以帮你继续做：

- 自动抽奖
- 自动领云空间
- 自动刷新 cookie
- 多平台签到系统

👉 直接说：

> 做一个「WPS 全自动签到 + 抽奖系统」

我可以帮你升级成完整自动化项目
