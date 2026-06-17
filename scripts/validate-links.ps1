$ErrorActionPreference = "Stop"
$root = Split-Path $PSScriptRoot -Parent
$markdown = Get-ChildItem -Path $root -Recurse -Filter *.md

foreach ($file in $markdown) {
  $content = Get-Content -Raw -Path $file.FullName
  $localLinks = [regex]::Matches($content, '\[[^\]]+\]\((?!https?://|#)([^)]+)\)')
  foreach ($link in $localLinks) {
    $target = $link.Groups[1].Value.Split("#")[0]
    if (-not $target) { continue }
    $resolved = Join-Path $file.DirectoryName $target
    if (-not (Test-Path $resolved)) {
      throw "Broken local link in $($file.FullName): $target"
    }
  }

  $urls = [regex]::Matches($content, '\[[^\]]+\]\((https?://[^)]+)\)')
  foreach ($url in $urls) {
    [void][System.Uri]$url.Groups[1].Value
  }
}

Write-Host "Link validation passed."
