"""并发调度 + 信号处理."""
import signal
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from .config import C, DIM, G, R, RST, Y
from .log import banner
from .moemail import get_available_domain
from .register import register_one
from .state import counter, print_lock, stop_event


def install_signal_handlers():
    def handler(signum, frame):
        with print_lock:
            print(f"\n{Y}! 已中断，停止派发新任务...{RST}")
        stop_event.set()
    signal.signal(signal.SIGINT, handler)
    try:
        signal.signal(signal.SIGTERM, handler)
    except Exception:
        pass


def run(count, jobs, proxies_list, output_file):
    install_signal_handlers()

    banner(f"\n{C}WindsurfX{RST}  {DIM}windsurf.com 自动注册{RST}")
    banner(f"{DIM}总数={count}  并发={jobs}  输出={output_file}  代理={len(proxies_list)}  （Ctrl+C 退出）{RST}\n")

    domain = get_available_domain()

    executor = ThreadPoolExecutor(max_workers=jobs)
    futures = []
    try:
        for i in range(count):
            if stop_event.is_set():
                break
            futures.append(executor.submit(register_one, i + 1, domain, proxies_list, output_file))

        pending = set(futures)
        while pending and not stop_event.is_set():
            _, pending = wait(pending, timeout=0.5, return_when=FIRST_COMPLETED)
    except KeyboardInterrupt:
        stop_event.set()
    finally:
        if stop_event.is_set():
            for f in futures:
                f.cancel()
            executor.shutdown(wait=False, cancel_futures=True)
            banner(f"{Y}! 正在退出，已完成的账号已保存{RST}")
        else:
            executor.shutdown(wait=True)

    print(f"\n{G}完成.{RST}  {G}成功={counter['ok']}{RST}  {R}失败={counter['fail']}{RST}  已保存到 {output_file}\n")
