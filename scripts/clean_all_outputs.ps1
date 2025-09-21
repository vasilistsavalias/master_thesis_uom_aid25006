# ==============================================================================
# Clean All Project Artifacts (PowerShell)
# ==============================================================================
# This script will delete all generated outputs, including data, models, and logs.

$ErrorActionPreference = "Stop"

Write-Host "`n===================================================================="
Write-Host "Clean All Project Artifacts"
Write-Host "===================================================================="
Write-Host "This script will delete all generated outputs, including data,"
Write-Host "models, and logs." -ForegroundColor Yellow

$choice = Read-Host "`nAre you sure you want to continue? (Y/[N])"
if ($choice -ne 'Y' -and $choice -ne 'y') {
    Write-Host "Aborted."
    exit
}

# Get the project root (one level up from the script's directory)
$projectRoot = (Get-Item -Path ".\" -Verbose).Parent.FullName

# --- Deleting Logs ---
$logsPath = Join-Path $projectRoot "logs"
if (Test-Path $logsPath) {
    Write-Host "Deleting log files..."
    Remove-Item -Recurse -Force $logsPath
}

# --- Deleting Pipeline Outputs ---
Write-Host "Deleting pipeline stage outputs..."
Get-ChildItem -Path $projectRoot -Directory -Filter "0*" | ForEach-Object {
    $outputPath = Join-Path $_.FullName "output"
    if (Test-Path $outputPath) {
        Write-Host "Deleting output for $($_.Name)..."
        Remove-Item -Recurse -Force $outputPath
    }
}

Write-Host "`n===================================================================="
Write-Host "Project cleaning complete." -ForegroundColor Green
Write-Host "===================================================================="

Read-Host -Prompt "Press Enter to exit"
