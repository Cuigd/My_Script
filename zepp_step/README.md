# Zepp Life 步数脚本

## 配置方式

脚本支持以下三种方式读取账号：

优先级：
1. ZEPP_ACCOUNTS 环境变量
2. xxxxx_sbs 环境变量
3. zepp_config.json 配置文件

---

## 环境变量格式

变量名：

```bash
ZEPP_ACCOUNTS
```

变量值：

```bash
账号1&密码1&最小步数&最大步数====账号2&密码2&最小步数&最大步数
```

示例：

```bash
abc1&xxxx&20000&30000====abcd2&yyyy&8000&15000
```

---

## 配置文件格式

文件名：

```bash
zepp_config.json
```

格式示例：

```json
{
  "accounts": [
    {
      "username": "账号1",
      "password": "密码1",
      "min_step": 20000,
      "max_step": 30000
    }
  ]
}
```
