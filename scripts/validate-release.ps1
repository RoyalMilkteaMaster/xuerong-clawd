[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repositoryRoot = Split-Path -Parent $PSScriptRoot
$releaseRoot = Join-Path $repositoryRoot "release\windows-x64"
$themeRoot = Join-Path $repositoryRoot "themes\xuerong-hd"
$settingsPath = Join-Path $repositoryRoot "settings\xuerong-defaults.json"
$manifestPath = Join-Path $repositoryRoot "release\SHA256SUMS.txt"

function Require-File([string]$Path) {
  if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
    throw "Missing required file: $Path"
  }
}

function Assert-Equal([object]$Actual, [object]$Expected, [string]$Message) {
  if ($Actual -ne $Expected) {
    throw "$Message (expected=$Expected actual=$Actual)"
  }
}

$requiredFiles = @(
  (Join-Path $releaseRoot "app.asar"),
  (Join-Path $releaseRoot "app.asar.unpacked\agents\codex-log-monitor.js"),
  (Join-Path $releaseRoot "app.asar.unpacked\agents\codex-user-input.js"),
  (Join-Path $themeRoot "theme.json"),
  $settingsPath,
  $manifestPath,
  (Join-Path $repositoryRoot "LICENSE"),
  (Join-Path $repositoryRoot "ASSET-LICENSE.md"),
  (Join-Path $repositoryRoot "NOTICE-XUERONG.md")
)
foreach ($file in $requiredFiles) { Require-File $file }

$utf8 = New-Object System.Text.UTF8Encoding($false)
$package = [IO.File]::ReadAllText((Join-Path $repositoryRoot "package.json"), $utf8) | ConvertFrom-Json
Assert-Equal $package.version "0.10.0" "Unexpected upstream package version"

$theme = [IO.File]::ReadAllText((Join-Path $themeRoot "theme.json"), $utf8) | ConvertFrom-Json
Assert-Equal $theme.version "2.2.0" "Unexpected Xuerong theme version"
$expectedThemeName = ([char]0x96EA) + ([char]0x7D68) + " HD"
Assert-Equal $theme.name $expectedThemeName "Unexpected Xuerong theme name"

$themeJson = $theme | ConvertTo-Json -Depth 50
$assetReferences = [regex]::Matches($themeJson, '"([A-Za-z0-9][A-Za-z0-9._-]*\.(?:webp|png|gif|svg))"(?=\s*(?:,|\]|\}))', 'IgnoreCase') |
  ForEach-Object { $_.Groups[1].Value } |
  Sort-Object -Unique
foreach ($asset in $assetReferences) {
  Require-File (Join-Path $themeRoot "assets\$asset")
}

$allowedSettings = @(
  "theme", "size", "savedPixelWidth", "savedPixelHeight",
  "sessionHudEnabled", "sessionHudShowStateLabels", "sessionHudShowElapsed",
  "sessionHudShowContextUsage", "sessionHudCleanupDetached", "sessionHudPinned",
  "allowEdgePinning", "disableMiniMode", "keepSizeAcrossDisplays", "textScale",
  "soundMuted", "soundVolume", "keepAwakeWhileWorking", "lowPowerIdleMode"
)
$settings = [IO.File]::ReadAllText($settingsPath, $utf8) | ConvertFrom-Json
foreach ($property in $settings.PSObject.Properties) {
  if ($allowedSettings -notcontains $property.Name) {
    throw "Unsafe or undocumented setting in defaults: $($property.Name)"
  }
}
Assert-Equal $settings.theme "xuerong-hd" "Unexpected default theme"

foreach ($line in Get-Content -LiteralPath $manifestPath) {
  if ([string]::IsNullOrWhiteSpace($line)) { continue }
  if ($line -notmatch '^([A-Fa-f0-9]{64})  (.+)$') {
    throw "Invalid SHA256SUMS line: $line"
  }
  $expectedHash = $Matches[1].ToUpperInvariant()
  $relativePath = $Matches[2].Replace('/', [IO.Path]::DirectorySeparatorChar)
  $filePath = Join-Path $repositoryRoot $relativePath
  Require-File $filePath
  $actualHash = (Get-FileHash -LiteralPath $filePath -Algorithm SHA256).Hash
  Assert-Equal $actualHash $expectedHash "Hash mismatch for $relativePath"
}

$releaseAsarHash = (Get-FileHash -LiteralPath (Join-Path $releaseRoot "app.asar") -Algorithm SHA256).Hash
Assert-Equal $releaseAsarHash "90529611FF1E19DCF2D102B70E0D9038877C1DA223484E2DFD1C760803B46A36" "Unexpected release app.asar"

function Read-NormalizedText([string]$Path) {
  return [IO.File]::ReadAllText($Path, $utf8).Replace("`r`n", "`n").Replace("`r", "`n")
}

$sourceMonitor = Read-NormalizedText (Join-Path $repositoryRoot "agents\codex-log-monitor.js")
$releaseMonitor = Read-NormalizedText (Join-Path $releaseRoot "app.asar.unpacked\agents\codex-log-monitor.js")
Assert-Equal $releaseMonitor $sourceMonitor "Release Codex monitor does not match source"

$sourceInput = Read-NormalizedText (Join-Path $repositoryRoot "agents\codex-user-input.js")
$releaseInput = Read-NormalizedText (Join-Path $releaseRoot "app.asar.unpacked\agents\codex-user-input.js")
Assert-Equal $releaseInput $sourceInput "Release Codex input parser does not match source"

$generatedPathPattern = '\\(?:node_modules|build)\\'
$oversized = Get-ChildItem -LiteralPath $repositoryRoot -Recurse -File |
  Where-Object { $_.FullName -notmatch $generatedPathPattern -and $_.Length -ge 100MB }
if ($oversized) {
  throw "GitHub rejects files >=100 MB: $($oversized.FullName -join ', ')"
}

$secretPatterns = @(
  'C:\\Users\\leslie',
  ('019f6bdc-' + '7222-74d2-af4b-c37fd2fa2130'),
  '-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
  '(?:sk|ghp)_[A-Za-z0-9]{20,}'
)
$textExtensions = @('.js', '.json', '.md', '.ps1', '.yml', '.yaml', '.txt', '.html', '.css')
$textFiles = Get-ChildItem -LiteralPath $repositoryRoot -Recurse -File |
  Where-Object {
    $textExtensions -contains $_.Extension.ToLowerInvariant() -and
    $_.FullName -notmatch $generatedPathPattern -and
    $_.FullName -notmatch '\\docs\\UPSTREAM-README'
  }
$dummyGitHubTokenPattern = 'ghp_' + 'abcdefghijklmnopqrstuvwxyz[A-Za-z0-9]+'
foreach ($file in $textFiles) {
  $content = Get-Content -LiteralPath $file.FullName -Raw -ErrorAction SilentlyContinue
  $contentForSecretScan = $content -replace $dummyGitHubTokenPattern, ''
  foreach ($pattern in $secretPatterns) {
    if ($contentForSecretScan -match $pattern) {
      throw "Potential personal or secret value in $($file.FullName): $pattern"
    }
  }
}

Write-Host "Xuerong repository and release validation passed."
