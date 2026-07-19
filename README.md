# 雪絨 — Clawd on Desk 貓娘桌面寵物

[English](README.en.md)

雪絨是一隻白色母布偶貓貓娘桌面寵物。
這個倉庫包含完整對應原始碼、雪絨 2.1.3 主題、已測試的 Windows x64 執行套件、安全設定範本，以及可以復原的一鍵安裝腳本。

![溫柔雪藍](01-gentle-snow-blue.png)

![活潑眨眼](02-playful-wink.png)

![害羞愛心](03-bashful-heart.png)

![雪絨動畫總覽](themes/xuerong-hd/qa/all-frames-v21.png)

## 功能

- 一般待機、agent工作中、待機、起床、被抓...等互動動畫。
- 邊緣模式專用Q版半身動畫。
- 自由拖曳系統，放開時依最終位置智慧判斷是否進入邊緣模式。
- Session HUD 顯示工作位置、執行狀態與 Codex context 進度。
- 可串接LINE、DISCORD、TELEGRAM通知使用者專案完成、或AGENTS正在等待指示。
- 個性化回覆設定。
- 一鍵安裝、一鍵卸除功能。
  

# 最簡單安裝（已有Clawd 0.12.0 推薦）

若您已經擁有Clawd on desk(https://github.com/rullerzhou-afk/clawd-on-desk)， 只想要擴增雪絨主題。
那您只需從 [GitHub Releases](https://github.com/RoyalMilkteaMaster/xuerong-clawd/releases) 下載 `Xuerong-HD-Theme-Installer.exe`，雙擊一次即可。安裝器只會把雪絨放到目前 Windows 使用者的 Clawd 主題目錄，不會修改 `app.asar`，也不需要系統管理員權限。

執行成功後，重新開啟 Clawd，進入 `設定 → 主題`，在下方的使用者主題選擇「雪絨 HD」即可更換clawd on desk主題。
若後續版本有所更新，只需重新至(https://github.com/RoyalMilkteaMaster/xuerong-clawd/releases)下載exe，並重新執行一次該 EXE 即可以更新主題。

解除安裝可執行：

```powershell
.\Xuerong-HD-Theme-Installer.exe /uninstall
```

若您不想執行第三方 EXE ，可改下載 `Xuerong-HD-Clawd-Theme.zip`，在 Clawd `設定 → 主題 → 匯入 Clawd 主題套件（.zip）` 中選取它。
這條路徑使用 Clawd 0.12.0 自己的匯入器。

<p align="left">
  <a href="https://github.com/RoyalMilkteaMaster/xuerong-clawd/releases/download/xuerong-theme-v2.4.0/Xuerong-HD-Theme-Installer.exe">
    <img src="assets/readme/windows-download-button.svg" width="180" alt="Windows 一鍵下載雪絨安裝器">
  </a>
</p>


> Windows 可能因為安裝器沒有商業程式碼簽章而顯示 SmartScreen。可改用 ZIP 匯入，不需要略過任何安全警告。


# 從clawd on desk 開始簡單安裝（未有Clawd 0.12.0 推薦）


## 第一步：先安裝 Clawd on Desk

1. 前往 Clawd on Desk 官方 GitHub：

   👉 [開啟 Clawd on Desk 官方 GitHub](https://github.com/rullerzhou-afk/clawd-on-desk)

2. 進入官方的 Releases 頁面：

   👉 [下載 Clawd on Desk](https://github.com/rullerzhou-afk/clawd-on-desk/releases)

3. 下載適合你電腦的安裝檔。

   一般的 Windows 電腦通常使用：

   ```text
   Clawd-on-Desk-Setup-版本號-x64.exe
   ```

   Windows ARM 電腦才需要下載 ARM64 版本。

4. 雙擊安裝檔，完成 Clawd on Desk 安裝。

5. 安裝完成後，請先開啟一次 Clawd on Desk，確認它可以正常執行。

6. 確認 Clawd 可以正常執行後，再回到這個雪絨頁面繼續下一步。

---

## 第二步：安裝雪絨主題

你可以選擇「一鍵安裝器」或「ZIP 匯入」。

### 選擇 A：使用雪絨一鍵安裝器

1. 下載雪絨安裝器：

   👉 [下載 Xuerong-HD-Theme-Installer.exe](https://github.com/RoyalMilkteaMaster/xuerong-clawd/releases/download/xuerong-theme-v2.4.0/Xuerong-HD-Theme-Installer.exe)

2. 下載完成後，雙擊：

   ```text
   Xuerong-HD-Theme-Installer.exe
   ```

3. 看到「雪絨 HD 已加入 Clawd 主題清單」後，關閉並重新開啟 Clawd。

4. 在 Clawd 裡依序選擇：

   ```text
   設定 → 主題 → 使用者主題 → 雪絨 HD
   ```

5. 完成，雪絨就會出現在桌面上。

> [!NOTE]
> 這個安裝器只會把雪絨主題放到目前 Windows 使用者的 Clawd 主題資料夾。
>
> 它不會修改 `app.asar`，也不需要系統管理員權限。

### Windows 出現 SmartScreen 怎麼辦？

因為這個安裝器沒有購買商業程式碼簽章，Windows 可能會顯示 SmartScreen 提醒。

不想略過 SmartScreen 的話，請改用下面的 ZIP 匯入方式。

---

### 選擇 B：使用 Clawd 自己的 ZIP 匯入功能

這個方式不需要執行任何第三方 EXE。

1. 下載雪絨主題 ZIP：

   👉 [下載 Xuerong-HD-Clawd-Theme.zip](https://github.com/RoyalMilkteaMaster/xuerong-clawd/releases/download/xuerong-theme-v2.4.0/Xuerong-HD-Clawd-Theme.zip)

2. 不要解壓縮這個 ZIP。

3. 開啟 Clawd on Desk。

4. 依序選擇：

   ```text
   設定 → 主題 → 匯入 Clawd 主題套件（.zip）
   ```

5. 選擇剛才下載的：

   ```text
   Xuerong-HD-Clawd-Theme.zip
   ```

6. 匯入完成後，選擇：

   ```text
   雪絨 HD
   ```

7. 如果角色沒有立即更新，請關閉並重新開啟 Clawd。

---

## 更新雪絨主題

如果你是使用 EXE 安裝，只要下載新版安裝器並重新執行一次即可。

安裝器會先備份原本的雪絨主題，再安裝新版。

如果你是使用 ZIP 匯入，而且 Clawd 顯示同名主題已存在，請先移除舊的「雪絨 HD」，再匯入新版 ZIP。

---

## 移除一般主題版

在雪絨安裝器所在的資料夾開啟 PowerShell，執行：

```powershell
.\Xuerong-HD-Theme-Installer.exe /uninstall
```

也可以直接關閉 Clawd，然後刪除這個資料夾：

```text
%APPDATA%\clawd-on-desk\themes\xuerong-hd
```

## 系統需求

- 完整雪絨修改版功能：Windows 10／11 x64、Clawd on Desk 0.10.0 以上 、PowerShell 5.1 或更新版本。
ZIP 也可用於其他 Clawd 支援的平台。

## Clawd 0.12.0 相容性

| 功能 | 主題 EXE／ZIP 在官方 0.12.0 |
|---|---|
| 雪絨一般動畫、睡眠、被抓與互動 | 可用 |
| 左右邊緣專用雪絨動畫 | 可用 |
| Clawd 原生 Session HUD／進度資訊 | 可用，仍取決於 Agent 整合是否正常 |
| 從邊緣直接自由拖曳 X/Y、放開智慧判斷 | 不可用；這是雪絨修改版核心功能 |
| Codex `request_user_input` 的自訂 HUD 選項卡 | 不可用；這是雪絨修改版監視器功能 |
| 0.12.0 的新版 WSL、Remote Approval、Discord 等功能 | 保留，因為主題安裝器不修改核心 |

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
