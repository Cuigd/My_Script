#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
青龙可运行的 WPS 自动化脚本模板

用途：
- 作为青龙拉库后的可执行 Python 脚本模板
- 通过环境变量读取账号、密码、Token、Cookie、Webhook 等信息
- 预留 WPS / 金山文档签到或 API 调用逻辑

青龙变量示例：
- WPS_USERNAME
- WPS_PASSWORD
- WPS_COOKIE
- WPS_TOKEN
- WPS_WEBHOOK
"""

from __future__ import annotations

import json
import os
import sys
import time
from typing import Dict, List
from urllib import request, parse
from urllib.error import URLError, HTTPError


SCRIPT_NAME = "WPS青龙任务模板"
SCRIPT_VERSION = "1.0.0"


def log(msg: str) -> None:
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"[{now}] {msg}")


def get_env(name: str, default: str = "") -> str:
    value = os.getenv(name, default).strip()
    return value


def mask(value: str) -> str:
    if not value:
        return "<empty>"
    if len(value) <= 6:
        return "*" * len(value)
    return value[:3] + "***" + value[-3:]


def split_multi_line(value: str) -> List[str]:
    if not value:
        return []
    return [item.strip() for item in value.splitlines() if item.strip()]


def load_accounts() -> List[Dict[str, str]]:
    usernames = split_multi_line(get_env("WPS_USERNAME"))
    passwords = split_multi_line(get_env("WPS_PASSWORD"))
    cookies = split_multi_line(get_env("WPS_COOKIE"))
    tokens = split_multi_line(get_env("WPS_TOKEN"))

    max_len = max(len(usernames), len(passwords), len(cookies), len(tokens), 1)
    accounts: List[Dict[str, str]] = []
    for idx in range(max_len):
        accounts.append(
            {
                "username": usernames[idx] if idx < len(usernames) else "",
                "password": passwords[idx] if idx < len(passwords) else "",
                "cookie": cookies[idx] if idx < len(cookies) else "",
                "token": tokens[idx] if idx < len(tokens) else "",
            }
        )
    return [acc for acc in accounts if any(acc.values())]


def send_webhook(text: str) -> None:
    webhook = get_env("WPS_WEBHOOK")
    if not webhook:
        return

    payload = json.dumps({"text": text}).encode("utf-8")
    req = request.Request(
        webhook,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=15) as resp:
            log(f"Webhook 推送完成，状态码: {resp.status}")
    except Exception as exc:
        log(f"Webhook 推送失败: {exc}")


def run_account(account: Dict[str, str], index: int) -> Dict[str, str]:
    username = account.get("username", "")
    cookie = account.get("cookie", "")
    token = account.get("token", "")

    log(f"开始处理第 {index} 个账号")
    log(f"用户名: {username or '<未提供>'}")
    if cookie:
        log(f"Cookie: {mask(cookie)}")
    if token:
        log(f"Token: {mask(token)}")

    # TODO:
    # 1. 如果你后续确定了 WPS 具体接口，可在这里发送 HTTP 请求
    # 2. 如果是 AirScript / 金山文档接口，也可以改成调用对应 API
    # 3. 如果需要签到逻辑，可在这里解析返回值并判断成功/失败

    # 当前先返回“模板成功执行”，用于验证青龙拉库与环境变量配置没问题
    return {
        "username": username or f"account_{index}",
        "status": "success",
        "message": "模板执行成功，请在 run_account() 中补充实际 WPS 逻辑",
    }


def main() -> int:
    log(f"启动 {SCRIPT_NAME} v{SCRIPT_VERSION}")
    accounts = load_accounts()
    if not accounts:
        log("未找到任何账号配置，请设置 WPS_USERNAME / WPS_PASSWORD / WPS_COOKIE / WPS_TOKEN")
        return 1

    results: List[Dict[str, str]] = []
    for i, account in enumerate(accounts, start=1):
        try:
            result = run_account(account, i)
        except (HTTPError, URLError) as exc:
            result = {
                "username": account.get("username") or f"account_{i}",
                "status": "failed",
                "message": f"网络请求失败: {exc}",
            }
        except Exception as exc:
            result = {
                "username": account.get("username") or f"account_{i}",
                "status": "failed",
                "message": f"运行异常: {exc}",
            }
        results.append(result)
        log(f"结果: {result['username']} -> {result['status']} | {result['message']}")

    success_count = sum(1 for item in results if item["status"] == "success")
    summary = f"{SCRIPT_NAME} 执行完成，成功 {success_count}/{len(results)}"
    log(summary)
    send_webhook(summary + "\n" + json.dumps(results, ensure_ascii=False, indent=2))
    return 0 if success_count == len(results) else 2


if __name__ == "__main__":
    sys.exit(main())
