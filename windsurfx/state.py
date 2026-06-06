"""线程间共享的状态."""
import threading

print_lock = threading.Lock()
counter = {"ok": 0, "fail": 0}
counter_lock = threading.Lock()
stop_event = threading.Event()


def inc_ok():
    with counter_lock:
        counter["ok"] += 1
        return counter["ok"]


def inc_fail():
    with counter_lock:
        counter["fail"] += 1
        return counter["fail"]
