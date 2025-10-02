# Define color codes for PowerShell
$Script:Green = [System.ConsoleColor]::Green
$Script:DefaultColor = [System.ConsoleColor]::White

# Get the project root directory
function Get-ProjectRoot {
    return (Get-Item $PSScriptRoot).Parent.FullName
}

# Create and activate virtual environment
function Initialize-VirtualEnvironment {
    param(
        [string]$ProjectRoot
    )
    
    $VenvPath = Join-Path $ProjectRoot "venv"
    
    # Create virtual environment if it doesn't exist
    if (-not (Test-Path $VenvPath)) {
        Write-Host "Creating virtual environment..."
        python -m venv $VenvPath
    }
   
    # Activate virtual environment
    try {
        if ($IsWindows) {
            & "$VenvPath/Scripts/Activate.ps1"
        } else {
            & bash -c "source '$VenvPath/bin/activate'"
        }
        Write-Host "Virtual environment activated"
        return $true
    } catch {
        Write-Warning "Failed to activate virtual environment: $_"
        return $false
    }
}

# Install Python dependencies
function Install-PythonDependencies {
    param(
        [string]$ProjectRoot
    )
    
    $RequirementsPath = Join-Path $ProjectRoot "server/requirements.txt"
    
    if (Test-Path $RequirementsPath) {
        Write-Host "Installing Python dependencies..."
        pip install -r $RequirementsPath
        return $LASTEXITCODE -eq 0
    } else {
        Write-Warning "Requirements file not found at $RequirementsPath; skipping pip install."
        return $false
    }
}

# Run Python script safely
function Invoke-PythonScript {
    param(
        [string]$ScriptPath,
        [string]$WorkingDirectory = $null
    )
    
    if (Test-Path $ScriptPath) {
        Write-Host "Running Python script: $ScriptPath"
        if ($WorkingDirectory) {
            $oldLocation = Get-Location
            Set-Location $WorkingDirectory
        }
        
        try {
            & python $ScriptPath
            return $LASTEXITCODE -eq 0
        } finally {
            if ($WorkingDirectory) {
                Set-Location $oldLocation
            }
        }
    } else {
        Write-Warning "Python script not found at $ScriptPath; skipping execution."
        return $false
    }
}

# Setup Flask environment variables
function Set-FlaskEnvironment {
    $env:FLASK_DEBUG = 1
    $env:FLASK_PORT = 5100
}

# Start a process with proper error handling
function Start-ManagedProcess {
    param(
        [string]$FilePath,
        [string]$WorkingDirectory,
        [string[]]$ArgumentList,
        [string]$ProcessName
    )
    
    try {
        Write-Host "Starting $ProcessName..."
        $process = Start-Process $FilePath `
            -WorkingDirectory $WorkingDirectory `
            -ArgumentList $ArgumentList `
            -PassThru `
            -NoNewWindow
        
        return $process
    } catch {
        Write-Warning "Failed to start $ProcessName : $_"
        return $null
    }
}

# Cleanup function for process management
function Stop-ManagedProcesses {
    param(
        [System.Diagnostics.Process[]]$Processes,
        [string]$InitialDirectory
    )
    
    Write-Host "Shutting down servers..."
    
    foreach ($process in $Processes) {
        if ($process -and -not $process.HasExited) {
            try {
                Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue
            } catch {
                Write-Warning "Failed to stop process $($process.Id): $_"
            }
        }
    }

    # Deactivate virtual environment if it exists
    if (Test-Path Function:\deactivate) {
        deactivate
    }

    # Return to initial directory
    if ($InitialDirectory) {
        Set-Location $InitialDirectory
    }
}

# Print colored success message
function Write-Success {
    param([string]$Message)
    Write-Host $Message -ForegroundColor $Script:Green
}

# Navigate to project root if in scripts directory
function Set-ProjectRoot {
    if ((Split-Path -Path (Get-Location) -Leaf) -eq "scripts") {
        Set-Location ..
    }
}

# Get appropriate NPM command based on OS
function Get-NpmCommand {
    if ($IsWindows) {
        return "npm.cmd"
    } else {
        return "npm"
    }
}

# Install Node.js dependencies
function Install-NodeDependencies {
    param(
        [string]$Directory
    )
    
    $oldLocation = Get-Location
    try {
        Set-Location $Directory -ErrorAction Stop
        Write-Host "Installing Node.js dependencies in $Directory..."
        npm install
        return $LASTEXITCODE -eq 0
    } catch {
        Write-Warning "Failed to install Node.js dependencies: $_"
        return $false
    } finally {
        Set-Location $oldLocation
    }
}