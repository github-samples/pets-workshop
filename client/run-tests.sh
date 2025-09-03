#!/bin/bash

# Simple test script that starts the app and runs Playwright tests
set -e

echo "Starting application servers in background..."

# Store current directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

# Start the application using the existing script
./scripts/start-app.sh &
APP_PID=$!

# Function to cleanup
cleanup() {
    echo "Cleaning up..."
    kill $APP_PID 2>/dev/null || true
    pkill -f "python.*app.py" 2>/dev/null || true
    pkill -f "npm.*dev" 2>/dev/null || true
    wait $APP_PID 2>/dev/null || true
}

# Trap signals to ensure cleanup
trap cleanup EXIT INT TERM

echo "Waiting for servers to start..."
sleep 10

# Check if servers are running
for i in {1..30}; do
    if curl -s http://localhost:4321 > /dev/null && curl -s http://localhost:5100/api/dogs > /dev/null; then
        echo "Servers are ready!"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "Servers failed to start"
        exit 1
    fi
    echo "Waiting for servers... ($i/30)"
    sleep 2
done

echo "Running Playwright tests..."
cd client
npx playwright test "$@"

echo "Tests completed!"