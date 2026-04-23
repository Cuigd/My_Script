#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
青龙可运行的 WPS 自动签到脚本（基于抓到的有效请求重放）

设计思路：
1. 不硬编码可能变化的旧接口
2. 使用浏览器/抓包工具里“已经成功签到过”的 curl 请求
3. 青龙每天重放该请求，实现自动签到

推荐环境变量：
- WPS_ACCOUNT_NAME        多账号名称，按行分隔，可选
- WPS_CHECKIN_CURL        多账号签到 curl，按行分隔（推荐）
- WPS_CHECKIN_CURL_B64    多账号签到 curl 的 base64 版本，按行分隔（更稳，推荐长命令时使用）
- WPS_WEBHOOK             通知地址，可选
- WPS_DRY_RUN             1/true 时仅解析不发送请求

可选：
- WPS_PAGEINFO_CURL       若你抓到了 page_info 请求，可补充用于检查奖励/次数
- WPS_LOTTERY_CURL        若你抓到了抽奖请求，可后续自行扩展
"""

from __future__ import annotations

import base64
import json
import os
import re
import shlex
import sys
import time
from typing import Dict, List, Optional, Tuple
from urllib import request
from urllib.error import HTTPError, URLError

SCRIPT_NAME = "WPS青龙自动签到"
SCRIPT_VERSION = "2.0.0"
DEFAULT_TIMEOUT = 20


def log(msg: str) -> None:
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"[{now}] {msg}")


def get_env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


def split_lines(value: str) -> List[str]:
    if not value:
        return []
    return [item.strip() for item in value.splitlines() if item.strip()]


def mask(value: str, keep: int = 4) -> str:
    if not value:
        return "<empty>"
    if len(value) <= keep * 2:
        return "*" * len(value)
    return value[:keep] + "***" + value[-keep:]


def to_bool(value: str) -> bool:
    return value.lower() in {"1", "true", "yes", "on", "y"}


def decode_b64_lines(lines: List[str]) -> List[str]:
    result: List[str] = []
    for line in lines:
        try:
            result.append(base64.b64decode(line).decode("utf-8"))
        except Exception as exc:
            raise ValueError(f"Base64 解码失败: {exc}") from exc
    return result


def normalize_curl(curl_cmd: str) -> str:
    curl_cmd = curl_cmd.strip()
    curl_cmd = curl_cmd.replace("\\\n", " ").replace("\r", " ").replace("\n", " ")
    curl_cmd = re.sub(r"\s+", " ", curl_cmd).strip()
    return curl_cmd


def parse_curl(curl_cmd: str) -> Dict[str, object]:
    cmd = normalize_curl(curl_cmd)
    if not cmd.startswith("curl ") and not cmd.startswith("curl.exe "):
        raise ValueError("提供的内容不是 curl 命令")

    parts = shlex.split(cmd, posix=True)
    method = "GET"
    url = ""
    headers: Dict[str, str] = {}
    body = b""

    i = 1
    while i < len(parts):
        part = parts[i]
        if part in {"-X", "--request"} and i + 1 < len(parts):
            method = parts[i + 1].upper()
            i += 2
            continue
        if part in {"-H", "--header"} and i + 1 < len(parts):
            header_line = parts[i + 1]
            if ":" in header_line:
                k, v = header_line.split(":", 1)
                headers[k.strip()] = v.strip()
            i += 2
            continue
        if part in {"--data", "--data-raw", "--data-binary", "--data-ascii", "-d"} and i + 1 < len(parts):
            body = parts[i + 1].encode("utf-8")
            if method == "GET":
                method = "POST"
            i += 2
            continue
        if not part.startswith("-") and not url:
            url = part
            i += 1
            continue
        i += 1

    if not url:
        raise ValueError("curl 中未解析到 URL")

    return {
        "method": method,
        "url": url,
        "headers": headers,
        "body": body,
    }


def send_http(req_conf: Dict[str, object], dry_run: bool = False) -> Tuple[int, str, Dict[str, str]]:
    method = str(req_conf["method"])
    url = str(req_conf["url"])
    headers = dict(req_conf.get("headers", {}))
    body = req_conf.get("body", b"")
    if isinstance(body, str):
        body = body.encode("utf-8")

    log(f"请求: {method} {url}")
    if "Cookie" in headers:
        log(f"Cookie: {mask(headers['Cookie'])}")
    elif "cookie" in headers:
        log(f"cookie: {mask(headers['cookie'])}")

    if dry_run:
        return 200, json.dumps({"dry_run": True, "url": url}, ensure_ascii=False), {}

    req = request.Request(url=url, data=body if method != "GET" else None, method=method)
    for k, v in headers.items():
        req.add_header(k, v)

    with request.urlopen(req, timeout=DEFAULT_TIMEOUT) as resp:
        raw = resp.read().decode("utf-8", errors="ignore")
        resp_headers = {k: v for k, v in resp.headers.items()}
        return resp.status, raw, resp_headers


def looks_like_success(status: int, text: str) -> Tuple[bool, str]:
    text_lower = text.lower()
    if status != 200:
        return False, f"HTTP {status}"
    success_keywords = [
        '"result":"ok"',
        '"success":true',
        '"code":0',
        '"msg":"ok"',
        '签到成功',
        '已签到',
        'success',
    ]
    repeated_keywords = [
        '已经签到',
        '重复签到',
        'already',
        '已领取',
    ]
    if any(k in text_lower for k in [s.lower() for s in success_keywords]):
        return True, "接口返回成功"
    if any(k in text_lower for k in [s.lower() for s in repeated_keywords]):
        return True, "今天可能已经签过"
    return True, "请求成功，但未命中特定成功关键字，请检查返回内容"


def brief_text(text: str, limit: int = 220) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text[:limit] + ("..." if len(text) > limit else "")


def send_webhook(text: str) -> None:
    webhook = get_env("WPS_WEBHOOK")
    if not webhook:
        return
    payload = json.dumps({"text": text}, ensure_ascii=False).encode("utf-8")
    req = request.Request(
        webhook,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=15) as resp:
            log(f"Webhook 已发送，状态码: {resp.status}")
    except Exception as exc:
        log(f"Webhook 发送失败: {exc}")


def load_accounts() -> List[Dict[str, str]]:
    names = split_lines(get_env("WPS_ACCOUNT_NAME"))
    curls = split_lines(get_env("WPS_CHECKIN_CURL"))
    curls_b64 = split_lines(get_env("WPS_CHECKIN_CURL_B64"))

    if curls_b64:
        curls.extend(decode_b64_lines(curls_b64))

    accounts: List[Dict[str, str]] = []
    for idx, curl_cmd in enumerate(curls, start=1):
        name = names[idx - 1] if idx - 1 < len(names) else f"WPS账号{idx}"
        accounts.append({"name": name, "curl": curl_cmd})
    return accounts


def run_account(account: Dict[str, str], index: int, dry_run: bool) -> Dict[str, str]:
    name = account["name"]
    curl_cmd = account["curl"]
    log(f"开始处理账号 {index}: {name}")

    parsed = parse_curl(curl_cmd)
    status, text, _ = send_http(parsed, dry_run=dry_run)
    ok, reason = looks_like_success(status, text)

    return {
        "account": name,
        "status": "success" if ok else "failed",
        "reason": reason,
        "http_status": str(status),
        "response": brief_text(text),
    }


def main() -> int:
    log(f"启动 {SCRIPT_NAME} v{SCRIPT_VERSION}")
    dry_run = to_bool(get_env("WPS_DRY_RUN", "0"))
    accounts = load_accounts()

    if not accounts:
        log("未找到账号。请设置 WPS_CHECKIN_CURL 或 WPS_CHECKIN_CURL_B64。")
        return 1

    results: List[Dict[str, str]] = []
    for idx, account in enumerate(accounts, start=1):
        try:
            result = run_account(account, idx, dry_run=dry_run)
        except (HTTPError, URLError) as exc:
            result = {
                "account": account.get("name", f"WPS账号{idx}"),
                "status": "failed",
                "reason": f"网络错误: {exc}",
                "http_status": "-",
                "response": "",
            }
        except Exception as exc:
            result = {
                "account": account.get("name", f"WPS账号{idx}"),
                "status": "failed",
                "reason": f"运行异常: {exc}",
                "http_status": "-",
                "response": "",
            }
        results.append(result)
        log(f"{result['account']} -> {result['status']} | {result['reason']}")

    success_count = sum(1 for item in results if item["status"] == "success")
    summary = f"{SCRIPT_NAME} 执行完成：成功 {success_count}/{len(results)}"
    log(summary)
    send_webhook(summary + "\n" + json.dumps(results, ensure_ascii=False, indent=2))
    return 0 if success_count == len(results) else 2


if __name__ == "__main__":
    sys.exit(main())
