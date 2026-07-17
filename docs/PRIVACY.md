# Preference sanitization

Only the following preference keys are distributed:

- theme and display size
- Session HUD visibility and presentation
- edge-mode enablement
- text scale
- local sound and power-behavior toggles

The following categories are deliberately excluded:

- `sessionAliases`
- `remoteSsh`
- `tgApproval` and `tgMigration`
- `agents`
- `hardwareBuddy`
- window coordinates and display identifiers
- update state
- all logs and Codex rollout files

The installer merges the whitelist into the recipient's existing preferences instead of replacing the complete file.

