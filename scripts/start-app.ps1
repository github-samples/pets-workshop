#!/usr/bin/env pwsh

. "$PSScriptRoot/common.ps1"

# Store initial directory
$InitialDir = Get-Location

# Navigate to project root if needed
Set-ProjectRoot

Write-Host "Starting API (Flask) server..."

# Get project root and initialize virtual environment
$ProjectRoot = Get-ProjectRoot

if (-not (Initialize-VirtualEnvironment -ProjectRoot $ProjectRoot)) {
    Write-Error "Failed to initialize virtual environment"
    Set-Location $InitialDir
    exit 1
}

# Install Python dependencies
if (-not (Install-PythonDependencies -ProjectRoot $ProjectRoot)) {
    Write-Warning "Failed to install Python dependencies"
    Set-Location $InitialDir
    exit 1
}

# Setup Flask environment
Set-FlaskEnvironment


# Start Python server
$serverWorkingDir = Join-Path $ProjectRoot "server"
$pythonProcess = Start-ManagedProcess -FilePath "python" -WorkingDirectory $serverWorkingDir -ArgumentList @("app.py") -ProcessName "Flask server"

if (-not $pythonProcess) {
    Write-Error "Failed to start Flask server"
    Set-Location $InitialDir
    exit 1
}

Write-Host "Starting client (Astro)..."

# Install Node.js dependencies and start client
$clientDir = Join-Path $ProjectRoot "client"
if (-not (Install-NodeDependencies -Directory $clientDir)) {
    Write-Warning "Failed to install Node.js dependencies"
}

$npmCmd = Get-NpmCommand
$clientProcess = Start-ManagedProcess -FilePath $npmCmd -WorkingDirectory $clientDir -ArgumentList @("run", "dev", "--", "--no-clearScreen") -ProcessName "Astro client"

if (-not $clientProcess) {
    Write-Error "Failed to start Astro client"
    Stop-ManagedProcesses -Processes @($pythonProcess) -InitialDirectory $InitialDir
    exit 1
}

# Sleep for 5 seconds
Start-Sleep -Seconds 5

# Display the server URLs
Write-Host ""
Write-Success "Server (Flask) running at: http://localhost:5100"
Write-Success "Client (Astro) server running at: http://localhost:4321"
Write-Host ""
Write-Host "Ctrl+C to stop the servers"

# Function to handle cleanup
function Cleanup {
    Stop-ManagedProcesses -Processes @($pythonProcess, $clientProcess) -InitialDirectory $InitialDir
    exit
}

# Register cleanup for script termination
$null = Register-EngineEvent -SourceIdentifier PowerShell.Exiting -Action { Cleanup }

try {
    # Keep the script running until Ctrl+C
    Wait-Process -Id $pythonProcess.Id
} finally {
    Cleanup
}
