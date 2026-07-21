# Agent 分工、合約與交接

## Root Agent

Root Agent 是唯一總控：建立 job contract、指定檔案擁有者、控制 GPU 排程、檢查所有報告、向使用者取得核准，並決定是否交給整合 Agent。Root 不接受子 Agent 只說「完成」而沒有產物與驗證證據。

## Job contract

每個 run 建立 `build/xuerong-animation-runs/<run-id>/job.json`：

```json
{
  "runId": "20260721-typing-seam",
  "status": "PLANNED",
  "animation": "typing.webp",
  "mode": "normal",
  "screenSide": "none",
  "sourceState": "working",
  "targetState": "working",
  "loopMode": "loop",
  "targetFps": 30,
  "preserveDuration": true,
  "durationMs": 2000,
  "identityBaseline": "themes/xuerong-hd/assets/idle.webp",
  "motionBaseline": "themes/xuerong-hd/assets/typing.webp",
  "startAnchor": "themes/xuerong-hd/assets/typing.webp#frame=0",
  "endAnchor": "themes/xuerong-hd/assets/typing.webp#frame=0",
  "maxScaleDelta": 0.05,
  "gpuRequired": true,
  "candidate": null,
  "qaReport": null,
  "visualReport": null,
  "userApproved": false
}
```

允許的狀態：

```text
PLANNED
GENERATING
DETERMINISTIC_QA
VISUAL_QA
NEEDS_REPAIR
AWAITING_USER
APPROVED
INTEGRATED
FAILED
```

## Agent ownership

| Agent | 可寫入 | 不可寫入 |
|---|---|---|
| `xuerong_animation_builder` | 自己 run 下的 candidate、work、build report | 正式 theme assets、theme.json、release、Git |
| `xuerong_deterministic_qa` | 自己 run 下的 qa report、contact sheets、preview | candidate 像素、正式資產、theme.json |
| `xuerong_visual_quality_reviewer` | 無，唯讀回報 | 所有檔案 |
| `xuerong_release_integrator` | 使用者核准後的正式資產、必要 theme/config、安裝與發佈產物 | 未核准 candidate、無關程式碼 |

共享檔案一律只有一位 primary writer。若合約、`theme.json` 或 run manifest 需要改動，交回 Root 或明確轉移擁有權。

## GPU 規則

- 同一時間最多一個本機 GPU 生成或補幀工作。
- 啟動前檢查目前 GPU 使用率與記憶體；其他專案正在重載時等待，不硬搶資源。
- Agent 等待 GPU 時可以讀檔、準備合約或做 CPU QA，但不能啟動第二個 GPU 工作。
- 不用多 Agent 把同一個連續動作拆成數段補幀；這會製造接縫與身份漂移。

## 交接格式

每次 Agent 回報都使用：

```markdown
## Producer
## Job / animation
## Frozen inputs
## Produced outputs
## Files written
## Commands and exit codes
## Contract checks
## Failed frames or warnings
## Known limitations
## Next owner and next action
```

## Root 驗收

Root 依序檢查：

1. 候選檔與報告路徑存在。
2. 實際 diff 沒有越權修改。
3. 數值 QA 是新跑的，不是沿用舊報告。
4. 視覺 QA 使用完整動畫與四種背景。
5. 使用者看到完整預覽並明確核准。
6. 整合後再次驗證正式目錄。

只有第 1 至 6 項都通過才能標記 `INTEGRATED`。commit、push、tag、安裝與 release 各自需要使用者明確要求。
