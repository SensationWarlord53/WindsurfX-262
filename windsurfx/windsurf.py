"""Windsurf API 客户端."""
import requests
from .config import BASE_URL, COMMON_HEADERS, REQUEST_TIMEOUT


def _post(path, payload, extra_headers=None, proxies=None):
    headers = {**COMMON_HEADERS, **(extra_headers or {})}
    url = f"{BASE_URL}{path}"
    resp = requests.post(url, headers=headers, json=payload, proxies=proxies, timeout=REQUEST_TIMEOUT)
    try:
        data = resp.json()
    except Exception:
        data = resp.text
    return resp, data


def check_connections(email, proxies=None):
    return _post("/_devin-auth/connections", {"product": "windsurf", "email": email}, proxies=proxies)


def email_start(email, proxies=None):
    return _post("/_devin-auth/email/start", {
        "email": email,
        "mode": "signup",
        "product": "Windsurf",
    }, proxies=proxies)


def email_complete(ev_token, code, password, name, proxies=None):
    return _post("/_devin-auth/email/complete", {
        "email_verification_token": ev_token,
        "code": code,
        "mode": "signup",
        "password": password,
        "name": name,
    }, proxies=proxies)


def post_auth(auth1_token, proxies=None):
    return _post(
        "/_backend/exa.seat_management_pb.SeatManagementService/WindsurfPostAuth",
        {},
        extra_headers={
            "connect-protocol-version": "1",
            "x-devin-auth1-token": auth1_token,
        },
        proxies=proxies,
    )


def make_session_headers(session_token, auth1_token, account_id, org_id):
    return {
        "connect-protocol-version": "1",
        "x-auth-token": session_token,
        "x-devin-session-token": session_token,
        "x-devin-auth1-token": auth1_token,
        "x-devin-account-id": account_id,
        "x-devin-primary-org-id": org_id,
    }


def get_current_user(session_headers, proxies=None):
    _, data = _post(
        "/_backend/exa.seat_management_pb.SeatManagementService/GetCurrentUser",
        {"generateProfilePictureUrl": True, "includeSubscription": True},
        extra_headers=session_headers,
        proxies=proxies,
    )
    return data
