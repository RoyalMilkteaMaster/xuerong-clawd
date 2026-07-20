# 雪絨 — Clawd on Desk 貓娘桌面寵物

[繁體中文](README.md) · [简体中文](README.zh-CN.md) · [English](README.en.md) · [日本語](README.ja-JP.md) · [한국어](README.ko-KR.md)

雪絨是一隻白色布偶貓貓娘桌面寵物。本倉庫提供雪絨 HD 主題、Windows 一鍵主題安裝器、可由 Clawd 匯入的 ZIP，以及舊版完整修改核心的對應原始碼。

![溫柔雪藍](01-gentle-snow-blue.png)

![活潑眨眼](02-playful-wink.png)

![害羞愛心](03-bashful-heart.png)

![雪絨動畫總覽](themes/xuerong-hd/qa/all-frames-v21.png)

## 目前版本

| 項目 | 版本 | 用途 |
|---|---:|---|
| 個人化 Clawd on Desk | `0.12.1-notifications.10` | Windows x64；加入 Discord／LINE 通知與通知回應設定 |
| 官方 Clawd on Desk | `0.12.0` | 官方穩定版 |
| 雪絨 HD 主題 | `2.4.1` | 建議安裝的目前主題版本 |
| 舊版雪絨程式套件 | `0.11.0` | 以 Clawd `0.10.0` 為基礎的舊版完整修改核心，僅供原始碼與相容性參考 |

## 功能

- 一般待機、工作中、睡眠、起床、被抓等互動動畫。
- 邊緣模式專用 Q 版半身動畫。
- 支援 Clawd 的 Session HUD、工作狀態與 Codex context 進度。
- 個人化 Clawd 版本可傳送 Discord／LINE 完成通知，並可在設定頁修改暱稱與回應。
- 提供主題 EXE 一鍵安裝、ZIP 匯入與移除方式。

## 最簡單安裝

安裝分成兩步：先安裝 Clawd on Desk 應用程式，再安裝雪絨主題。兩個 EXE 的用途不同，請不要混用。

### 第一步：安裝 Clawd on Desk

#### 選擇 A：個人化 Clawd（Windows x64，建議）

個人化版本目前是 `0.12.1-notifications.10`，包含：

- Discord Bot 完成通知與設定頁。
- LINE Messaging API 手機通知與設定頁。
- 可修改暱稱及完成／中斷／權限／選擇回應的「通知回應」頁面。
- Discord／LINE 選配通知安裝與除錯指南。

<p align="left">
  <a href="https://github.com/RoyalMilkteaMaster/clawd-on-desk/releases/download/v0.12.1-notifications.10/Clawd-on-Desk-Setup-0.12.1-notifications.10-x64.exe">
    <img src="assets/readme/windows-download-button.svg" width="180" alt="下載個人化 Clawd on Desk 0.12.1-notifications.10 Windows x64 安裝器">
  </a>
</p>

