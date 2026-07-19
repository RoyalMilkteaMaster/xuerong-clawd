# 雪絨 — Clawd on Desk 貓娘桌面寵物

<p align="center">
  <a href="https://github.com/RoyalMilkteaMaster/xuerong-clawd/releases/download/xuerong-theme-v2.1.3/Xuerong-HD-Theme-Installer.exe">
    <img src="assets/readme/windows-download-button.svg" width="760" alt="Windows 一鍵下載雪絨安裝器">
  </a>
</p>

[English](README.en.md)

雪絨是一隻白色母布偶貓貓娘桌面寵物。這個倉庫包含完整對應原始碼、雪絨 2.1.3 主題、已測試的 Windows x64 執行套件、安全設定範本，以及可以復原的一鍵安裝腳本。

## LINE 頭像

### 1．溫柔雪藍

![溫柔雪藍](01-gentle-snow-blue.png)

### 2．活潑眨眼

![活潑眨眼](02-playful-wink.png)

### 3．害羞愛心

![害羞愛心](03-bashful-heart.png)

![雪絨動畫總覽](themes/xuerong-hd/qa/all-frames-v21.png)

## 最簡單安裝（Clawd 0.12.0 推薦）

從 [GitHub Releases](https://github.com/RoyalMilkteaMaster/xuerong-clawd/releases) 下載 `Xuerong-HD-Theme-Installer.exe`，雙擊一次即可。安裝器只會把雪絨放到目前 Windows 使用者的 Clawd 主題目錄，不會修改 `app.asar`，也不需要系統管理員權限。

安裝後重新開啟 Clawd，進入 `設定 → 主題`，在下方的使用者主題選擇「雪絨 HD」。重複執行同一個 EXE 可以更新主題；解除安裝可執行：

```powershell
.\Xuerong-HD-Theme-Installer.exe /uninstall
```

不想執行第三方 EXE 時，可改下載 `Xuerong-HD-Clawd-Theme.zip`，在 Clawd `設定 → 主題 → 匯入 Clawd 主題套件（.zip）` 中選取它。這條路徑使用 Clawd 0.12.0 自己的匯入器。

> Windows 可能因為安裝器沒有商業程式碼簽章而顯示 SmartScreen。可改用 ZIP 匯入，不需要略過任何安全警告。

## 功能

- 一般待機、工作、打電腦、睡眠、起床、被抓與互動動畫。
- 左右螢幕邊緣使用專用半身動畫，不是直接縮小一般角色。
- 邊緣模式可直接自由拖曳 X/Y，放開時依最終位置智慧判斷是否進入邊緣模式。
- 一般拖曳可讓角色可見寬度最多約 50% 超出螢幕，不會被透明圖片邊框堵住。
- Session HUD 顯示工作位置、執行狀態與 Codex context 進度。
- Codex 發出 `request_user_input` 時，HUD 會顯示問題與選項。
- 點選 HUD 選項會複製文字並開啟 Codex；最後送出仍由使用者在 Codex 確認。
- 安裝前自動備份原本 Clawd 與偏好設定。

## 系統需求

- 單純安裝雪絨主題：Windows 10／11 與 Clawd on Desk 0.12.0；ZIP 也可用於其他 Clawd 支援的平台。
- 完整雪絨修改版功能：Windows 10／11 x64、Clawd on Desk 0.10.0、PowerShell 5.1 或更新版本。

舊的完整功能安裝器只接受官方 0.10.0 x64 `app.asar`，或本倉庫已安裝過的版本。不要在 0.12.0 使用 `-ForceUnsupported`：它會以舊核心覆蓋 0.12.0，而不是把功能安全地合併進新版。

## Clawd 0.12.0 相容性

| 功能 | 主題 EXE／ZIP 在官方 0.12.0 |
|---|---|
| 雪絨一般動畫、睡眠、被抓與互動 | 可用 |
| 左右邊緣專用雪絨動畫 | 可用 |
| Clawd 原生 Session HUD／進度資訊 | 可用，仍取決於 Agent 整合是否正常 |
| 從邊緣直接自由拖曳 X/Y、放開智慧判斷 | 不可用；這是雪絨修改版核心功能 |
| Codex `request_user_input` 的自訂 HUD 選項卡 | 不可用；這是雪絨修改版監視器功能 |
| 0.12.0 的新版 WSL、Remote Approval、Discord 等功能 | 保留，因為主題安裝器不修改核心 |

雪絨主題已通過 Clawd 0.12.0 的官方 `validate-theme.js` 與 ZIP 匯入器驗證。若要同時保留 0.12.0 新功能和全部雪絨特殊互動，需要另外把修改移植到 0.12.0 核心；本次主題安裝器不做這件事。

## 完整修改版安裝（僅限 Clawd 0.10.0）

以下是只提供給需要完整雪絨修改版功能、且仍使用 Clawd 0.10.0 的舊安裝方式。下載並解壓縮 GitHub Release ZIP，在資料夾內開啟 PowerShell：

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\installer\install.ps1
```

只檢查、不修改電腦：

```powershell
.\installer\install.ps1 -ValidateOnly
```

復原到最近一次安裝前狀態：

```powershell
.\installer\restore.ps1
```

備份會放在 `%APPDATA%\clawd-on-desk\xuerong-backups`。

## 安全設定

安裝器只合併 [settings/xuerong-defaults.json](settings/xuerong-defaults.json) 內的白名單設定，不會複製或覆蓋：

- Codex／Clawd 工作紀錄
- 工作階段別名
- 遠端 SSH 設定
- Telegram 設定
- Agent 私人設定
- Hardware Buddy 設定

## 版本來源

- 上游：[rullerzhou-afk/clawd-on-desk](https://github.com/rullerzhou-afk/clawd-on-desk)
- 上游基準 commit：`9ccafb84680d7068baa35e2d91c0800f81c7b475`
- Clawd 版本：`0.10.0`
- 雪絨主題：`2.1.3`
- 雪絨程式套件：`0.11.0`

原始上游繁中說明保留在 [docs/UPSTREAM-README.zh-TW.md](docs/UPSTREAM-README.zh-TW.md)。

## 開發與驗證

```powershell
npm ci
npm test
powershell -ExecutionPolicy Bypass -File .\scripts\validate-release.ps1
powershell -ExecutionPolicy Bypass -File .\installer\build-theme-installer.ps1
powershell -ExecutionPolicy Bypass -File .\installer\test-theme-installer.ps1
```

雪絨相關測試與已知環境限制記錄在 [docs/VALIDATION.md](docs/VALIDATION.md)。

## 授權

Clawd on Desk 與修改後程式碼使用 GNU AGPL-3.0，詳見 [LICENSE](LICENSE) 與 [NOTICE.md](NOTICE.md)。

雪絨角色與動畫素材使用獨立的個人非商業分享條款，詳見 [ASSET-LICENSE.md](ASSET-LICENSE.md)。
