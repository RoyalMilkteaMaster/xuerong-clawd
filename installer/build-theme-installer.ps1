[CmdletBinding()]
param(
  [string]$OutputDirectory
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repositoryRoot = Split-Path -Parent $PSScriptRoot
if ([string]::IsNullOrWhiteSpace($OutputDirectory)) {
  $OutputDirectory = Join-Path $repositoryRoot "dist"
}
$themeSource = Join-Path $repositoryRoot "themes\xuerong-hd"
$sourceFile = Join-Path $PSScriptRoot "theme-only\XuerongThemeInstaller.cs"
$compiler = Join-Path $env:WINDIR "Microsoft.NET\Framework64\v4.0.30319\csc.exe"
$stageRoot = Join-Path $env:TEMP ("xuerong-theme-build-" + [guid]::NewGuid().ToString("N"))
$themeStage = Join-Path $stageRoot "xuerong-hd"
$embeddedZip = Join-Path $stageRoot "XuerongTheme.zip"
$nativeZip = Join-Path $OutputDirectory "Xuerong-HD-Clawd-Theme.zip"
$installerExe = Join-Path $OutputDirectory "Xuerong-HD-Theme-Installer.exe"

function Require-File([string]$Path) {
  if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
    throw "Required file is missing: $Path"
  }
}

Require-File $compiler
Require-File $sourceFile
Require-File (Join-Path $themeSource "theme.json")
Require-File (Join-Path $themeSource "assets\idle.webp")

$null = Get-Content -LiteralPath (Join-Path $themeSource "theme.json") -Raw -Encoding UTF8 | ConvertFrom-Json
Add-Type -AssemblyName System.IO.Compression.FileSystem

try {
  New-Item -ItemType Directory -Path $themeStage -Force | Out-Null
  New-Item -ItemType Directory -Path $OutputDirectory -Force | Out-Null
  Copy-Item -LiteralPath (Join-Path $themeSource "theme.json") -Destination $themeStage -Force
  Copy-Item -LiteralPath (Join-Path $themeSource "assets") -Destination $themeStage -Recurse -Force

  Remove-Item -LiteralPath $embeddedZip, $nativeZip, $installerExe -Force -ErrorAction SilentlyContinue
  [IO.Compression.ZipFile]::CreateFromDirectory($stageRoot, $nativeZip, [IO.Compression.CompressionLevel]::Optimal, $false)
  [IO.Compression.ZipFile]::CreateFromDirectory($themeStage, $embeddedZip, [IO.Compression.CompressionLevel]::Optimal, $false)

  $compilerArguments = @(
    "/nologo",
    "/target:winexe",
    "/optimize+",
    "/platform:anycpu",
    "/out:$installerExe",
    "/resource:$embeddedZip,XuerongTheme.zip",
    "/reference:System.dll",
    "/reference:System.Core.dll",
    "/reference:System.Windows.Forms.dll",
    "/reference:System.IO.Compression.dll",
    "/reference:System.IO.Compression.FileSystem.dll",
    "/reference:System.Web.Extensions.dll",
    $sourceFile
  )
  & $compiler $compilerArguments
  if ($LASTEXITCODE -ne 0) {
    throw "C# compiler failed with exit code $LASTEXITCODE"
  }

  $hashes = @(
    Get-FileHash -LiteralPath $installerExe -Algorithm SHA256
    Get-FileHash -LiteralPath $nativeZip -Algorithm SHA256
  )
  $hashLines = $hashes | ForEach-Object { "$($_.Hash)  $([IO.Path]::GetFileName($_.Path))" }
  [IO.File]::WriteAllLines(
    (Join-Path $OutputDirectory "SHA256SUMS-theme-installer.txt"),
    $hashLines,
    (New-Object Text.UTF8Encoding($false))
  )

  Write-Host "Built: $installerExe"
  Write-Host "Built: $nativeZip"
} finally {
  Remove-Item -LiteralPath $stageRoot -Recurse -Force -ErrorAction SilentlyContinue
}
