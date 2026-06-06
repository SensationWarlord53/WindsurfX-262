"""moemail临时邮箱 API 客户端."""
import re
import time
import requests
from .config import MOEMAIL_BASE, MOEMAIL_HEADERS, MOEMAIL_TIMEOUT, EMAIL_POLL_TIMEOUT, EMAIL_POLL_INTERVAL, DIM
from .log import log
from .state import stop_event


def _get(path, params=None):
    resp = requests.get(
        f"{MOEMAIL_BASE}{path}",
        headers=MOEMAIL_HEADERS,
        params=params,
        timeout=MOEMAIL_TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json()


def _post(path, payload=None):
    resp = requests.post(
        f"{MOEMAIL_BASE}{path}",
        headers={**MOEMAIL_HEADERS, "Content-Type": "application/json"},
        json=payload or {},
        timeout=MOEMAIL_TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json()


def get_available_domain():
    config = _get("/api/config")
    raw = config.get("emailDomains", "")
    domains = [d.strip() for d in raw.split(",") if d.strip()]
    if not domains:
        raise RuntimeError("moemail 返回的 emailDomains 为空")
    return domains[0]


def create_temp_email(name, domain, expiry_ms=3600000):
    return _post("/api/emails/generate", {
        "name": name,
        "expiryTime": expiry_ms,
        "domain": domain,
    })


def poll_for_code(email_id, tid, timeout=EMAIL_POLL_TIMEOUT, interval=EMAIL_POLL_INTERVAL):
    """轮询临时邮箱直到收到 6 位数字验证码."""
    deadline = time.time() + timeout
    seen = set()
    while time.time() < deadline:
        if stop_event.is_set():
            raise KeyboardInterrupt("stopped")
        data = _get(f"/api/emails/{email_id}")
        for msg in data.get("messages", []):
            mid = msg.get("id")
            if mid in seen:
                continue
            seen.add(mid)
            body = msg.get("content", "") or msg.get("text", "") or msg.get("html", "") or ""
            match = re.search(r"\b(\d{6})\b", body)
            if match:
                return match.group(1), msg
        remaining = int(deadline - time.time())
        log(tid, DIM, "~", f"等待邮件... 剩余 {remaining}s")
        time.sleep(interval)
    raise TimeoutError("等待验证码邮件超时")
