# 雪絨（Xuerong）— Clawd on Desk 猫娘デスクトップペット

[繁體中文](README.md) · [简体中文](README.zh-CN.md) · [English](README.en.md) · [日本語](README.ja-JP.md) · [한국어](README.ko-KR.md)

雪絨（Xuerong）は白いラグドール猫の猫娘デスクトップコンパニオンです。このリポジトリでは、雪絨 HD テーマ、Windows 用ワンクリックテーマインストーラー、Clawd からインポートできる ZIP、および旧フル改造ランタイムの対応ソースを提供しています。

![優しいスノーブルー](01-gentle-snow-blue.png)

![元気なウインク](02-playful-wink.png)

![照れたハート](03-bashful-heart.png)

![雪絨アニメーション一覧](themes/xuerong-hd/qa/all-frames-v21.png)

## 現在のバージョン

| 項目 | バージョン | 用途 |
|---|---:|---|
| 個人向け Clawd on Desk | `0.12.1-notifications.10` | Discord／LINE 通知と通知返信設定を追加した Windows x64 版 |
| 公式 Clawd on Desk | `0.12.0` | 公式安定版 |
| 雪絨 HD テーマ | `2.4.1` | 現在推奨するテーマ版 |
| 旧雪絨ランタイムパッケージ | `0.11.0` | Clawd `0.10.0` ベースの旧フル改造版。ソースと互換性確認用 |

## 機能

- 待機、作業中、睡眠、起床、つかまれた状態などのインタラクティブアニメーション。
- エッジモード専用のちびキャラ上半身アニメーション。
- Clawd の Session HUD、タスク状態、Codex context 進捗に対応。
- 個人向け Clawd 版では Discord／LINE 完了通知と、ニックネーム・返信文の編集が可能。
- テーマ EXE、ZIP インポート、更新、削除手順を用意。

## 最も簡単なインストール

インストールは 2 段階です。先に Clawd on Desk アプリをインストールし、その後で雪絨テーマを追加します。2 つの EXE は用途が異なります。

### 手順 1：Clawd on Desk をインストール

#### 選択 A：個人向け Clawd（Windows x64、推奨）

現在の `0.12.1-notifications.10` には次の機能があります。

- Discord Bot の完了通知と設定ページ。
- LINE Messaging API のモバイル通知と設定ページ。
- ニックネームと完了／中断／権限／選択返信を編集できる「通知返信」ページ。
- Discord／LINE の任意通知セットアップ・トラブルシューティングガイド。

<p align="left">
  <a href="https://github.com/RoyalMilkteaMaster/clawd-on-desk/releases/download/v0.12.1-notifications.10/Clawd-on-Desk-Setup-0.12.1-notifications.10-x64.exe">
    <img src="assets/readme/windows-download-button.svg" width="180" alt="個人向け Clawd on Desk 0.12.1-notifications.10 Windows x64 インストーラーをダウンロード">
  </a>
</p>

