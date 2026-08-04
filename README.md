# 雪絨 — Clawd on Desk 貓娘桌面寵物

[English](README.en.md)

雪絨是一隻白色布偶貓貓娘桌面寵物。
這個倉庫包含完整對應原始碼、雪絨 2.5.10 主題、已測試的 Windows x64 執行套件、安全設定範本，以及可以復原的一鍵安裝腳本。

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
  

# 最簡單安裝

## 第一步：先安裝 Clawd on Desk

1. 前往我的 Clawd on Desk 個人化 GitHub 或 Clawd on Desk 官方 GitHub：
   
   👉 [開啟 Clawd on Desk 個人化 GitHub](https://github.com/RoyalMilkteaMaster/clawd-on-desk/releases/tag/v0.12.1-notifications.12)
   
   👉 [開啟 Clawd on Desk 官方 GitHub](https://github.com/rullerzhou-afk/clawd-on-desk)

   > 我的個人化 Clawd on Desk 新增了:
    - Discord Bot 完成通知與設定頁。
    - LINE Messaging API 手機通知與設定頁。
    - 自訂「通知回應」修改頁面，可自行修改暱稱、以及完成／中斷／權限／選擇 回應。
    - Discord／LINE 選配通知安裝與除錯指南。
  
   建議安裝個人化 Clawd on Desk。下載 `Clawd-on-Desk-Setup-0.12.1-notifications.11-x64.exe`，雙擊一次即可。這個安裝器會安裝或升級 Clawd on Desk 個人化版本；雪絨主題請依照下方第二步另行安裝。

   若您已經安裝官方 Clawd on Desk，也可以直接下載 個人化 Clawd on Desk，該執行檔會直接添上上述擴充功能。

  3. 雙擊安裝檔，完成 Clawd on Desk 安裝。

  4. 安裝完成後，請先開啟一次 Clawd on Desk，確認它可以正常執行。

  5. 確認 Clawd 可以正常執行後，再回到這個雪絨頁面繼續下一步。

     
若您已經擁有官方版 Clawd on desk， 只想要擴增雪絨主題。
那您只需從此處
<p align="left">
  <a href="https://github.com/RoyalMilkteaMaster/xuerong-clawd/releases/latest/download/Xuerong-HD-Theme-Installer.exe">
    <img src="assets/readme/windows-download-button.svg" width="180" alt="Windows 一鍵下載雪絨安裝器">
  </a>
</p>
下載 `Xuerong-HD-Theme-Installer.exe`，雙擊一次即可。
安裝器只會把雪絨放到目前 Windows 使用者的 Clawd 主題目錄，不會修改 `app.asar`，也不需要系統管理員權限。

執行成功後，重新開啟 Clawd，進入 `設定 → 主題`，在下方的使用者主題選擇「雪絨 HD」即可更換clawd on desk主題。
若後續版本有所更新，只需重新至(https://github.com/RoyalMilkteaMaster/xuerong-clawd/releases)下載exe，並重新執行一次該 EXE 即可以更新主題。
> Windows 可能因為安裝器沒有商業程式碼簽章而顯示 SmartScreen。可改用 ZIP 匯入，不需要略過任何安全警告。

## 第二步：安裝雪絨主題

你可以選擇「一鍵安裝器」或「ZIP 匯入」。

### 選擇 A：使用雪絨一鍵安裝器

1. 下載雪絨安裝器：

<p align="left">
  <a href="https://github.com/RoyalMilkteaMaster/xuerong-clawd/releases/latest/download/Xuerong-HD-Theme-Installer.exe">
    <img src="assets/readme/windows-download-button.svg" width="180" alt="Windows 一鍵下載雪絨安裝器">
  </a>
</p>

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
> 因為這個安裝器沒有購買商業程式碼簽章，Windows 可能會顯示 SmartScreen 提醒。

### 選擇 B：使用 Clawd 自己的 ZIP 匯入功能

這個方式不需要執行任何第三方 EXE。

1. 下載雪絨主題 ZIP：

   👉 [下載 Xuerong-HD-Clawd-Theme.zip](https://github.com/RoyalMilkteaMaster/xuerong-clawd/releases/latest/download/Xuerong-HD-Clawd-Theme.zip)

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
- Clawd 版本：`Clawd 0.12.1-notifications.11
- 雪絨主題：`2.5.10`
- 雪絨程式套件：`0.11.0`

原始上游繁中說明保留在 [docs/UPSTREAM-README.zh-TW.md](docs/UPSTREAM-README.zh-TW.md)。

## 更新:開源自主開發桌面萌寵agents與skills

本倉庫公開包含 repo-local `xuerong-animation-studio` skill，以及動畫製作、程式化 QA、視覺 QA、發布整合共 4 個專職 Codex agents。
供想自行開發萌寵的使用者使用。
`xuerong-animation-studio` skill 包含:完整分工、GPU 排程、24／30 FPS限制、5% 角色誤差尺寸限制、紅綠白色版去背、首尾接縫與驗收。
規格請參閱 [雪絨動畫多 Agent 系統]
(docs/agent-system/XUERONG_ANIMATION_AGENTS.md)。


### 使用 Codex 製作自己的專屬萌寵

clone 本倉庫後，使用 Codex 開啟專案根目錄並建立一個新的任務：

將你想要的萌寵圖片置入codex聊天窗，下提示詞:
```text
使用 $xuerong-animation-studio 幫我新增或修改雪絨動畫。
使用 $xuerong-animation-studio 修改雪絨的 .webp，建立 job contract ，開始幫我生成桌寵動圖。
```
> 建議至少提供一張清楚、完整、沒有遮擋的正面全身圖；若有側面、背面、表情或服裝細節圖，也一起提供。
> 新角色必須使用獨立的 theme ID，例如 `my-cat`。
> 不要覆蓋 `themes/xuerong-hd`，也不要把雪絨圖片當作自己的角色素材重新發布。
> 雪絨素材的使用條件請參閱 [ASSET-LICENSE.md](ASSET-LICENSE.md)。

直接分批複製以下提示詞，分批生成動畫。
(一次完成所有動畫，品質會比較差，分批製作動畫效果會較好)

1.第一段提示詞只做規劃，不要立刻生成全部動畫：

```text
我要根據這個任務附上的參考圖片，製作一個新的 Clawd on Desk 動態寵物。

角色名稱：<角色名稱>
theme ID：<只用小寫英文、數字與連字號，例如 my-cat>
角色個性：<例如活潑、害羞、黏人>
一般模式：完整角色
邊緣模式：專用 Q 版半身角色

請把 xuerong-clawd 當作技術與檔案格式範例，但不要複製雪絨圖片，也不要修改 themes/xuerong-hd。

目前只做以下工作：
1. 讀取 AGENTS.md、themes/xuerong-hd/theme.json、狀態映射與動畫 QA 規格。
2. 檢查我的參考圖片是否足以保持角色一致性。
3. 列出新主題需要的全部一般、互動、睡眠與邊緣模式動畫。
4. 提出角色基準、畫布、尺寸、方向、24 或 30 FPS、動畫批次與驗收計畫。
5. 告訴我還缺哪些圖片或決定。

不要生成圖片、不要修改正式資產、不要安裝、不要 commit 或 push。
提出計畫後停下來等我確認。
```

2.確認計畫後，用第二段提示詞建立新角色自己的工作環境：

```text
我確認剛才的計畫。請為 <theme-id> 建立獨立的開發結構，但先不要製作動畫。

要求：
1. 建立 themes/<theme-id>/theme.json 與 assets 目錄，不修改 xuerong-hd。
2. 以現有 theme schema 為格式參考，換成新角色名稱、作者、版本與獨立檔名。
3. 從 xuerong-animation-studio 的流程建立 <theme-id>-animation-studio，但必須把雪絨專有名稱、路徑、髮色、服裝與動作描述全部替換成新角色規格。
4. 建立對應的 Builder、Deterministic QA、Visual QA、Release Integrator agents。
5. 設定候選輸出到 build/<theme-id>-animation-runs/，禁止直接生成到正式 assets。
6. 建立或更新 bundle validator，確認 skill、agents、theme ID 與所有必要路徑存在。
7. 顯示完整 diff、驗證結果與下一步；不要安裝、commit 或 push。
```

3.
工作環境通過驗證後，用第三段提示詞建立兩張角色基準：

```text
使用 $<theme-id>-animation-studio，根據我核准的參考圖片製作角色基準候選。

先只製作：
1. 一般模式 idle：512 x 512 RGBA 透明背景。
2. 邊緣模式 mini-idle：專為只露出半身設計，不是把一般模式直接縮小。

要求保持臉、眼睛、頭髮、耳朵、服裝、配件、色彩與比例一致。
請輸出透明、棋盤、深色與洋紅背景預覽，檢查白膜、破圖、游離碎片與透明邊緣。
先讓我核准兩張基準，再製作其他動畫；不要整合到正式 assets。
```

兩張基準核准後，再分批製作動畫。不要一次要求 Codex 生成全部動作：

```text
使用 $<theme-id>-animation-studio，依照已核准的 idle 與 mini-idle 基準製作第一批候選動畫。

本批動作：idle、working/typing、grabbed、poke-left、poke-right、double-love、annoyed。
輸出固定 24 FPS 或 30 FPS，增加幀數時保持原始總長度與節奏。
人物視覺尺寸相對同模式基準最多差 5%。
檢查重複幀、跳幀、忽快忽慢、鬼影、殘影、果凍感、局部扭曲、五官漂移、白膜與首尾接縫。
同一時間最多執行一個本機 GPU 工作；啟動前先檢查 GPU 是否正被其他專案使用。
每個動作完成後執行 Deterministic QA 與 Visual QA，提供完整預覽和逐項 PASS/FAIL。
不要整合失敗或尚未經我核准的候選動畫。
```

建議後續分成：

- 第二批：`yawning → dozing → collapsing → sleeping → waking → idle` 完整睡眠鏈。
- 第三批：`mini-enter`、`mini-idle`、`mini-peek`、`mini-working`、`mini-alert`、`mini-happy`、`mini-sleep` 與退出過場。
- 第四批：其他通知、錯誤、思考、行走與角色專屬動作。

> (一次完成所有動畫，品質會比較差，分批製作動畫效果會較好)



#### 驗證雪絨 Agent／Skill 套件

```powershell
python .\scripts\validate-xuerong-agent-bundle.py --project-root .
python .\scripts\validate-xuerong-v213-smooth.py --self-check
```

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
