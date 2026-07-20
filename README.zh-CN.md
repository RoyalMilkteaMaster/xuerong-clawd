# 雪绒 — Clawd on Desk 猫娘桌面宠物

[繁體中文](README.md) · [简体中文](README.zh-CN.md) · [English](README.en.md) · [日本語](README.ja-JP.md) · [한국어](README.ko-KR.md)

雪绒是一只白色布偶猫猫娘桌面宠物。本仓库提供雪绒 HD 主题、Windows 一键主题安装器、可由 Clawd 导入的 ZIP，以及旧版完整修改核心的对应源代码。

![温柔雪蓝](01-gentle-snow-blue.png)

![活泼眨眼](02-playful-wink.png)

![害羞爱心](03-bashful-heart.png)

![雪绒动画总览](themes/xuerong-hd/qa/all-frames-v21.png)

## 当前版本

| 项目 | 版本 | 用途 |
|---|---:|---|
| 个性化 Clawd on Desk | `0.12.1-notifications.10` | Windows x64；增加 Discord／LINE 通知与通知回复设置 |
| 官方 Clawd on Desk | `0.12.0` | 官方稳定版 |
| 雪绒 HD 主题 | `2.4.1` | 当前推荐安装的主题版本 |
| 旧版雪绒程序包 | `0.11.0` | 基于 Clawd `0.10.0` 的旧版完整修改核心，仅供源代码与兼容性参考 |

## 功能

- 普通待机、工作中、睡眠、起床、被抓等交互动画。
- 边缘模式专用 Q 版半身动画。
- 支持 Clawd 的 Session HUD、任务状态与 Codex context 进度。
- 个性化 Clawd 版本可发送 Discord／LINE 完成通知，并可在设置页修改昵称与回复。
- 提供主题 EXE 一键安装、ZIP 导入、更新与卸载方式。

## 最简单的安装方式

安装分为两步：先安装 Clawd on Desk 应用，再安装雪绒主题。两个 EXE 的用途不同，请勿混用。

### 第一步：安装 Clawd on Desk

#### 选项 A：个性化 Clawd（Windows x64，推荐）

个性化版本目前为 `0.12.1-notifications.10`，包括：

- Discord Bot 完成通知与设置页。
- LINE Messaging API 手机通知与设置页。
- 可修改昵称及完成／中断／权限／选择回复的“通知回复”页面。
- Discord／LINE 可选通知安装与故障排查指南。

<p align="left">
  <a href="https://github.com/RoyalMilkteaMaster/clawd-on-desk/releases/download/v0.12.1-notifications.10/Clawd-on-Desk-Setup-0.12.1-notifications.10-x64.exe">
    <img src="assets/readme/windows-download-button.svg" width="180" alt="下载个性化 Clawd on Desk 0.12.1-notifications.10 Windows x64 安装器">
  </a>
</p>

