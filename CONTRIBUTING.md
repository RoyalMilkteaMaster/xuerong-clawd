# Contributing

Thank you for helping improve Xuerong Clawd.

## Before opening a pull request

1. Keep changes compatible with the supported Clawd `0.10.0` base.
2. Do not commit personal paths, Codex session data, API keys, chat logs, or private references.
3. Keep Xuerong artwork changes separate from upstream code changes when practical.
4. Run the focused tests and release validator described in [`docs/VALIDATION.md`](docs/VALIDATION.md).
5. Explain visible animation or interaction changes and attach a short screen recording when useful.

## Code style

- Prefer small functions with descriptive names and early returns.
- Preserve existing behavior unless the change is intentional and tested.
- Add or update tests for interaction, state, IPC, and monitor changes.
- Do not add generated dependencies or local build caches to Git.

## Artwork

Code contributions follow [`LICENSE`](LICENSE). Xuerong artwork follows
[`ASSET-LICENSE.md`](ASSET-LICENSE.md). By contributing artwork, you confirm that you
have permission to submit it under those asset terms.

## Reporting security issues

Follow [`SECURITY.md`](SECURITY.md) instead of opening a public issue for a suspected
credential, privacy, or code-execution vulnerability.
