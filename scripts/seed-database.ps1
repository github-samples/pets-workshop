#!/usr/bin/env pwsh

# Source common utilities
. "$PSScriptRoot/common.ps1"

# Get project root
$ProjectRoot = Get-ProjectRoot

# Initialize virtual environment
if (-not (Initialize-VirtualEnvironment -ProjectRoot $ProjectRoot)) {
    Write-Error "Failed to initialize virtual environment"
    exit 1
}

# Install Python dependencies
if (-not (Install-PythonDependencies -ProjectRoot $ProjectRoot)) {
    Write-Warning "Failed to install Python dependencies"
}

# Run seed database script
try {
    $seedScript = Join-Path $ProjectRoot "server/utils/seed_database.py"
    Write-Host "Seeding database (idempotent)..."
    
    if (-not (Invoke-PythonScript -ScriptPath $seedScript)) {
        Write-Warning "Seeding failed or script not found"
        exit 1
    }
} catch {
    Write-Warning "Seeding failed: $_"
    exit 1
}
