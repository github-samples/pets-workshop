#!/bin/bash

# Color codes
export GREEN='\033[0;32m'
export NC='\033[0m' # No Color

# Get the project root directory
get_project_root() {
    local index="${1:-0}"
    local script_dir="$(cd "$(dirname "${BASH_SOURCE[$index]}")" && pwd)"
    echo "$script_dir/.."
}

# Get the appropriate Python command based on OS
get_python_command() {
    if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        echo "py"
    else
        echo "python3"
    fi
}

# Create and activate virtual environment
setup_virtual_env() {
    local project_root="$1"
    local python_cmd=$(get_python_command)
    
    cd "$project_root" || {
        echo "Error: Could not navigate to project root: $project_root"
        return 1
    }

    # Create virtual environment if it doesn't exist
    if [[ ! -d "venv" ]]; then
        echo "Creating virtual environment..."
        $python_cmd -m venv venv
    fi

    # Activate virtual environment
    if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        source venv/Scripts/activate || . venv/Scripts/activate
    else
        source venv/bin/activate || . venv/bin/activate
    fi

    if [[ $? -ne 0 ]]; then
        echo "Error: Could not activate virtual environment"
        return 1
    fi

    echo "Virtual environment activated"
    return 0
}

# Install Python dependencies
install_python_deps() {
    local project_root="$1"
    
    if [[ -f "$project_root/server/requirements.txt" ]]; then
        echo "Installing Python dependencies..."
        pip install -r "$project_root/server/requirements.txt"
        return $?
    else
        echo "Warning: requirements.txt not found at $project_root/server/requirements.txt"
        return 1
    fi
}

# Navigate to server directory safely
navigate_to_server() {
    local project_root="$1"
    local initial_dir="$2"
    
    cd "$project_root/server" || {
        echo "Error: server directory not found"
        if [[ -n "$initial_dir" ]]; then
            cd "$initial_dir"
        fi
        return 1
    }
    return 0
}

# Run Python script with appropriate command
run_python_script() {
    local script_path="$1"
    local python_cmd=$(get_python_command)
    
    if [[ -f "$script_path" ]]; then
        echo "Running Python script: $script_path"
        $python_cmd "$script_path"
        return $?
    else
        echo "Error: Python script not found: $script_path"
        return 1
    fi
}

# Cleanup function for process management
cleanup_processes() {
    local server_pid="$1"
    local client_pid="$2"
    local initial_dir="$3"
    
    echo "Shutting down servers..."
    
    # Kill processes and their child processes
    if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        [[ -n "$server_pid" ]] && taskkill //F //T //PID $server_pid 2>/dev/null
        [[ -n "$client_pid" ]] && taskkill //F //T //PID $client_pid 2>/dev/null
    else
        # Send SIGTERM first to allow graceful shutdown
        [[ -n "$server_pid" ]] && kill -TERM $server_pid 2>/dev/null
        [[ -n "$client_pid" ]] && kill -TERM $client_pid 2>/dev/null
        
        # Wait briefly for graceful shutdown
        sleep 2
        
        # Then force kill if still running
        if [[ -n "$server_pid" ]] && ps -p $server_pid > /dev/null 2>&1; then
            pkill -P $server_pid 2>/dev/null
            kill -9 $server_pid 2>/dev/null
        fi
        
        if [[ -n "$client_pid" ]] && ps -p $client_pid > /dev/null 2>&1; then
            pkill -P $client_pid 2>/dev/null
            kill -9 $client_pid 2>/dev/null
        fi
    fi

    # Deactivate virtual environment if active
    if [[ -n "${VIRTUAL_ENV}" ]]; then
        deactivate
    fi

    # Return to initial directory
    if [[ -n "$initial_dir" ]]; then
        cd "$initial_dir"
    fi
}

# Setup common environment variables for Flask
setup_flask_env() {
    export FLASK_DEBUG=1
    export FLASK_PORT=5100
}

# Print colored message
print_success() {
    local message="$1"
    echo -e "${GREEN}${message}${NC}"
}

# Check if running from scripts directory and navigate to project root
ensure_project_root() {
    if [[ $(basename $(pwd)) == "scripts" ]]; then
        cd ..
    fi
}