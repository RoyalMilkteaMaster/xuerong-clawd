# Xuerong — Catgirl Desktop Pet for Clawd on Desk

[繁體中文](README.md) · [简体中文](README.zh-CN.md) · [English](README.en.md) · [日本語](README.ja-JP.md) · [한국어](README.ko-KR.md)

Xuerong (雪絨) is a white ragdoll catgirl desktop companion. This repository provides the Xuerong HD theme, a one-click Windows theme installer, a Clawd-importable ZIP, and the corresponding source for the legacy fully patched runtime.

![Gentle snow blue](01-gentle-snow-blue.png)

![Playful wink](02-playful-wink.png)

![Bashful heart](03-bashful-heart.png)

![Xuerong animation overview](themes/xuerong-hd/qa/all-frames-v21.png)

## Current versions

| Item | Version | Purpose |
|---|---:|---|
| Personalized Clawd on Desk | `0.12.1-notifications.10` | Windows x64 build with Discord/LINE notifications and editable notification replies |
| Official Clawd on Desk | `0.12.0` | Official stable release |
| Xuerong HD theme | `2.4.1` | Current recommended theme release |
| Legacy Xuerong runtime package | `0.11.0` | Legacy full runtime based on Clawd `0.10.0`; kept for source and compatibility reference |

## Features

- Idle, working, sleeping, waking, grabbed, and other interactive animations.
- Dedicated chibi half-body animations for edge mode.
- Works with Clawd Session HUD, task status, and Codex context progress.
- The personalized Clawd build supports Discord/LINE completion notifications and editable nicknames and replies.
- One-click theme EXE, ZIP import, update, and uninstall paths.

## Easiest installation

Installation has two steps: install the Clawd on Desk application first, then install the Xuerong theme. The two EXE files serve different purposes.

### Step 1: Install Clawd on Desk

#### Option A: Personalized Clawd (Windows x64, recommended)

Version `0.12.1-notifications.10` adds:

- Discord bot completion notifications and a settings page.
- LINE Messaging API mobile notifications and a settings page.
- A Notification Replies page for editing the nickname and completion/interruption/permission/choice replies.
- A Discord/LINE optional notification setup and troubleshooting guide.

<p align="left">
  <a href="https://github.com/RoyalMilkteaMaster/clawd-on-desk/releases/download/v0.12.1-notifications.10/Clawd-on-Desk-Setup-0.12.1-notifications.10-x64.exe">
    <img src="assets/readme/windows-download-button.svg" width="180" alt="Download personalized Clawd on Desk 0.12.1-notifications.10 for Windows x64">
  </a>
</p>

