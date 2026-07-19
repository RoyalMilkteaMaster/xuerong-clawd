[CmdletBinding()]
param(
  [string]$InstallerPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repositoryRoot = Split-Path -Parent $PSScriptRoot
if ([string]::IsNullOrWhiteSpace($InstallerPath)) {
  $InstallerPath = Join-Path $repositoryRoot "dist\Xuerong-HD-Theme-Installer.exe"
}
$InstallerPath = (Resolve-Path -LiteralPath $InstallerPath).Path
$testRoot = Join-Path $env:TEMP ("xuerong-theme-installer-test-" + [guid]::NewGuid().ToString("N"))
$themePath = Join-Path $testRoot "themes\xuerong-hd"
$env:XUERONG_THEME_INSTALL_ROOT = $testRoot

try {
  New-Item -ItemType Directory -Path $testRoot -Force | Out-Null

  $install = Start-Process -FilePath $InstallerPath -ArgumentList "/quiet" -WindowStyle Hidden -Wait -PassThru
  if ($install.ExitCode -ne 0) { throw "First install failed: $($install.ExitCode)" }
  if (-not (Test-Path -LiteralPath (Join-Path $themePath "theme.json") -PathType Leaf)) {
    throw "Installed theme.json is missing"
  }

  $update = Start-Process -FilePath $InstallerPath -ArgumentList "/quiet" -WindowStyle Hidden -Wait -PassThru
  if ($update.ExitCode -ne 0) { throw "Theme update failed: $($update.ExitCode)" }
  $backupRoot = Join-Path $testRoot "xuerong-theme-installer-backups"
  if (@(Get-ChildItem -LiteralPath $backupRoot -Directory).Count -ne 1) {
    throw "Theme update did not create exactly one backup"
  }

  $uninstall = Start-Process -FilePath $InstallerPath -ArgumentList "/uninstall", "/quiet" -WindowStyle Hidden -Wait -PassThru
  if ($uninstall.ExitCode -ne 0) { throw "Theme uninstall failed: $($uninstall.ExitCode)" }
  if (Test-Path -LiteralPath $themePath) { throw "Theme directory remains after uninstall" }

  Write-Host "Theme installer install/update/uninstall test passed."
} finally {
  Remove-Item Env:XUERONG_THEME_INSTALL_ROOT -ErrorAction SilentlyContinue
  if (Test-Path -LiteralPath $testRoot) {
    Remove-Item -LiteralPath $testRoot -Recurse -Force
  }
}
