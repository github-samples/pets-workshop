#!/bin/bash

# setup-environment.sh - Sets up Python virtual environment and installs all dependencies

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

echo -e "${GREEN}Setting up development environment...${NC}"

# Check if we're in scripts directory and navigate accordingly
if [[ $(basename $(pwd)) == "scripts" ]]; then
    cd ..
fi

# Verify we're in the project root
if [[ ! -d "server" ]] || [[ ! -d "client" ]]; then
    handle_error "Not in project root directory. Please run from the project root or scripts directory."
fi

echo -e "${YELLOW}Setting up Python virtual environment...${NC}"

# Check OS and use appropriate Python command
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    # Windows
    if ! py -m venv server/venv; then
        handle_error "Failed to create Python virtual environment"
    fi
    
    if ! source server/venv/Scripts/activate; then
        handle_error "Failed to activate Python virtual environment"
    fi
else
    # macOS/Linux
    if ! python3 -m venv server/venv; then
        handle_error "Failed to create Python virtual environment"
    fi
    
    if ! source server/venv/bin/activate; then
        handle_error "Failed to activate Python virtual environment"
    fi
fi

echo -e "${YELLOW}Installing Python dependencies...${NC}"
if ! pip install -r server/requirements.txt; then
    handle_error "Failed to install Python dependencies"
fi

echo -e "${YELLOW}Installing npm dependencies...${NC}"
cd client || handle_error "client directory not found"

if ! npm install; then
    handle_error "Failed to install npm dependencies"
fi

cd ..

echo -e "${GREEN}Environment setup completed successfully!${NC}"
echo -e "${GREEN}Python virtual environment: server/venv${NC}"
echo -e "${GREEN}All dependencies installed.${NC}"
echo ""
echo -e "${YELLOW}To activate the Python environment manually:${NC}"
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    echo "  source server/venv/Scripts/activate"
else
    echo "  source server/venv/bin/activate"
fi

# Return to initial directory
cd "$INITIAL_DIR"
