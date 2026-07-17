# Xuerong for Clawd on Desk

[繁體中文](README.zh-TW.md)

Xuerong (雪絨) is a white ragdoll catgirl desktop companion for the Windows build of Clawd on Desk 0.10.0. This repository contains the complete corresponding source, the Xuerong 2.1.3 theme, a tested Windows x64 runtime patch, safe preference defaults, and reversible installation scripts.

![Xuerong animation contact sheet](themes/xuerong-hd/qa/all-frames-v21.png)

## Features

- Full Xuerong animation set, including idle, work, typing, sleep, wake, grab, and reactions.
- Dedicated left/right edge-mode animation rather than a scaled full-body pose.
- Free two-axis dragging from edge mode and smart edge-mode selection on release.
- Up to 50% of the visible character may cross an outer screen edge.
- Clawd-style Session HUD with current work location, state, and context progress.
- Codex `request_user_input` questions appear as HUD option cards.
- Clicking an option copies its label and opens Codex; Codex remains responsible for final submission.
- Existing Clawd installation and preferences are backed up before installation.

## Requirements

- Windows 10 or Windows 11, x64.
- Clawd on Desk 0.10.0 installed in the current Windows user account.
- PowerShell 5.1 or later.

The installer accepts the official 0.10.0 x64 `app.asar` and this repository's already-patched build. Other Clawd versions are rejected unless the user explicitly passes `-ForceUnsupported`.

## Install

Download and extract the release ZIP, open PowerShell in the extracted folder, then run:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\installer\install.ps1
```

Validation without changing the computer:

```powershell
.\installer\install.ps1 -ValidateOnly
```

Restore the most recent pre-install backup:

```powershell
.\installer\restore.ps1
```

The backup is stored under `%APPDATA%\clawd-on-desk\xuerong-backups`.

## Safe settings

The installer merges only the keys in [settings/xuerong-defaults.json](settings/xuerong-defaults.json). It does not replace session aliases, remote SSH settings, Telegram settings, agent configuration, hardware settings, or work history.

## Source and provenance

- Upstream: [rullerzhou-afk/clawd-on-desk](https://github.com/rullerzhou-afk/clawd-on-desk)
- Upstream base commit: `9ccafb84680d7068baa35e2d91c0800f81c7b475`
- Upstream application version: `0.10.0`
- Xuerong theme version: `2.1.3`
- Xuerong runtime package version: `0.11.0`

The original upstream documentation is retained in [docs/UPSTREAM-README.md](docs/UPSTREAM-README.md).

## Development and validation

```powershell
npm ci
npm test
powershell -ExecutionPolicy Bypass -File .\scripts\validate-release.ps1
```

The focused Xuerong regression suite is documented in [docs/VALIDATION.md](docs/VALIDATION.md).

## License

Clawd on Desk and the modified source are distributed under the GNU Affero General Public License v3.0. See [LICENSE](LICENSE) and [NOTICE.md](NOTICE.md).

Xuerong character art and animation assets use the separate personal, non-commercial grant in [ASSET-LICENSE.md](ASSET-LICENSE.md).

