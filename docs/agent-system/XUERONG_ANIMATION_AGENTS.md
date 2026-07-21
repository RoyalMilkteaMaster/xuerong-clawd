# 雪絨動畫多 Agent 系統

這套 repo-local 配置沿用 AIPE03 Godzilla Codex Integration 的分層格式：

```text
AGENTS.md
├─ .codex/agents/*.toml          專職 Agent 與寫入權限
├─ .agents/skills/*/SKILL.md     可重用的總控流程
├─ .agents/skills/*/references/  動畫硬規格、狀態配方、交接合約
└─ scripts/validate-xuerong-agent-bundle.py
```

## 角色

| Agent | 責任 | 寫入範圍 |
|---|---|---|
| Root Agent | 合約、排程、檔案擁有權、使用者核准、最終決策 | 由目前任務決定 |
| `xuerong_animation_builder` | 製作單一完整候選動作 | 指定 run 的 candidate/work |
| `xuerong_deterministic_qa` | 幀率、時長、尺寸、透明、接縫與接觸表 | 指定 run 的 qa |
| `xuerong_visual_quality_reviewer` | 獨立完整動畫與轉場視覺檢查 | 唯讀 |
| `xuerong_release_integrator` | 核准後整合、安裝與發佈 | 正式資產與要求的發佈檔 |

## 執行順序

```text
使用者確認動作
→ Root 凍結基準與 job contract
→ Builder 只產候選檔
→ Deterministic QA
→ Visual QA
→ 使用者看完整預覽並核准
→ Integrator 整合
→ 從正式路徑重新驗證
```

## 並行界線

- 可以並行：不同 run 的獨立動畫、已完成候選的 CPU QA、唯讀視覺檢查。
- 不可並行：兩個本機 GPU 補幀工作、多人修改同一 WebP、把同一睡眠鏈拆給多個 Builder、QA 讀取仍在寫入的候選檔。
- 每個共享檔案只有一位 primary writer。

## 啟用

Codex 需在新的任務中重新載入 repo-local `AGENTS.md`、`.codex/agents` 與 `.agents/skills`。如果需要四個工作槽，可把 `.codex/config.toml.example` 的 `[agents]` 區段合併到個人或專案 Codex 設定；不要覆蓋既有設定。
