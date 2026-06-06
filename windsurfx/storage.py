"""accounts.json / 代理文件读写."""
import json
import os
from .state import print_lock


def save_account(account, output_file):
    with print_lock:
        accounts = []
        if os.path.exists(output_file):
            with open(output_file, "r", encoding="utf-8") as f:
                try:
                    accounts = json.load(f)
                except Exception:
                    accounts = []
        accounts.append(account)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(accounts, f, indent=2, ensure_ascii=False)


def load_proxies(path):
    if not path or not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return [line.strip() for line in f if line.strip()]
