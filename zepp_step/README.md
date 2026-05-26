# Zepp Life 步数脚本

## 同步维护规则

以后每次同步或修改本目录脚本时，需要同时更新本 README，记录本次修改内容、配置变化和使用说明，避免脚本逻辑与说明不一致。

---

## 当前版本说明

本版本支持通过环境变量或配置文件管理 Zepp Life 账号，适合 GitHub Actions、青龙面板、本地 Python 环境等场景使用。

账号读取优先级：

1. `ZEPP_ACCOUNTS` 环境变量
2. `xxxxx_sbs` 旧版环境变量
3. `zepp_config.json` 配置文件

---

## 环境变量配置方式

推荐使用 `ZEPP_ACCOUNTS`。

变量名：

```bash
ZEPP_ACCOUNTS
```

变量值格式：

```bash
账号1&密码1&最小步数&最大步数====账号2&密码2&最小步数&最大步数
```

示例：

```bash
abc1&xxxx&20000&30000====abcd2&yyyy&8000&15000
```

说明：

- 多账号之间使用 `====` 分隔
- 每个账号内部使用 `&` 分隔
- 每个账号可单独设置最小步数和最大步数
- 环境变量优先级高于配置文件

---

## 配置文件方式

配置文件名：

```bash
zepp_config.json
```

配置文件需要和脚本放在同一目录。

示例：

```json
{
  "accounts": [
    {
      "username": "账号1",
      "password": "密码1",
      "min_step": 20000,
      "max_step": 30000
    },
    {
      "username": "账号2",
      "password": "密码2",
      "min_step": 8000,
      "max_step": 15000
    }
  ]
}
```

---

## 文件说明

```text
zepp_step/
├── 最终_步数脚本_环境变量_配置文件版.py   # 主脚本
├── zepp_config.json                       # 配置文件模板
└── README.md                              # 使用说明与同步记录
```

---

## 修改记录

### 2026-05-26

- 上传 Zepp Life 步数脚本目录
- 添加 `zepp_config.json` 配置模板
- 添加环境变量配置说明
- 明确账号读取优先级
- 新增同步规则：以后每次修改脚本时同步更新 README
