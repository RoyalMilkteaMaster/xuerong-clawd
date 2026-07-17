# Xuerong Clawd v0.11.0

This is the first shareable Xuerong Clawd package, based on Clawd on Desk `0.10.0`.

## Highlights

- Xuerong HD theme `2.1.3` with consistent character scale and smoother state changes.
- Dedicated left/right mini edge animations with automatic mirroring.
- Free dragging from mini mode, including vertical-first drags and automatic edge-mode selection at release.
- Up to half of the visible pet can be dragged beyond the left or right screen edge.
- Work-state HUD with session status and context progress.
- Codex pending-choice cards and terminal-focus integration.
- Sleep entry, stable closed-eye sleep, occasional peek, and restored wake animation.
- Installer with SHA-256 verification, automatic backup, settings whitelist, and restore script.

## Supported base

- Windows x64
- Clawd on Desk `0.10.0`
- Official base `app.asar` SHA-256:
  `D10BB79B221CBB5BE3319B0B65DB4CCA94E9913483A2F79AB388FF553C726FB5`

The installer also recognizes this release's already-patched hash, so reinstalling the
same release is safe. Other bases require the explicit `-ForceUnsupported` switch and
are not guaranteed to work.

## Validation

- Focused Node tests: `459 passed, 0 failed`
- PowerShell 5.1 parser checks: passed
- Installer `-ValidateOnly`: passed
- Release hashes, theme assets, source/runtime parity, GitHub file-size limit, and
  personal/secret-value scan: passed

See [`docs/VALIDATION.md`](../docs/VALIDATION.md) for reproducible commands.

## Licensing

- Program source: [`LICENSE`](../LICENSE) (AGPL-3.0, inherited from upstream)
- Xuerong character artwork: [`ASSET-LICENSE.md`](../ASSET-LICENSE.md)
- Attribution and provenance: [`NOTICE-XUERONG.md`](../NOTICE-XUERONG.md)
