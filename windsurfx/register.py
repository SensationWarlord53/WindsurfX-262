"""单个账号的完整注册流程."""
import datetime
import json
import random
from .config import C, DIM, G, R, Y, MAX_EMAIL_RETRIES
from .generators import parse_proxy, rand_email_prefix, rand_name, rand_password
from .log import kv, log
from .moemail import create_temp_email, poll_for_code
from .state import inc_fail, inc_ok
from .storage import save_account
from .windsurf import (
    check_connections,
    email_complete,
    email_start,
    get_current_user,
    make_session_headers,
    post_auth,
)


def _find_available_email(tid, domain, proxies):
    """循环创建临时邮箱直到撞上一个 windsurf 未注册的地址."""
    for attempt in range(MAX_EMAIL_RETRIES):
        name = rand_email_prefix()
        mailbox = create_temp_email(name, domain)
        email_id = mailbox["id"]
        email = mailbox.get("address") or f"{name}@{domain}"
        log(tid, C, "+", f"邮箱: {email}")

        _, conn_data = check_connections(email, proxies)
        method = conn_data.get("auth_method", {}).get("method")
        if method == "not_found":
            return email_id, email
        reason = conn_data.get("error") or method or "已注册"
        log(tid, Y, "~", f"邮箱已被占用 ({reason})，重试 ({attempt + 1}/{MAX_EMAIL_RETRIES})")
    return None, None


def register_one(tid, domain, proxies_list, output_file):
    proxies = None
    if proxies_list:
        proxy_str = random.choice(proxies_list)
        proxies = parse_proxy(proxy_str)
        log(tid, DIM, "~", f"使用代理 {proxy_str}")

    try:
        email_id, email = _find_available_email(tid, domain, proxies)
        if not email_id:
            log(tid, R, "✗", f"尝试 {MAX_EMAIL_RETRIES} 次后仍未找到可用邮箱")
            return None

        password = rand_password()
        name = rand_name()

        _, start_data = email_start(email, proxies)
        if not start_data.get("ok"):
            err_msg = start_data.get("message") or start_data.get("error") or json.dumps(start_data)[:200]
            log(tid, R, "✗", f"发送验证码失败: {err_msg}")
            return None
        ev_token = start_data["email_verification_token"]
        log(tid, DIM, "~", "验证码已发送，等待邮件...")

        code, _ = poll_for_code(email_id, tid)
        log(tid, G, "✓", f"验证码: {code}")

        _, complete_data = email_complete(ev_token, code, password, name, proxies)
        auth1_token = complete_data.get("token")
        if not auth1_token:
            log(tid, R, "✗", f"注册失败: {complete_data}")
            return None

        _, session_data = post_auth(auth1_token, proxies)
        session_token = session_data.get("sessionToken")
        account_id = session_data.get("accountId")
        org_id = session_data.get("primaryOrgId")
        if not session_token:
            log(tid, R, "✗", "换取 session 失败")
            return None

        session_headers = make_session_headers(session_token, auth1_token, account_id, org_id)
        user_data = get_current_user(session_headers, proxies)
        u = user_data.get("user", {})

        account = {
            "email": u.get("email"),
            "name": u.get("name"),
            "password": password,
            "user_id": u.get("id"),
            "account_id": account_id,
            "org_id": org_id,
            "auth1_token": auth1_token,
            "session_token": session_token,
            "api_key": u.get("apiKey"),
            "registered_at": datetime.datetime.utcnow().isoformat() + "Z",
        }
        save_account(account, output_file)
        total_ok = inc_ok()

        log(tid, G, "✓", f"注册成功: {email}  [已完成 {total_ok}]")
        kv(tid, "session_token", (session_token or "")[:40] + "...")
        kv(tid, "api_key", (u.get("apiKey") or "")[:40] + "...")
        return account

    except KeyboardInterrupt:
        return None
    except Exception as e:
        inc_fail()
        log(tid, R, "✗", f"出错: {e}")
        return None
