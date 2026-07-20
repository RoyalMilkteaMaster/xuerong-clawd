# 설융(Xuerong) — Clawd on Desk 고양이 소녀 데스크톱 펫

[繁體中文](README.md) · [简体中文](README.zh-CN.md) · [English](README.en.md) · [日本語](README.ja-JP.md) · [한국어](README.ko-KR.md)

설융(雪絨, Xuerong)은 흰색 랙돌 고양이 소녀 데스크톱 컴패니언입니다. 이 저장소는 설융 HD 테마, Windows 원클릭 테마 설치 프로그램, Clawd에서 가져올 수 있는 ZIP, 그리고 이전 전체 패치 런타임의 대응 소스를 제공합니다.

![부드러운 스노 블루](01-gentle-snow-blue.png)

![장난스러운 윙크](02-playful-wink.png)

![수줍은 하트](03-bashful-heart.png)

![설융 애니메이션 전체 보기](themes/xuerong-hd/qa/all-frames-v21.png)

## 현재 버전

| 항목 | 버전 | 용도 |
|---|---:|---|
| 개인화 Clawd on Desk | `0.12.1-notifications.10` | Discord/LINE 알림 및 알림 답변 설정이 포함된 Windows x64 버전 |
| 공식 Clawd on Desk | `0.12.0` | 공식 안정 버전 |
| 설융 HD 테마 | `2.4.1` | 현재 권장 테마 버전 |
| 이전 설융 런타임 패키지 | `0.11.0` | Clawd `0.10.0` 기반의 이전 전체 패치 버전. 소스와 호환성 참고용 |

## 기능

- 대기, 작업 중, 수면, 기상, 잡힘 등 상호작용 애니메이션.
- 가장자리 모드 전용 치비 상반신 애니메이션.
- Clawd Session HUD, 작업 상태, Codex context 진행률 지원.
- 개인화 Clawd 버전에서 Discord/LINE 완료 알림과 닉네임 및 답변 편집 지원.
- 테마 EXE 원클릭 설치, ZIP 가져오기, 업데이트 및 제거 절차 제공.

## 가장 쉬운 설치 방법

설치는 두 단계입니다. 먼저 Clawd on Desk 앱을 설치한 뒤 설융 테마를 설치합니다. 두 EXE 파일은 용도가 다릅니다.

### 1단계: Clawd on Desk 설치

#### 선택 A: 개인화 Clawd (Windows x64, 권장)

현재 `0.12.1-notifications.10` 버전에는 다음 기능이 포함됩니다.

- Discord Bot 완료 알림과 설정 페이지.
- LINE Messaging API 모바일 알림과 설정 페이지.
- 닉네임 및 완료/중단/권한/선택 답변을 편집하는 알림 답변 페이지.
- Discord/LINE 선택 알림 설치 및 문제 해결 가이드.

<p align="left">
  <a href="https://github.com/RoyalMilkteaMaster/clawd-on-desk/releases/download/v0.12.1-notifications.10/Clawd-on-Desk-Setup-0.12.1-notifications.10-x64.exe">
    <img src="assets/readme/windows-download-button.svg" width="180" alt="개인화 Clawd on Desk 0.12.1-notifications.10 Windows x64 설치 프로그램 다운로드">
  </a>
</p>

