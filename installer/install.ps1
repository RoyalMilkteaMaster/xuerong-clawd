[CmdletBinding()]
param(
  [string]$InstallDirectory = (Join-Path $env:LOCALAPPDATA "Programs\Clawd on Desk"),
  [switch]$ValidateOnly,
  [switch]$ForceUnsupported
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repositoryRoot = Split-Path -Parent $PSScriptRoot
$releaseRoot = Join-Path $repositoryRoot "release\windows-x64"
$themeSource = Join-Path $repositoryRoot "themes\xuerong-hd"
$settingsPath = Join-Path $repositoryRoot "settings\xuerong-defaults.json"
$hashManifest = Join-Path $repositoryRoot "release\SHA256SUMS.txt"
$resourcesDirectory = Join-Path $InstallDirectory "resources"
$executablePath = Join-Path $InstallDirectory "Clawd on Desk.exe"
$installedAsar = Join-Path $resourcesDirectory "app.asar"
$installedAgents = Join-Path $resourcesDirectory "app.asar.unpacked\agents"
$preferencesDirectory = Join-Path $env:APPDATA "clawd-on-desk"
$preferencesPath = Join-Path $preferencesDirectory "clawd-prefs.json"
$themesDirectory = Join-Path $preferencesDirectory "themes"
$themeDestination = Join-Path $themesDirectory "xuerong-hd"
$backupRoot = Join-Path $preferencesDirectory "xuerong-backups"

$supportedInputHashes = @(
  "D10BB79B221CBB5BE3319B0B65DB4CCA94E9913483A2F79AB388FF553C726FB5",
  "90529611FF1E19DCF2D102B70E0D9038877C1DA223484E2DFD1C760803B46A36"
)

function Require-File([string]$Path) {
  if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
    throw "Required file is missing: $Path"
  }
}

function Assert-ReleaseHashes {
  Require-File $hashManifest
  foreach ($line in Get-Content -LiteralPath $hashManifest) {
    if ([string]::IsNullOrWhiteSpace($line)) { continue }
    if ($line -notmatch '^([A-Fa-f0-9]{64})  (.+)$') {
      throw "Invalid SHA256SUMS line: $line"
    }
    $expectedHash = $Matches[1].ToUpperInvariant()
    $relativePath = $Matches[2].Replace('/', [IO.Path]::DirectorySeparatorChar)
    $filePath = Join-Path $repositoryRoot $relativePath
    Require-File $filePath
    $actualHash = (Get-FileHash -LiteralPath $filePath -Algorithm SHA256).Hash
    if ($actualHash -ne $expectedHash) {
      throw "Hash mismatch: $relativePath"
    }
  }
}

function Copy-DirectoryContents([string]$Source, [string]$Destination) {
  if (-not (Test-Path -LiteralPath $Destination)) {
    New-Item -ItemType Directory -Path $Destination -Force | Out-Null
  }
  Copy-Item -Path (Join-Path $Source '*') -Destination $Destination -Recurse -Force
}

Require-File $executablePath
Require-File $installedAsar
Require-File (Join-Path $releaseRoot "app.asar")
Require-File (Join-Path $releaseRoot "app.asar.unpacked\agents\codex-log-monitor.js")
Require-File (Join-Path $releaseRoot "app.asar.unpacked\agents\codex-user-input.js")
Require-File (Join-Path $themeSource "theme.json")
Require-File $settingsPath

Assert-ReleaseHashes
$utf8 = New-Object System.Text.UTF8Encoding($false)
$null = [IO.File]::ReadAllText((Join-Path $themeSource "theme.json"), $utf8) | ConvertFrom-Json
$defaults = [IO.File]::ReadAllText($settingsPath, $utf8) | ConvertFrom-Json

$installedHash = (Get-FileHash -LiteralPath $installedAsar -Algorithm SHA256).Hash
if (-not $ForceUnsupported -and $supportedInputHashes -notcontains $installedHash) {
  throw "Unsupported Clawd app.asar ($installedHash). Install Clawd on Desk 0.10.0 x64, or explicitly pass -ForceUnsupported after making a separate backup."
}

if ($ValidateOnly) {
  Write-Host "Validation passed. No files were changed."
  exit 0
}

$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$backupDirectory = Join-Path $backupRoot $timestamp
New-Item -ItemType Directory -Path $backupDirectory -Force | Out-Null

