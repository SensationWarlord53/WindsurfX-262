"""环境变量、常量、ANSI 颜色码."""
import os
from dotenv import load_dotenv

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(_ROOT, ".env"))

BASE_URL = "https://windsurf.com"
MOEMAIL_BASE = os.environ["MOEMAIL_BASE"]
MOEMAIL_API_KEY = os.environ["MOEMAIL_API_KEY"]

COMMON_HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36 Edg/148.0.0.0",
    "accept": "*/*",
    "origin": "https://windsurf.com",
    "referer": "https://windsurf.com/account/register",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "content-type": "application/json",
}

MOEMAIL_HEADERS = {
    "X-API-Key": MOEMAIL_API_KEY,
    "User-Agent": "Mozilla/5.0",
}

# ANSI 颜色
G = "\033[92m"
Y = "\033[93m"
R = "\033[91m"
C = "\033[96m"
W = "\033[97m"
DIM = "\033[2m"
RST = "\033[0m"

# 默认值
DEFAULT_OUTPUT = "accounts.json"
MAX_EMAIL_RETRIES = 10
EMAIL_POLL_TIMEOUT = 120
EMAIL_POLL_INTERVAL = 5
REQUEST_TIMEOUT = 30
MOEMAIL_TIMEOUT = 15