직접 다운로드: [`Clawd-on-Desk-Setup-0.12.1-notifications.10-x64.exe`](https://github.com/RoyalMilkteaMaster/clawd-on-desk/releases/download/v0.12.1-notifications.10/Clawd-on-Desk-Setup-0.12.1-notifications.10-x64.exe)

> 이것은 **Clawd 앱 설치 프로그램**이며 설융 테마 설치 프로그램이 아닙니다. 설치 전에 Clawd를 종료하세요. 알림은 기본적으로 꺼져 있으며 설치 파일에는 사용자의 Discord/LINE Token이 포함되지 않습니다.

전체 설정은 [Discord/LINE 선택 알림 설치 가이드](https://github.com/RoyalMilkteaMaster/clawd-on-desk/blob/agent/notifications-0.12.1/docs/guides/notifications.zh-TW.md)(번체 중국어)를 참고하세요.

#### 선택 B: 공식 Clawd 0.12.0

- [공식 v0.12.0 Release 열기](https://github.com/rullerzhou-afk/clawd-on-desk/releases/tag/v0.12.0)
- [Windows x64 설치 프로그램 직접 다운로드](https://github.com/rullerzhou-afk/clawd-on-desk/releases/download/v0.12.0/Clawd-on-Desk-Setup-0.12.0-x64.exe)

공식 버전에는 위의 개인화 Discord/LINE 설정이 없지만 설융 테마는 정상적으로 설치하고 사용할 수 있습니다.

설치 후 Clawd를 한 번 실행하여 정상 동작을 확인하세요.

### 2단계: 설융 테마 설치

#### 선택 A: 설융 원클릭 테마 설치 프로그램

<p align="left">
  <a href="https://github.com/RoyalMilkteaMaster/xuerong-clawd/releases/download/xuerong-theme-v2.4.1/Xuerong-HD-Theme-Installer.exe">
    <img src="assets/readme/windows-download-button.svg" width="180" alt="설융 HD 2.4.1 Windows 테마 설치 프로그램 다운로드">
  </a>
</p>

직접 다운로드: [`Xuerong-HD-Theme-Installer.exe`](https://github.com/RoyalMilkteaMaster/xuerong-clawd/releases/download/xuerong-theme-v2.4.1/Xuerong-HD-Theme-Installer.exe)

1. Clawd를 종료합니다.
2. `Xuerong-HD-Theme-Installer.exe`를 더블클릭합니다.
3. “설융 HD가 Clawd 테마 목록에 추가되었습니다”라는 메시지가 나오면 Clawd를 다시 실행합니다.
4. `설정 → 테마 → 사용자 테마 → 설융 HD`를 선택합니다.

> 테마 설치 프로그램은 현재 Windows 사용자의 Clawd 테마 폴더에 설융만 추가합니다. `app.asar`를 수정하지 않으며 관리자 권한도 필요하지 않습니다.

#### 선택 B: Clawd ZIP 가져오기 사용

1. [`Xuerong-HD-Clawd-Theme.zip` 다운로드](https://github.com/RoyalMilkteaMaster/xuerong-clawd/releases/download/xuerong-theme-v2.4.1/Xuerong-HD-Clawd-Theme.zip).
2. ZIP 압축을 풀지 마세요.
3. Clawd에서 `설정 → 테마 → Clawd 테마 패키지(.zip) 가져오기`를 선택합니다.
4. 다운로드한 ZIP을 선택하고 “설융 HD”로 전환합니다.
5. 캐릭터가 바로 갱신되지 않으면 Clawd를 다시 시작합니다.

## 설융 테마 업데이트

- EXE 설치: 새 테마 설치 프로그램을 다운로드하여 다시 실행합니다. 이전 테마는 먼저 백업됩니다.
- ZIP 가져오기: 같은 이름의 테마가 이미 있다고 표시되면 기존 “설융 HD”를 제거한 뒤 새 ZIP을 가져옵니다.
- 모든 버전: [GitHub Releases](https://github.com/RoyalMilkteaMaster/xuerong-clawd/releases).

## 설융 테마 제거

테마 설치 프로그램이 있는 폴더에서 PowerShell을 엽니다.

```powershell
.\Xuerong-HD-Theme-Installer.exe /uninstall
```

또는 Clawd를 종료한 후 다음 폴더를 삭제합니다.

```text
%APPDATA%\clawd-on-desk\themes\xuerong-hd
```

## 호환성과 요구 사항

- 개인화 Clawd: Windows 10/11 x64.
- 공식 Clawd: 설융 2.4.1은 공식 `0.12.0` 테마 절차에 맞춰 배포되었습니다.
- 테마 EXE: Windows, PowerShell 5.1 이상.
- 테마 ZIP: Clawd가 지원하는 다른 플랫폼에서도 사용 가능.
- 테마 설치 프로그램은 테마만 추가하며 Discord/LINE 알림이나 다른 핵심 기능을 추가하지 않습니다.
- 이 저장소의 이전 전체 패치 런타임은 Clawd `0.10.0` 전용입니다. `0.12.x`에 이전 `-ForceUnsupported` 옵션을 사용하지 마세요.

## 보안과 개인정보

- 설융 테마 설치 프로그램은 작업 기록, SSH, Agent, Telegram, Discord 또는 LINE 설정을 덮어쓰지 않습니다.
- 개인화 Clawd 설치 파일에는 Bot Token, LINE Channel Access Token, 채널 ID 또는 사용자 ID가 포함되지 않습니다.
- 서명되지 않은 Windows 설치 프로그램은 SmartScreen을 표시할 수 있습니다. 테마 EXE를 실행하고 싶지 않다면 ZIP 가져오기를 사용하세요.
- 설융 테마의 허용 목록 기본 설정은 [settings/xuerong-defaults.json](settings/xuerong-defaults.json)에 있습니다.

## 버전과 출처

- 개인화 Clawd: [RoyalMilkteaMaster/clawd-on-desk](https://github.com/RoyalMilkteaMaster/clawd-on-desk)
- 개인화 Release: [`v0.12.1-notifications.10`](https://github.com/RoyalMilkteaMaster/clawd-on-desk/releases/tag/v0.12.1-notifications.10)
- 공식 upstream: [rullerzhou-afk/clawd-on-desk](https://github.com/rullerzhou-afk/clawd-on-desk)
- 설융 테마: `2.4.1`
- 이전 전체 패치 런타임: Clawd `0.10.0`, 설융 런타임 패키지 `0.11.0`
- 이전 upstream 기준 commit: `9ccafb84680d7068baa35e2d91c0800f81c7b475`

원래 upstream 영어 README는 [docs/UPSTREAM-README.md](docs/UPSTREAM-README.md)에 보관되어 있습니다.

## 개발과 검증

```powershell
npm ci
npm test
powershell -ExecutionPolicy Bypass -File .\scripts\validate-release.ps1
powershell -ExecutionPolicy Bypass -File .\installer\build-theme-installer.ps1
powershell -ExecutionPolicy Bypass -File .\installer\test-theme-installer.ps1
```

검증 기록은 [docs/VALIDATION.md](docs/VALIDATION.md)를 참고하세요.

## 라이선스

Clawd on Desk와 수정된 소스 코드는 GNU AGPL-3.0으로 배포됩니다. [LICENSE](LICENSE)와 [NOTICE.md](NOTICE.md)를 참고하세요.

설융 캐릭터와 애니메이션 자산에는 별도의 개인·비상업 공유 조건이 적용됩니다. [ASSET-LICENSE.md](ASSET-LICENSE.md)를 참고하세요.
