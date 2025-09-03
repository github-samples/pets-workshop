#!/bin/bash

# run-e2e-tests.sh - Runs Playwright end-to-end tests for the client
#
# Usage:
#   ./scripts/run-e2e-tests.sh                           # Run all tests
#   ./scripts/run-e2e-tests.sh --headed                  # Run with browser UI
#   ./scripts/run-e2e-tests.sh --project=chromium        # Run only chromium tests
#   ./scripts/run-e2e-tests.sh e2e-tests/homepage.spec.ts # Run specific test file
#
# This script handles:
# - Installing dependencies if needed
# - Installing Playwright browsers
# - Running tests with the application servers started automatically
# - Passing through any arguments to the Playwright test command

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

echo -e "${GREEN}Running Playwright end-to-end tests...${NC}"

# Check if we're in scripts directory and navigate accordingly
if [[ $(basename $(pwd)) == "scripts" ]]; then
    SCRIPT_DIR=$(pwd)
    cd ..
else
    SCRIPT_DIR="./scripts"
fi

# Verify we're in the project root
if [[ ! -d "client" ]]; then
    handle_error "Not in project root directory. Please run from the project root or scripts directory."
fi

# Navigate to client directory
cd client || handle_error "client directory not found"

# Check if node_modules exists
if [[ ! -d "node_modules" ]]; then
    echo -e "${YELLOW}Dependencies not found. Installing dependencies...${NC}"
    if ! npm install; then
        handle_error "Failed to install dependencies"
    fi
fi

# Check if Playwright browsers are installed
echo -e "${YELLOW}Ensuring Playwright browsers are installed...${NC}"
if ! npx playwright install --with-deps chromium; then
    handle_error "Failed to install Playwright browsers"
fi

echo -e "${YELLOW}Running end-to-end tests...${NC}"

# Run tests with configurable options
# Default to running all tests unless specific options are passed
if [[ $# -eq 0 ]]; then
    # No arguments, run all tests
    if npm run test:e2e; then
        echo -e "${GREEN}All e2e tests passed!${NC}"
        EXIT_CODE=0
    else
        echo -e "${RED}Some e2e tests failed!${NC}"
        EXIT_CODE=1
    fi
else
    # Pass through any arguments to the test command
    echo -e "${YELLOW}Running tests with options: $@${NC}"
    if npx playwright test "$@"; then
        echo -e "${GREEN}E2E tests completed successfully!${NC}"
        EXIT_CODE=0
    else
        echo -e "${RED}E2E tests failed!${NC}"
        EXIT_CODE=1
    fi
fi

# Return to initial directory
cd "$INITIAL_DIR"

exit $EXIT_CODE
