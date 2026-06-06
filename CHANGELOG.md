# Changelog

本项目所有显著变更将记录在此文件，遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 格式，
版本号遵循 [语义化版本 2.0.0](https://semver.org/lang/zh-CN/)。

## [0.1.0] - 2026-05-17

### 新增

- Windsurf (windsurf.com) 自动注册流程
- 基于 ThreadPoolExecutor 的并发注册（`-j` 参数）
- 通过 [moemail](https://github.com/beilunyang/moemail) 临时邮箱自动接收验证码
- 单代理 (`-p`) 与代理池文件 (`--proxy-file`) 支持
- `accounts.json` 凭证持久化（含 `auth1_token` / `session_token` / `api_key`）
- 自适应邮箱前缀生成器，遇撞名自动换前缀重试
- `Ctrl+C` 优雅退出：停止派发新任务，正在跑的任务在轮询节点退出
- 模块化项目结构（`windsurfx/` 包），按职责拆分
- `.env` 配置（`MOEMAIL_BASE` / `MOEMAIL_API_KEY`）
- MIT 开源协议

[0.1.0]: https://github.com/huey1in/WindsurfX/releases/tag/v0.1.0