直接下载：[`Clawd-on-Desk-Setup-0.12.1-notifications.10-x64.exe`](https://github.com/RoyalMilkteaMaster/clawd-on-desk/releases/download/v0.12.1-notifications.10/Clawd-on-Desk-Setup-0.12.1-notifications.10-x64.exe)

> 这是 **Clawd 应用安装器**，不是雪绒主题安装器。安装前请先关闭 Clawd。通知默认关闭，安装文件不包含任何用户的 Discord／LINE Token。

完整通知设置请阅读 [Discord／LINE 可选通知安装指南](https://github.com/RoyalMilkteaMaster/clawd-on-desk/blob/agent/notifications-0.12.1/docs/guides/notifications.zh-TW.md)（繁体中文）。

#### 选项 B：官方 Clawd 0.12.0

- [打开官方 v0.12.0 Release](https://github.com/rullerzhou-afk/clawd-on-desk/releases/tag/v0.12.0)
- [直接下载 Windows x64 安装器](https://github.com/rullerzhou-afk/clawd-on-desk/releases/download/v0.12.0/Clawd-on-Desk-Setup-0.12.0-x64.exe)

官方版不包含上述个性化 Discord／LINE 设置，但可以正常安装并使用雪绒主题。

安装完成后请先启动一次 Clawd，确认程序可以正常运行。

### 第二步：安装雪绒主题

#### 选项 A：雪绒一键主题安装器

<p align="left">
  <a href="https://github.com/RoyalMilkteaMaster/xuerong-clawd/releases/download/xuerong-theme-v2.4.1/Xuerong-HD-Theme-Installer.exe">
    <img src="assets/readme/windows-download-button.svg" width="180" alt="下载雪绒 HD 2.4.1 Windows 主题安装器">
  </a>
</p>

直接下载：[`Xuerong-HD-Theme-Installer.exe`](https://github.com/RoyalMilkteaMaster/xuerong-clawd/releases/download/xuerong-theme-v2.4.1/Xuerong-HD-Theme-Installer.exe)

1. 关闭 Clawd。
2. 双击 `Xuerong-HD-Theme-Installer.exe`。
3. 看到“雪绒 HD 已加入 Clawd 主题列表”后，重新启动 Clawd。
4. 选择 `设置 → 主题 → 用户主题 → 雪绒 HD`。

> 主题安装器只会把雪绒放入当前 Windows 用户的 Clawd 主题目录，不会修改 `app.asar`，也不需要管理员权限。

#### 选项 B：使用 Clawd 的 ZIP 导入功能

1. [下载 `Xuerong-HD-Clawd-Theme.zip`](https://github.com/RoyalMilkteaMaster/xuerong-clawd/releases/download/xuerong-theme-v2.4.1/Xuerong-HD-Clawd-Theme.zip)。
2. 不要解压 ZIP。
3. 打开 Clawd，选择 `设置 → 主题 → 导入 Clawd 主题包（.zip）`。
4. 选择下载的 ZIP，再切换到“雪绒 HD”。
5. 如果角色没有立即更新，请重启 Clawd。

## 更新雪绒主题

- 使用 EXE 安装：下载新版主题安装器并重新运行，安装器会先备份旧主题。
- 使用 ZIP 导入：如果 Clawd 提示同名主题已存在，请先移除旧的“雪绒 HD”，再导入新版 ZIP。
- 所有雪绒版本：[GitHub Releases](https://github.com/RoyalMilkteaMaster/xuerong-clawd/releases)。

## 移除雪绒主题

在主题安装器所在目录打开 PowerShell：

```powershell
.\Xuerong-HD-Theme-Installer.exe /uninstall
```

也可以先关闭 Clawd，再删除：

```text
%APPDATA%\clawd-on-desk\themes\xuerong-hd
```

## 兼容性与系统要求

- 个性化 Clawd：Windows 10／11 x64。
- 官方 Clawd：雪绒 2.4.1 已针对官方 `0.12.0` 主题流程发布。
- 主题 EXE：Windows、PowerShell 5.1 或更高版本。
- 主题 ZIP：可用于其他 Clawd 支持的平台。
- 主题安装器只添加主题，不会增加 Discord／LINE 通知或其他核心功能。
- 本仓库的旧版完整修改核心仅适用于 Clawd `0.10.0`；不要使用旧版 `-ForceUnsupported` 覆盖 `0.12.x`。

## 安全与隐私

- 雪绒主题安装器不会覆盖任务记录、SSH、Agent、Telegram、Discord 或 LINE 设置。
- 个性化 Clawd 安装文件不包含 Bot Token、LINE Channel Access Token、频道 ID 或用户 ID。
- 未签名的 Windows 安装器可能触发 SmartScreen。如果不想运行主题 EXE，可改用 ZIP 导入。
- 雪绒主题的默认白名单设置位于 [settings/xuerong-defaults.json](settings/xuerong-defaults.json)。

## 版本来源

- 个性化 Clawd：[RoyalMilkteaMaster/clawd-on-desk](https://github.com/RoyalMilkteaMaster/clawd-on-desk)
- 个性化 Clawd Release：[`v0.12.1-notifications.10`](https://github.com/RoyalMilkteaMaster/clawd-on-desk/releases/tag/v0.12.1-notifications.10)
- 官方上游：[rullerzhou-afk/clawd-on-desk](https://github.com/rullerzhou-afk/clawd-on-desk)
- 雪绒主题：`2.4.1`
- 旧版完整修改核心：Clawd `0.10.0`、雪绒程序包 `0.11.0`
- 旧版上游基准 commit：`9ccafb84680d7068baa35e2d91c0800f81c7b475`

原始上游繁体中文说明保留在 [docs/UPSTREAM-README.zh-TW.md](docs/UPSTREAM-README.zh-TW.md)。

## 开发与验证

```powershell
npm ci
npm test
powershell -ExecutionPolicy Bypass -File .\scripts\validate-release.ps1
powershell -ExecutionPolicy Bypass -File .\installer\build-theme-installer.ps1
powershell -ExecutionPolicy Bypass -File .\installer\test-theme-installer.ps1
```

验证记录请参阅 [docs/VALIDATION.md](docs/VALIDATION.md)。

## 许可证

Clawd on Desk 与修改后的源代码使用 GNU AGPL-3.0，详见 [LICENSE](LICENSE) 与 [NOTICE.md](NOTICE.md)。

雪绒角色与动画素材使用独立的个人非商业分享条款，详见 [ASSET-LICENSE.md](ASSET-LICENSE.md)。
