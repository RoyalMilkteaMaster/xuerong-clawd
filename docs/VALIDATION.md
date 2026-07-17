# Validation record

## Runtime package

- Package: `release/windows-x64/app.asar`
- SHA-256: `90529611FF1E19DCF2D102B70E0D9038877C1DA223484E2DFD1C760803B46A36`
- Installed package hash matched the release artifact.
- Clawd on Desk restarted successfully after installation.
- Runtime monitoring resumed and continued processing Codex events.

## Focused regression suite

The focused suite covers Codex monitor input requests, state snapshots, Session HUD, IPC, free edge dragging, mini mode, hit rendering, visible margins, and work-area clamping.

Result during package preparation: 459 passed, 0 failed.

## Full upstream suite

The complete upstream test runner also contains environment-dependent tests for WMI access, command lookup, theme cache writes, sidecar package layout, and platform shells. Those unrelated tests were not used as the release gate in the restricted build environment.

## Theme QA

The repository retains the installed theme's contact sheets, animation previews, build metadata, and validation JSON under `themes/xuerong-hd/qa`.

