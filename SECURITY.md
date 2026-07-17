# Security and privacy

## Public repository contents

This repository intentionally excludes Clawd preferences, session logs, Codex rollout logs, API credentials, remote SSH settings, Telegram configuration, session aliases, absolute user profile paths, and generated-image source rollouts.

## Installer behavior

The installer reads the existing Clawd preferences only to merge the documented whitelist in `settings/xuerong-defaults.json`. It creates a local backup before writing and does not transmit data.

The installer does not download dependencies, contact a remote service, or require administrator rights when Clawd on Desk is installed for the current Windows user.

## Reporting

Before reporting a problem, remove usernames, session identifiers, terminal commands, remote hostnames, and local paths from logs or screenshots.