直接ダウンロード：[`Clawd-on-Desk-Setup-0.12.1-notifications.10-x64.exe`](https://github.com/RoyalMilkteaMaster/clawd-on-desk/releases/download/v0.12.1-notifications.10/Clawd-on-Desk-Setup-0.12.1-notifications.10-x64.exe)

> これは **Clawd アプリのインストーラー**であり、雪絨テーマのインストーラーではありません。インストール前に Clawd を終了してください。通知は初期状態で無効であり、ユーザーの Discord／LINE Token は含まれません。

詳しい設定は [Discord／LINE 任意通知セットアップガイド](https://github.com/RoyalMilkteaMaster/clawd-on-desk/blob/agent/notifications-0.12.1/docs/guides/notifications.zh-TW.md)（繁体字中国語）を参照してください。

#### 選択 B：公式 Clawd 0.12.0

- [公式 v0.12.0 Release を開く](https://github.com/rullerzhou-afk/clawd-on-desk/releases/tag/v0.12.0)
- [Windows x64 インストーラーを直接ダウンロード](https://github.com/rullerzhou-afk/clawd-on-desk/releases/download/v0.12.0/Clawd-on-Desk-Setup-0.12.0-x64.exe)

公式版には上記の個人向け Discord／LINE 設定はありませんが、雪絨テーマは通常どおり利用できます。

インストール後に一度 Clawd を起動し、正常に動作することを確認してください。

### 手順 2：雪絨テーマをインストール

#### 選択 A：雪絨ワンクリックテーマインストーラー

<p align="left">
  <a href="https://github.com/RoyalMilkteaMaster/xuerong-clawd/releases/download/xuerong-theme-v2.4.1/Xuerong-HD-Theme-Installer.exe">
    <img src="assets/readme/windows-download-button.svg" width="180" alt="雪絨 HD 2.4.1 Windows テーマインストーラーをダウンロード">
  </a>
</p>

直接ダウンロード：[`Xuerong-HD-Theme-Installer.exe`](https://github.com/RoyalMilkteaMaster/xuerong-clawd/releases/download/xuerong-theme-v2.4.1/Xuerong-HD-Theme-Installer.exe)

1. Clawd を終了します。
2. `Xuerong-HD-Theme-Installer.exe` をダブルクリックします。
3. 「雪絨 HD が Clawd のテーマ一覧に追加されました」と表示されたら、Clawd を再起動します。
4. `設定 → テーマ → ユーザーテーマ → 雪絨 HD` を選択します。

> テーマインストーラーは、現在の Windows ユーザーの Clawd テーマフォルダーに雪絨を追加するだけです。`app.asar` を変更せず、管理者権限も不要です。

#### 選択 B：Clawd の ZIP インポートを使用

1. [`Xuerong-HD-Clawd-Theme.zip` をダウンロード](https://github.com/RoyalMilkteaMaster/xuerong-clawd/releases/download/xuerong-theme-v2.4.1/Xuerong-HD-Clawd-Theme.zip)します。
2. ZIP を展開しないでください。
3. Clawd を開き、`設定 → テーマ → Clawd テーマパッケージ（.zip）をインポート` を選択します。
4. ダウンロードした ZIP を選び、「雪絨 HD」に切り替えます。
5. キャラクターがすぐ更新されない場合は Clawd を再起動します。

## 雪絨テーマの更新

- EXE で導入した場合：新しいテーマインストーラーをダウンロードして再実行します。旧テーマは先にバックアップされます。
- ZIP で導入した場合：同名テーマが存在すると表示されたら、旧「雪絨 HD」を削除してから新しい ZIP をインポートします。
- すべてのリリース：[GitHub Releases](https://github.com/RoyalMilkteaMaster/xuerong-clawd/releases)。

## 雪絨テーマの削除

テーマインストーラーのあるフォルダーで PowerShell を開きます。

```powershell
.\Xuerong-HD-Theme-Installer.exe /uninstall
```

または Clawd を終了して、次のフォルダーを削除します。

```text
%APPDATA%\clawd-on-desk\themes\xuerong-hd
```

## 互換性と動作要件

- 個人向け Clawd：Windows 10／11 x64。
- 公式 Clawd：雪絨 2.4.1 は公式 `0.12.0` のテーマ手順向けにリリースされています。
- テーマ EXE：Windows、PowerShell 5.1 以降。
- テーマ ZIP：Clawd が対応する他のプラットフォームでも使用可能。
- テーマインストーラーはテーマだけを追加し、Discord／LINE 通知などのコア機能は追加しません。
- このリポジトリの旧フル改造ランタイムは Clawd `0.10.0` 専用です。`0.12.x` に旧 `-ForceUnsupported` を使わないでください。

## セキュリティとプライバシー

- 雪絨テーマインストーラーは、タスク履歴、SSH、Agent、Telegram、Discord、LINE 設定を上書きしません。
- 個人向け Clawd インストーラーには Bot Token、LINE Channel Access Token、チャンネル ID、ユーザー ID は含まれません。
- 署名されていない Windows インストーラーは SmartScreen を表示する場合があります。テーマ EXE を実行したくない場合は ZIP インポートを利用してください。
- 雪絨テーマの許可済み既定設定は [settings/xuerong-defaults.json](settings/xuerong-defaults.json) にあります。

## バージョンと由来

- 個人向け Clawd：[RoyalMilkteaMaster/clawd-on-desk](https://github.com/RoyalMilkteaMaster/clawd-on-desk)
- 個人向け Release：[`v0.12.1-notifications.10`](https://github.com/RoyalMilkteaMaster/clawd-on-desk/releases/tag/v0.12.1-notifications.10)
- 公式 upstream：[rullerzhou-afk/clawd-on-desk](https://github.com/rullerzhou-afk/clawd-on-desk)
- 雪絨テーマ：`2.4.1`
- 旧フル改造ランタイム：Clawd `0.10.0`、雪絨ランタイムパッケージ `0.11.0`
- 旧 upstream ベース commit：`9ccafb84680d7068baa35e2d91c0800f81c7b475`

元の upstream 英語 README は [docs/UPSTREAM-README.md](docs/UPSTREAM-README.md) に保存されています。

## 開発と検証

```powershell
npm ci
npm test
powershell -ExecutionPolicy Bypass -File .\scripts\validate-release.ps1
powershell -ExecutionPolicy Bypass -File .\installer\build-theme-installer.ps1
powershell -ExecutionPolicy Bypass -File .\installer\test-theme-installer.ps1
```

検証記録は [docs/VALIDATION.md](docs/VALIDATION.md) を参照してください。

## ライセンス

Clawd on Desk と変更後のソースコードは GNU AGPL-3.0 で提供されます。[LICENSE](LICENSE) と [NOTICE.md](NOTICE.md) を参照してください。

雪絨のキャラクターおよびアニメーション素材には、個人・非商用向けの別ライセンスが適用されます。[ASSET-LICENSE.md](ASSET-LICENSE.md) を参照してください。