直接下載：[`Clawd-on-Desk-Setup-0.12.1-notifications.10-x64.exe`](https://github.com/RoyalMilkteaMaster/clawd-on-desk/releases/download/v0.12.1-notifications.10/Clawd-on-Desk-Setup-0.12.1-notifications.10-x64.exe)

> 這是 **Clawd 應用程式安裝器**，不是雪絨主題安裝器。若 Clawd 正在執行，請先關閉再安裝。通知預設關閉，安裝檔不包含任何使用者的 Discord／LINE Token。

完整通知設定請閱讀 [Discord／LINE 選配通知安裝指南](https://github.com/RoyalMilkteaMaster/clawd-on-desk/blob/agent/notifications-0.12.1/docs/guides/notifications.zh-TW.md)。

#### 選擇 B：官方 Clawd 0.12.0

- [開啟官方 v0.12.0 Release](https://github.com/rullerzhou-afk/clawd-on-desk/releases/tag/v0.12.0)
- [直接下載 Windows x64 安裝器](https://github.com/rullerzhou-afk/clawd-on-desk/releases/download/v0.12.0/Clawd-on-Desk-Setup-0.12.0-x64.exe)

官方版沒有上述個人化 Discord／LINE 通知頁，但可以正常安裝雪絨主題。

安裝完成後，先開啟一次 Clawd，確認程式可以正常執行。

### 第二步：安裝雪絨主題

#### 選擇 A：雪絨一鍵主題安裝器

<p align="left">
  <a href="https://github.com/RoyalMilkteaMaster/xuerong-clawd/releases/download/xuerong-theme-v2.4.1/Xuerong-HD-Theme-Installer.exe">
    <img src="assets/readme/windows-download-button.svg" width="180" alt="下載雪絨 HD 2.4.1 Windows 主題安裝器">
  </a>
</p>

直接下載：[`Xuerong-HD-Theme-Installer.exe`](https://github.com/RoyalMilkteaMaster/xuerong-clawd/releases/download/xuerong-theme-v2.4.1/Xuerong-HD-Theme-Installer.exe)

1. 關閉 Clawd。
2. 雙擊 `Xuerong-HD-Theme-Installer.exe`。
3. 看到「雪絨 HD 已加入 Clawd 主題清單」後，重新開啟 Clawd。
4. 選擇 `設定 → 主題 → 使用者主題 → 雪絨 HD`。

> 主題安裝器只會把雪絨放到目前 Windows 使用者的 Clawd 主題資料夾，不會修改 `app.asar`，也不需要系統管理員權限。

#### 選擇 B：使用 Clawd 的 ZIP 匯入功能

1. [下載 `Xuerong-HD-Clawd-Theme.zip`](https://github.com/RoyalMilkteaMaster/xuerong-clawd/releases/download/xuerong-theme-v2.4.1/Xuerong-HD-Clawd-Theme.zip)。
2. 不要解壓縮 ZIP。
3. 開啟 Clawd，選擇 `設定 → 主題 → 匯入 Clawd 主題套件（.zip）`。
4. 選擇下載的 ZIP，再切換至「雪絨 HD」。
5. 若角色沒有立即更新，請重新啟動 Clawd。

## 更新雪絨主題

- 使用 EXE 安裝：下載新版主題安裝器並重新執行，安裝器會先備份舊主題。
- 使用 ZIP 匯入：若 Clawd 顯示同名主題已存在，先移除舊的「雪絨 HD」，再匯入新版 ZIP。
- 所有雪絨版本：[GitHub Releases](https://github.com/RoyalMilkteaMaster/xuerong-clawd/releases)。

## 移除雪絨主題

在主題安裝器所在資料夾開啟 PowerShell：

```powershell
.\Xuerong-HD-Theme-Installer.exe /uninstall
```

也可以先關閉 Clawd，再刪除：

```text
%APPDATA%\clawd-on-desk\themes\xuerong-hd
```

## 相容性與系統需求

- 個人化 Clawd：Windows 10／11 x64。
- 官方 Clawd：雪絨 2.4.1 已針對官方 `0.12.0` 主題流程發佈。
- 主題 EXE：Windows、PowerShell 5.1 或更新版本。
- 主題 ZIP：可用於其他 Clawd 支援的平台。
- 主題安裝器只新增主題，不會加入 Discord／LINE 通知或其他核心功能。
- 本倉庫的舊版完整修改核心只適用於 Clawd `0.10.0`；不要用舊版 `-ForceUnsupported` 覆蓋 `0.12.x`。

## 安全與隱私

- 雪絨主題安裝器不會覆蓋工作紀錄、SSH、Agent、Telegram、Discord 或 LINE 設定。
- 個人化 Clawd 安裝檔不包含 Bot Token、LINE Channel Access Token、頻道 ID 或使用者 ID。
- 未簽署的 Windows 安裝器可能顯示 SmartScreen。若不想執行主題 EXE，可改用 ZIP 匯入。
- 雪絨主題的預設白名單設定位於 [settings/xuerong-defaults.json](settings/xuerong-defaults.json)。

## 版本來源

- 個人化 Clawd：[RoyalMilkteaMaster/clawd-on-desk](https://github.com/RoyalMilkteaMaster/clawd-on-desk)
- 個人化 Clawd Release：[`v0.12.1-notifications.10`](https://github.com/RoyalMilkteaMaster/clawd-on-desk/releases/tag/v0.12.1-notifications.10)
- 官方上游：[rullerzhou-afk/clawd-on-desk](https://github.com/rullerzhou-afk/clawd-on-desk)
- 雪絨主題：`2.4.1`
- 舊版完整修改核心：Clawd `0.10.0`、雪絨程式套件 `0.11.0`
- 舊版上游基準 commit：`9ccafb84680d7068baa35e2d91c0800f81c7b475`

原始上游繁中說明保留在 [docs/UPSTREAM-README.zh-TW.md](docs/UPSTREAM-README.zh-TW.md)。

## 開發與驗證

```powershell
npm ci
npm test
powershell -ExecutionPolicy Bypass -File .\scripts\validate-release.ps1
powershell -ExecutionPolicy Bypass -File .\installer\build-theme-installer.ps1
powershell -ExecutionPolicy Bypass -File .\installer\test-theme-installer.ps1
```

驗證紀錄請見 [docs/VALIDATION.md](docs/VALIDATION.md)。

## 授權

Clawd on Desk 與修改後程式碼使用 GNU AGPL-3.0，詳見 [LICENSE](LICENSE) 與 [NOTICE.md](NOTICE.md)。

雪絨角色與動畫素材使用獨立的個人非商業分享條款，詳見 [ASSET-LICENSE.md](ASSET-LICENSE.md)。
