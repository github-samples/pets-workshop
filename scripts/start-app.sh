#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

# Store initial directory
INITIAL_DIR=$(pwd)

# Navigate to project root if needed
ensure_project_root

echo "Starting API (Flask) server..."

# Get project root and setup virtual environment
PROJECT_ROOT=$(get_project_root)

# Setup virtual environment
setup_virtual_env "$PROJECT_ROOT" || {
    echo "Error: Failed to setup virtual environment"
    cd "$INITIAL_DIR"
    exit 1
}

# Install Python dependencies
install_python_deps "$PROJECT_ROOT" || {
    echo "Error: Failed to install Python dependencies"
    cd "$INITIAL_DIR"
    exit 1
}

# Navigate to server directory and setup Flask environment
navigate_to_server "$PROJECT_ROOT" "$INITIAL_DIR" || {
    exit 1
}

setup_flask_env

# Start Python server in background
python_cmd=$(get_python_command)
$python_cmd app.py &
SERVER_PID=$!

echo "Starting client (Astro)..."
cd ../client || {
    echo "Error: client directory not found"
    cd "$INITIAL_DIR"
    exit 1
}
npm install
npm run dev -- --no-clearScreen &

# Store the SvelteKit server process ID
CLIENT_PID=$!

# Sleep for 3 seconds
sleep 5

# Display the server URLs
echo ""
print_success "Server (Flask) running at: http://localhost:5100"
print_success "Client (Astro) server running at: http://localhost:4321"
echo ""

echo "Ctl-C to stop the servers"

# Function to handle script termination
cleanup() {
    cleanup_processes "$SERVER_PID" "$CLIENT_PID" "$INITIAL_DIR"
    exit 0
}

# Trap multiple signals
trap cleanup SIGINT SIGTERM SIGQUIT EXIT

# Keep the script running
wait