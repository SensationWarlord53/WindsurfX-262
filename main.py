"""WindsurfX - 入口."""
import argparse
import os

from windsurfx.config import DEFAULT_OUTPUT
from windsurfx.runner import run
from windsurfx.storage import load_proxies


def main():
    parser = argparse.ArgumentParser(prog="windsurfx", description="WindsurfX - Windsurf 自动注册")
    parser.add_argument("-n", "--count",   type=int, default=1,              help="注册账号总数 (默认: 1)")
    parser.add_argument("-j", "--jobs",    type=int, default=1,              help="并发数 (默认: 1)")
    parser.add_argument("-p", "--proxy",   type=str, default=None,           help="单个代理，如 http://127.0.0.1:7890")
    parser.add_argument("--proxy-file",    type=str, default=None,           help="代理池文件，每行一条")
    parser.add_argument("-o", "--output",  type=str, default=DEFAULT_OUTPUT, help=f"输出 json 文件 (默认: {DEFAULT_OUTPUT})")
    args = parser.parse_args()

    proxies_list = load_proxies(args.proxy_file)
    if args.proxy:
        proxies_list.append(args.proxy)

    output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), args.output)
    run(args.count, args.jobs, proxies_list, output_file)


if __name__ == "__main__":
    main()
