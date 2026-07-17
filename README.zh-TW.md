# 雪絨 — Clawd on Desk 貓娘桌面寵物

[English](README.md)

雪絨是一隻白色母布偶貓貓娘桌面寵物。這個倉庫包含完整對應原始碼、雪絨 2.1.3 主題、已測試的 Windows x64 執行套件、安全設定範本，以及可以復原的一鍵安裝腳本。

![雪絨動畫總覽](themes/xuerong-hd/qa/all-frames-v21.png)

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

- Windows 10／11 x64。
- 已安裝 Clawd on Desk 0.10.0。
- PowerShell 5.1 或更新版本。

安裝器只接受官方 0.10.0 x64 `app.asar`，或本倉庫已安裝過的版本。其他 Clawd 版本預設拒絕安裝，避免更新後硬套舊程式造成損壞。

## 安裝

下載並解壓縮 GitHub Release ZIP，在資料夾內開啟 PowerShell：

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
```

雪絨相關測試與已知環境限制記錄在 [docs/VALIDATION.md](docs/VALIDATION.md)。

## 授權

Clawd on Desk 與修改後程式碼使用 GNU AGPL-3.0，詳見 [LICENSE](LICENSE) 與 [NOTICE.md](NOTICE.md)。

雪絨角色與動畫素材使用獨立的個人非商業分享條款，詳見 [ASSET-LICENSE.md](ASSET-LICENSE.md)。

