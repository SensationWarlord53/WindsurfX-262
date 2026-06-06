"""日志辅助函数."""
import datetime
from .config import DIM, RST, Y
from .state import print_lock


def ts():
    return datetime.datetime.now().strftime("%H:%M:%S")


def log(tid, color, symbol, msg):
    with print_lock:
        print(f"{DIM}[{ts()}][#{tid:02d}]{RST} {color}{symbol} {msg}{RST}")


def kv(tid, key, val):
    with print_lock:
        print(f"           {DIM}{key:<14}{RST} {Y}{val}{RST}")


def banner(text):
    with print_lock:
        print(text)