$installedMonitor = Join-Path $installedAgents "codex-log-monitor.js"
$installedUserInput = Join-Path $installedAgents "codex-user-input.js"
$hadMonitor = Test-Path -LiteralPath $installedMonitor -PathType Leaf
$hadUserInput = Test-Path -LiteralPath $installedUserInput -PathType Leaf
$hadPreferences = Test-Path -LiteralPath $preferencesPath -PathType Leaf
$hadTheme = Test-Path -LiteralPath $themeDestination -PathType Container

Copy-Item -LiteralPath $installedAsar -Destination (Join-Path $backupDirectory "app.asar") -Force
if ($hadMonitor) {
  Copy-Item -LiteralPath $installedMonitor -Destination (Join-Path $backupDirectory "codex-log-monitor.js") -Force
}
if ($hadUserInput) {
  Copy-Item -LiteralPath $installedUserInput -Destination (Join-Path $backupDirectory "codex-user-input.js") -Force
}
if ($hadPreferences) {
  Copy-Item -LiteralPath $preferencesPath -Destination (Join-Path $backupDirectory "clawd-prefs.json") -Force
}
if ($hadTheme) {
  Copy-Item -LiteralPath $themeDestination -Destination (Join-Path $backupDirectory "xuerong-hd") -Recurse -Force
}

$backupMetadata = [ordered]@{
  createdAt = (Get-Date).ToUniversalTime().ToString("o")
  installDirectory = $InstallDirectory
  inputAppAsarSha256 = $installedHash
  hadMonitor = $hadMonitor
  hadUserInputModule = $hadUserInput
  hadPreferences = $hadPreferences
  hadTheme = $hadTheme
}
$utf8NoBom = $utf8
[IO.File]::WriteAllText(
  (Join-Path $backupDirectory "backup.json"),
  ($backupMetadata | ConvertTo-Json -Depth 5),
  $utf8NoBom
)

try {
  Get-Process -Name "Clawd on Desk" -ErrorAction SilentlyContinue | Stop-Process -Force
  Start-Sleep -Milliseconds 900

  if (-not (Test-Path -LiteralPath $installedAgents)) {
    New-Item -ItemType Directory -Path $installedAgents -Force | Out-Null
  }
  Copy-Item -LiteralPath (Join-Path $releaseRoot "app.asar") -Destination $installedAsar -Force
  Copy-Item -LiteralPath (Join-Path $releaseRoot "app.asar.unpacked\agents\codex-log-monitor.js") -Destination $installedMonitor -Force
  Copy-Item -LiteralPath (Join-Path $releaseRoot "app.asar.unpacked\agents\codex-user-input.js") -Destination $installedUserInput -Force

  Copy-DirectoryContents $themeSource $themeDestination

  if (-not (Test-Path -LiteralPath $preferencesDirectory)) {
    New-Item -ItemType Directory -Path $preferencesDirectory -Force | Out-Null
  }
  $preferences = if ($hadPreferences) {
    [IO.File]::ReadAllText($preferencesPath, $utf8) | ConvertFrom-Json
  } else {
    [pscustomobject]@{}
  }
  foreach ($property in $defaults.PSObject.Properties) {
    $preferences | Add-Member -MemberType NoteProperty -Name $property.Name -Value $property.Value -Force
  }
  [IO.File]::WriteAllText(
    $preferencesPath,
    ($preferences | ConvertTo-Json -Depth 30),
    $utf8NoBom
  )

  $installedReleaseHash = (Get-FileHash -LiteralPath $installedAsar -Algorithm SHA256).Hash
  if ($installedReleaseHash -ne "90529611FF1E19DCF2D102B70E0D9038877C1DA223484E2DFD1C760803B46A36") {
    throw "Installed app.asar hash verification failed."
  }

  Start-Process -FilePath $executablePath -WindowStyle Hidden
  Write-Host "Xuerong 0.11.0 installed successfully."
  Write-Host "Backup: $backupDirectory"
} catch {
  if (Test-Path -LiteralPath $executablePath) {
    Start-Process -FilePath $executablePath -WindowStyle Hidden -ErrorAction SilentlyContinue
  }
  Write-Error "Installation failed. Original files are preserved in $backupDirectory. Run installer\restore.ps1 -BackupDirectory `"$backupDirectory`". $($_.Exception.Message)"
}
