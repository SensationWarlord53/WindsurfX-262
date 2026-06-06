"""随机邮箱前缀、密码、昵称生成."""
import random
import string
import time


def rand_str(n=8):
    return "".join(random.choices(string.ascii_lowercase, k=n))


def rand_email_prefix():
    """生成长且独特的邮箱前缀，最小化撞名概率."""
    tail = str(int(time.time() * 1000))[-6:]
    styles = [
        lambda: rand_str(random.randint(8, 12)) + str(random.randint(1000, 9999)),
        lambda: rand_str(random.randint(6, 9)) + "." + rand_str(random.randint(5, 8)) + str(random.randint(10, 999)),
        lambda: rand_str(random.randint(6, 9)) + "_" + rand_str(random.randint(5, 8)) + str(random.randint(10, 999)),
        lambda: rand_str(random.randint(5, 8)) + "." + rand_str(random.randint(5, 8)) + tail,
        lambda: rand_str(random.randint(8, 12)) + tail,
        lambda: rand_str(random.randint(6, 9)) + "-" + rand_str(random.randint(5, 8)) + str(random.randint(100, 999)),
        lambda: rand_str(1).upper() + rand_str(random.randint(8, 11)) + str(random.randint(1000, 9999)),
    ]
    return random.choice(styles)()


def rand_password():
    return "Ws@" + rand_str(6) + str(random.randint(10, 99))


def rand_name():
    return rand_str(4).capitalize() + " " + rand_str(5).capitalize()


def parse_proxy(proxy_str):
    if not proxy_str:
        return None
    if "://" not in proxy_str:
        proxy_str = "http://" + proxy_str
    return {"http": proxy_str, "https": proxy_str}
