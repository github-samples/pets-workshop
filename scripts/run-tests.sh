#!/bin/bash

# run-tests.sh - Runs Python unit tests for the server

# Define color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Store initial directory
INITIAL_DIR=$(pwd)

# Function to handle errors
handle_error() {
    echo -e "${RED}Error: $1${NC}"
    cd "$INITIAL_DIR"
    exit 1
}

echo -e "${GREEN}Running Python unit tests...${NC}"

# Check if we're in scripts directory and navigate accordingly
if [[ $(basename $(pwd)) == "scripts" ]]; then
    SCRIPT_DIR=$(pwd)
    cd ..
else
    SCRIPT_DIR="./scripts"
fi

# Verify we're in the project root
if [[ ! -d "server" ]]; then
    handle_error "Not in project root directory. Please run from the project root or scripts directory."
fi

# Check if virtual environment exists
if [[ ! -d "server/venv" ]]; then
    echo -e "${YELLOW}Virtual environment not found. Setting up environment first...${NC}"
    if ! bash "$SCRIPT_DIR/setup-environment.sh"; then
        handle_error "Failed to set up environment"
    fi
fi

echo -e "${YELLOW}Activating virtual environment...${NC}"

# Navigate to server directory
cd server || handle_error "server directory not found"

# Activate virtual environment
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    # Windows
    if ! source venv/Scripts/activate; then
        handle_error "Failed to activate Python virtual environment"
    fi
else
    # macOS/Linux
    if ! source venv/bin/activate; then
        handle_error "Failed to activate Python virtual environment"
    fi
fi

echo -e "${YELLOW}Running tests...${NC}"

# Run tests with verbose output
if python -m unittest; then
    echo -e "${GREEN}All tests passed!${NC}"
    EXIT_CODE=0
else
    echo -e "${RED}Some tests failed!${NC}"
    EXIT_CODE=1
fi

# Deactivate virtual environment
deactivate

# Return to initial directory
cd "$INITIAL_DIR"

exit $EXIT_CODE
