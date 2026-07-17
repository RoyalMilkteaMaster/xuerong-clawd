[CmdletBinding()]
param(
  [string]$BackupDirectory,
  [string]$InstallDirectory = (Join-Path $env:LOCALAPPDATA "Programs\Clawd on Desk")
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$resourcesDirectory = Join-Path $InstallDirectory "resources"
$executablePath = Join-Path $InstallDirectory "Clawd on Desk.exe"
$installedAsar = Join-Path $resourcesDirectory "app.asar"
$installedAgents = Join-Path $resourcesDirectory "app.asar.unpacked\agents"
$preferencesDirectory = Join-Path $env:APPDATA "clawd-on-desk"
$preferencesPath = Join-Path $preferencesDirectory "clawd-prefs.json"
$themeDestination = Join-Path $preferencesDirectory "themes\xuerong-hd"
$backupRoot = Join-Path $preferencesDirectory "xuerong-backups"

if ([string]::IsNullOrWhiteSpace($BackupDirectory)) {
  $latest = Get-ChildItem -LiteralPath $backupRoot -Directory -ErrorAction SilentlyContinue |
    Where-Object { Test-Path -LiteralPath (Join-Path $_.FullName "backup.json") } |
    Sort-Object Name -Descending |
    Select-Object -First 1
  if ($null -eq $latest) {
    throw "No Xuerong backup was found under $backupRoot"
  }
  $BackupDirectory = $latest.FullName
}

$BackupDirectory = (Resolve-Path -LiteralPath $BackupDirectory).Path
$metadataPath = Join-Path $BackupDirectory "backup.json"
$backupAsar = Join-Path $BackupDirectory "app.asar"
if (-not (Test-Path -LiteralPath $metadataPath -PathType Leaf)) {
  throw "Invalid backup: backup.json is missing."
}
if (-not (Test-Path -LiteralPath $backupAsar -PathType Leaf)) {
  throw "Invalid backup: app.asar is missing."
}
if (-not (Test-Path -LiteralPath $executablePath -PathType Leaf)) {
  throw "Clawd on Desk executable is missing: $executablePath"
}

$utf8 = New-Object System.Text.UTF8Encoding($false)
$metadata = [IO.File]::ReadAllText($metadataPath, $utf8) | ConvertFrom-Json
$installedMonitor = Join-Path $installedAgents "codex-log-monitor.js"
$installedUserInput = Join-Path $installedAgents "codex-user-input.js"

Get-Process -Name "Clawd on Desk" -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Milliseconds 900

Copy-Item -LiteralPath $backupAsar -Destination $installedAsar -Force

if ($metadata.hadMonitor -eq $true) {
  Copy-Item -LiteralPath (Join-Path $BackupDirectory "codex-log-monitor.js") -Destination $installedMonitor -Force
} elseif (Test-Path -LiteralPath $installedMonitor) {
  Remove-Item -LiteralPath $installedMonitor -Force
}

if ($metadata.hadUserInputModule -eq $true) {
  Copy-Item -LiteralPath (Join-Path $BackupDirectory "codex-user-input.js") -Destination $installedUserInput -Force
} elseif (Test-Path -LiteralPath $installedUserInput) {
  Remove-Item -LiteralPath $installedUserInput -Force
}

if (Test-Path -LiteralPath $themeDestination) {
  Remove-Item -LiteralPath $themeDestination -Recurse -Force
}
if ($metadata.hadTheme -eq $true) {
  Copy-Item -LiteralPath (Join-Path $BackupDirectory "xuerong-hd") -Destination $themeDestination -Recurse -Force
}

if ($metadata.hadPreferences -eq $true) {
  Copy-Item -LiteralPath (Join-Path $BackupDirectory "clawd-prefs.json") -Destination $preferencesPath -Force
} elseif (Test-Path -LiteralPath $preferencesPath) {
  Remove-Item -LiteralPath $preferencesPath -Force
}

Start-Process -FilePath $executablePath -WindowStyle Hidden
Write-Host "Clawd on Desk was restored from: $BackupDirectory"