Direct download: [`Clawd-on-Desk-Setup-0.12.1-notifications.10-x64.exe`](https://github.com/RoyalMilkteaMaster/clawd-on-desk/releases/download/v0.12.1-notifications.10/Clawd-on-Desk-Setup-0.12.1-notifications.10-x64.exe)

> This is the **Clawd application installer**, not the Xuerong theme installer. Close Clawd before installing. Notifications are disabled by default, and the installer contains no user's Discord or LINE tokens.

See the [Discord/LINE optional notification guide](https://github.com/RoyalMilkteaMaster/clawd-on-desk/blob/agent/notifications-0.12.1/docs/guides/notifications.zh-TW.md) for complete setup and troubleshooting instructions (Traditional Chinese).

#### Option B: Official Clawd 0.12.0

- [Open the official v0.12.0 release](https://github.com/rullerzhou-afk/clawd-on-desk/releases/tag/v0.12.0)
- [Download the Windows x64 installer](https://github.com/rullerzhou-afk/clawd-on-desk/releases/download/v0.12.0/Clawd-on-Desk-Setup-0.12.0-x64.exe)

The official build does not include the personalized Discord/LINE settings, but it can install and use the Xuerong theme normally.

Launch Clawd once after installation and confirm that it runs correctly.

### Step 2: Install the Xuerong theme

#### Option A: One-click Xuerong theme installer

<p align="left">
  <a href="https://github.com/RoyalMilkteaMaster/xuerong-clawd/releases/download/xuerong-theme-v2.4.1/Xuerong-HD-Theme-Installer.exe">
    <img src="assets/readme/windows-download-button.svg" width="180" alt="Download the Xuerong HD 2.4.1 Windows theme installer">
  </a>
</p>

Direct download: [`Xuerong-HD-Theme-Installer.exe`](https://github.com/RoyalMilkteaMaster/xuerong-clawd/releases/download/xuerong-theme-v2.4.1/Xuerong-HD-Theme-Installer.exe)

1. Close Clawd.
2. Double-click `Xuerong-HD-Theme-Installer.exe`.
3. When the installer reports that Xuerong HD was added to the Clawd theme list, reopen Clawd.
4. Select `Settings → Theme → User themes → Xuerong HD`.

> The theme installer only places Xuerong in the current Windows user's Clawd theme directory. It does not modify `app.asar` and does not require administrator privileges.

#### Option B: Import the ZIP with Clawd

1. [Download `Xuerong-HD-Clawd-Theme.zip`](https://github.com/RoyalMilkteaMaster/xuerong-clawd/releases/download/xuerong-theme-v2.4.1/Xuerong-HD-Clawd-Theme.zip).
2. Do not extract the ZIP.
3. Open Clawd and select `Settings → Theme → Import Clawd theme package (.zip)`.
4. Choose the downloaded ZIP, then select Xuerong HD.
5. Restart Clawd if the character does not update immediately.

## Updating Xuerong

- EXE installation: download and run the newer theme installer. It backs up the previous theme first.
- ZIP import: if Clawd reports that a theme with the same name already exists, remove the old Xuerong HD theme before importing the new ZIP.
- All releases: [GitHub Releases](https://github.com/RoyalMilkteaMaster/xuerong-clawd/releases).

## Removing Xuerong

Open PowerShell in the theme installer's directory:

```powershell
.\Xuerong-HD-Theme-Installer.exe /uninstall
```

Or close Clawd and delete:

```text
%APPDATA%\clawd-on-desk\themes\xuerong-hd
```

## Compatibility and requirements

- Personalized Clawd: Windows 10/11 x64.
- Official Clawd: Xuerong 2.4.1 was released for the official `0.12.0` theme workflow.
- Theme EXE: Windows with PowerShell 5.1 or later.
- Theme ZIP: usable on other platforms supported by Clawd.
- The theme installer only adds a theme; it does not add Discord/LINE notifications or other core features.
- The legacy fully patched runtime in this repository is only for Clawd `0.10.0`. Do not use the legacy `-ForceUnsupported` option on `0.12.x`.

## Security and privacy

- The Xuerong theme installer does not overwrite task history, SSH, Agent, Telegram, Discord, or LINE settings.
- The personalized Clawd installer contains no bot token, LINE Channel Access Token, channel ID, or user ID.
- Unsigned Windows installers may trigger SmartScreen. Use the ZIP import path if you prefer not to run the theme EXE.
- Xuerong's allowlisted default settings are in [settings/xuerong-defaults.json](settings/xuerong-defaults.json).

## Source and provenance

- Personalized Clawd: [RoyalMilkteaMaster/clawd-on-desk](https://github.com/RoyalMilkteaMaster/clawd-on-desk)
- Personalized release: [`v0.12.1-notifications.10`](https://github.com/RoyalMilkteaMaster/clawd-on-desk/releases/tag/v0.12.1-notifications.10)
- Official upstream: [rullerzhou-afk/clawd-on-desk](https://github.com/rullerzhou-afk/clawd-on-desk)
- Xuerong theme: `2.4.1`
- Legacy full runtime: Clawd `0.10.0`, Xuerong runtime package `0.11.0`
- Legacy upstream base commit: `9ccafb84680d7068baa35e2d91c0800f81c7b475`

The original upstream English README is retained at [docs/UPSTREAM-README.md](docs/UPSTREAM-README.md).

## Development and validation

```powershell
npm ci
npm test
powershell -ExecutionPolicy Bypass -File .\scripts\validate-release.ps1
powershell -ExecutionPolicy Bypass -File .\installer\build-theme-installer.ps1
powershell -ExecutionPolicy Bypass -File .\installer\test-theme-installer.ps1
```

See [docs/VALIDATION.md](docs/VALIDATION.md) for validation records.

## License

Clawd on Desk and the modified source code are licensed under GNU AGPL-3.0. See [LICENSE](LICENSE) and [NOTICE.md](NOTICE.md).

The Xuerong character and animation assets use separate personal, non-commercial sharing terms. See [ASSET-LICENSE.md](ASSET-LICENSE.md).
